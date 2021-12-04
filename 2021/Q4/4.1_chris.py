from time import perf_counter
from pathlib import Path
import numpy as np


INPUT_FILE = str(Path(__file__).parent.joinpath("input_chris.txt").resolve())

with open(INPUT_FILE, 'r') as f:
    input_text = f.readlines()
in_list = [num.strip() for num in input_text]
in_list = '\n'.join(in_list).split('\n\n')

draws = [int(n) for n in in_list.pop(0).split(',')]
boards = [[[int(n) for n in row.strip().split(' ') if n != ''] for row in board.split('\n')] for board in in_list]
boards = [(board, [[False]*5 for i in range(5)]) for board in boards]

time_start = perf_counter()

def check_board_wins(board):
    for i in range(5):
        if sum(board[i]) == 5:
            return True
        if sum([row[i] for row in board]) == 5:
            return True
    return False
    

for num in draws:
    for (board, win_board) in boards:
        for i in range(5):
            for j in range(5):
                if board[i][j] == num:
                    # print(board, num)
                    # print(board[i][j])
                    win_board[i][j] = True
        if check_board_wins(win_board):
            b_sum = 0
            for i in range(5):
                for j in range(5):
                    if win_board[i][j] == False:
                        b_sum += board[i][j]
            # print(board)
            # print(win_board)
            
            print('num', num)
            print('b_sum', b_sum)
            print(num * b_sum)
            raise Exception()

time_end = perf_counter()

print(time_end-time_start)        
