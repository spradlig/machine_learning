"""
Module:
    base.py

Description:
    This file holds the SplitBase and DatasetBase classes. The SplitBase class refers to the Training,
    Validation, and Testing splits. The DatasetBase is a base class for the full Dataset, including
    the splits.

    These classes are not intended to be used themselves. They should be subclassed.

Usage:
    from dataset.base import SplitBase, DatasetBase

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
        Gabe Spradlin | 30-Dec-2022
"""

"""
TODOs:
    1)
"""

# Standard library imports
import pandas as pd
from sklearn.model_selection import StratifiedShuffleSplit

# Tool imports
import utils


class SplitBase:
    """
    The SplitBase class is intended to hold one of the Training, Validation, or Testing splits of the dataset.
    It provides a common interface for all datasets to conform to so that downstream code can leverage the common
    API.
    """

    def __init__(
            self,
            source: str,
            title: str,
            features: pd.DataFrame,
            answers: [pd.Series, pd.DataFrame, None]
    ):
        """
        Instantiate the class.

        Args:
            source:     String describing how to find the data source. If this is a file on
                        a local hard drive, then this string is the full path and filename.
                        If this data source is an OpenML dataset then this is some descriptive
                        string with that name and the dataset ID.
            title:      This is a descriptive string for the dataset. Its primary use-case is
                        as part of titles on analysis plots. It should be unique enough that
                        plots of other datasets cannot be confused with this dataset.
            features:   This is a pandas DataFrame holding the features for the dataset.
            answers:    For supervised learning, this is a pandas Series or DataFrame holding
                        the correct answers for the dataset. The answer in row i in answers
                        should be the answer to the instance in row i of features. When the
                        dataset is not a supervised learning dataset, then this can be None.
        """

        self._inputs = locals()

        self._source = source
        self._title = title
        self._features = features
        self._answers = answers

    def __str__(self) -> str:
        output = f'{self.__class__.__name__}:\n'
        output += utils.strings.formatted_line(f'Title: {self.title}', tab_level=1)
        output += utils.strings.formatted_line(f'Source: {self.source}', tab_level=1)
        output += utils.strings.formatted_line(f'Features: {self.features.info()}', tab_level=1)

        if self.answers is not None:
            output += utils.strings.formatted_line(f'Answers: {self.answers.info()}', tab_level=1)

        return output

    def __repr__(self) -> str:
        output = utils.strings.formatted_line(f'{self.__class__.__name__}(', tab_level=1)
        for k, v in self._inputs.items():
            if k == 'self':
                continue

            output += utils.strings.formatted_line(f'{k}={v.__repr__()}', tab_level=2)

        output += utils.strings.formatted_line(')', tab_level=1)
        return output

    @property
    def source(self) -> str:
        return self._source

    @property
    def features(self) -> pd.DataFrame:
        return self._features

    @property
    def answers(self) -> [pd.Series, pd.DataFrame, None]:
        return self._answers

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str):
        if len(value) > 0:
            self._title = value


class DatasetBase:
    """
    The DatasetBase class is intended to hold the entire dataset. It automatically splits the
    dataset into Training, Validation, and Testing based on values provided in the split_percentages
    instantiation arg. The full dataset is cleaned and normalized prior to being split so that the
    splits are ready to be used by everything downstream without further processing and without
    repeating potentially time-consuming calculations.
    """

    def __init__(
            self,
            source: str,
            title: str,
            column_headers: list[str],
            answers_column: str,
            split_percentages: dict,
            normalization: dict,
            cleaning: dict
    ):
        """
        Instantiate the class.

        Args:
            source:                 String describing how to find the data source. If this is a file on
                                    a local hard drive, then this string is the full path and filename.
                                    If this data source is an OpenML dataset then this is some descriptive
                                    string with that name and the dataset ID.
            title:                  This is a descriptive string for the dataset. Its primary use-case is
                                    as part of titles on analysis plots. It should be unique enough that
                                    plots of other datasets cannot be confused with this dataset.
            column_headers:         List of column header strings for the dataset.
            answers_column:         The column header for the answers (if this is supervised learning).
            split_percentages:      A dict with keys 'training', 'validation', and 'testing' where each
                                    key have a value [0, 1) and the sum of all values = 1.
            normalization:          A dict defining the normalization by column.
            cleaning:               A dict defining the cleaning preferences by column.
        """

        self._inputs = locals()

        self._source = source
        self._title = title
        self._column_headers = column_headers
        self._answers_column = answers_column
        self._split_percentages = split_percentages
        self._normalization = normalization
        self._cleaning = cleaning

        # Define the dataset splits.
        self._full, self._training, self._validation, self._testing = None, None, None, None

        self._create_dataset()

    def _create_dataset(self):
        """
        This method reads in the data from the source, normalizes the data as
        proscribed, and splits the data as proscribed. Then returns the processed
        dataset splits.

        Returns:
            N/A - instance variables are set.
        """

        # Set self._full, self._training, self._validation, and self._testing below.
        # Load the full dataset into self._full. The dataset should be cleaned, normalized,
        # and anything that is necessary (like dropping columns) prior to being split.
        # Then call self._split().
        raise NotImplementedError

    def _split(self):
        """
        This method splits the full dataset into the Training, Validation, and Testing datasets.

        Returns:
            N/A - instance variables are set.
        """

        df = self._full
        splits = self._split_percentages

        # Modified from:
        #   https://stackoverflow.com/questions/40829137/stratified-train-validation-test-split-in-scikit-learn
        train_other_split = StratifiedShuffleSplit(
            n_splits=1,
            test_size=(1 - splits['training']),
            random_state=splits['random_seed']
        )
        for train_index, test_valid_index in train_other_split.split(df, df.target):
            training_set = df.iloc[train_index]
            test_valid_set = df.iloc[test_valid_index]

        validation_test_split = StratifiedShuffleSplit(
            n_splits=1,
            test_size=(splits['testing'] / (splits['testing'] + splits['validation']))
        )
        for test_index, valid_index in validation_test_split.split(test_valid_set, test_valid_set.target):
            testing_set = test_valid_set.iloc[test_index]
            validation_set = test_valid_set.iloc[valid_index]

        self._testing = testing_set
        self._validation = validation_set
        self._training = training_set

    def __str__(self) -> str:
        output = f'{self.__class__.__name__}:\n'
        output += utils.strings.formatted_line(f'Title: {self.title}', tab_level=1)
        output += utils.strings.formatted_line(f'Source: {self.source}', tab_level=1)
        output += utils.strings.formatted_line(f'Split Percentages: {self._split_percentages}', tab_level=1)
        output += utils.strings.formatted_line(f'Normalization: {self._normalization}', tab_level=1)
        output += utils.strings.formatted_line(f'Cleaning: {self._cleaning}', tab_level=1)

        return output

    def __repr__(self) -> str:
        output = utils.strings.formatted_line(f'{self.__class__.__name__}(', tab_level=1)
        for k, v in self._inputs.items():
            if k == 'self':
                continue

            output += utils.strings.formatted_line(f'{k}={v.__repr__()}', tab_level=2)

        output += utils.strings.formatted_line(')', tab_level=1)
        return output

    @property
    def source(self) -> str:
        return self._source

    @property
    def split_percentages(self) -> dict:
        return self._split_percentages

    @property
    def normalization(self) -> dict:
        return self._normalization

    @property
    def cleaning(self) -> dict:
        return self._cleaning

    @property
    def training(self) -> [SplitBase, None]:
        return self._training

    @property
    def validation(self) -> [SplitBase, None]:
        return self._validation

    @property
    def testing(self) -> [SplitBase, None]:
        return self._testing

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str):
        if len(value) > 0:
            self._title = value
