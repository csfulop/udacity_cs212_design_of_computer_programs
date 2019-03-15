# -----------------
# User Instructions
#
# Write a function, play_pig, that takes two strategy functions as input,
# plays a game of pig between the two strategies, and returns the winning
# strategy. Enter your code at line 41.
#
# You may want to borrow from the random module to help generate die rolls.

import random

HOLD = 'hold'
ROLL = 'roll'
POSSIBLE_MOVES = [ROLL, HOLD]
OTHER = {1: 0, 0: 1}
GOAL = 50
TURN_LIMIT = 1000


def clueless(state):
    "A strategy that ignores the state and chooses at random from possible moves."
    return random.choice(POSSIBLE_MOVES)


def hold(state):
    """Apply the hold action to a state to yield a new state:
    Reap the 'pending' points and it becomes the other player's turn."""
    (p, me, you, pending) = state
    return (OTHER[p], you, me + pending, 0)


def roll(state, d):
    """Apply the roll action to a state (and a die roll d) to yield a new state:
    If d is 1, get 1 point (losing any accumulated 'pending' points),
    and it is the other player's turn. If d > 1, add d to 'pending' points."""
    (p, me, you, pending) = state
    if d == 1:
        return (OTHER[p], you, me + 1, 0)  # pig out; other player's turn
    else:
        return (p, me, you, pending + d)  # accumulate die roll in pending


def play_pig(A, B):
    """Play a game of pig between two players, represented by their strategies.
    Each time through the main loop we ask the current player for one decision,
    which must be 'hold' or 'roll', and we update the state accordingly.
    When one player's score exceeds the goal, return that player."""
    state = (0, 0, 0, 0)
    for i in range(TURN_LIMIT):
        (p, me, you, pending) = state
        if me >= GOAL:
            return B if p else A
        action = B(state) if p else A(state)
        if action == HOLD:
            state = hold(state)
        elif action == ROLL:
            state = roll(state, random.randint(1, 6))
        else:
            raise Exception('Invalid action:' + action)


def always_roll(state):
    return ROLL


def always_hold(state):
    return HOLD


def test():
    for _ in range(10):
        winner = play_pig(always_hold, always_roll)
        assert winner.__name__ == 'always_roll'
    for _ in range(10):
        winner = play_pig(always_roll, always_hold)
        assert winner.__name__ == 'always_roll'
    return 'tests pass'


print(test())
