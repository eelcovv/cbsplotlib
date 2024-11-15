import pytest

from cbsplotlib.utils import format_thousands_label


def test_format_thousands_label_positive_integers():
    """
    Test format_thousands_label with positive integers.

    This test verifies that positive integers are correctly formatted
    with spaces as thousand separators.
    """
    assert format_thousands_label(1234, None) == "1 234"
    assert format_thousands_label(1234567, None) == "1 234 567"


def test_format_thousands_label_negative_integers():
    """
    Test format_thousands_label with negative integers.

    This test verifies that negative integers are correctly formatted
    with spaces as thousand separators and a negative sign.
    """
    assert format_thousands_label(-1234, None) == "-1 234"
    assert format_thousands_label(-1234567, None) == "-1 234 567"
    assert format_thousands_label(-1234, None) == "-1 234"
    assert format_thousands_label(-1234567, None) == "-1 234 567"


def test_format_thousands_label_floating_point_numbers():
    """
    Test format_thousands_label with floating point numbers.

    This test verifies that floating point numbers are correctly formatted
    with spaces as thousand separators and the decimal part is removed.
    """
    assert format_thousands_label(1234.56, None) == "1 234"
    assert format_thousands_label(1234567.89, None) == "1 234 567"
    assert format_thousands_label(1234.56, None) == "1 234"
    assert format_thousands_label(1234567.89, None) == "1 234 567"


def test_format_thousands_label_zero():
    """
    Test format_thousands_label with zero.

    This test verifies that zero is correctly formatted
    as a string "0" without any thousand separators.
    """
    assert format_thousands_label(0, None) == "0"


def test_format_thousands_label_non_numeric_input():
    """
    Test format_thousands_label with non-numeric input.

    This test verifies that passing a non-numeric input to
    format_thousands_label raises a TypeError.
    """
    with pytest.raises(ValueError):
        format_thousands_label("abc", None)
