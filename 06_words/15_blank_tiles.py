# -----------------
# User Instructions
#
# Modify our scrabble program to accept blank tiles and score
# them appropriately. You can do this in whatever manner you
# wish as long as you match the given test cases.

LETTERS = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

POINTS = dict(A=1, B=3, C=3, D=2, E=1, F=4, G=2, H=4, I=1, J=8, K=5, L=1, M=3, N=1, O=1, P=3, Q=10, R=1, S=1, T=1, U=1,
              V=4, W=4, X=8, Y=4, Z=10, _=0)
for L in LETTERS:
    POINTS[L.lower()] = 0


def bonus_template(quadrant):
    "Make a board from the upper-left quadrant."
    return mirror(list(map(mirror, quadrant.split())))


def mirror(sequence): return sequence + sequence[-2::-1]


SCRABBLE = bonus_template("""
|||||||||
|3..:...3
|.2...;..
|..2...:.
|:..2...:
|....2...
|.;...;..
|..:...:.
|3..:...*
""")

WWF = bonus_template("""
|||||||||
|...3..;.
|..:..2..
|.:..:...
|3..;...2
|..:...:.
|.2...3..
|;...:...
|...:...*
""")

BONUS = WWF

DW, TW, DL, TL = '23:;'


def removed(letters, remove):
    "Return a str of letters, but with each letter in remove removed once."
    for L in remove:
        letters = letters.replace(L, '', 1)
    return letters


def prefixes(word):
    "A list of the initial sequences of a word, not including the complete word."
    return [word[:i] for i in range(len(word))]


def transpose(matrix):
    "Transpose e.g. [[1,2,3], [4,5,6]] to [[1, 4], [2, 5], [3, 6]]"
    # or [[M[j][i] for j in range(len(M))] for i in range(len(M[0]))]
    return list(map(list, zip(*matrix)))


def readwordlist(filename):
    "Return a pair of sets: all the words in a file, and all the prefixes. (Uppercased.)"
    wordset = set(open(filename).read().upper().split())
    prefixset = set(p for word in wordset for p in prefixes(word))
    return wordset, prefixset


WORDS, PREFIXES = readwordlist('words4k.txt')


class anchor(set):
    "An anchor is where a new word can be placed; has a set of allowable letters."

    def __str__(self): return '.'


ANY = anchor(LETTERS)  # The anchor that can be any letter


def is_letter(sq):
    return isinstance(sq, str) and sq in LETTERS


def is_empty(sq):
    "Is this an empty square (no letters, but a valid position on board)."
    return sq == '.' or sq == '*' or isinstance(sq, set)


def add_suffixes(hand, pre, start, row, results, anchored=True):
    "Add all possible suffixes, and accumulate (start, word) pairs in results."
    i = start + len(pre)
    if pre.upper() in WORDS and anchored and not is_letter(row[i]):
        results.add((start, pre))
    if pre.upper() in PREFIXES:
        sq = row[i]
        if is_letter(sq):
            add_suffixes(hand, pre + sq, start, row, results)
        elif is_empty(sq):
            possibilities = sq if isinstance(sq, set) else ANY
            for L in hand:
                if L == '_':
                    letters = set(map(lambda x: x.lower(), LETTERS))
                else:
                    letters = {L}
                for letter in letters:
                    if letter.upper() in possibilities:
                        add_suffixes(hand.replace(L, '', 1), pre + letter, start, row, results)
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


prev_hand, prev_results = '', set()  # cache for find_prefixes


def find_prefixes(hand, pre='', results=None):
    ## Cache the most recent full hand (don't cache intermediate results)
    global prev_hand, prev_results
    if hand == prev_hand: return prev_results
    if results is None: results = set()
    if pre == '': prev_hand, prev_results = hand, results
    # Now do the computation
    if pre in WORDS or pre in PREFIXES: results.add(pre)
    if pre in PREFIXES:
        for L in hand:
            find_prefixes(hand.replace(L, '', 1), pre + L, results)
    return results


def row_plays(hand, row):
    "Return a set of legal plays in row.  A row play is an (start, 'WORD') pair."
    results = set()
    ## To each allowable prefix, add all suffixes, keeping words
    for (i, sq) in enumerate(row[1:-1], 1):
        if isinstance(sq, set):
            pre, maxsize = legal_prefix(i, row)
            if pre:  ## Add to the letters already on the board
                start = i - len(pre)
                add_suffixes(hand, pre, start, row, results, anchored=False)
            else:  ## Empty to left: go through the set of all possible prefixes
                for pre in find_prefixes(hand):
                    if len(pre) <= maxsize:
                        start = i - len(pre)
                        add_suffixes(removed(hand, pre), pre, start, row, results,
                                     anchored=False)
    return results


def find_cross_word(board, i, j):
    """Find the vertical word that crosses board[j][i]. Return (j2, w),
    where j2 is the starting row, and w is the word"""
    sq = board[j][i]
    w = sq if is_letter(sq) else '.'
    for j2 in range(j, 0, -1):
        sq2 = board[j2 - 1][i]
        if is_letter(sq2):
            w = sq2 + w
        else:
            break
    for j3 in range(j + 1, len(board)):
        sq3 = board[j3][i]
        if is_letter(sq3):
            w = w + sq3
        else:
            break
    return (j2, w)


def neighbors(board, i, j):
    """Return a list of the contents of the four neighboring squares,
    in the order N,S,E,W."""
    return [board[j - 1][i], board[j + 1][i],
            board[j][i + 1], board[j][i - 1]]


def set_anchors(row, j, board):
    """Anchors are empty squares with a neighboring letter. Some are resticted
    by cross-words to be only a subset of letters."""
    for (i, sq) in enumerate(row[1:-1], 1):
        neighborlist = (N, S, E, W) = neighbors(board, i, j)
        # Anchors are squares adjacent to a letter.  Plus the '*' square.
        if sq == '*' or (is_empty(sq) and any(map(is_letter, neighborlist))):
            if is_letter(N) or is_letter(S):
                # Find letters that fit with the cross (vertical) word
                (j2, w) = find_cross_word(board, i, j)
                row[i] = anchor(L for L in LETTERS if w.replace('.', L) in WORDS)
            else:  # Unrestricted empty square -- any letter will fit.
                row[i] = ANY


def calculate_score(board, pos, direction, hand, word):
    "Return the total score for this play."
    total, crosstotal, word_mult = 0, 0, 1
    starti, startj = pos
    di, dj = direction
    other_direction = DOWN if direction == ACROSS else ACROSS
    for (n, L) in enumerate(word):
        i, j = starti + n * di, startj + n * dj
        sq = board[j][i]
        b = BONUS[j][i]
        word_mult *= (1 if is_letter(sq) else
                      3 if b == TW else 2 if b in (DW, '*') else 1)
        letter_mult = (1 if is_letter(sq) else
                       3 if b == TL else 2 if b == DL else 1)
        total += POINTS[L] * letter_mult
        if isinstance(sq, set) and sq is not ANY and direction is not DOWN:
            crosstotal += cross_word_score(board, L, (i, j), other_direction)
    return crosstotal + word_mult * total


def cross_word_score(board, L, pos, direction):
    "Return the score of a word made in the other direction from the main word."
    i, j = pos
    (j2, word) = find_cross_word(board, i, j)
    return calculate_score(board, (i, j2), DOWN, L, word.replace('.', L))


ACROSS, DOWN = (1, 0), (0, 1)  # Directions that words can go


def horizontal_plays(hand, board):
    "Find all horizontal plays -- (score, pos, word) pairs -- across all rows."
    results = set()
    for (j, row) in enumerate(board[1:-1], 1):
        set_anchors(row, j, board)
        for (i, word) in row_plays(hand, row):
            score = calculate_score(board, (i, j), ACROSS, hand, word)
            results.add((score, (i, j), word))
    return results


def all_plays(hand, board):
    """All plays in both directions. A play is a (score, pos, dir, word) tuple,
    where pos is an (i, j) pair, and dir is a (delta-_i, delta_j) pair."""
    hplays = horizontal_plays(hand, board)
    vplays = horizontal_plays(hand, transpose(board))
    return (set((score, (i, j), ACROSS, w) for (score, (i, j), w) in hplays) |
            set((score, (i, j), DOWN, w) for (score, (j, i), w) in vplays))


def make_play(play, board):
    "Put the word down on the board."
    (score, (i, j), (di, dj), word) = play
    for (n, L) in enumerate(word):
        board[j + n * dj][i + n * di] = L.upper()
    return board


NOPLAY = None


def best_play(hand, board):
    "Return the highest-scoring play.  Or None."
    plays = all_plays(hand, board)
    # for play in plays:
    #     print(play)
    return sorted(plays)[-1] if plays else NOPLAY


def a_board():
    return list(map(list, ['|||||||||||||||||',
                           '|J............I.|',
                           '|A.....BE.C...D.|',
                           '|GUY....F.H...L.|',
                           '|||||||||||||||||']))


def show(board, bonus=BONUS):
    "Print the board."
    ###Your code here.
    for row, bonus_row in zip(board, bonus):
        print(' '.join(sq if is_letter(sq) else sqb for sq, sqb in zip(row, bonus_row)))


DEBUG_TEST_RUN = True


def test():
    def ok(hand, n, s, d, w):
        board = a_board()
        result = best_play(hand, board)
        test_case = result[:3] == (n, s, d) and result[-1].upper() == w.upper()
        # if not test_case:
        if DEBUG_TEST_RUN:
            show(board)
            print(hand)
            new_board = make_play(result, board)
            show(new_board)
            print((n, s, d, w))
            print(result)
        return test_case

    assert ok('ABCEHKN', 64, (3, 2), (1, 0), 'BACKBENCH')
    assert ok('_BCEHKN', 62, (3, 2), (1, 0), 'BaCKBENCH')
    assert ok('__CEHKN', 61, (9, 1), (1, 0), 'KiCk')
    return 'tests pass'


print(test())
