"""
Module:
    openml.py

Description:
    This file holds the Split and Dataset classes for the OpenML data source.

Usage:
    from dataset import Openml_Split, Openml_Dataset

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
import requests
from sklearn.datasets import fetch_openml

# Tool imports
import utils
from dataset.base import SplitBase, DatasetBase


class Split(SplitBase):
    """
    The SplitBase class is intended to hold one of the Training, Validation, or Testing splits of the dataset.
    It provides a common interface for all datasets to conform to so that downstream code can leverage the common
    API.
    """


class Dataset(DatasetBase):
    """
    The DatasetBase class is intended to hold the entire dataset. It automatically splits the
    dataset into Training, Validation, and Testing based on values provided in the split_percentages
    instantiation arg. The full dataset is cleaned and normalized prior to being split so that the
    splits are ready to be used by everything downstream without further processing and without
    repeating potentially time-consuming calculations.
    """

    def __init__(
            self,
            id: int,
            column_headers: list[str],
            answers_column: str,
            split_percentages: dict
    ):
        """
        Instantiate the class.

        Args:
            id:                     The ID given to the dataset by OpenML. For example, the credit-g
                                    dataset is ID 31.
                                    https://www.openml.org/search?type=data&sort=runs&status=active&id=31
            column_headers:         List of column header strings for the dataset.
            answers_column:         The column header for the answers (if this is supervised learning).
            split_percentages:      A dict with keys 'training', 'validation', and 'testing' where each
                                    key have a value [0, 1) and the sum of all values = 1.
        """

        tmp_locals = locals()

        res = requests.get(f'https://api.openml.org/api/v1/json/data/{id}')
        dataset_description = res.json()['data_set_description']

        self._data_id = id

        super().__init__(
            source=f'OpenML_{dataset_description["name"]}_{dataset_description["id"]}_{dataset_description["upload_date"]}',
            title=f'OpenML_{dataset_description["name"]}_{dataset_description["id"]}',
            column_headers=column_headers,
            answers_column=answers_column,
            split_percentages=split_percentages,
        )

        # Override the self._inputs set by __init__ in DatasetBase as this won't allow anyone to
        # recreate the class.
        self._inputs = tmp_locals

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

        df_X, df_y = fetch_openml(data_id=self._data_id, return_X_y=True)

        if df_y is not None:
            # Combine features + answers since that is what DatasetBase is expecting.
            df_X[self._answers_column] = df_y.copy()

        if len(self._column_headers) == 0:
            self._column_headers = list(self._full.columns)

        try:
            self._column_headers.remove(self._answers_column)
        except ValueError:
            # The answers column wasn't in the column headers.
            pass

        self._full = df_X

        self._split()
