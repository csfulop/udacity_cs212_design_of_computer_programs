# -----------------
# User Instructions
#
# The find_prefixes function takes a hand, a prefix, and a
# results list as input.
# Modify the find_prefixes function to cache previous results
# in order to improve performance.
import time


def prefixes(word):
    "A list of the initial sequences of a word, not including the complete word."
    return [word[:i] for i in range(len(word))]


def readwordlist(filename):
    "Return a pair of sets: all the words in a file, and all the prefixes. (Uppercased.)"
    wordset = set(open(filename).read().upper().split())
    prefixset = set(p for word in wordset for p in prefixes(word))
    return wordset, prefixset


WORDS, PREFIXES = readwordlist('words4k.txt')


class anchor(set):
    "An anchor is where a new word can be placed; has a set of allowable letters."


LETTERS = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
ANY = anchor(LETTERS)  # The anchor that can be any letter


def is_letter(sq):
    return isinstance(sq, str) and sq in LETTERS


def is_empty(sq):
    "Is this an empty square (no letters, but a valid position on board)."
    return sq == '.' or sq == '*' or isinstance(sq, set)


def add_suffixes(hand, pre, start, row, results, anchored=True):
    "Add all possible suffixes, and accumulate (start, word) pairs in results."
    i = start + len(pre)
    if pre in WORDS and anchored and not is_letter(row[i]):
        results.add((start, pre))
    if pre in PREFIXES:
        sq = row[i]
        if is_letter(sq):
            add_suffixes(hand, pre + sq, start, row, results)
        elif is_empty(sq):
            possibilities = sq if isinstance(sq, set) else ANY
            for L in hand:
                if L in possibilities:
                    add_suffixes(hand.replace(L, '', 1), pre + L, start, row, results)
    return results


def legal_prefix(i, row):
    """A legal prefix of an anchor at row[i] is either a string of letters
    already on the board, or new letters that fit into an empty space.
    Return the tuple (prefix_on_board, maxsize) to indicate this.
    E.g. legal_prefix(a_row, 9) == ('BE', 2) and for 6, ('', 2)."""
    s = i
    while is_letter(row[s - 1]): s -= 1
    if s < i:  ## There is a prefix
        return ''.join(row[s:i]), i - s
    while is_empty(row[s - 1]) and not isinstance(row[s - 1], set): s -= 1
    return ('', i - s)


###Modify this function. You may need to modify
# variables outside this function as well.

def find_prefixes_old(hand, pre='', results=None):
    """Find all prefixes (of words) that can be made from letters in hand."""
    if results is None: results = set()
    if pre in PREFIXES:
        results.add(pre)
        for L in hand:
            find_prefixes_old(hand.replace(L, '', 1), pre + L, results)
    return results


prev_hand, prev_results = '', set()  # cache for find_prefixes


def find_prefixes(hand, pre='', results=None):
    """Find all prefixes (of words) that can be made from letters in hand."""
    global prev_hand, prev_results
    if results is None:
        results = set()
    if hand == prev_hand:
        return prev_results
    if pre == '':
        prev_results = results
        prev_hand = hand
    if pre in PREFIXES:
        results.add(pre)
        for L in hand:
            find_prefixes(hand.replace(L, '', 1), pre + L, results)
    return results


def timedcall(fn, *args):
    "Call function with args; return the time in seconds and result."
    t0 = time.clock()
    result = fn(*args)
    t1 = time.clock()
    return t1 - t0, result


def test_prefix(hand):
    t1, result1 = timedcall(find_prefixes_old, hand)
    t2, result2 = timedcall(find_prefixes, hand)
    t3, result3 = timedcall(find_prefixes, hand)
    print('hand=', hand)
    print('t1=%f, t2=%f, t3=%f' % (t1, t2, t3))
    # print('result1=', result1)
    # print('result2=', result2)
    assert result1 == result2
    assert result2 == result3
    assert t3 < t2


def test():
    test_prefix('AB')
    test_prefix('TOXENSI')
    test_prefix('ABECEDR')

    return 'tests pass'


print(test())
