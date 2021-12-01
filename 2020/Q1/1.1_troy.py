from time import perf_counter


INPUT_FILE = r"C:\Users\Troy\Documents\Git Dev\Advent of Code\2020\1.1\input_troy.txt"
TARGET_INT = 2020

expenses = {}
with open(INPUT_FILE) as f:
    for l in f.readlines():
        expenses[int(l)] = True

startTime = perf_counter()

# find pair of numbers
for d1 in expenses.keys():
    d2 = 2020 - d1

    try:
        if expenses[d2]:
            # if d2 in expenses.keys():
            final_num = d1 * d2
            break

    except KeyError:
        pass


print(perf_counter() - startTime)