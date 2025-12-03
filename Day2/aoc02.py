import re
import sys
import argparse
from math import floor

FILENAME = "./Input.txt"
DIAL_STARTING = 50
DIAL_SEGMENTS = 100

def ProcessInputfile(filename):
    print(f"Processing input file: {filename}")
    with open(filename, 'r') as f:
        line = f.read().strip()
        if not line:
            return []
        
    print(f"Read {len(line)} lines from file.")
    # break lines into character and number
    tokens = [t.strip() for t in line.split(',') if t.strip()]
    result = []
    for tok in tokens:
        parts = tok.split('-', 1)
        if len(parts) != 2:
            print(f"Warning: can't parse token '{tok}'", file=sys.stderr)
            continue
        a_s, b_s = parts[0].strip(), parts[1].strip()
        try:
            a = int(a_s)
            b = int(b_s)
        except ValueError:
            print(f"Warning: can't parse numbers in token '{tok}'", file=sys.stderr)
            continue
        result.append((a, b))

    return result


def ProcessA(ranges_to_check):

    results = []
    for item in ranges_to_check:
        print(f"Processing range: {item}")
        # iterate start values between a and b (inclusive)
        for current in range(item[0], item[1] + 1):
            # turn end into string.
            # go halfway between length of it.. split it and if equal add to results
            current_str = str(current)
            length = len(current_str)
            half = length / 2
            if length % 2 == 0:
                first_half = current_str[:int(half)]
                second_half = current_str[int(half):]
                if first_half == second_half:
                    print(f" {current}: length even, halves equal, adding")
                    results.append(current)
                else:
                    print(f" {current}: length odd, skipping")
               
    return results  

def find_nonoverlapping(haystack: str, needle: str) -> list[int]:
    """Return start indices of non-overlapping occurrences of needle in haystack."""
    if not needle:
        return []
    res = []
    i = 0
    step = len(needle)
    while True:
        i = haystack.find(needle, i)
        if i == -1:
            break
        print(f"   Found non-overlapping '{needle}' in '{haystack}' at index {i}")
        res.append(i)
        i += step  # skip past this match
    return res

def ProcessB(ranges_to_check):

    results = []
    for item in ranges_to_check:
        print(f"Processing range: {item}")
        # iterate start values between a and b (inclusive)
        for current in range(item[0], item[1] + 1):
            # turn end into string.
            # go halfway between length of it.. split it and if equal add to results
            current_str = str(current)
            length = len(current_str)
            
            half = length // 2
            for split in range(1, half + 1):
                
                first_half = current_str[:int(split)]
                second_half = current_str[int(split):]
                print(f" Checking split size {split} for number {current_str} => {first_half}, {second_half} ")
                copies = find_nonoverlapping(second_half, first_half)
                needed_copies = (len(second_half) / split) #half

                if len(copies) == needed_copies :
                    print(f" {current}: good copyies found, adding {copies} {first_half}, {second_half}")
                    results.append(current)
                    break
                

               
    return results  

def main():
    parser = argparse.ArgumentParser(description="Parse file lines with a character and a number.")
    parser.add_argument("filename", help="Input file to parse")
    args = parser.parse_args()

    # 1. Parse the input file
    inv_item_ranges = ProcessInputfile(args.filename)
    print(inv_item_ranges)

    # 2. Process data.
    invalids = ProcessB(inv_item_ranges)
    print(f"List of invalid items:\n {invalids} ")

    total = 0
    # 3. Sum up the invalidates data
    for item in invalids:
        total = total + item
    print(f"Final total of invalid items: {total} for items {len(invalids)}")


if __name__ == "__main__":
    main()