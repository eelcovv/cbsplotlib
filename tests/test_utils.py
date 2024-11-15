import pytest

from cbsplotlib.utils import format_thousands_label


def test_format_thousands_label_positive_integers():
    assert format_thousands_label(1234, None) == "1 234"
    assert format_thousands_label(1234567, None) == "1 234 567"


def test_format_thousands_label_negative_integers():
    assert format_thousands_label(-1234, None) == "-1 234"
    assert format_thousands_label(-1234567, None) == "-1 234 567"


def test_format_thousands_label_floating_point_numbers():
    assert format_thousands_label(1234.56, None) == "1 234"
    assert format_thousands_label(1234567.89, None) == "1 234 567"


def test_format_thousands_label_zero():
    assert format_thousands_label(0, None) == "0"


def test_format_thousands_label_non_numeric_input():
    with pytest.raises(TypeError):
        format_thousands_label("abc", None)
