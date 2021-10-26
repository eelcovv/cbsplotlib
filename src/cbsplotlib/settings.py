"""
Definition of CBS rbg colors. Based on the color rgb definitions from the cbs LaTeX template
"""

import logging
import math

import matplotlib as mpl

from cbsplotlib.colors import get_color_palette

_logger = logging.getLogger(__name__)

RATIO_OPTIONS = {"golden_ratio", "equal", "from_rows"}


class CBSPlotSettings(object):
    """
    Class to hold the figure size for a standard document

    Parameters
    ----------
    number_of_figures_rows: int, optional
        Number of figure rows, default = 2
    number_of_figures_cols: int, optional
        Number of figure cols, default = 1
    text_width_in_pt: float, optional
        Width of the text in pt, default = 392.64
    text_height_in_pt: float, optional
        Height of the text in pt: default = 693
    text_margin_bot_in_inch: float, optional
        Space at the bottom in inch. Default = 1 inch
    text_height_in_inch: float, optional
        Explicitly over rules the calculated text height if not None. Default = None
    text_width_in_inch = None,
        Explicitly over rules the calculated text height if not None. Default = None
    plot_parameters: dict, optional
        Dictionary with plot settings. If None (default), take the cbs defaults
    color_palette: {"koel", "warm"}, optional
        Pick color palette for the plot. Default is "koel"
    font_size: int, optional
        Size of all fonts. Default = 8

    Notes
    ----------
    * The variables are set to make sure that the figure have the exact same size as the document,
      such that we do not have to rescale them. In this way the fonts will have the same size
      here as in the document
    """

    def __init__(self,
                 fig_width_in_inch: float = None,
                 fig_height_in_inch: float = None,
                 number_of_figures_cols: int = 1,
                 number_of_figures_rows: int = 2,
                 text_width_in_pt: float = 392.64813,
                 text_height_in_pt: float = 693,
                 text_margin_bot_in_inch: float = 1.0,  # margin in inch
                 ratio_option="golden_ratio",
                 plot_parameters: dict = None,
                 color_palette: str = "koel",
                 font_size: int = 8
                 ):

        # set scale factor
        inches_per_pt = 1 / 72.27

        self.number_of_figures_rows = number_of_figures_rows
        self.number_of_figures_cols = number_of_figures_cols
        self.text_width_in_pt = text_width_in_pt
        self.text_height_in_pt = text_height_in_pt
        self.text_margin_bot_in_inch = text_margin_bot_in_inch

        self.text_height = text_height_in_pt * inches_per_pt,
        self.text_width = text_width_in_pt * inches_per_pt

        inches_per_pt = 1 / 72.27
        text_width_in_pt = 392.64813  # add the line \showthe\columnwidth above you figure in latex
        text_height_in_pt = 693  # add the line \showthe\columnwidth above you figure in latex
        text_height = text_height_in_pt * inches_per_pt
        text_width = text_width_in_pt * inches_per_pt
        text_margin_bot = 1.0  # margin in inch

        golden_mean = (math.sqrt(5) - 1) / 2

        if fig_width_in_inch is not None:
            self.fig_width = fig_width_in_inch
        else:
            self.fig_width = text_width / number_of_figures_cols

        if fig_height_in_inch is not None:
            self.fig_height = fig_height_in_inch
        elif ratio_option == "golden_ratio":
            self.fig_height = self.fig_width * golden_mean
        elif ratio_option == "equal":
            self.fig_height = self.fig_width
        elif ratio_option == "from_rows":
            self.fig_height = (text_height - text_margin_bot) / number_of_figures_rows
        else:
            raise ValueError(f"fig height is not given by 'fig_height_in_inch' and 'ratio_option' "
                             f"= {ratio_option} is not in {RATIO_OPTIONS}")

        self.fig_size = (self.fig_width, self.fig_height)

        if plot_parameters is not None:
            params = plot_parameters
        else:
            params = {'axes.labelsize': font_size,
                      'font.size': font_size,
                      'legend.fontsize': font_size,
                      'xtick.labelsize': font_size,
                      'ytick.labelsize': font_size,
                      'figure.figsize': self.fig_size,
                      'grid.color': 'cbs:highchartslichtgrijs',
                      'hatch.color': 'cbs:highchartslichtgrijs',
                      'axes.prop_cycle': get_color_palette(color_palette),
                      'axes.edgecolor': "cbs:grijs",
                      'axes.linewidth': 1.5,
                      }

        mpl.rcParams.update(params)


