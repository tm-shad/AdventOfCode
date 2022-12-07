from pathlib import Path
import logging
import argparse
from typing import List, Tuple

import numpy as np


class File:
    def __init__(self, name, size) -> None:
        self.name = name
        self.size = int(size)

    @staticmethod
    def from_line(line: str):
        size, name = line.split(" ")

        return File(name=name, size=size)

    def to_string(self, depth=0) -> str:
        rep_str = " " * 2 * depth + f"- {self.name} (file, size={self.size})\n"

        return rep_str


class Dir:
    def __init__(self, name, subdirs, files) -> None:
        self.name = name
        self.subdirs = subdirs
        self.files = files

    @staticmethod
    def from_line(line: str):
        if line.startswith("$ cd "):
            name = line[len("$ cd ") :]
        elif line.startswith("dir "):
            name = line[len("dir ") :]

        return Dir(name, list(), list())

    @staticmethod
    def from_in_str(lines: str):
        fs = Dir.from_line(lines.pop(0))

        while len(lines) > 0:
            line = lines.pop(0)
            if line == "$ cd ..":
                break
            elif line.startswith("$ cd"):
                subdir, lines = Dir.from_in_str([line] + lines)
                fs.subdirs.append(subdir)
            elif line.startswith("$ ls"):
                files, _, lines = parse_ls(lines)
                fs.files.extend(files)
                # fs.subdirs.extend(subdirs)

        return fs, lines

    def to_string(self, depth=0) -> str:
        rep_str = " " * 2 * depth + f"- {self.name} (dir)\n"

        for d in self.subdirs:
            rep_str = rep_str + d.to_string(depth=depth + 1)

        for f in self.files:
            rep_str = rep_str + f.to_string(depth=depth + 1)

        return rep_str

    def get_size(self) -> int:
        size = 0

        for d in self.subdirs:
            size += d.get_size()

        for f in self.files:
            size += f.size

        return size

    def get_limited_size(self) -> List:
        size = 0
        valid_sizes = []

        for d in self.subdirs:
            size += d.get_size()
            valid_sizes.extend(d.get_limited_size())

        for f in self.files:
            size += f.size

        if size < 100000:
            valid_sizes.append(self)

        return valid_sizes

    def get_all_dirs(self):
        l = [self]
        for d in self.subdirs:
            l.extend(d.get_all_dirs())

        return l


def parse_ls(lines: List[str]) -> Tuple[List[File], List[Dir], List[str]]:
    files = []
    dirs = []

    while len(lines) > 0:
        line = lines.pop(0)
        if line.startswith("$"):
            # end of list
            lines = [line] + lines
            break
        elif line.startswith("dir"):
            dirs.append(Dir.from_line(line))
        else:
            files.append(File.from_line(line))

    return files, dirs, lines


def read_file(file_path: Path) -> str:

    with open(file_path) as f:
        in_str = f.read()

    return in_str


def main(input_path: Path):
    in_str = read_file(input_path).strip()

    lines = in_str.split("\n")
    filesystem, _ = Dir.from_in_str(lines)
    print(filesystem.to_string())

    l = filesystem.get_all_dirs()
    min_size = 30000000 - (70000000 - l[0].get_size())

    return min(
        [i for i in l if i.get_size() >= min_size], key=lambda i: i.get_size()
    ).get_size()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument("file")

    args = parser.parse_args()

    input_file = str(Path(__file__).parent.joinpath(args.file).resolve())

    print(main(input_file))