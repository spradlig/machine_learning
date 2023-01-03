"""
Module:
    __init__.py

Description:
    This file allows for the code in this package to operate similar to any pip/conda installed
    package.

Usage:
    N/A

License:
    https://creativecommons.org/licenses/by-nc-nd/4.0/
    Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)
    See LICENSE.txt

"""

"""
Version History:
    Original:
        Gabe Spradlin | 12-Dec-2022
"""

"""
TODOs:
    1)
"""


# Standard library imports
import os
import json
import copy

# Tool imports
from local_config import LOCAL_ENV
import utils


class Config:
    """
    This class reads in a json config file, recursively parses it to populate all reference, and
    finally instantitates any classes that are requested.

    The raw property provided the raw contents of the config file. The parsed property provides the
    recursively parsed config with all references populated. The instantiated property provides the
    config will all requested objects instantiated. The only purpose of the raw property is to double
    the correct file was loaded. The parsed property is really about producing a static config file
    without references for reproduceability reasons. The instantiated property is what should be
    used almost always.
    """

    COMMENT_PREFIX = '__'
    REFERENCE_IDENTIFIER = '$'

    def __init__(self, config_file: str):
        """
        Instantiate the class.

        Args:
            config_file:    Full path and file name of the top-level config
                            file to run.
        """

        self._inputs = locals()

        if config_file.find(os.sep) < 0:
            # This is just the file name with no path. Assume the path
            # is the configs subdirectory.
            config_file = os.path.join(LOCAL_ENV.DIRECTORIES.configs, config_file)

        self._config_file = config_file
        self._raw_config, self._parsed_config, self._instantiated = None, None, None
        self.fetch()

    def __str__(self) -> str:
        output = f'{self.__class__.__name__}:\n'
        output += utils.strings.formatted_line(f'File: {self.file}', tab_level=1)

        return output

    def __repr__(self) -> str:
        output = utils.strings.formatted_line(f'{self.__class__.__name__}(', tab_level=1)
        for k, v in self._inputs.items():
            if k == 'self':
                continue

            output += utils.strings.formatted_line(f'{k}={repr(v)}', tab_level=2)

        output += utils.strings.formatted_line(')', tab_level=1)
        return output

    def load_json_file(self, file_name: str) -> dict:
        """
        Read the raw config file using the json package.

        Args:
            file_name:  Full path and file name of the config file.

        Returns:
            (dict) The raw config dict unchanged from what is in the file.
        """

        if self.REFERENCE_IDENTIFIER in file_name:
            # The presence of a $ means we are referencing a directory contained in
            # LOCAL_ENV.DIRECTORIES. We need to swap out that placeholder for the
            # directory in order to be able to load the file.
            subdir_name = utils.strings.extract_between(
                full_str=file_name,
                left=self.REFERENCE_IDENTIFIER,
                right=self.REFERENCE_IDENTIFIER,
                include=False
            )

            subdir = getattr(LOCAL_ENV.DIRECTORIES, subdir_name)
            original_reference = f'{self.REFERENCE_IDENTIFIER}{subdir_name}{self.REFERENCE_IDENTIFIER}'
            file_name = file_name.replace(original_reference, subdir)

        with open(file_name) as f:
            raw_config = json.load(f)

        return raw_config

    def parse_object(self, object_config: dict) -> dict:
        """
        The raw config dict is a series of nested dicts. Each sub-dict could define something
        or reference another config file. A sub-dict that defines an object requires that the
        object be instantiated.

        This function instantiates the defined objects.

        Args:
            object_config:  Object specific config, not the full sim config.

        Returns:
            (dict) Same dict that was provided in object_config except that the object was
                instantiated and the added to the dict in the "instance" field.
        """

        # Load the module and the specific class. Then instantiate the class.
        module = __import__(object_config['module'], fromlist=[object_config['class']])

        try:
            # object = getattr(module, object_config['class'])
            object_config['object_'] = getattr(module, object_config['class'])
            #     object_config['instance'] = object(**object_config['args'])
        except AttributeError:
            # object_config['instance'] = None
            object_config['object_'] = None
            print(f'The following object did not get created. {object_config}')

        return object_config

    def recursively_parse_references(self, config: dict) -> dict:
        """
        The raw config dict is a series of nested dicts. Each sub-dict could define something
        or reference another config file. This function recursively parses those nested
        config dicts replacing references and instantiating objects so teh final output config
        dict has everything that is needed.

        Args:
            config:     Raw config dict, i.e. output of json.load on the config file.

        Returns:
            (dict)      Parsed config dict.
        """

        output_config = copy.deepcopy(config)
        tmp = {}
        for k, v in config.items():
            if k[:2] == self.COMMENT_PREFIX:
                # Ignore comments.
                continue

            if isinstance(v, dict):
                if k == 'object':
                    output_config[k] = self.recursively_parse_references(config=self.parse_object(v))
                else:
                    output_config[k] = self.recursively_parse_references(config=v)
            else:
                if k == 'reference':
                    tmp = self.load_json_file(v)

                    # Execute the overrides on the dict before actually
                    # instantiating the classes since the overrides are
                    # instantiation overrides. Also, do it before doing
                    # a recursive parsing of the dict so we have the final
                    # dict before starting to instantiate objects.
                    for ok, ov in config['override'].items():
                        tmp['object']['args'][ok] = ov

                    tmp = self.recursively_parse_references(config=tmp)
                    for kk, vv in tmp.items():
                        output_config[kk] = vv

                    output_config['source'] = v
                    output_config.pop('reference', None)

        return output_config

    def does_this_still_need_parsing(self, config: dict) -> bool:
        """
        The json file config could lead to scenarios where "reference" leads to files
        with other "reference" entries and "object" entries, etc. The recursion will
        catch most of this but it sometimes will not.

        This function determines if the config dict still needs parsing.

        Args:
            config:     Parsed config dict.

        Returns:
            (bool)  True if this still needs parsing, False otherwise.
        """

        for k, v in config.items():
            if k == 'reference':
                return True

            if k == 'object' and 'object_' not in v:
                return True

            if isinstance(v, dict):
                v_result = self.does_this_still_need_parsing(v)

                if v_result is True:
                    return True

        return False

    def instantiate_objects(self, config: dict) -> dict:
        """
        The json file config has been parsed and all object imports have been extracts. All
        arg overrides have been applied.

        This function instantiates the objects.

        Args:
            config:     Parsed config dict.

        Returns:
            (dict)  config with the objects instantiated and a new field added to
                    the 'object' fields. That new field is 'instance' and it holds
                    the instantiated object.
        """

        output_config = copy.deepcopy(config)
        for k, v in config.items():
            if isinstance(v, dict):
                output_config[k] = self.instantiate_objects(v)

            if k == 'object_':
                if v is not None:
                    # The args are often objects, so instantiate them first.
                    output_config['args'] = self.instantiate_objects(output_config['args'])

                    # Now instantiate the object with its args.
                    output_config['instance'] = v(**output_config['args'])

        return output_config

    def fetch(self) -> dict:
        """
        Fetch the raw config dict from the config file at file_name and
        parse it.

        Returns:
            (dict) The resulting parsed config dict.
        """

        self._raw_config = self.load_json_file(file_name=self._config_file)
        self._parsed_config = self.recursively_parse_references(config=copy.copy(self._raw_config))

        # Since the referencing within the config files could become reference to references to ...
        # the parsing may need to happen more than once. Here I use an arbitrary number of
        # iterations on the recursion.
        while self.does_this_still_need_parsing(config=self._parsed_config) is True:
            self._parsed_config = self.recursively_parse_references(config=copy.copy(self._parsed_config))

        self._instantiated = self.instantiate_objects(self._parsed_config)

    @property
    def file(self) -> str:
        return self._config_file

    @property
    def raw(self) -> dict:
        # This is the raw file as a dict before any parsing is done.
        return self._raw_config

    @property
    def parsed(self) -> dict:
        # This would be the version to print if you wanted a full config with all references
        # filled. This will be the full config without instantiated objects. Best for printing
        # and generating a reproduceable json file that contains no references.
        return self._parsed_config

    @property
    def instantiated(self) -> dict:
        # This is the one the code uses to perform the full run set.
        return self._instantiated