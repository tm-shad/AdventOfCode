from pathlib import Path
from collections import Counter, defaultdict
from copy import copy, deepcopy
from functools import partial
import math
from pprint import pprint

from pathlib import Path

# input_path = Path(f'{__file__}/../input_example.txt').resolve()
input_path = Path(f'{__file__}/../input_chris.txt').resolve()

with open(input_path) as f:
    input_text = f.readlines()



print(input_path)

input_text = [line.strip() for line in input_text]

print(input_text)

symbols = []
for i in range(len(input_text)):
    for j in range(len(input_text[0])):
        char = input_text[i][j]
        if char.isdigit() or char == '.':
            continue
        symbols.append((i,j))

# print(symbols)

nums = []
coords = set()
seen_coords = set()
for sym in symbols:
    for i in range(-1, 2):
        for j in range(-1, 2):
            x = sym[0]+i
            y = sym[1]+j
            if x < 0 or x > len(input_text) or y < 0 or y > len(input_text[0]):
                continue
            if not input_text[x][y].isdigit():
                continue
            print(input_text[x][y])
            if (x,y) in seen_coords:
                continue
            seen_coords.add((x,y))

            k = y
            while k >= 0:
                if input_text[x][k].isdigit():
                    seen_coords.add((x, k))
                else:
                    break
                k -= 1
            k += 1
            start_coords = (x, k)
            print("start", input_text[x][k])

            while k <= len(input_text[0])-1:
                if input_text[x][k].isdigit():
                    seen_coords.add((x, k))
                else:
                    break
                k += 1
            k -= 1
            end_coords = (x, k)

            print(start_coords, end_coords)
            print(input_text[x][start_coords[1]:end_coords[1]+1])
            nums.append(int(input_text[x][start_coords[1]:end_coords[1]+1]))
                
print("SUM", sum(nums))
# numbers = set()
# for sym in symbols:
#     for i in range(-1, 2):
#         for j in range(-1, 2):
#             if sym[0]+i

#             if not input_text[sym[0]+i][sym[1]+j].isdigit():
#                 continue
#             print(input_text[sym[0]+i][sym[1]+j])
#             k = sym[1]+j
#             while k >= 0:
#                 if input_text[sym[0]+i][k].isdigit():
#                     print(input_text[sym[0]+i][k])
#                     k -= 1
#                 else:
#                     k -=1
#                     break
#             k += 1
#             start_coords = (sym[0]+i, k)
#             print(start_coords)
#             while k <= len(input_text[0]):
#                 if input_text[sym[0]+i][k].isdigit():
#                     print(input_text[sym[0]+i][k])
#                     k += 1
#                 else:
#                     k += 1
#                     break
#             k -= 1
#             end_coords = (sym[0]+i, k)
#             print(input_text[end_coords[0]][end_coords[1]])
#             print(start_coords, end_coords)
#             numbers.add((start_coords, end_coords))

# print(numbers)


# nums = []
# for start_coords, end_coords in numbers:
#     num = input_text[start_coords[0]][start_coords[1]:end_coords[1]]
#     print(num)
#     # nums.append()
