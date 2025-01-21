from collections import defaultdict, namedtuple
import functools
import bisect

import math
from operator import mul
import pathlib
from numpy import Infinity
from tqdm import tqdm
from tqdm.contrib.concurrent import process_map

UP= complex(-1,0)
DOWN= complex(1,0)
LEFT= complex(0,-1)
RIGHT= complex(0,1)

class Map():
    def __init__(self, chunk_str, map_size: int):
        self.chunk_list = [complex(int(line.split(",")[1]), int(line.split(",")[0])) for line in chunk_str.splitlines()]

        self.w = map_size+1
        self.h = map_size+1
        self.start = complex(0,0)
        self.end = complex(map_size,map_size)

        # add walls
        self.landed_chunks = set()
        for i in range(self.w):
            self.landed_chunks.add(complex(-1,i))
            self.landed_chunks.add(complex(self.h,i))
        for i in range(self.h):
            self.landed_chunks.add(complex(i,-1))
            self.landed_chunks.add(complex(i,self.w))

    def __str__(self):
        str_map = ""
        for i in range(-1,self.h+1):
            for j in range(-1,self.w+1):
                if complex(i,j) in self.landed_chunks:
                    str_map += "#"
                else:
                    str_map += "."
            str_map += "\n"
        
        return str_map
    
    def similate_chunks(self, iteration: int):
        for chunk in self.chunk_list[:iteration]:
            self.landed_chunks.add(chunk)
        return chunk

    @functools.lru_cache(maxsize=None)
    def calc_h(self, x: complex) -> float:
        return abs(x.real-self.end.real) + abs(x.imag-self.end.imag)

    def solve(self, last_path: list[complex] | None=None, last_added_chunk:complex|None=None):
        Point = namedtuple('Point', 'g h pos path')
        seen_points = set()

        # start with the last path, if defined
        p_stack = [Point(0,self.calc_h(self.start),self.start, [])]
        if last_path is not None:
            try:
                cutt_off = last_path.index(last_added_chunk)
                last_path = last_path[:cutt_off]
            except ValueError:
                pass

            curr_g = 0
            for pos in last_path:
                curr_g += 1
            # seen_points.add(pos)
            p_stack = [Point(curr_g,self.calc_h(pos),pos, last_path)]
        else:
            p_stack = [Point(0,self.calc_h(self.start),self.start, [])]


        while len(p_stack)>0:
            point = p_stack.pop(0)
            
            # check if we're at the end of the maze
            if point.pos == self.end:
                # self.print_path(point.path)
                return point.g,point.path
            
            # else check all possible moves
            for next_v in [UP, DOWN, LEFT, RIGHT]:
                next_pos = next_v+point.pos
                next_point = Point(point.g + 1, self.calc_h(next_pos), next_pos, point.path + [next_pos])

                # if point_min_f[next_point.pos] < next_point.g+next_point.h:
                if point.pos in seen_points:
                    continue
                elif next_pos in self.landed_chunks:
                    continue # can't move into a walls/chunks
                else:
                    # point_min_f[next_point.pos] = next_point.g+next_point.h
                    bisect.insort(p_stack, next_point, key=lambda x: x.g+x.h)
            
            seen_points.add(point.pos)
        
        return None,None
    
    def print_path(self, path: list[complex]):
        path = set(path)
        map_str = ""

        for i in range(-1,self.h+1):
            for j in range(-1,self.w+1):
                if complex(i,j) in path:
                    map_str += "O"
                elif complex(i,j) in self.landed_chunks:
                    map_str += "#"
                else:
                    map_str += " "
            map_str += "\n"
        
        print(map_str)



def part_1(chunk_str: str, map_size: int, fallen_chunks: int):
    chunk_map = Map(chunk_str, map_size)
    # print(chunk_map)
    chunk_map.similate_chunks(fallen_chunks)
    # print(chunk_map)
    
    return chunk_map.solve()[0]

def part_2(chunk_str: str, map_size: int, fallen_chunks: int):
    chunk_map = Map(chunk_str, map_size)

    last_chunk = chunk_map.similate_chunks(fallen_chunks)
    ret,last_path = chunk_map.solve()
    for i in tqdm(range(fallen_chunks+1,len(chunk_str.splitlines()))):
        last_chunk = chunk_map.similate_chunks(i)
        ret,last_path = chunk_map.solve(last_path,last_chunk)
        if ret is None:
            return f"{int(last_chunk.imag)},{int(last_chunk.real)}"
        


input = (pathlib.Path("input_aoc.txt").read_text(), 70, 1024)
# input = (pathlib.Path("input_example.txt").read_text(), 6, 12)


print(part_1(*input))
print(part_2(*input))