from pathlib import Path
import numpy as np

INPUT_FILE = str(Path(__file__).parent.joinpath("input_example.txt").resolve())
# INPUT_FILE = str(Path(__file__).parent.joinpath("input_troy.txt").resolve())


with open(INPUT_FILE) as f:
    lines = f.readlines()


# create array
data = np.array([[int(c) for c in l if c in ["0", "1"]] for l in lines])

# calculate correct bits

gamma_str = ""
epsilon_str = ""
for i in range(len(data[0])):
    gamma_str += str(np.argmax(np.bincount(data.transpose()[i])))
    epsilon_str += str(np.argmin(np.bincount(data.transpose()[i])))

gamma = int(gamma_str, base=2)
epsilon = int(epsilon_str, base=2)
print(gamma, epsilon)
print(gamma * epsilon)