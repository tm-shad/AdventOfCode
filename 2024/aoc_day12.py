from collections import defaultdict
import functools

import math
import pathlib
from tqdm import tqdm
from tqdm.contrib.concurrent import process_map

UP= complex(-1,0)
DOWN= complex(1,0)
LEFT= complex(0,-1)
RIGHT= complex(0,1)

class Region:
    def __init__(self, points: set[complex], char: str):
        self.points = points
        self._char = char

    @property
    def area(self) -> int:
        return len(self.points)

    @property
    def perimiter(self) -> int:
        basic_perimiter = 4*self.area

        for p in self.points:
            for v in [UP, DOWN, LEFT, RIGHT]:
                if p+v in self.points:
                    basic_perimiter -= 1
        
        return basic_perimiter
    
    @property
    def price(self) -> int:
        return self.area*self.perimiter
    
    @property
    def sides(self) -> int:
        sides = 0
        for v in [UP, DOWN, LEFT, RIGHT]:
            offset_v = v*complex(0,1)
            seen_points = set()
            unseen_points = self.points.copy()

            while(len(unseen_points)>0):
                pending_side_points = set([unseen_points.pop()])
                seen_side_points = set()

                while(len(pending_side_points)>0):
                    curr_point = pending_side_points.pop()


                    # check if 90 degrees offset is filled
                    if offset_v+curr_point in self.points:
                        # not a side worth checking
                        unseen_points.discard(curr_point)
                        continue
                    else:
                        # keep looking left and right
                        for next_point in [curr_point+v, curr_point-v]:
                            # check if a point in the current region
                            if next_point not in pending_side_points.union(seen_side_points) and next_point in self.points:
                                unseen_points.discard(next_point)
                                pending_side_points.add(next_point)

                    seen_side_points.add(curr_point)
                seen_points.update(seen_side_points)
                sides += 1 if len(seen_side_points)>0 else 0
        
        return sides
                

    @property
    def discount_price(self) -> int:
        return self.area*self.sides

class RegionMap:
    def __init__(self, flat_map: str):
        self.w = len(flat_map.splitlines()[0])
        self.h = len(flat_map.splitlines())
        self.regions = RegionMap.load_map(flat_map)

    @staticmethod
    def load_map(flat_map: str) -> list[Region]:
        unallocated_points = set()
        char_map = defaultdict(lambda: '-')
        for i, line in enumerate(flat_map.splitlines()):
            for j, char in enumerate(line):
                unallocated_points.add(complex(i,j))
                char_map[complex(i,j)] = char
        
        regions = []


        while(len(unallocated_points)>0):
            unseen_points = set([unallocated_points.pop()])
            seen_points = set()

            while(len(unseen_points)>0):
                curr_point = unseen_points.pop()
                
                for v in [UP, DOWN, LEFT, RIGHT]:
                    next_point = curr_point + v
                    if next_point not in unseen_points.union(seen_points) and char_map[curr_point] == char_map[next_point]:
                        unseen_points.add(next_point)
                
                seen_points.add(curr_point)
                unallocated_points.discard(curr_point)
                
            
            regions.append(Region(seen_points, char_map[curr_point]))
        
        return regions
    

    @property
    def total_area(self) -> int:
        return sum([r.area for r in self.regions])

    @property
    def total_perimiter(self) -> int:
        return sum([r.perimiter for r in self.regions])
    
    @property
    def total_price(self) -> int:
        return sum([r.price for r in self.regions])
    
    @property
    def total_discount_price(self) -> int:
        return sum([r.discount_price for r in self.regions])

def part_1(input: str):
    regions = RegionMap(input)
    return regions.total_price

def part_2(input: str):
    regions = RegionMap(input)
    return regions.total_discount_price


input = pathlib.Path("input_aoc.txt").read_text()
# input = pathlib.Path("input_example.txt").read_text()
print(part_1(input))
print(part_2(input))