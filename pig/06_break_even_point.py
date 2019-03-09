import math

million = 1000000


def Q(state, action, U):
    "The expected value of taking action in state, according to utility U"
    if action == 'hold':
        return U(state + 1 * million)
    if action == 'gamble':
        return U(state + 3 * million) * 0.5 + U(state) * 0.5


U = math.log10

# What is c such that Q(c,'gamble',U) == Q(c,'hold',U)
print(min(
    [(abs(Q(c, 'gamble', U) - Q(c, 'hold', U)), c) for c in range(100000, 10000000, 100000)],
    key=lambda x: x[0]
))
