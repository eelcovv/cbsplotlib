"""
Definition of CBS rbg colors. Based on the color rgb definitions from the cbs LaTeX template
"""

import logging
import math
from pathlib import Path

import numpy as np
import matplotlib as mpl
import matplotlib.patches as mpatches
from matplotlib.path import Path as mPath
from matplotlib.image import imread
import matplotlib.transforms as trn
from PIL import Image
from matplotlib import colors as mcolors

logger = logging.getLogger(__name__)

CBS_COLORS_RBG = {
    "corporateblauw": (39, 29, 108),
    "corporatelichtblauw": (0, 161, 205),
    "donkerblauw": (0, 88, 184),
    "donkerblauwvergrijsd": (22, 58, 114),
    "lichtblauw": (0, 161, 205),  # zelfde als corporatelichtblauw
    "lichtblauwvergrijsd": (5, 129, 162),
    "geel": (255, 204, 0),
    "geelvergrijsd": (255, 182, 0),
    "oranje": (243, 146, 0),
    "oranjevergrijsd": (206, 124, 0),
    "rood": (233, 76, 10),
    "roodvergrijsd": (178, 61, 2),
    "roze": (175, 14, 128),
    "rozevergrijsd": (130, 4, 94),
    "grasgroen": (83, 163, 29),
    "grasgroenvergrijsd": (72, 130, 37),
    "appelgroen": (175, 203, 5),
    "appelgroenvergrijsd": (137, 157, 12),
    "violet": (172, 33, 142),
    "lichtgrijs": (224, 224, 224),  # 12% zwart
    "grijs": (102, 102, 102),  # 60% zwart
    "logogrijs": (115, 115, 115),  # 55% zwart
    "codekleur": (88, 88, 88),
}

# prepend 'cbs:' to all color names to prevent collision
CBS_COLORS = {"cbs:" + name: (value[0] / 255, value[1] / 255, value[2] / 255)
              for name, value in CBS_COLORS_RBG.items()}

# update the matplotlib colors
mcolors.get_named_colors_mapping().update(CBS_COLORS)

# deze dictionairy bevat meerdere palettes
CBS_PALETS = dict(
    koel=[
        "cbs:corporatelichtblauw",
        "cbs:donkerblauw",
        "cbs:appelgroen",
        "cbs:grasgroen",
        "cbs:oranje",
        "cbs:roze",
    ],
    warm=[
        "cbs:rood",
        "cbs:geel",
        "cbs:roze",
        "cbs:oranje",
        "cbs:grasgroen",
        "cbs:appelgroen",
    ]
)


def get_color_palette(style="koel"):
    """
    Set the color palette

    Parameters
    ----------
    style: {"koel", "warm"), optional
        Color palette to pick. Default = "koel"

    Returns
    -------
    mpl.cycler:
        cbs_color_cycle

    Notes
    -----
    in order to set the cbs color palette default::

        import matplotlib as mpl
        from cbs_utils.plotting import get_color_palette
        mpl.rcParams.update({'axes.prop_cycle': get_color_palette("warm")}
    """
    try:
        cbs_palette = CBS_PALETS[style]
    except KeyError:
        raise KeyError(f"Did not recognised style {style}. Should be one of {CBS_PALETS.keys()}")
    else:
        cbs_color_cycle = mpl.cycler(color=cbs_palette)

    return cbs_color_cycle


def report_colors():
    for name, value in CBS_COLORS.items():
        logger.info("{:20s}: {}".format(name, value))