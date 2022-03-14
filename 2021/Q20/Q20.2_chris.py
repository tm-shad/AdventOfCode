from pathlib import Path
from collections import Counter, defaultdict
from copy import copy, deepcopy
from functools import partial
import math
from pprint import pprint

# input_path = Path(f'{__file__}/../input_example.txt').resolve()
input_path = Path(f'{__file__}/../input_chris.txt').resolve()

print(input_path)

with open(input_path) as f:
    input_text = f.readlines()

blocks = ''.join(input_text).split('\n\n')

def generate_orientations():
    orientations = [
        # Choose facing direction
        # lambda x, y, z: ( x,  y,  z), # Facing x
        # lambda x, y, z: (-x, -y,  z), # Facing -x
        # lambda x, y, z: ( y, z ,  x), # Facing y ##########
        # lambda x, y, z: (-y, -z,  x), # Facing -y ########
        # lambda x, y, z: ( z,  x,  y), # Facing z
        # lambda x, y, z: (-z, -x,  y), # Facing -z

        # Facing positive x, which way is up
        lambda x, y, z: ( x,  y,  z), # 0 degree turn
        lambda x, y, z: ( x,  z, -y), # 90 degree turn
        lambda x, y, z: ( x, -y, -z), # 180 degree turn
        lambda x, y, z: ( x, -z,  y), # 270 degree turn
    ]

    # Choose facing direction
    # Need to use this partial function weirdness otherwise functions don't generate properly.
    orientations = [
        [
            # Facing positive x, which way is up
            # partial(lambda x, y, z, func=None: (*func( x,  y,  z),), func=orientation), # 0 degree turn
            # partial(lambda x, y, z, func=None: (*func( x,  z, -y),), func=orientation), # 90 degree turn
            # partial(lambda x, y, z, func=None: (*func( x, -y, -z),), func=orientation), # 180 degree turn
            # partial(lambda x, y, z, func=None: (*func( x, -z,  y),), func=orientation), # 270 degree turn

            # Choose facing direction
            partial(lambda x, y, z, func=None: (*func( x,  y,  z),), func=deepcopy(orientation)), # Facing x
            partial(lambda x, y, z, func=None: (*func(-x, -y,  z),), func=deepcopy(orientation)), # Facing -x
            partial(lambda x, y, z, func=None: (*func( y, z ,  x),), func=deepcopy(orientation)), # Facing y ##########
            partial(lambda x, y, z, func=None: (*func(-y, -z,  x),), func=deepcopy(orientation)), # Facing -y ########
            partial(lambda x, y, z, func=None: (*func( z,  x,  y),), func=deepcopy(orientation)), # Facing z
            partial(lambda x, y, z, func=None: (*func(-z, -x,  y),), func=deepcopy(orientation)), # Facing -z

            ] for orientation in orientations
    ]

    orientations = [i for j in orientations for i in j]

    return orientations

# def generate_orientations():
#     # This is the WRONG method, producing 48 distinct orientations, half of which are invalid.

#     # Choose XYZ permutation
#     orientations = [
#         lambda x, y, z: (x, y, z),
#         lambda x, y, z: (x, z, y),
#         lambda x, y, z: (y, x, z),
#         lambda x, y, z: (y, z, x),
#         lambda x, y, z: (z, y, x),
#         lambda x, y, z: (z, x, y),
#         ]

#     # Choose XYZ negation
#     # Need to use this partial function weirdness otherwise functions don't generate properly.
#     orientations = [
#         [
#             partial(lambda x, y, z, func=None: (*func( x,  y,  z),), func=orientation),
#             partial(lambda x, y, z, func=None: (*func( x,  y, -z),), func=orientation),
#             partial(lambda x, y, z, func=None: (*func( x, -y,  z),), func=orientation),
#             partial(lambda x, y, z, func=None: (*func(-x,  y,  z),), func=orientation),
#             partial(lambda x, y, z, func=None: (*func( x, -y, -z),), func=orientation),
#             partial(lambda x, y, z, func=None: (*func(-x, -y,  z),), func=orientation),
#             partial(lambda x, y, z, func=None: (*func(-x,  y, -z),), func=orientation),
#             partial(lambda x, y, z, func=None: (*func(-x, -y, -z),), func=orientation),
#             ] for orientation in orientations
#     ]

#     orientations = [i for j in orientations for i in j]

#     return orientations

orientations = generate_orientations()
coords = []
# print('len ori', len(orientations))
for orientation in orientations:
    coord = orientation(1, 2, 3)
    if coord in coords:
        print("coord found twice", coord)
    coords.append(coord)
# [print(i, coord) for i, coord in enumerate(coords)]

blocks = {block.split('\n')[0]: block.split('\n')[1:] for block in blocks}

# Find the matches
matches = {block_name: {} for block_name in blocks.keys()}
for block_name1, block1 in blocks.items():
    points1 = [point.split(',') for point in block1]
    points1 = {(int(point[0]), int(point[1]), int(point[2])) for point in points1}
    for block_name2, block2 in blocks.items():
        match_found = False
        if block_name1 is block_name2:
            continue
        points2 = [point.split(',') for point in block2]
        points2 = {(int(point[0]), int(point[1]), int(point[2])) for point in points2}

        for i_ori, orientation in enumerate(orientations):
            match_found = False
            ori_points2 = {orientation(*point) for point in points2}

            for translate_point1 in points1:
                for translate_point2 in ori_points2:
                    dx, dy, dz = (
                        translate_point1[0] - translate_point2[0],
                        translate_point1[1] - translate_point2[1],
                        translate_point1[2] - translate_point2[2],
                    )

                    translate_points2 = {(
                        point[0] + dx,
                        point[1] + dy,
                        point[2] + dz,
                    ) for point in ori_points2}

                    if len(points1 & translate_points2) >= 12:
                        # print("Potential Match")
                        # If scanner 1 still has points in range.
                        if any([all([abs(ax)<=1000 for ax in far_point]) 
                        for far_point in (translate_points2 - points1)]):
                            break
                        # If scanner 2 still has points in range.
                        if any([all([abs(ax)<=1000 for ax in (a-b for a, b in zip(far_point, (dx, dy, dz)))]) 
                        for far_point in (points1 - translate_points2)]):
                            break
                        # print("Match Found", i_ori, block_name1, block_name2, dx, dy, dz)
                        transform = partial(
                            lambda x, y, z, 
                            func=None, 
                            dx=None, dy=None, dz=None
                            : 
                            tuple(a+b for a,b in zip(func(x, y, z),(dx, dy, dz))), 
                            func=deepcopy(orientation),
                            dx=dx, dy=dy, dz=dz
                        )
                        print(block_name1, block_name2, transform(1, 2, 3))
                        matches[block_name1][block_name2] = deepcopy(transform)
                        # matches[block_name1][block_name2] = (i_ori, orientation, dx, dy, dz)
                        # print(points1.intersection(translate_points2))
                        match_found = True
                        break
                    # if len(points1.intersection(translate_points2)) > 1:
                    #     print(len(points1.intersection(translate_points2)), i_ori, block_name1, block_name2, dx, dy, dz)

                if match_found:
                    break
            # if match_found:
            #     break

# pprint(matches)

# print("Match test")
# for k, v in matches.items():
#     for k2, v2 in v.items():
#         print(k, k2, v2(1,2,3))

# Reconstruct the point map.
print("Reconstructing")
point_maps = []
seen_scanners = set()
scanner_positions = [(0,0,0)]

for scanner_name1, match_dict in matches.items():
    if scanner_name1 in seen_scanners:
        continue
    seen_scanners.add(scanner_name1)
    points1 = [point.split(',') for point in blocks[scanner_name1]]
    points1 = {(int(point[0]), int(point[1]), int(point[2])) for point in points1}
    # print("Mapped", scanner_name1)
    # pprint(points1)

    search_queue = [(k, scanner_name1, v) for k,v in match_dict.items()]
    # print(search_queue)
    while search_queue:
        # scanner_name2, (i_ori2, orientation2, dx2, dy2, dz2) = search_queue.pop(0)
        scanner_name2, path2, transform2 = search_queue.pop(0)
        if scanner_name2 in seen_scanners:
            continue
        seen_scanners.add(scanner_name2)
        points2 = [point.split(',') for point in blocks[scanner_name2]]
        points2 = {(int(point[0]), int(point[1]), int(point[2])) for point in points2}
        transform_points2 = {transform2(*point) for point in points2}

        # print("Mapped", path2, scanner_name2)
        print(scanner_name1, scanner_name2, transform2(1, 2, 3))
        scanner_positions.append(transform2(0,0,0))
        # pprint(points1)
        # pprint(transform_points2)
        # print(len(points1 & translate_points2))
        points1 = points1 | transform_points2
        # print(scanner_name1, scanner_name2, (i_ori2, orientation2, dx2, dy2, dz2))
        

        for scanner_name3, transform3 in matches[scanner_name2].items():
            new_transform = partial(
                lambda x, y, z, 
                func1=None, func2=None
                : 
                func1(*func2(x, y, z)),
                func1=copy(transform2),
                func2=copy(transform3),
                )
            search_queue.append((scanner_name3, f"{path2} {scanner_name2}", copy(new_transform)))
            

    point_maps.append(points1)

num_beacons = 0
print("Num Maps", len(point_maps))
for point_map in point_maps:
    num_beacons += len(point_map)
print("Num Beacons", num_beacons)

dists = []
for scanner1 in scanner_positions:
    for scanner2 in scanner_positions:
        dists.append(
              (scanner1[0]-scanner2[0])
            + (scanner1[1]-scanner2[1])
            + (scanner1[2]-scanner2[2])
            )

print("Max Dist", max(dists))