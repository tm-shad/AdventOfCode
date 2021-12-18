from pathlib import Path

# INPUT_FILE = str(Path(__file__).parent.joinpath("input_example.txt").resolve())
INPUT_FILE = str(Path(__file__).parent.joinpath("input_troy.txt").resolve())


with open(INPUT_FILE) as f:
    lines = f.readlines()


# create array
data = np.array([[int(c) for c in l if c in ["0", "1"]] for l in lines])


def foo(data, oxygen_flag):
    pottential = [i for i in range(len(data))]
    for i in range(len(data[0])):
        frequency = np.unique(data.transpose()[i][pottential], return_counts=True)[1]
        # filter out
        if frequency[0] != frequency[1]:
            # a most common
            most_common = np.argmax(np.bincount(data.transpose()[i][pottential]))
        else:
            most_common = 1

        pottential = [
            ptr
            for ptr in pottential
            if data[ptr][i] == most_common
            and oxygen_flag
            or data[ptr][i] != most_common
            and not (oxygen_flag)
        ]

        if len(pottential) == 1:
            break

    return int("".join([str(i) for i in data[pottential][0]]), base=2)


print(foo(data, True))
print(foo(data, False))
print(foo(data, True) * foo(data, False))
