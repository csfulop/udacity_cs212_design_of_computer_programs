# -----------------
# User Instructions
#
# This problem deals with the one-player game foxes_and_hens. This
# game is played with a deck of cards in which each card is labelled
# as a hen 'H', or a fox 'F'.
#
# A player will flip over a random card. If that card is a hen, it is
# added to the yard. If it is a fox, all of the hens currently in the
# yard are removed.
#
# Before drawing a card, the player has the choice of two actions,
# 'gather' or 'wait'. If the player gathers, she collects all the hens
# in the yard and adds them to her score. The drawn card is discarded.
# If the player waits, she sees the next card.
#
# Your job is to define two functions. The first is do(action, state),
# where action is either 'gather' or 'wait' and state is a tuple of
# (score, yard, cards). This function should return a new state with
# one less card and the yard and score properly updated.
#
# The second function you define, strategy(state), should return an
# action based on the state. This strategy should average at least
# 1.5 more points than the take5 strategy.

import random


def foxes_and_hens(strategy, foxes=7, hens=45):
    """Play the game of foxes and hens."""
    # A state is a tuple of (score-so-far, number-of-hens-in-yard, deck-of-cards)
    state = (score, yard, cards) = (0, 0, 'F' * foxes + 'H' * hens)
    while cards:
        action = strategy(state)
        state = (score, yard, cards) = do(action, state)
    return score + yard


def do(action, state):
    "Apply action to state, returning a new state."
    # Make sure you always use up one card.
    #
    # your code here
    (score, yard, cards) = state
    cards = list(cards)
    next_card = cards.pop(random.randrange(len(cards)))
    cards = ''.join(cards)
    if action == 'wait':
        if next_card == 'H':
            return (score, yard + 1, cards)
        if next_card == 'F':
            return (score, 0, cards)
        raise ValueError('Invalid card: ' + next_card)
    if action == 'gather':
        return (score + yard, 0, cards)
    raise ValueError('Invalid action: ' + action)


def take5(state):
    "A strategy that waits until there are 5 hens in yard, then gathers."
    (score, yard, cards) = state
    if yard < 5:
        return 'wait'
    else:
        return 'gather'


def average_score(strategy, N=1000):
    return sum(foxes_and_hens(strategy) for _ in range(N)) / float(N)


def superior(A, B=take5):
    "Does strategy A have a higher average score than B, by more than 1.5 point?"
    score_a = average_score(A)
    score_b = average_score(B)
    print('score(A)=%f, score(B)=%f' % (score_a, score_b))
    return score_a - score_b > 1.5


def strategy(state):
    # your code here
    (score, yard, cards) = state
    foxes = cards.count('F')
    if foxes == 0 or yard < len(cards) / foxes - 3:
        return 'wait'
    else:
        return 'gather'


from functools import update_wrapper


def decorator(d):
    "Make function d a decorator: d wraps a function fn."

    def _d(fn):
        return update_wrapper(d(fn), fn)

    update_wrapper(_d, d)
    return _d


@decorator
def memo(f):
    """Decorator that caches the return value for each call to f(args).
    Then when called again with same args, we can just look it up."""
    cache = {}

    def _f(*args):
        try:
            return cache[args]
        except KeyError:
            cache[args] = result = f(*args)
            return result
        except TypeError:
            # some element of args can't be a dict key
            return f(args)

    return _f


def actions(state):
    "Available actions in state"
    (score, yard, cards) = state
    if yard > 0:
        return ('wait', 'gather')
    else:
        return ('wait',)


def draw_fox(cards):
    "The deck after drawing a Fox"
    return cards.replace('F', '', 1)


def draw_hen(cards):
    "The deck after drawing a Hen"
    return cards.replace('H', '', 1)


@memo
def U_foxes(state):
    "Utility of the given state"
    (score, yard, cards) = state
    if not cards:  # Utility is the score if there are no more cards
        return score + yard
    else:  # Utility if the maximum Quality of the available actions
        qs = list(Q_foxes(state, action, U_foxes) for action in actions(state))
        return max(qs)


def Q_foxes(state, action, U):
    "The expected Utility of choosing action in state."
    (score, yard, cards) = state
    foxes = cards.count('F')
    hens = cards.count('H')
    if action == 'wait':
        e_foxes, e_hens = 0, 0
        if foxes > 0:
            e_foxes = U((score, 0, draw_fox(cards))) * foxes / float(len(cards))
        if hens > 0:
            e_hens = U((score, yard + 1, draw_hen(cards))) * hens / float(len(cards))
        return e_foxes + e_hens
    if action == 'gather':
        e_foxes, e_hens = 0, 0
        if foxes > 0:
            e_foxes = U((score + yard, 0, draw_fox(cards))) * foxes / float(len(cards))
        if hens > 0:
            e_hens = U((score + yard, 0, draw_hen(cards))) * hens / float(len(cards))
        return e_foxes + e_hens
    raise ValueError(action)


def best_action(state, actions, Q, U):
    "Return the optimal action for a state, given U."

    def EU(action): return Q(state, action, U)

    return max(actions(state), key=EU)


def best_strategy(state):
    return best_action(state, actions, Q_foxes, U_foxes)


def test():
    gather = do('gather', (4, 5, 'F' * 4 + 'H' * 10))
    assert (gather == (9, 0, 'F' * 3 + 'H' * 10) or
            gather == (9, 0, 'F' * 4 + 'H' * 9))

    wait = do('wait', (10, 3, 'FFHH'))
    assert (wait == (10, 4, 'FFH') or
            wait == (10, 0, 'FHH'))

    assert superior(strategy)
    assert superior(best_strategy)
    return 'tests pass'


print(test())
