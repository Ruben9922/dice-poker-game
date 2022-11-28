import pytest

from main import is_full_house, is_n_of_a_kind, is_straight, calculate_score_for_single_value


@pytest.mark.parametrize("dice,expected", [
    ([1, 2, 3, 4, 5], False),
    ([1, 1, 1, 1, 1], True),
    ([1, 1, 1, 1, 3], False),
    ([1, 1, 1, 2, 2], True),
    ([2, 2, 1, 1, 1], True),
    ([2, 1, 2, 1, 2], True),
    ([2, 2, 2, 1, 2], False),
    ([1, 2, 3, 4, 4], False),
    ([1, 2, 3, 3, 3], False),
])
def test_is_full_house(dice, expected):
    assert is_full_house(dice) == expected


@pytest.mark.parametrize("dice,n,expected", [
    ([1, 2, 3, 4, 5], 4, False),
    ([1, 2, 3, 4, 4], 4, False),
    ([1, 2, 3, 3, 3], 4, False),
    ([1, 2, 2, 2, 2], 4, True),
    ([1, 1, 1, 1, 1], 4, True),
    ([1, 1, 1, 1, 2], 4, True),
    ([1, 1, 2, 1, 1], 4, True),

    ([1, 2, 3, 4, 5], 3, False),
    ([1, 2, 3, 4, 4], 3, False),
    ([1, 2, 3, 3, 3], 3, True),
    ([1, 1, 2, 2, 2], 3, True),
    ([1, 2, 2, 2, 2], 3, True),
    ([1, 1, 1, 1, 1], 3, True),
    ([1, 1, 1, 2, 2], 3, True),
    ([1, 2, 2, 1, 1], 3, True),
])
def test_is_n_of_a_kind(dice, n, expected):
    assert is_n_of_a_kind(dice, n) == expected


@pytest.mark.parametrize("dice,straight_length,expected", [
    ([1, 2, 3, 4, 5], 4, True),
    ([1, 2, 3, 4, 4], 4, True),
    ([1, 2, 3, 3, 4], 4, True),
    ([1, 2, 3, 3, 3], 4, False),
    ([1, 2, 2, 2, 2], 4, False),
    ([1, 1, 1, 1, 1], 4, False),
    ([1, 2, 3, 5, 6], 4, False),
    ([1, 2, 4, 5, 6], 4, False),
    ([5, 6, 3, 2, 1], 4, False),
    ([5, 6, 3, 1, 4], 4, True),

    ([1, 2, 3, 4, 5], 5, True),
    ([2, 3, 4, 5, 6], 5, True),
    ([1, 2, 3, 4, 4], 5, False),
    ([1, 2, 3, 3, 3], 5, False),
    ([1, 2, 2, 2, 2], 5, False),
    ([1, 1, 1, 1, 1], 5, False),
    ([1, 2, 3, 5, 6], 5, False),
    ([1, 2, 4, 5, 6], 5, False),
    ([5, 6, 3, 1, 2], 5, False),
    ([3, 1, 2, 5, 4], 5, True),
    ([3, 6, 2, 5, 4], 5, True),
])
def test_is_straight(dice, straight_length, expected):
    assert is_straight(dice, straight_length) == expected


@pytest.mark.parametrize("dice,value,expected", [
    ([2, 4, 5, 2, 1], 2, 4),
    ([2, 4, 4, 2, 1], 5, 0),
    ([6, 6, 6, 6, 6], 6, 30),
])
def test_calculate_score_for_single_value(dice, value, expected):
    assert calculate_score_for_single_value(dice, value) == expected
