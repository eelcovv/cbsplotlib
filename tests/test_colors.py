import pytest

from cbsplotlib.colors import CBS_COLORS_HEX

__author__ = "Eelco van Vliet"
__copyright__ = "Eelco van Vliet"
__license__ = "MIT"


def test_hex():
    """API Tests"""

    assert CBS_COLORS_HEX["corporateblauw"] == "#271D6C"
