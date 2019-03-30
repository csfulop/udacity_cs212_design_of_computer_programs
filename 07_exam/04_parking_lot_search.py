"""
UNIT 4: Search

Your task is to maneuver a car in a crowded parking lot. This is a kind of
puzzle, which can be represented with a diagram like this:

| | | | | | | |
| G G . . . Y |
| P . . B . Y |
| P * * B . Y @
| P . . B . . |
| O . . . A A |
| O . S S S . |
| | | | | | | |

A '|' represents a wall around the parking lot, a '.' represents an empty square,
and a letter or asterisk represents a car.  '@' marks a goal square.
Note that there are long (3 spot) and short (2 spot) cars.
Your task is to get the car that is represented by '**' out of the parking lot
(on to a goal square).  Cars can move only in the direction they are pointing.
In this diagram, the cars GG, AA, SSS, and ** are pointed right-left,
so they can move any number of squares right or left, as long as they don't
bump into another car or wall.  In this diagram, GG could move 1, 2, or 3 spots
to the right; AA could move 1, 2, or 3 spots to the left, and ** cannot move
at all. In the up-down direction, BBB can move one up or down, YYY can move
one down, and PPP and OO cannot move.

You should solve this puzzle (and ones like it) using search.  You will be
given an initial state like this diagram and a goal location for the ** car;
in this puzzle the goal is the '.' empty spot in the wall on the right side.
You should return a path -- an alternation of states and actions -- that leads
to a state where the car overlaps the goal.

An action is a move by one car in one direction (by any number of spaces).
For example, here is a successor state where the AA car moves 3 to the left:

| | | | | | | |
| G G . . . Y |
| P . . B . Y |
| P * * B . Y @
| P . . B . . |
| O A A . . . |
| O . . . . . |
| | | | | | | |

And then after BBB moves 2 down and YYY moves 3 down, we can solve the puzzle
by moving ** 4 spaces to the right:

| | | | | | | |
| G G . . . . |
| P . . . . . |
| P . . . . * *
| P . . B . Y |
| O A A B . Y |
| O . . B . Y |
| | | | | | | |

You will write the function

    solve_parking_puzzle(start, N=N)

where 'start' is the initial state of the puzzle and 'N' is the length of a side
of the square that encloses the pieces (including the walls, so N=8 here).

We will represent the grid with integer indexes. Here we see the
non-wall index numbers (with the goal at index 31):

 |  |  |  |  |  |  |  |
 |  9 10 11 12 13 14  |
 | 17 18 19 20 21 22  |
 | 25 26 27 28 29 30 31
 | 33 34 35 36 37 38  |
 | 41 42 43 44 45 46  |
 | 49 50 51 52 53 54  |
 |  |  |  |  |  |  |  |

The wall in the upper left has index 0 and the one in the lower right has 63.
We represent a state of the problem with one big tuple of (object, locations)
pairs, where each pair is a tuple and the locations are a tuple.  Here is the
initial state for the problem above in this format:
"""

puzzle1a = (
    ('@', (31,)),
    ('*', (26, 27)),
    ('G', (9, 10)),
    ('Y', (14, 22, 30)),
    ('P', (17, 25, 33)),
    ('O', (41, 49)),
    ('B', (20, 28, 36)),
    ('A', (45, 46)),
    ('|', (0, 1, 2, 3, 4, 5, 6, 7, 8, 15, 16, 23, 24, 32, 39,
           40, 47, 48, 55, 56, 57, 58, 59, 60, 61, 62, 63)))

# A solution to this puzzle is as follows:

#     path = solve_parking_puzzle(puzzle1, N=8)
#     path_actions(path) == [('A', -3), ('B', 16), ('Y', 24), ('*', 4)]

# That is, move car 'A' 3 spaces left, then 'B' 2 down, then 'Y' 3 down,
# and finally '*' moves 4 spaces right to the goal.

# Your task is to define solve_parking_puzzle:

N = 8


def solve_parking_puzzle(start, N=N):
    """Solve the puzzle described by the starting position (a tuple
    of (object, locations) pairs).  Return a path of [state, action, ...]
    alternating items; an action is a pair (object, distance_moved),
    such as ('B', 16) to move 'B' two squares down on the N=8 grid."""
    return shortest_path_search(start, successors, is_goal)


# But it would also be nice to have a simpler format to describe puzzles,
# and a way to visualize states.
# You will do that by defining the following two functions:

def locs(start, n, incr=1):
    "Return a tuple of n locations, starting at start and incrementing by incr."
    return tuple(start + i for i in range(0, n * incr, incr))


def grid(cars, N=N):
    """Return a tuple of (object, locations) pairs -- the format expected for
    this puzzle.  This function includes a wall pair, ('|', (0, ...)) to
    indicate there are walls all around the NxN grid, except at the goal
    location, which is the middle of the right-hand wall; there is a goal
    pair, like ('@', (31,)), to indicate this. The variable 'cars'  is a
    tuple of pairs like ('*', (26, 27)). The return result is a big tuple
    of the 'cars' pairs along with the walls and goal pairs."""
    exit = (N // 2 - 1) * N + N - 1
    board = [('@', (exit,))]
    board.extend(list(cars))
    boarders = [y * N + x
                for y in range(N)
                for x in range(N)
                if y in (0, N - 1) or x in (0, N - 1) and y * N + x != exit]
    board.append(('|', tuple(boarders)))
    return tuple(board)


def show(state, N=N):
    "Print a representation of a state as an NxN grid."
    # Initialize and fill in the board.
    board = ['.'] * N ** 2
    for (c, squares) in state:
        for s in squares:
            board[s] = c
    # Now print it out
    for i, s in enumerate(board):
        print(s, end=' ')
        if i % N == N - 1: print()


# Here we see the grid and locs functions in use:

puzzle1 = grid((
    ('*', locs(26, 2)),
    ('G', locs(9, 2)),
    ('Y', locs(14, 3, N)),
    ('P', locs(17, 3, N)),
    ('O', locs(41, 2, N)),
    ('B', locs(20, 3, N)),
    ('A', locs(45, 2))))

puzzle1_G1 = grid((
    ('*', locs(26, 2)),
    ('G', locs(10, 2)),
    ('Y', locs(14, 3, N)),
    ('P', locs(17, 3, N)),
    ('O', locs(41, 2, N)),
    ('B', locs(20, 3, N)),
    ('A', locs(45, 2))))

puzzle1_Bm8 = grid((
    ('*', locs(26, 2)),
    ('G', locs(9, 2)),
    ('Y', locs(14, 3, N)),
    ('P', locs(17, 3, N)),
    ('O', locs(41, 2, N)),
    ('B', locs(12, 3, N)),
    ('A', locs(45, 2))))

puzzle2 = grid((
    ('*', locs(26, 2)),
    ('B', locs(20, 3, N)),
    ('P', locs(33, 3)),
    ('O', locs(41, 2, N)),
    ('Y', locs(51, 3))))

puzzle3 = grid((
    ('*', locs(25, 2)),
    ('B', locs(19, 3, N)),
    ('P', locs(36, 3)),
    ('O', locs(45, 2, N)),
    ('Y', locs(49, 3))))

puzzle4done = grid((
    ('*', locs(30, 2)),
))


# Here are the shortest_path_search and path_actions functions from the unit.
# You may use these if you want, but you don't have to.

def shortest_path_search(start, successors, is_goal):
    """Find the shortest path from start state to a state
    such that is_goal(state) is true.
    successor: (state) -> Dict[state,action]
    is_goal: (state) -> bool"""
    if is_goal(start):
        return [start]
    explored = set()  # set of states we have visited
    frontier = [[start]]  # ordered list of paths we have blazed
    while frontier:
        path = frontier.pop(0)
        s = path[-1]
        for (state, action) in successors(s).items():
            if state not in explored:
                explored.add(state)
                path2 = path + [action, state]
                if is_goal(state):
                    return path2
                else:
                    frontier.append(path2)
    return []


def path_actions(path):
    "Return a list of actions in this path."
    return path[1::2]


def is_goal(state):
    s = _state_dict(state)
    return s['@'][0] in s['*']


def _state_dict(state):
    return {k: v for (k, v) in state}


def successors(state):
    result = {}
    actions = _available_actions(state)
    for action in actions:
        result[_apply_action(state, action)] = action
    return result


def _available_actions(state):
    actions = []
    s = _state_dict(state)
    for car, pos in s.items():
        if car in ('@', '|'):
            continue
        increment = pos[1] - pos[0]
        move = -increment
        while pos[0] + move > 0 and _is_free(state, pos[0] + move):
            actions.append((car, move))
            move -= increment
        move = increment
        while pos[-1] + move <= max(s['|']) and _is_free(state, pos[-1] + move):
            actions.append((car, move))
            move += increment
    return actions


def _is_free(state, pos):
    for item in state:
        if item[0] == '@': continue
        if pos in item[1]: return False
    return True


def _apply_action(state, action):
    result = []
    for item in state:
        if action[0] == item[0]:
            result.append((item[0], tuple(pos + action[1] for pos in item[1])))
        else:
            result.append(item)
    return tuple(result)


def tests():
    assert locs(26, 2) == (26, 27)
    assert locs(20, 3, N) == (20, 28, 36)

    show(puzzle1)
    assert puzzle1a == puzzle1

    assert _state_dict(puzzle1) == {
        '@': (31,),
        '*': (26, 27),
        'G': (9, 10),
        'Y': (14, 22, 30),
        'P': (17, 25, 33),
        'O': (41, 49),
        'B': (20, 28, 36),
        'A': (45, 46),
        '|': (0, 1, 2, 3, 4, 5, 6, 7, 8, 15, 16, 23, 24, 32, 39, 40, 47, 48, 55, 56, 57, 58, 59, 60, 61, 62, 63)
    }

    assert is_goal(puzzle1) == False
    assert is_goal(puzzle4done) == True

    assert _is_free(puzzle1, 9) == False
    assert _is_free(puzzle1, 11) == True
    assert _is_free(puzzle1, 8) == False
    assert _is_free(puzzle1, 1) == False
    assert _is_free(puzzle1, 31) == True

    assert set(_available_actions(puzzle1)) == \
           {('G', 1), ('G', 2), ('G', 3), ('Y', 8), ('B', -8), ('B', 8), ('B', 16), ('A', -1), ('A', -2), ('A', -3)}

    assert _apply_action(puzzle1, ('G', 1)) == puzzle1_G1
    assert _apply_action(puzzle1, ('B', -8)) == puzzle1_Bm8

    succ = successors(puzzle1)
    assert sorted(list(succ.values())) == sorted(_available_actions(puzzle1))
    ok_G1 = ok_Bm8 = False
    for (state, action) in successors(puzzle1).items():
        if action == ('G', 1):
            assert state == puzzle1_G1
            ok_G1 = True
        if action == ('B', -8):
            assert state == puzzle1_Bm8
            ok_Bm8 = True
    assert ok_G1
    assert ok_Bm8

    result = shortest_path_search(puzzle1, successors, is_goal)
    assert path_actions(result) == [('A', -3), ('Y', 24), ('B', 16), ('*', 4)]
    assert path_actions(solve_parking_puzzle(puzzle1)) == [('A', -3), ('Y', 24), ('B', 16), ('*', 4)]

    assert path_actions(solve_parking_puzzle(puzzle4done)) == []

    return 'tests pass'


print(tests())
