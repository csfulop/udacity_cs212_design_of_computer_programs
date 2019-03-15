"""
Using enumeration to calculate conditional probabilities
"""

import itertools
from fractions import Fraction

sex = 'BG'


def product(*variables):
    return list(map(''.join, itertools.product(*variables)))


two_kids = product(sex, sex)
print('Two kids: ', two_kids)

one_boy = [s for s in two_kids if 'B' in s]
print('One boy | Two kids: ', one_boy)


def two_boys(s):
    return s.count('B') == 2


def condP(predicate, event):
    pred = [s for s in event if predicate(s)]
    return Fraction(len(pred), len(event))


print('P(Two boy | One boy) = ', condP(two_boys, one_boy))
print()

days = 'MTWtFsS'
two_kids_days = product(sex, days, sex, days)
print('Two kids: ', two_kids_days)
print('len(Two kids) = ', len(two_kids_days))

one_boy_on_Tuesday = [s for s in two_kids_days if 'BT' in s]
print('One boy | Two kids :', one_boy_on_Tuesday)
print('len(One boy | Two kids) = ', len(one_boy_on_Tuesday))

print('P(Two boy } One boy) = ',condP(two_boys, one_boy_on_Tuesday))
