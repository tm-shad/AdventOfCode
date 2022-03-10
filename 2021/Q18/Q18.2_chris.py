from pathlib import Path
from collections import Counter, defaultdict
from copy import copy
import math

# input_path = Path(f'{__file__}/../input_example.txt').resolve()
# input_path = Path(f'{__file__}/../input_example1.txt').resolve()
input_path = Path(f'{__file__}/../input_chris.txt').resolve()

print(input_path)

with open(input_path) as f:
    input_text = f.readlines()

lines = [line.strip() for line in input_text]

class Pair():
    def __init__(self, data, depth=0, is_left=True, parent=None):
        # print(data)
        self.string = data
        self.depth = depth
        self.is_left = is_left
        self.parent = parent

        left, right = self.find_left_right(data)
        # print("left", left)
        # print("right", right)
        if left.isdigit():
            left = int(left)
        else:
            left = Pair(left, depth=depth+1, is_left=True, parent=self)

        if right.isdigit():
            right = int(right)
        else:
            right = Pair(right, depth=depth+1, is_left=False, parent=self)

        self.left = left
        self.right = right

    def find_left_right(self, data):
        # print("split data", data)
        # data = data[1:-1]
        op_count = 0
        for i in range(len(data)):
            char = data[i]
            if char == '[':
                op_count += 1
            elif char == ']':
                op_count -= 1
            elif char == ',':
                if op_count == 1:
                    return data[1:i], data[i+1:-1]
        
        raise Exception("It don't work.", data)

    def __repr__(self):
        return f'[{self.left.__repr__()},{self.right.__repr__()}]'

    def reduce(self):
        if self.reduce_explode():
            return True
        if self.reduce_split():
            return True

    def reduce_explode(self):
        if self.depth == 4:
            self.explode()
            return True

        if not isinstance(self.left, int):
            if self.left.reduce_explode():
                return True

        if not isinstance(self.right, int):
            if self.right.reduce_explode():
                return True

    def reduce_split(self):
        if not isinstance(self.left, int):
            if self.left.reduce_split():
                return True

        if isinstance(self.left, int):
            if self.left > 9:
                self.split_left()
                return True

        if not isinstance(self.right, int):
            if self.right.reduce_split():
                return True

        if isinstance(self.right, int):
            if self.right > 9:
                self.split_right()
                return True

        return False
        
    def explode(self):
        left = self.left
        right = self.right

        # Left-element traverses until we find a different left. Then goes down right side.
        node = self
        while True:
            if not node:
                break
            if not node.is_left:
                node = node.parent
                break
            node = node.parent
        # print('node is', node)
        if node:
            if isinstance(node.left, int):
                node.left += left
            else:
                node = node.left
                while True:
                    if not node:
                        break
                    if isinstance(node.right, int):
                        break
                    node = node.right
                if node:
                    node.right += left

        # Right-element traverses until we find a different right. Then goes down left side.
        node = self
        while True:
            if not node:
                break
            if node.is_left:
                node = node.parent
                break
            node = node.parent
        # print('node is', node)
        if node:
            if isinstance(node.right, int):
                node.right += right
            else:
                node = node.right
                while True:
                    if not node:
                        break
                    if isinstance(node.left, int):
                        break
                    node = node.left
                if node:
                    node.left += right

        if self.is_left:
            self.parent.left = 0
        else:
            self.parent.right = 0    

    def split_left(self):
        left = math.floor(self.left/2.0)
        right = math.ceil(self.left/2.0)
        self.left = Pair(f'[{left},{right}]', depth=self.depth+1, is_left=True, parent=self)
        
    def split_right(self):
        left = math.floor(self.right/2.0)
        right = math.ceil(self.right/2.0)
        self.right = Pair(f'[{left},{right}]', depth=self.depth+1, is_left=False, parent=self)

    def add(self, other):
        return Pair(f'[{self.__repr__()},{other.__repr__()}]')

    def get_magnitude_sum(self):
        if isinstance(self.left, int):
            left = self.left
        else:
            left = self.left.get_magnitude_sum()

        if isinstance(self.right, int):
            right = self.right
        else:
            right = self.right.get_magnitude_sum()

        return 3*left + 2*right


# pair = Pair(lines[0])

# for pair in [
#     "[[[[[9,8],1],2],3],4]",
#     "[7,[6,[5,[4,[3,2]]]]]",
#     "[[6,[5,[4,[3,2]]]],1]",
#     "[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]",
#     "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]",
#     "[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]"
# ]:
#     pair = Pair(pair)
#     print(pair.get_magnitude_sum())
#     print(pair)

#     rep = pair.__repr__()
#     pair.reduce()
#     while rep != pair.__repr__():
#         print(pair)
#         rep = pair.__repr__()
#         pair.reduce()


# lines = [
#     "[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]",
#     "[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]",
#     "[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]",
#     "[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]",
#     "[7,[5,[[3,8],[1,4]]]]",
#     "[[2,[2,2]],[8,[8,1]]]",
#     "[2,9]",
#     "[1,[[[9,3],9],[[9,0],[0,7]]]]",
#     "[[[5,[7,4]],7],1]",
#     "[[[[4,2],2],6],[8,7]]",
# ]

# pair = None
# for line in lines:
#     print("  ", pair)
#     if not pair:
#         pair = Pair(line) 
#     else:
#         print("+ ", line)
#         pair = pair.add(Pair(line))
    
#     rep = pair.__repr__()
#     pair.reduce()
#     while rep != pair.__repr__():
#         # print(pair)
#         rep = pair.__repr__()
#         pair.reduce()
#     print("= ", pair)
#     print()
# print(pair.get_magnitude_sum())

magnetudes = []
for i in range(len(lines)):
    for j in range(len(lines)):
        if i == j:
            continue
        pair = Pair(lines[i]).add(Pair(lines[j]))
        rep = pair.__repr__()
        pair.reduce()
        while rep != pair.__repr__():
            # print(pair)
            rep = pair.__repr__()
            pair.reduce()
        magnetudes.append(pair.get_magnitude_sum())

print(sorted(magnetudes, reverse=True))