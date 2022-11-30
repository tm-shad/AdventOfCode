from dataclasses import dataclass
from pathlib import Path
from collections import Counter, defaultdict
from copy import copy, deepcopy
from functools import partial
import math
from pprint import pprint
from itertools import product

input_path = Path(f'{__file__}/../input_example.txt').resolve()
# input_path = Path(f'{__file__}/../input_example1.txt').resolve()
# input_path = Path(f'{__file__}/../input_chris.txt').resolve()

print(input_path)

with open(input_path) as f:
    input_text = f.readlines()

boxes = set()

sign = lambda x: math.copysign(1, x)

def find_and_split(box1, box2):
    # Find box1 in box2, then split box2
    boxes = set()

    box1_corners = list(product(box1[0], box1[1], box1[2]))
    box2_corners = list(product(box2[0], box2[1], box2[2]))
    # For each corner of box1
    for corner1 in box1_corners:
        # If corner1 is a box2 corner, it's useless.
        if corner1 in box2_corners:
            continue
        # If corner1 in box2
        if (
                (box2[0][0] <= corner1[0]) and (corner1[0] <= box2[0][1])
            and (box2[1][0] <= corner1[1]) and (corner1[1] <= box2[1][1])
            and (box2[2][0] <= corner1[2]) and (corner1[2] <= box2[2][1])
        ):
            # Find the split that includes corner1
            opposite_corner1 = None
            for opposite_corner1 in box1_corners:
                if all(c1!=c2 for c1,c2 in zip(opposite_corner1, corner1)):
                    break # Set opposite_corner
            dx = sign(corner1[0]-opposite_corner1[0])
            dy = sign(corner1[1]-opposite_corner1[1])
            dz = sign(corner1[2]-opposite_corner1[2])

            # Split the boxes
            new_boxes = set()
            for corner2, congruent_corner1 in zip(box2_corners, box1_corners):
                # If we are the 3D opposite to corner1, we get corner1 in our borders.
                cdx = (opposite_corner1[0] != congruent_corner1[0]) * dx
                cdy = (opposite_corner1[1] != congruent_corner1[1]) * dy
                cdz = (opposite_corner1[2] != congruent_corner1[2]) * dz

                # if opposite_corner1 == congruent_corner1:
                #     new_boxes.add(tuple([
                #         (*sorted([corner1[0], corner2[0]]),),
                #         (*sorted([corner1[1], corner2[1]]),),
                #         (*sorted([corner1[2], corner2[2]]),),
                #     ]))
                # Otherwise we are 1 less in size
                # else:
                #     new_boxes.add(tuple([
                #         (*sorted([corner1[0]+dx, corner2[0]]),),
                #         (*sorted([corner1[1]+dy, corner2[1]]),),
                #         (*sorted([corner1[2]+dz, corner2[2]]),),
                #     ]))
                new_boxes.add(tuple([
                    (*sorted([corner1[0]+cdx, corner2[0]]),),
                    (*sorted([corner1[1]+cdy, corner2[1]]),),
                    (*sorted([corner1[2]+cdz, corner2[2]]),),
                ]))
                boxes = boxes | new_boxes
    return boxes

for i, line in enumerate(input_text):
    line = line.strip()
    instruction, ranges = line.split(' ')
    print("Line", i)
    print("Instruction", instruction)
    (xmin, xmax), (ymin, ymax), (zmin, zmax) = [
        (int(num) for num in box_range.split('=')[1].split('..')) 
        for box_range in ranges.split(',')
        ]
    if any([abs(num)>50 for num in [xmin, xmax, ymin, ymax, zmin, zmax]]):
        continue
    operator_boxes = set()
    operator_boxes.add(tuple([(xmin, xmax), (ymin, ymax), (zmin, zmax)]))
    prev_op_boxes = None
    k=0
    while operator_boxes != prev_op_boxes:
        print(k)
        k+=1
        prev_op_boxes = copy(operator_boxes)
        for box1 in list(operator_boxes):
            for root_box in list(boxes):
                boxes.remove(root_box)
                root_boxes = set()
                root_boxes.add(root_box)
                prev_root_boxes = None
                j=0
                while root_boxes != prev_root_boxes:
                    print(j)
                    j+=1
                    prev_root_boxes = copy(root_boxes)
                    for box2 in list(root_boxes):
                        if box1 == box2:
                            continue

                        new_boxes = find_and_split(box1, box2)
                        # print("New Boxes", new_boxes)
                        if len(new_boxes) > 0:
                            root_boxes.remove(box2)
                            root_boxes = root_boxes | new_boxes

                        new_boxes = find_and_split(box2, box1)
                        if len(new_boxes) > 0:
                            operator_boxes.discard(box1)
                            operator_boxes = operator_boxes | new_boxes

                boxes = boxes | root_boxes
        if instruction == 'on':
            boxes = boxes | operator_boxes
        elif instruction == 'off':
            boxes = boxes - operator_boxes
        else:
            print("BUG")

                        


sum = 0
for box in boxes:
    sum += (
         (box[0][1]-box[0][0])
        *(box[1][1]-box[1][0])
        *(box[2][1]-box[2][0])
        )

print("SUM", sum)