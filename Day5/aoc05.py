import re
import sys
import argparse
from math import floor


def ProcessInputfile(filename):
    print(f"Processing input file: {filename}")
    fresh_ids = []
    inventory = []

    process_inventories = False

    with open(filename, 'r') as file:
        lines = file.readlines()
        fresh_pattern = re.compile(r'^\s*([+-]?\d+)\s*-\s*([+-]?\d+)\s*$')
        inventory_pattern = re.compile(r'^\s*([.])\s*$')

        print("Reading lines from file...")
        print(lines)

        for line in lines:
            
            if line.strip() == '':
                # process next as inventory.
                process_inventories = True
                print("Switching to inventory processing.")
                continue
            else:
                print(f"Processing line: '{line.strip()}'")

            if not process_inventories:
                match = fresh_pattern.match(line.strip())
                if match:
                    a = int(match.group(1))
                    b = int(match.group(2))
                    fresh_ids.append( (a,b) )
            else:
                # process inventory line
                item =int(line.strip())
                inventory.append(item)

    return fresh_ids, inventory




def Process(fresh_ids, inventory_to_check):
    fresh_items = []

    fresh_ids.sort(key=lambda t: t[0])
    print(f"Sorted fresh ID ranges: {fresh_ids}")
    # find overlaps
    for i in range(len(fresh_ids)-1, -1, -1):

        if (i - 1) < 0:
            break
        current_start, current_end = fresh_ids[i]
        prev_start, prev_end = fresh_ids[i - 1]

        print(f"Checking ranges: {fresh_ids[i-1]} and {fresh_ids[i]}")
        if prev_end >= current_start:
            # There is an overlap
            merged_start = min(current_start, prev_start)
            merged_end = max(current_end, prev_end)
            fresh_ids[i-1 ] = (merged_start, merged_end)
            del fresh_ids[i]
            print(f"Merged ranges: {fresh_ids}\n")


    print(f"\n\n\n\n\n\FINAL Merged fresh ID ranges: {fresh_ids}")
    total_possible_fresh = 0
    for start, end in fresh_ids:
        total_possible_fresh += (end - start + 1)


    for item in inventory_to_check:
        for start, end in fresh_ids:
            if start <= item <= end:
                fresh_items.append(item)
                continue
    return fresh_items, total_possible_fresh


def main():
    total_fresh_foods = 0
    parser = argparse.ArgumentParser(description="Parse file lines with a character and a number.")
    parser.add_argument("filename", help="Input file to parse")
    args = parser.parse_args()

    # 1. Parse the input file
    fresh, inventory = ProcessInputfile(args.filename)
    print(f"Fresh IDs: {fresh}")
    print(f"pending items: {inventory}")


    # 2. Process data.
    results, total_possible_fresh_foods = Process(fresh, inventory)
    print(f"\n\n\n\n\n\n\n\nConfirmed Fresh : {results}\n\n\n\n\n\n\n\n")

    total_fresh_foods += len(results)
    print(f"Total valid:\n {total_fresh_foods} and possible {total_possible_fresh_foods}  ")


if __name__ == "__main__":
    main()