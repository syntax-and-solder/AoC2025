import re
import sys
import argparse
from math import floor


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

def Process(wall_array):

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
    split_count = Process(map)
    print(f"Total splits: {split_count}")


if __name__ == "__main__":
    main()