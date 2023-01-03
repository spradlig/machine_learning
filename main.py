"""
Module:
    main.py

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


# Tool imports
import configs


def execute_exploratory_analysis(config_file: str):
    """

    Args:
        config_file:

    Returns:

    """

    config = configs.Config(config_file=config_file)

    # Steps - see the notes/Kozyrkov_12steps.md
    # 0 - Reality Check and Setup - this isn't part of the code base.
    # 1 - Define your Objective - this isn't really part of the code base but informs the config file.
    # 2 - Data Collection - this happens as part of the config creation.
    # 3 - Split the Data - this should be done before preprocessing, feature engineering, etc.
    # 4 - Exploratory Data Analysis - this should be done on the Training Set only.
    # 5 - Prepare Your Tools -
