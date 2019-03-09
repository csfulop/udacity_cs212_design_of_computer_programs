# -----------------
# User Instructions
#
# In this problem, you will complete the code for the hold_at(x)
# function. This function returns a strategy function (note that
# hold_at is NOT the strategy function itself). The returned
# strategy should hold if and only if pending >= x or if the
# player has reached the goal.
from hamcrest.core import assert_that
from hamcrest.core.core import is_

GOAL = 50
ROLL = 'roll'
HOLD = 'hold'


def hold_at(x):
    """Return a strategy that holds if and only if
    pending >= x or player reaches goal."""

    def strategy(state):
        (p, me, you, pending) = state
        if me + pending >= GOAL or pending >= x:
            return HOLD
        else:
            return ROLL

    strategy.__name__ = 'hold_at(%d)' % x
    return strategy


goal = 50


def test():
    assert_that(hold_at(30)((1, 29, 15, 20)), is_('roll'))
    assert_that(hold_at(30)((1, 29, 15, 21)), is_('hold'))
    assert_that(hold_at(15)((0, 2, 30, 10)), is_('roll'))
    assert_that(hold_at(15)((0, 2, 30, 15)), is_('hold'))
    return 'tests pass'


print(test())
