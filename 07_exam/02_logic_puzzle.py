"""
UNIT 2: Logic Puzzle

You will write code to solve the following logic puzzle:

1. The person who arrived on Wednesday bought the laptop.
2. The programmer is not Wilkes.
3. Of the programmer and the person who bought the droid,
   one is Wilkes and the other is Hamming.
4. The writer is not Minsky.
5. Neither Knuth nor the person who bought the tablet is the manager.
6. Knuth arrived the day after Simon.
7. The person who arrived on Thursday is not the designer.
8. The person who arrived on Friday didn't buy the tablet.
9. The designer didn't buy the droid.
10. Knuth arrived the day after the manager.
11. Of the person who bought the laptop and Wilkes,
    one arrived on Monday and the other is the writer.
12. Either the person who bought the iphone or the person who bought the tablet
    arrived on Tuesday.

You will write the function logic_puzzle(), which should return a list of the
names of the people in the order in which they arrive. For example, if they
happen to arrive in alphabetical order, Hamming on Monday, Knuth on Tuesday, etc.,
then you would return:

['Hamming', 'Knuth', 'Minsky', 'Simon', 'Wilkes']

(You can assume that the days mentioned are all in the same week.)
"""
import itertools

NAMES = ['Wilkes', 'Hamming', 'Minsky', 'Knuth', 'Simon']


def logic_puzzle():
    "Return a list of the names of the people, in the order they arrive."
    ## your code here; you are free to define additional functions if needed
    DAYS = (Monday, Tuesday, Wednesday, Thursday, Friday) = (1, 2, 3, 4, 5)
    orderings = list(itertools.permutations(DAYS))
    for (Laptop, Droid, Tablet, Iphone, _) in orderings:
        if Laptop != Wednesday: continue  # 1
        if Tablet == Friday: continue  # 8
        if Tuesday not in (Iphone, Tablet): continue  # 12
        for (Programmer, Writer, Manager, Designer, _) in orderings:
            if Designer == Thursday: continue  # 7
            if Designer == Droid: continue  # 9
            for (Wilkes, Hamming, Minsky, Knuth, Simon) in orderings:
                if Wilkes == Programmer: continue  # 2
                if {Programmer, Droid} != {Wilkes, Hamming}: continue  # 3
                if Writer == Minsky: continue  # 4
                if Knuth == Tablet or Manager in (Knuth, Tablet): continue  # 5
                if Knuth != Simon + 1: continue  # 6
                if Knuth != Manager + 1: continue  # 10
                if Wilkes == Laptop or Monday == Writer or {Wilkes, Laptop} != {Monday, Writer}: continue  # 11
                # print(Laptop, Droid, Tablet, Iphone)
                # print(Programmer, Writer, Manager, Designer)
                # print(Wilkes, Hamming, Minsky, Knuth, Simon)
                day_name_map = {day: NAMES[name] for name, day in enumerate((Wilkes, Hamming, Minsky, Knuth, Simon))}
                return list(day_name_map[day] for day in DAYS)


print(logic_puzzle())
