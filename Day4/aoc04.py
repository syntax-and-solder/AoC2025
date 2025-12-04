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
            if skip_empty and line == '':
                continue
            # if you want to strip surrounding whitespace, use line = line.strip()
            row = list(line) if keep_whitespace else list(line)
            result.append(row)
        return result 


def Process(wall_array):

    results = []

    for row_idx, row in enumerate(wall_array, start=1):
        print(f"Processing row {row_idx}: {''.join(row)}")
        for col_idx, char in enumerate(row, start=1):
            if char == '@':
                paper_count = 0
                print(f"Found '@' at row {row_idx}, column {col_idx}")
                # convert to 0-based indices
                r = row_idx - 1
                c = col_idx - 1

                # check the 8 neighbors with bounds checks
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        if dr == 0 and dc == 0:
                            continue
                        rr = r + dr
                        cc = c + dc
                        if 0 <= rr < len(wall_array) and 0 <= cc < len(wall_array[rr]):
                            if wall_array[rr][cc] == '@':
                                paper_count += 1
                                print(f"\tAdjacent '@' count: {paper_count} ")

                if paper_count < 4: 
                    results.append((row_idx, col_idx))  
                    print(f"\tMovable roll found at ({row_idx}, {col_idx}) with {paper_count}  {results}")      
    print(f"Total movable rolls found: {len(results)}")

    return results  


def UpdateWall(map, results):
    for (row_idx, col_idx) in results:
        print(f"Updating wall at ({row_idx}, {col_idx}) from '@' to '.'")
        # convert to 0-based indices
        r = row_idx - 1
        c = col_idx - 1
        map[r][c] = '.'
    return map


def main():
    parser = argparse.ArgumentParser(description="Parse file lines with a character and a number.")
    parser.add_argument("filename", help="Input file to parse")
    args = parser.parse_args()

    # 1. Parse the input file
    map = ProcessInputfile(args.filename)
    print(map)

    total_rolls = 0;

    while True:
        # 2. Process data.
        results = Process(map)

        if not results:
            print("No more movable rolls found. Exiting.")
            break

        total_rolls += len(results)
        print(f"Movable rolls:\n {total_rolls} ")

        map = UpdateWall(map, results)
        print(f"Updated wall: {map}")
        #break

    total_rolls += len(results)
    print(f"Final Movable rolls:\n {total_rolls} ")


if __name__ == "__main__":
    main()