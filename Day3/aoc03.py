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


def Process(battery_array):

    results = []

    for battery in battery_array:
        # process each battery string
        battery_len = len(battery)
        sorted_chars_largest = sorted(battery[0:battery_len-1], reverse=True)
        # find order of top 2 items.
        index_largest = battery.index(sorted_chars_largest[0])
        print(f"largest find {index_largest} for char {sorted_chars_largest[0]} ")
        print(f"remainding of battery to search {battery[(index_largest+1):]}")

        sorted_chars_next_largest = sorted(battery[(index_largest+1):], reverse=True)
        print(f"next largest find {sorted_chars_next_largest}")
        if not sorted_chars_next_largest:
            print(f"No next largest found for battery {battery}, skipping.")
            continue
        index_next_largest = battery.index(sorted_chars_next_largest[0])
        max_charge = (int(sorted_chars_largest[0]) *10) + int(sorted_chars_next_largest[0] )

        results.append(max_charge)
        print(f"max charge is {max_charge} now {results} ")

    return results  

def main():
    parser = argparse.ArgumentParser(description="Parse file lines with a character and a number.")
    parser.add_argument("filename", help="Input file to parse")
    args = parser.parse_args()

    # 1. Parse the input file
    batteries = ProcessInputfile(args.filename)
    print(batteries)

    # 2. Process data.
    max_charge_list = Process(batteries)
    print(f"List of invalid items:\n {max_charge_list} ")

    total = 0
    # 3. Sum up the1 invalidates data
    for item in max_charge_list:
       total = total + item
    print(f"Final total of invalid items: {total} for items {len(max_charge_list)}")


if __name__ == "__main__":
    main()