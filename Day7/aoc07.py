
import sys
import argparse
from functools import lru_cache
from typing import List, Tuple


def ProcessInputfile(filename):
    print(f"Processing input file: {filename}")
    result = []

    keep_whitespace=False
    skip_empty=True
    with open(filename, 'r') as f:
        for line in f:
            # remove trailing newline only
            line = line.rstrip('\n')
            result.append(line)
        return result 

def find_all_char_indices(s: str, ch: str) -> list[int]:
    """Return all indices where character ch appears in s."""
    return [i for i, c in enumerate(s) if c == ch]

def ProcessBFS(wall_array):

    results = []
    found_start = False
    split_count = 0

    # do all lines except last
    for row_index in range(len(wall_array) - 1):
        row = wall_array[row_index]
        next_row = wall_array[row_index + 1]

        print(f"Processing row {row_index}: {row}")
        if (found_start == False):
            # Find start position. S and  send lazer below it on next line. |
            start_index = row.find('S')
            if (start_index != -1):
                found_start = True
                print(f"Found start at index {start_index} on row {row_index}")
                next_row = next_row[:start_index] + '|' + next_row[start_index+1:] 
        else:
            # find each | and check next for ^ splitters in string
            lasers = find_all_char_indices(row, '|')
            for laser_index in lasers:
                print(f" Found laser at index {laser_index} on row {row_index}")
                # check next row at this index
                if next_row[laser_index] == '^':
                    # splitter found, split beam
                    split_count += 1
                    print(f"  Splitter found at index {laser_index} on next row {row_index + 1}, splitting beam.")
                    # update next row to have two beams left and right of splitter
                    left_part = next_row[:laser_index]
                    right_part = next_row[laser_index+1:]
                    if laser_index > 0:
                        left_part = left_part[:-1] + '|'
                    if laser_index < len(next_row) - 1:
                        right_part = '|' + right_part[1:]
                    next_row = left_part + '^' + right_part
                else:
                    # just continue down
                    next_row = next_row[:laser_index] + '|' + next_row[laser_index+1:]
        wall_array[row_index + 1] = next_row

        print_map(wall_array)
    return split_count  


# This is completely copilot generated for the sake of learning.
def ProcessDFS(wall_array: List[str]) -> int:
    """
    Count unique timelines using a memoized DFS, then produce a visual map.

    Counting rules:
      - Beam starts one row below 'S'.
      - Out-of-bounds = one timeline end (count = 1).
      - Traversable chars: '.', '^', 'S'
      - '^' splits into (r+1, c-1) and (r+1, c+1).
      - '.' or 'S' continue straight down (r+1, c).
    """
    mat = [list(r) for r in wall_array]
    rows = len(mat)
    if rows == 0:
        return 0

    # locate 'S'
    start_r = start_c = None
    for r, row in enumerate(mat):
        c = ''.join(row).find('S')
        if c != -1:
            start_r, start_c = r, c
            break
    if start_r is None:
        raise ValueError("Start 'S' not found")

    def in_bounds(r: int, c: int) -> bool:
        return 0 <= r < rows and 0 <= c < len(mat[r])

    def is_traversable_char(ch: str) -> bool:
        return ch in ('.', '^', 'S')

    @lru_cache(maxsize=None)
    def dfs_count(r: int, c: int) -> int:
        # leaving the map is a single timeline end
        if not in_bounds(r, c):
            return 1
        ch = mat[r][c]
        # hitting a non-traversable char inside the map is a terminal end
        if not is_traversable_char(ch):
            return 1
        if ch == '^':
            return dfs_count(r + 1, c - 1) + dfs_count(r + 1, c + 1)
        else:
            return dfs_count(r + 1, c)

    unique_timelines_count = dfs_count(start_r + 1, start_c)

    # Build a visual map of all cells that are part of any reachable path.
    visual = [list(r) for r in wall_array]
    stack: List[Tuple[int, int]] = [(start_r + 1, start_c)]
    seen = set()
    while stack:
        r, c = stack.pop()
        if not in_bounds(r, c):
            continue
        if (r, c) in seen:
            continue
        ch = visual[r][c]
        if not is_traversable_char(ch):
            continue
        seen.add((r, c))
        if ch == '^':
            # keep the '^' visually
            stack.append((r + 1, c - 1))
            stack.append((r + 1, c + 1))
        else:
            # mark beam path
            visual[r][c] = '|'
            stack.append((r + 1, c))

    # print final visual map
    for line in [''.join(row) for row in visual]:
        print(line)

    return unique_timelines_count


def print_map(map):
    for line in map:
        print(line)



def main():
    parser = argparse.ArgumentParser(description="Parse file lines with a character and a number.")
    parser.add_argument("filename", help="Input file to parse")
    args = parser.parse_args()

    # 1. Parse the input file
    map = ProcessInputfile(args.filename)
    print_map(map)


    # 2. Process data.
    count = ProcessDFS(map)
    print(f"Total unique timelines: {count}")


if __name__ == "__main__":
    main()