from time import perf_counter


INPUT_FILE = r"C:\Users\Troy\Documents\Git Dev\Advent of Code\2020\1.1\input_troy.txt"

expenses = {}
with open(INPUT_FILE) as f:
    for l in f.readlines():
        expenses[int(l)] = True

startTime = perf_counter()

# find pair of numbers
TARGET_INT = 2020

expenses_list = list(expenses.keys())
final_num = None
for i, d1 in enumerate(expenses_list):
    target_2 = 2020 - d1
    for d2 in expenses_list[i:]:
        d3 = target_2 - d2
        try:
            if expenses[d3]:
                # if d2 in expenses.keys():
                final_num = d1 * d2 * d3
                break

        except KeyError:
            pass

    if final_num is not None:
        break


print(perf_counter() - startTime)
print(final_num)