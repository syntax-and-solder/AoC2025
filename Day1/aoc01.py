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
        lines = f.readlines()
        print(f"Read {len(lines)} lines from file.")
        # break lines into character and number
        pattern = re.compile(r'^\s*([LR])\s*(\d+)\s*$', re.I)
        result = []
        for line in lines:
            match = pattern.match(line.strip())
            if match:
                char = match.group(1)
                num = int(match.group(2))
                result.append((char, num))
        return result 

def CountRotations(dial_in, direction, ticks): 
    # return number of rotations on the dial
    rotations = 0

    while ticks >= DIAL_SEGMENTS:
        rotations = rotations + 1
        ticks = ticks - DIAL_SEGMENTS

    if direction == 'L':
        
        # apply remaining ticks
        dial_out = dial_in - ticks
        if dial_out < 0 and dial_in != 0:
            rotations = rotations + 1
         
    elif direction == 'R':
        dial_out = dial_in + ticks
        if dial_out > DIAL_SEGMENTS and dial_in != 0:
            rotations = rotations + 1
    else:
        print(f"Unknown direction: {direction}")
        dial_out = dial_in

    return dial_out, rotations 


def ProcessDialInstructions(dial_in, cross_count, zero_hit,  direction, ticks):
    # return result on the dial
    zero_cross = False
    rotations = 0

    dial_out, rotations = CountRotations(dial_in, direction, ticks)
   
    if rotations > 0: 
        cross_count = cross_count + rotations
        print(f"Zero crossing occurred! Count: {cross_count}")

    dial_out = dial_out % DIAL_SEGMENTS

    if dial_out == 0:
        zero_hit = zero_hit + 1
        print(f"Dial hit zero! Hit count: {zero_hit}")

    return dial_out, cross_count, zero_hit

def main():
    parser = argparse.ArgumentParser(description="Parse file lines with a character and a number.")
    parser.add_argument("filename", help="Input file to parse")
    args = parser.parse_args()

    directions = ProcessInputfile(args.filename)
    print(directions)
    dial = DIAL_STARTING
    zero_crossing_count = 0
    zero_hit_count = 0
    for ch, num in directions:
        print(ch, num)
        dial, zero_crossing_count, zero_hit_count =  ProcessDialInstructions(dial, zero_crossing_count, zero_hit_count, ch, num)
        print(f"Dial now at: {dial} after moving {ch}{num} zero crossings: {zero_crossing_count}")

    print(f"Final dial position: {dial} and zero crossings: {zero_crossing_count} and hits: {zero_hit_count} total {zero_crossing_count + zero_hit_count}")


if __name__ == "__main__":
    main()