"""
Module:
    <file_name_goes_here>.py

Description:
    <Short description, but thorough, of what is included in the file.>

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


# Tool imports


def deduplicate(haystack: str, needle: str):
    """
    Remove duplicate substring (needle) within a larger string (haystack).

    Args:
        haystack:   Full string to searched and modified.
        needle:     Substring where 1 instance is allowed, all other instances
                    are removed.

    Returns:
        (str) Original string with the duplicate substrings removed.
    """

    # From: https://stackoverflow.com/questions/42216559/fastest-way-to-deduplicate-contiguous-characters-in-string-python
    if haystack.find(needle * 2) != -1:
        return deduplicate(haystack.replace(needle * 2, needle), needle)

    return haystack


def formatted_line(info: str, tab_level: int = 1) -> str:
    """
    Helper tool for formatting lines with indentation.

    Args:
        info:       The text to be formatted.
        tab_level:  The level of indentation.

    Returns:
        (str) Formatted string
    """

    tabs = tab_level * '\t'
    info = info.replace('\n', f'\n{tabs}')
    return f'{tabs}{info}\n'


def extract_remainder_right_of(full_str: str, search_str: str, include: bool = False) -> str:
    """
    Extract everything to the right of the search_str from the full_str and return it. Note
    that if search_str appears twice in full_str, the return will be everything to the right
    of the 1st instance of search_str in full_str.

    Args:
        full_str:       The full string to be searched.
        search_str:     The substring to be found in full_str.
        include:        If True, the return will begin with search_str. If False, then
                        return will start with the first char after search_str.

    Returns:
        (str)   Everything to the right of the search_str in full_string. If search_str is
                not in full_str then the return is an empty str.
    """

    index = full_str.find(search_str)

    if index == -1:
        return ''

    if include is True:
        return full_str[index:]
    else:
        return full_str[index + len(search_str):]


def extract_remainder_left_of(full_str: str, search_str: str, include: bool = False) -> str:
    """
    Extract everything to the left of the search_str from the full_str and return it. Note
    that if search_str appears twice in full_str, the return will be everything to the left
    of the 1st instance of search_str in full_str.

    Args:
        full_str:       The full string to be searched.
        search_str:     The substring to be found in full_str.
        include:        If True, the return will end with search_str. If False, then
                        return will end with the last char before search_str.

    Returns:
        (str)   Everything to the left of the search_str in full_string. If search_str is
                not in full_str then the return is an empty str.
    """

    index = full_str.find(search_str)

    if index == -1:
        return ''

    if include is True:
        return full_str[:index + len(search_str)]
    else:
        return full_str[:index]


def extract_between(full_str: str, left: str, right: str, include: bool = False) -> str:
    """
    Extract everything between the left and right search strings from the full_str and return
    it. Note that if left or right appears twice in full_str, the return will be everything
    between the 1st left and the 1st right.

    Args:
        full_str:       The full string to be searched.
        left:           The left substring to be found in full_str.
        right:          The right substring to be found in full_str.
        include:        If True, the return will end with search_str. If False, then
                        return will end with the last char before search_str.

    Returns:
        (str)   Everything between left and right in full_string. If search_str is
                not in full_str then the return is an empty str.
    """

    left_forward = extract_remainder_right_of(full_str=full_str, search_str=left, include=include)
    return extract_remainder_left_of(full_str=left_forward, search_str=right, include=include)
