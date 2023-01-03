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


COMMENT_PREFIX = '__'


def load_json_file(file_name: str) -> dict:
    """
    Read the raw config file using the json package.

    Args:
        file_name:  Full path and file name of the config file.

    Returns:
        (dict) The raw config dict unchanged from what is in the file.
    """

    if '$' in file_name:
        # The presence of a $ means we are referencing a directory contained in
        # LOCAL_ENV.DIRECTORIES. We need to swap out that placeholder for the
        # directory in order to be able to load the file.
        subdir_name = utils.strings.extract_between(full_str=file_name, left='$', right='$', include=False)
        subdir = getattr(LOCAL_ENV.DIRECTORIES, subdir_name)
        file_name = file_name.replace(f'${subdir_name}$', subdir)

    with open(file_name) as f:
        raw_config = json.load(f)

    return raw_config


def parse_object(object_config: dict) -> dict:
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


def recursively_parse_references(config: dict) -> dict:
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
        if k[:2] == COMMENT_PREFIX:
            # Ignore comments.
            continue

        if isinstance(v, dict):
            if k == 'object':
                output_config[k] = recursively_parse_references(config=parse_object(v))
            else:
                output_config[k] = recursively_parse_references(config=v)
        else:
            if k == 'reference':
                tmp = load_json_file(v)

                # Execute the overrides on the dict before actually
                # instantiating the classes since the overrides are
                # instantiation overrides. Also, do it before doing
                # a recursive parsing of the dict so we have the final
                # dict before starting to instantiate objects.
                for ok, ov in config['override'].items():
                    tmp['object']['args'][ok] = ov

                tmp = recursively_parse_references(config=tmp)
                for kk, vv in tmp.items():
                    output_config[kk] = vv

                output_config['source'] = v
                output_config.pop('reference', None)

    return output_config


def does_this_still_need_parsing(config: dict) -> bool:
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
            v_result = does_this_still_need_parsing(v)

            if v_result is True:
                return True

    return False


def instantiate_objects(config: dict) -> dict:
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
            output_config[k] = instantiate_objects(v)

        if k == 'object_':
            if v is not None:
                # The args are often objects, so instantiate them first.
                output_config['args'] = instantiate_objects(output_config['args'])

                # Now instantiate the object with its args.
                output_config['instance'] = v(**output_config['args'])

    return output_config


def fetch(file_name: str) -> dict:
    """
    Fetch the raw config dict from the config file at file_name and
    parse it.

    Args:
        file_name:  Full path and file name of the config file.

    Returns:
        (dict) The resulting parsed config dict.
    """

    raw_config = load_json_file(file_name=file_name)
    parsed_config = recursively_parse_references(config=copy.copy(raw_config))

    # Since the referencing within the config files could become reference to references to ...
    # the parsing may need to happen more than once. Here I use an arbitrary number of
    # iterations on the recursion.
    while does_this_still_need_parsing(config=parsed_config) is True:
        parsed_config = recursively_parse_references(config=copy.copy(parsed_config))

    return instantiate_objects(parsed_config)
