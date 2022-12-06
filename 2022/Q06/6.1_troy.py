from pathlib import Path
import logging
import argparse

import numpy as np


def read_file(file_path: Path) -> str:

    with open(file_path) as f:
        in_str = f.read()

    return in_str


def main(input_path: Path):
    in_str = read_file(input_path).strip()

    for i in range(len(in_str) - 4 + 1):
        if len(set(in_str[i : i + 4])) >= 4:
            break

    print(i + 4)

    return None


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument("file")

    args = parser.parse_args()

    input_file = str(Path(__file__).parent.joinpath(args.file).resolve())

    print(main(input_file))