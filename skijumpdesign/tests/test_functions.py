import pytest

from ..functions import make_jump
from ..utils import InvalidJumpError


@pytest.mark.xfail(strict=True)
def test_make_jump_expected_to_fail():

    # ValueError: x and y arrays must have at least 2 entries
    make_jump(-15.0, 0.0, 30.0, 20.0, 2.7)

    # TODO : Fix these.
    # Invalid value in sqrt, these hang after the sqrt warning, no errors.
    #make_jump(-10.0, 0.0, 30.0, 23.0, 0.2)
    #make_jump(-10.0, 0.0, 30.0, 20.0, 0.1)
    #make_jump(-11.2, 0.0, 40.0, 10.2, 0.54)

def test_invalid_fall_height():

    # Shouldn't be able to pass in 0.0 as the fall height.
    with pytest.raises(InvalidJumpError):
        make_jump(-25.0, 0.0, 30.0, 20.0, 0.0)


def test_fall_height_too_large():

    with pytest.raises(InvalidJumpError):
        make_jump(-15.0, 0.0, 30.0, 15.0, 2.7)

    with pytest.raises(InvalidJumpError):
        make_jump(-10.0, 0.0, 30.0, 20.0, 2.0)

    with pytest.raises(InvalidJumpError):
        make_jump(-15.0, 0.0, 30.0, 20.0, 3.0)

    with pytest.raises(InvalidJumpError):
        # Used to be: ValueError: x and y arrays must have at least 2 entries
        make_jump(-15.0, 0.0, 30.0, 20.0, 3.0)


def test_skier_flies_forever():

    # Flying skier never contacts surface.
    with pytest.raises(InvalidJumpError):
        make_jump(-10.0, 0.0, 30.0, 20.0, 1.5)

    with pytest.raises(InvalidJumpError):
        # Used to be: ValueError: need at least one array to concatenate
        # Also has: while loop ran more than 1000 times
        make_jump(-15.0, 0.0, 30.0, 20.0, 2.8)


def test_slow_skier():
    # Short approach length such that skier can't get over
    # the jump.
    with pytest.raises(InvalidJumpError):
        make_jump(-30.0, 0.0, 1.0, 45.0, 0.5)


def test_problematic_jump_parameters():

    # these are all regression tests

    # This used to cause a RuntimeWarning: Invalid value in arsin in
    # LandingTransitionSurface.calc_trans_acc() before the fix.
    make_jump(-26.0, 0.0, 3.0, 27.0, 0.6)

    # Divide by zero in scipy/integrate/_ivp/rk.py
    # RuntimeWarning: divide by zero encountered in double_scalars
    # Both of these seem to create a valid jumps.
    make_jump(-10.0, 10.0, 30.0, 20.0, 0.2)
    make_jump(-45.0, 0.0, 30.0, 0.0, 0.2)
    make_jump(-45.0, 0.0, 30.0, 0.0, 0.3)

    # Used to be: while loop ran more than 1000 times
    # this first situation seems to be that the acceleration at max landing
    # can't be below the threshold, thus the landing transition point ends up
    # under the parent slope surface.
    make_jump(-45.0, 0.0, 30.0, 0.0, 0.2)  # fixed, regression test
    make_jump(-45.0, 0.0, 30.0, 0.0, 0.3)  # fixed, regression test
    # the following jump can't find appropriate landing point and generates a
    # unrealistic curve
    make_jump(-30.0, 0.0, 1.0, 15.0, 0.5)
