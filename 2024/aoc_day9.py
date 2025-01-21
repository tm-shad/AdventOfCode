import pathlib
from typing import Any
from tqdm import tqdm
from tqdm.contrib.concurrent import process_map
import bisect
input = pathlib.Path("input_aoc.txt").read_text()
# input = pathlib.Path("input_example.txt").read_text()


class DiskMap():
    map: list[str]
    free_blocks: list[list[int, int]]
    left_free_ptr: int
    right_data_ptr: int
    def __init__(self, input_map: str):
        self.map = []
        self.free_blocks = []
        self.left_free_ptr = None
        self.left_data_ptr = None
        self.right_data_ptr = None
        is_data = True
        data_id = 0
        for data_w in input_map:
            if(is_data):
                self.left_data_ptr = len(self.map)
                self.map += [data_id]*int(data_w)
                data_id += 1
                self.right_data_ptr = len(self.map) - 1
            else:
                if self.left_free_ptr is None:
                    self.left_free_ptr = len(self.map)
                self.map += ["."]*int(data_w)
                
                if int(data_w)>0:
                    self.free_blocks.append(
                        [len(self.map)-int(data_w), len(self.map)]
                        )
            is_data = not(is_data)
        
        self.compress_free_blocks()
        
    def compress_free_blocks(self):
        i = 0
        while i < len(self.free_blocks)-1:
            while(i < len(self.free_blocks)-1 and self.free_blocks[i][1]==self.free_blocks[i+1][0]):
                self.free_blocks[i][1] = self.free_blocks[i+1][1]
                self.free_blocks.pop(i+1)
            i+=1

    def __repr__(self)->str:
        return self.__str__() + f" | {self.map[self.left_data_ptr:self.right_data_ptr+1]}"
    
    def __str__(self)->str:
        return "".join(str(i) for i in self.map)
    
    def compress(self):
        # loop intil crossover
        # pbar = tqdm(total=self.right_data_ptr-self.left_free_ptr)
        while self.left_free_ptr < self.right_data_ptr:
            # print(self)
            # swap
            self.map[self.left_free_ptr], self.map[self.right_data_ptr] = self.map[self.right_data_ptr], self.map[self.left_free_ptr]

            # increment
            while self.map[self.left_free_ptr] != ".":
                self.left_free_ptr += 1
                # pbar.update(1)
            # decrement
            while self.map[self.right_data_ptr] == ".":
                self.right_data_ptr -= 1
                # pbar.update(1)
        # print(self)

    def smart_compress(self):
        # loop intil crossover
        pbar = tqdm(total=self.right_data_ptr-self.left_free_ptr)
        while self.right_data_ptr > 0:
            curr_w = self.right_data_ptr - self.left_data_ptr + 1
            assert self.map[self.right_data_ptr] == self.map[self.left_data_ptr]

            if curr_w>0:
                # look for big enough free block
                block_id, free_block = next(((i,(l,r)) for i,(l,r) in enumerate(self.free_blocks)
                                             if (r-l>=curr_w)
                                             and r<=self.left_data_ptr
                                             ), (None,None))

                if block_id is None:
                    # can't move the current data
                    pass
                else:
                    # can move data
                    self.map[free_block[0]:free_block[0]+curr_w], self.map[self.left_data_ptr:self.right_data_ptr+1] = self.map[self.left_data_ptr:self.right_data_ptr+1], self.map[free_block[0]:free_block[0]+curr_w]

                    bisect.insort(self.free_blocks,[self.left_data_ptr,self.right_data_ptr+1])
                    if curr_w==(free_block[1]-free_block[1]):
                        self.free_blocks.pop(block_id)
                    else:
                        self.free_blocks[block_id] = [free_block[0]+curr_w,free_block[1]]
                        self.compress_free_blocks()
                
            # move data ptrs
            pbar.update(self.right_data_ptr-self.left_data_ptr+1)
            self.right_data_ptr = self.left_data_ptr-1
            while(self.map[self.right_data_ptr] =="."):
                self.right_data_ptr-=1
                pbar.update(1)
                if(self.right_data_ptr < 0):
                    continue
                
            self.left_data_ptr = self.right_data_ptr
            while(self.left_data_ptr>0 and self.map[self.right_data_ptr] == self.map[self.left_data_ptr]):
                self.left_data_ptr -= 1
            self.left_data_ptr += 1



        
            

    def checksum(self):
        return sum([i*int(id) for i,id in enumerate(self.map) if id != "."])


        

def part_1(input: str):
    map = DiskMap(input)

    print(map)
    map.compress()
    print(map)

    return map.checksum()

def part_2(input: str):
    map = DiskMap(input)

    # print(map)
    map.smart_compress()
    # print(map)

    return map.checksum()



# print(part_1(input))
print(part_2(input))