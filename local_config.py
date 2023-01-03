"""
Module:
    local_config.py

Description:
    Items such as data directories, plotting preferences, etc. can be defined
    in this file. Many of the items can be automatically determined but not all.

Usage:
    from local_config import LOCAL_ENV

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
        Gabe Spradlin | 13-Dec-2022
"""

"""
TODOs:
    1)
"""

# Standard library imports
from matplotlib import pyplot as plt
import plotly.io as pio
import os
import platform
from dataclasses import dataclass, field

# Tool imports


plt.style.use('fivethirtyeight')

# Render plotly interactive plots in a browser.
pio.renderers.default = 'browser'

# Render the plots inline for Spyder.
# pio.renderers.default = 'svg'

# Automatically determine where the directory of this file.
base_dir = os.path.dirname(__file__) + os.sep
print(f'Machine Learning Base Directory: {base_dir}')


@dataclass(frozen=True)
class Directories:
    """
    This class holds the directories for the ML project. They are read-only.

    Reference on using dataclasses:
        https://www.pythontutorial.net/python-oop/python-dataclass/
    """

    base: str = base_dir
    cache: str = field(init=False)
    configs: str = os.path.join(base_dir, 'configs')
    dataset: str = os.path.join(base_dir, 'dataset')
    docs: str = os.path.join(base_dir, 'docs')
    graphics: str = os.path.join(base_dir, 'graphics')
    examples: str = os.path.join(base_dir, 'examples')

    def __post_init__(self):
        """
        This sets sub-directories and therefore needs to happen after the
        higher level directories have been set.

        Returns:
            N/A
        """

        # Can't do this because it is frozen.
        # self.cache = os.path.join(self.data, 'cache')

        # So we work around it like this:
        #   https://stackoverflow.com/questions/53756788/how-to-set-the-value-of-dataclass-field-in-post-init-when-frozen-true
        # object.__setattr__(self, 'results', os.path.join(self.data, 'results'))
        pass


# DIRECTORIES is capitalized because it should be treated as a constant outside this file.
DIRECTORIES = Directories()


@dataclass(frozen=True)
class LocalEnv:
    """
    This class holds all local env values in a read-only class.
    """

    OS_IS_WINDOWS: bool = 'Windows' in platform.platform()
    DIRECTORIES: Directories = DIRECTORIES


# It is recommended that you use only the class(es) below.
LOCAL_ENV = LocalEnv()
