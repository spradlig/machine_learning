# -*- coding: utf-8 -*-
"""
Module:
    plotting_tools.py

Description:
    This file is a place to hold generically useful plotting tools.

Usage:
    from src.utils.plotting_tools import set_axes_options, DEFAULT_FIGURE_SIZE
    
    # This function alters the axis's properties per the kwargs. See the function for a full list of
    # valid kwargs.
    set_axes_options(ax=ax, **kwargs) 
    
    # DEFAULT_FIGURE_SIZE is a constant.

Notes:


References:

"""


"""
Version History:
    Original:
        GS | 02-Nov-21
"""

"""
TODOs:
    1)
"""

# Standard Library Imports
from matplotlib import pyplot as plt
import numpy as np

# Custom Package Imports


# plt.style.use('fivethirtyeight')

DEFAULT_FIGURE_SIZE = (14, 8)
DEFAULT_PLOT_COLORS = [
    'midnightblue',
    'darkorange',
    'forestgreen',
    'firebrick',
    'indigo',
    'sienna',
    'crimson',
    'tab:olive',
    'tab:cyan',
    'darkslateblue',
    'goldenrod',
    'darkgreen',
    'tab:red',
    'darkmagenta',
    'saddlebrown',
    'pink',
    'gray',
    'olivedrab',
    'darkcyan',
    'tab:blue',
    'orange',
    'gold',
    'lime',
    'orangered',
    'violet',
    'tab:brown',
    'silver',
    'turquoise'
]


def create_new_figure(figsize: tuple = DEFAULT_FIGURE_SIZE, is_3d: bool = False) -> dict:
    # This function simply creates a new figure with the provided size.
    if is_3d is False:
        fig, ax = plt.subplots(figsize=figsize)
    else:
        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot(projection='3d')

    return {'fig': fig, 'ax': ax}


def create_new_figure_with_1_column_of_axes(
        number_of_axes: int = 1,
        figsize: tuple = DEFAULT_FIGURE_SIZE
) -> dict:
    # This function creates a new figure with the number of subplot axes requested.
    # All subplots will are in a single column, meaning 1 is above the other.
    fig, axs = plt.subplots(figsize=figsize, nrows=number_of_axes)

    # The subplots are all in a tuple. Let's break them out and give them slightly
    # more useful names.
    output = {'fig': fig, 'all_axes': axs}
    for index, ax in enumerate(axs):
        output[f'row{index}'] = ax

    return output


def create_new_figure_with_1_row_of_axes(
        number_of_axes: int = 1,
        figsize: tuple = DEFAULT_FIGURE_SIZE
) -> dict:
    # This function creates a new figure with the number of subplot axes requested.
    # All subplots will are in a single row, meaning 1 is to the left of the other.
    fig, axs = plt.subplots(figsize=figsize, ncols=number_of_axes)

    # The subplots are all in a tuple. Let's break them out and give them slightly
    # more useful names.
    output = {'fig': fig, 'all_axes': axs}
    for index, ax in enumerate(axs):
        output[f'col{index}'] = ax

    return output


def create_new_figure_with_grid_of_axes(
        number_of_rows: int = 1,
        number_of_cols: int = 1,
        figsize: tuple = DEFAULT_FIGURE_SIZE
) -> dict:
    # This function creates a new figure with the number of subplot axes requested.
    # All subplots will are in a single row, meaning 1 is to the left of the other.
    fig, axs = plt.subplots(figsize=figsize, ncols=number_of_cols, nrows=number_of_rows)

    # The subplots are all in a tuple. Let's break them out and give them slightly
    # more useful names.
    output = {'fig': fig, 'all_axes': axs}
    for row in range(number_of_rows):
        for col in range(number_of_cols):
            output[f'row{row}_col{col}'] = axs[row, col]

    return output


def set_axes_options(ax, **kwargs):
    """
    This method provides a simple, all in one, place for altering the matplotlib plot.

    Args:
        ax:                 Handle to an existing axes object.
        kwargs:             The kwargs are how you pass in other parameters like ylabel. The available options are:
                                options = {
                                    'yticks': ax.set_yticks,
                                    'xticks': ax.set_xticks,
                                    'zticks': ax.set_zticks,
                                    'yticklabels': ax.set_yticklabels,
                                    'xticklabels': ax.set_xticklabels,
                                    'zticklabels': ax.set_zticklabels,
                                    'ylabel': ax.set_ylabel,
                                    'xlabel': ax.set_xlabel,
                                    'zlabel': ax.set_zlabel,
                                    'ylim': ax.set_ylim,
                                    'xlim': ax.set_xlim,
                                    'zlim': ax.set_zlim,
                                    'title': ax.set_title,
                                    'legend': ax.legend,
                                    'position': ax.set_position,
                                }

                            The kwargs can also accept 'az' and 'el' which are applied by using:
                                ax.azim = kwargs['az'] or ax.elev = kwargs['el']

                                This is only valid for 3D plots where you wish to set the viewing angle.

    Returns:
        N/A - alterations are made inplace and directly to the axes provided.
    """

    ax.grid('on')

    options = {
        'yticks': ax.set_yticks,
        'xticks': ax.set_xticks,
        'yticklabels': ax.set_yticklabels,
        'xticklabels': ax.set_xticklabels,
        'ylabel': ax.set_ylabel,
        'xlabel': ax.set_xlabel,
        'ylim': ax.set_ylim,
        'xlim': ax.set_xlim,
        'title': ax.set_title,
        'legend': ax.legend,
        'position': ax.set_position,
    }
    
    try:
        options['zticks'] = ax.set_zticks
    except AttributeError:
        # The axes object doesn't include a z, therefore we ignore the z
        # axis properties.
        pass
    
    try:
        options['zticklabels'] = ax.set_zticklabels
    except AttributeError:
        # The axes object doesn't include a z, therefore we ignore the z
        # axis properties.
        pass
    
    try:
        options['zlabel'] = ax.set_zlabel
    except AttributeError:
        # The axes object doesn't include a z, therefore we ignore the z
        # axis properties.
        pass
    
    try:
        options['zlim'] = ax.set_zlim
    except AttributeError:
        # The axes object doesn't include a z, therefore we ignore the z
        # axis properties.
        pass
    
    # Loop through the options.
    for option, function in options.items():
        if option in kwargs:
            function(kwargs[option])

    if 'az' in kwargs:
        ax.azim = kwargs['az']

    if 'el' in kwargs:
        ax.elev = kwargs['el']

    ax.figure.tight_layout()


def set_label_rotation(ax, axis: str = 'x', rotation: float = 45.):
    """
    This function allows the user to rotate the labels on any plot axis.

    Args:
        ax:             Axes object handle where the data and tickmarks already exist.
        axis:           The axis - x, y, or z - where the labels should be rotated.
        rotation:       The desired rotation of the labels. [deg]

    Returns:
        N/A - the axes object (ax) is manipulated directly.
    """

    axis = axis.lower()

    if abs(rotation) > 180.:
        raise ValueError(f'Valid rotations are between [-180, +180] degrees.')

    if axis == 'x':
        ticklabels = ax.get_xticklabels
    elif axis == 'y':
        ticklabels = ax.get_yticklabels
    elif axis == 'z':
        ticklabels = ax.get_xticklabels
    else:
        raise ValueError(f'Axis value {axis} is not recognized.')

    for tick in ticklabels():
        tick.set_rotation(rotation)
        tick.set_ha('right')

    ax.figure.tight_layout()
