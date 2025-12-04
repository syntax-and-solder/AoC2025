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


def ProcessA(battery_array):

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

def ProcessB(battery_array):
    # find top 12 values in each battery to get the charge.
    # but these are 15 digit strings, so need to find the largest 12 digit number in order possible.
    results = []
    TARGET_LENGTH = 12
    for battery in battery_array:
        # process each battery string
        battery_len = len(battery)
        start_index = 0
        value_str = ''
        print(f"Processing battery {battery} ")

        while start_index < battery_len and len(value_str) < TARGET_LENGTH:
            remaining_needed = TARGET_LENGTH - len(value_str)
            # allowed last start for this pick so we still have enough digits left
            end_exclusive = battery_len - (remaining_needed - 1)
            window = battery[start_index:end_exclusive]
            if not window:
                break

            # pick the maximum digit in the allowed window
            chosen = max(window)
            rel_idx = window.index(chosen)
            abs_idx = start_index + rel_idx
            print(f"\tlargest find {rel_idx} (abs {abs_idx}) for char {chosen} from {window} ")

            value_str += chosen
            print(f"\tvalue so far {value_str} ")

            # advance to the element in the main battery after the chosen one
            start_index = abs_idx + 1
            print(f"\tremaining of battery to search @index[{start_index}] {battery[start_index:]}\n")

        max_charge = int(value_str)
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
    max_charge_list = ProcessB(batteries)
    print(f"List of invalid items:\n {max_charge_list} ")

    total = 0
    # 3. Sum up the1 invalidates data
    for item in max_charge_list:
       total = total + item
    print(f"Final total of invalid items: {total} for items {len(max_charge_list)}")


if __name__ == "__main__":
    main()