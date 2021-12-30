from os import DirEntry
from pathlib import Path
import logging
from enum import IntEnum
from time import perf_counter

from tqdm import tqdm

from math import floor, ceil


logging.basicConfig(level=logging.ERROR)

INPUT_FILE = str(Path(__file__).parent.joinpath("input_example.txt").resolve())
INPUT_FILE = str(Path(__file__).parent.joinpath("input_troy.txt").resolve())

with open(INPUT_FILE) as f:
    lines = f.readlines()

time_start = perf_counter()


class Direction(IntEnum):
    LEFT = -1
    RIGHT = 1


class Leaf:
    def __init__(self, value, parent, leaf_index: int = -1) -> None:
        self.value = value
        self.parent = parent
        self.indentation = self.parent.indentation + 1

        if leaf_index == -1:
            self.leaf_list.append(self)
        else:
            self.leaf_list.insert(leaf_index, self)
        logging.debug(f"Adding leaf with value {self.value}")

    def __str__(self):
        return f"{self.value}"

    def __repr__(self):
        return f"{self}"

    def update_parent(self, new_parent):
        self.parent = new_parent
        self.indentation = self.parent.indentation + 1

    def magnitude(self):
        return self.value

    @property
    def leaf_list(self):
        return self.parent.leaf_list


class Tree:
    #
    # Constructors
    #
    def __init__(self, left, right, parent=None, default_leaf_list=None):
        self.branches = {
            Direction.LEFT: left,
            Direction.RIGHT: right,
        }
        self.parent = parent

        self._leaf_list = None
        if self.parent is None:
            self._leaf_list = [] if default_leaf_list is None else default_leaf_list

        if parent is not None:
            self.indentation = self.parent.indentation + 1
        else:
            self.indentation = 1

    @staticmethod
    def from_list_data(data, parent=None):
        in_data = {Direction.LEFT: None, Direction.RIGHT: None}
        in_data[Direction.LEFT], in_data[Direction.RIGHT] = data

        new_tree = Tree(None, None, parent)
        for dir_key in [Direction.LEFT, Direction.RIGHT]:
            if type(in_data[dir_key]) == int:
                new_tree.branches[dir_key] = Leaf(
                    value=in_data[dir_key], parent=new_tree
                )
            else:
                new_tree.branches[dir_key] = Tree.from_list_data(
                    data=in_data[dir_key], parent=new_tree
                )

        return new_tree

    @staticmethod
    def from_string(string):
        new_tree = Tree.from_list_data(eval(string))
        assert str(new_tree) == string
        return new_tree

    #
    # Left & Right Properties
    #
    @property
    def left(self):
        return self.branches[Direction.LEFT]

    @left.setter
    def left(self, value):
        self.branches[Direction.LEFT] = value

    @property
    def right(self):
        return self.branches[Direction.RIGHT]

    @right.setter
    def right(self, value):
        self.branches[Direction.RIGHT] = value

    #
    # String representation
    #
    def __str__(self):
        return f"[{self.left},{self.right}]"

    def __repr__(self):
        return f"{self}"

    #
    # Addition with other trees
    #
    def update_parent(self, new_parent, default_leaf_list=None):
        self.parent = new_parent
        self.indentation = new_parent.indentation + 1

        if self.parent is None:
            self._leaf_list = [] if default_leaf_list is None else default_leaf_list
        else:
            self._leaf_list = None

        for i in self.branches.values():
            i.update_parent(self)

    def update_branch(self, old_branch, new_branch):
        for (
            k,
            v,
        ) in self.branches.items():
            if v == old_branch:
                self.branches[k] = new_branch

    def __add__(self, other):
        assert type(other) == type(self)

        new_parent = Tree(
            left=self,
            right=other,
            parent=None,
            default_leaf_list=self.leaf_list + other.leaf_list,
        )

        for node in new_parent.branches.values():
            node.update_parent(new_parent)
            node.update_parent(new_parent)
        logging.info(f"after addition: {new_parent}")

        new_parent.reduce()

        return new_parent

    @property
    def leaf_list(self):
        if self.parent is None:
            return self._leaf_list
        else:
            return self.parent.leaf_list

    #
    # Reduction functions
    #
    def reduce(self):
        has_changed = True

        while has_changed:
            if self.explode():
                continue
            elif self.split():
                continue
            else:
                has_changed = False

    def explode(self):
        # look for the first leaf that can explode
        explode_node = next(
            (l.parent for l in self.leaf_list if l.parent.indentation > 4),
            None,
        )
        if explode_node is None:
            return False
        else:
            logging.debug(f"can explode: {explode_node}")

            # explode left
            i = self.leaf_list.index(explode_node.left)
            if i > 0:
                self.leaf_list[i - 1].value += self.leaf_list[i].value
            self.leaf_list.pop(i)

            # explode right
            i = self.leaf_list.index(explode_node.right)
            if i < len(self.leaf_list) - 1:
                self.leaf_list[i + 1].value += self.leaf_list[i].value
            self.leaf_list.pop(i)

            # set node to zero leaf
            new_leaf = Leaf(value=0, parent=explode_node.parent, leaf_index=i)
            explode_node.parent.update_branch(explode_node, new_leaf)

            logging.info(f"after explosion: {self}")

            return True

    def split(self):
        # look for the first leaf that can split
        split_leaf = next(
            (l for l in self.leaf_list if l.value >= 10),
            None,
        )
        if split_leaf is None:
            return False
        else:
            logging.debug(f"can split: {split_leaf}")

            i = self.leaf_list.index(split_leaf)
            self.leaf_list.pop(i)

            new_branch = Tree(None, None, parent=split_leaf.parent)
            new_branch.left = Leaf(
                value=floor(split_leaf.value / 2), parent=new_branch, leaf_index=i
            )
            new_branch.right = Leaf(
                value=ceil(split_leaf.value / 2), parent=new_branch, leaf_index=i + 1
            )

            split_leaf.parent.update_branch(split_leaf, new_branch)

            logging.info(f"after split: {self}")
            return True

    def magnitude(self):
        return 3 * self.left.magnitude() + 2 * self.right.magnitude()


mags = {}
highest_mag = (-999, None)

for i in tqdm(range(len(lines)), ncols=100, total=len(lines)):
    for j in tqdm(
        range(len(lines)), position=1, leave=False, ncols=100, total=len(lines)
    ):
        if i == j:
            continue
        else:
            curr_mag = (
                Tree.from_string(lines[i].strip()) + Tree.from_string(lines[j].strip())
            ).magnitude()

            if curr_mag > highest_mag[0]:
                highest_mag = (curr_mag, (i, j))

print(highest_mag)

time_end = perf_counter()
print(time_end - time_start)
# original = 6.097582
# new = 6.5476598
