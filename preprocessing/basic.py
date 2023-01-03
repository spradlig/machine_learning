"""
Module:
    basic.py

Description:
    <Short description, but thorough, of what is included in the file.>

Usage:
    <from some_module import some_function>
    <Provide a simple example for each class and function in the file.>

Notes:


References:


License:
    https://creativecommons.org/licenses/by-nc-nd/4.0/
    Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)
    See LICENSE.txt

"""

"""
Version History:
    Original:
        Gabe Spradlin | 02-Jan-2023
"""

"""
TODOs:
    1)
"""

# Standard library imports
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import FeatureUnion
import pandas as pd

# Tool imports


# Below are classes derived from here: https://www.kaggle.com/code/baghern/a-deep-dive-into-sklearn-pipelines
class TextSelector(BaseEstimator, TransformerMixin):
    """
    Transformer to select a single column from the data frame to perform additional transformations on
    Use on text columns in the data
    """

    def __init__(self, key):
        self.key = key

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X[self.key]


class NumberSelector(BaseEstimator, TransformerMixin):
    """
    Transformer to select a single column from the data frame to perform additional transformations on
    Use on numeric columns in the data
    """

    def __init__(self, key):
        self.key = key

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X[[self.key]]


# This class was modified from: https://stackoverflow.com/questions/68402691/adding-dropping-column-instance-into-a-pipeline
class ColumnDropper(BaseEstimator, TransformerMixin):
    def __init__(self, columns: list[str]):
        """

        Args:
            columns:
        """

        self._columns_to_drop = columns

    def transform(self, X: pd.DataFrame, y: [pd.DataFrame, None] = None):
        return X.drop(self._columns_to_drop, axis=1)

    def fit(self, X: pd.DataFrame, y: [pd.DataFrame, None] = None):
        return self


class Basic:
    """
    Very basic (minimal) preprocessing pipeline which will extract each column, determine
    if it is text or numbers, select the column, and apply a scaling object to it.
    """

    def __init__(
            self,
            text_scaler=TfidfVectorizer(stop_words='english'),
            number_scaler=StandardScaler(),
            null_threshold=1.
    ):
        """
        Instantiate the class.

        Args:
            text_scaler:    The method to vectorize/scale text columns.
            number_scaler:  The method to scale numeric columns.
            null_threshold: Percent [0, 1] of the column which can be null. Equal to
                            or above this percentage and the column gets dropped. This
                            defaults to 1 which means the column could be all NaNs/Null
                            and still not get dropped.
        """

        self._inputs = locals()

        self._text_scaler = text_scaler
        self._number_scaler = number_scaler
        self._null_threshold = null_threshold

    def _null_analysis(self, df: pd.DataFrame):
        """

        Args:
            df:

        Returns:


        References:
            https://python-data-science.readthedocs.io/en/latest/preprocess.html
        """

        '''
        desc: get nulls for each column in counts & percentages
        arg: dataframe
        return: dataframe
        '''

        null_cnt = df.isnull().sum()  # calculate null counts
        # null_cnt = null_cnt[null_cnt != 0]  # remove non-null cols
        null_percent = null_cnt / len(df)  # calculate null percentages
        null_table = pd.concat([pd.DataFrame(null_cnt), pd.DataFrame(null_percent)], axis=1)
        null_table.columns = ['counts', 'percentage']
        null_table.sort_values('counts', ascending=False, inplace=True)

        return null_table

    def __call__(self, df: pd.DataFrame) -> Pipeline:
        """
        Generate the preprocessing pipeline.

        Args:
            df:         A pandas DataFrame of features to preprocess.

        Returns:
            (Pipeline)  A pipeline for preprocessing of the data before doing
                        feature engineering.
        """

        null_table = self._null_analysis(df=df)
        high_null_table = null_table[null_table['percentage'] >= self.null_threshold]
        bad_columns = list(high_null_table.index)

        column_pipelines = []
        for col in df.columns:
            if isinstance(df[col][0], str):
                pipeline = Pipeline(
                    [
                        ('selector', TextSelector(key=col)),
                        ('tfidf', self.text_scaler)
                    ]
                )
            else:
                pipeline = Pipeline(
                    [
                        ('selector', NumberSelector(key=col)),
                        ('scaler', self.number_scaler)
                    ]
                )

            column_pipelines.append((col, pipeline))

        return Pipeline([
            ('remove_too_many_nulls', ColumnDropper(bad_columns)),
            ('preprocessing', FeatureUnion(column_pipelines))
        ])

    @property
    def number_scaler(self):
        return self._number_scaler

    @property
    def text_scaler(self):
        return self._text_scaler

    @property
    def null_threshold(self) -> float:
        return self._null_threshold
