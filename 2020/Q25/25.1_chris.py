from time import perf_counter
from pathlib import Path


INPUT_FILE = str(Path(__file__).parent.joinpath("input_chris.txt").resolve())

with open(INPUT_FILE, 'r') as f:
    input_text = f.readlines()
in_list = [int(num.strip()) for num in input_text]

print(in_list)

time_start = perf_counter()

# real_card_pub = in_list[0]
# real_door_pub = in_list[1]

def transform(value, subj_num, loop_size):
    for i in range(loop_size):
        value = value * subj_num
        value = value % 20201227
    return value

subj_num = 7

loop_sizes = []
# for i in range(100):
loop_size = 0
pub = 1
while pub not in in_list:
    loop_size += 1
    pub = transform(pub, subj_num, 1)
    

in_list.remove(pub)
print(in_list)
print(loop_size)
print(transform(1, in_list[0], loop_size))

# loop_size = 13 # SECRET. 1 for Card, 1 for Door.
# door_pub = transform(subj_num, door_loop)
# print('door\'s public key', door_pub)

# print(transform(card_pub, door_loop))
# print(transform(door_pub, card_loop))



time_end = perf_counter()

print(time_end-time_start)        