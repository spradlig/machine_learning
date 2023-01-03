"""
Module:
    file.py

Description:
    This file holds a FileTools class which contains a number of useful
    file related utilities.

Usage:
    <from some_module import some_function>
    <Provide a simple example for each class and function in the file.>

Notes:


References:


"""

"""
Version History:
    Original:
        GS | 28-Oct-22
"""

"""
TODOs:
    1)
"""

# Standard library imports
import os
from pathlib import Path
from collections import namedtuple
from datetime import datetime
import re
import pandas as pd

# Tool imports
from utils import strings


file_pieces = namedtuple(
    'file_pieces',
    [
        'path',
        'parts',
        'directory',
    ]
)


class FileSearch:
    """

    """

    def __init__(self, search_directory: str, file_pattern: str):
        """

        Args:
            search_directory:
            file_pattern:
        """

        self._search_directory = search_directory
        self._file_pattern = file_pattern
        self._results = None

    def _file_search_obsolete(self) -> dict:
        """
        This function recursively searches a directory for files matching a
        provided pattern.

        Returns:
            (dict)          Dict with Key: File name w/o path, Value: File object
                            containing the information provided by the Path library.
        """

        output = {'directories': {}}
        for path in Path(self._search_directory).rglob(self._file_pattern):
            file_directory = ''
            for p in path.parts[:-1]:
                file_directory += p + os.sep

            output[path.name] = file_pieces(
                path=path,
                parts=path.parts,
                directory=strings.deduplicate(file_directory, os.sep),
            )

            file_dir = output[path.name].directory
            if file_dir not in output['directories']:
                output['directories'][file_dir] = []

            output['directories'][file_dir].append(path.name)

        return output

    def _file_search(self) -> dict:
        """
        This function recursively searches a directory for files matching a
        provided pattern.

        Returns:
            (dict)          Dict with Key: File name w/o path, Value: file_pieces namedtuple
                            containing the information provided by the Path library.
        """

        output = {}
        for path in Path(self._search_directory).rglob(self._file_pattern):
            file_directory = ''
            for p in path.parts[:-1]:
                file_directory += p + os.sep

            output[path.name] = file_pieces(
                path=path,
                parts=path.parts,
                directory=strings.deduplicate(file_directory, os.sep),
            )

        return output

    @property
    def results(self) -> dict:
        if self._results is None:
            self._results = self._file_search()

        return self._results
