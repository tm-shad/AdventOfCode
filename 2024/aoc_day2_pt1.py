import pathlib


input = pathlib.Path("input_aoc.txt").read_text()
# input = pathlib.Path("input_example.txt").read_text()


def safe_check(fuzzy_error):
    safe_map = {}
    for j, line in enumerate(input.splitlines()):
        original_line = line.split()
        for i in range(len(original_line)):
            line = original_line
            line = line[:i] + line[i+1:] if fuzzy_error else line
            diffs = [int(l)-int(r) for l,r in zip(line, line[1:])]
            if (all(i>0 for i in diffs) or all(i<0 for i in diffs)) and all(abs(i)<=3 for i in diffs):
                safe_map[j] = True

    return sum(k for k in safe_map.values() if k is True)

print(safe_check(False))  # part 1
print(safe_check(True))  # part 2