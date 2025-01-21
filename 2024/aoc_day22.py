from collections import defaultdict, namedtuple
import functools
import bisect

import math
from operator import mul
import pathlib
from numpy import Infinity
from tqdm import tqdm
from tqdm.contrib.concurrent import process_map

# To mix a value into the secret number, calculate the bitwise XOR of the given value and the secret number.
# Then, the secret number becomes the result of that operation.
mix = lambda x,secret_num: x ^ secret_num

# To prune the secret number, calculate the value of the secret number modulo 16777216.
# Then, the secret number becomes the result of that operation.
prune = lambda secret_num: secret_num % 16777216

@functools.lru_cache(maxsize=None)
def monkey_encrypt(secret_num: int) -> int:
    # Calculate the result of multiplying the secret number by 64. Then, mix this result into the secret number. Finally, prune the secret number.
    secret_num = prune(mix(secret_num*64,secret_num))
    # Calculate the result of dividing the secret number by 32. Round the result down to the nearest integer. Then, mix this result into the secret number. Finally, prune the secret number.
    secret_num = prune(mix(secret_num//32,secret_num))
    # Calculate the result of multiplying the secret number by 2048. Then, mix this result into the secret number. Finally, prune the secret number.
    secret_num = prune(mix(secret_num*2048,secret_num))

    return secret_num



def part_1(input: str):
    total = 0

    for i in tqdm(input.splitlines()):
        i = int(i)
        for _ in tqdm(range(2000),leave=False):
            i = monkey_encrypt(i)
        total += i


    return total

get_price = lambda x: x % 10

def find_monkeys_sell_prices(secret_num: int, max_sequence: int = 2000) -> dict[tuple[int,int,int,int], int]:
    trend_to_first_price = {}
    historic_trend = []
    last_price = None
    price_diff = None

    for _ in range(max_sequence):
        secret_num = monkey_encrypt(secret_num)
        curr_price = get_price(secret_num)

        if last_price is not None:
            price_diff = curr_price-last_price
        last_price = curr_price

        if price_diff is not None:
            historic_trend.append(price_diff)
        
        if len(historic_trend)>=4:
            price_diff_key = tuple(historic_trend)

            if price_diff_key not in trend_to_first_price:
                trend_to_first_price[price_diff_key] = curr_price

            historic_trend.pop(0)

    return trend_to_first_price

def part_2(input: str):
    running_totals = defaultdict(lambda: 0)

    for i in tqdm(input.splitlines()):
        i = int(i)
        new_sell_prices = find_monkeys_sell_prices(i)

        for k,v in new_sell_prices.items():
            running_totals[k] += v
    
    k = max(running_totals, key=running_totals.get)

    return k, running_totals[k]
        


input = (pathlib.Path("input_aoc.txt").read_text())
# input = (pathlib.Path("input_example.txt").read_text())


# print(part_1(input))
print(part_2(input))