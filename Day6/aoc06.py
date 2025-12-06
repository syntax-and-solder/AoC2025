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
            
            parts = line.strip().split()
            element = []
            for p in parts:
                try:
                    element.append(int(p))
                except ValueError:
                    element.append(p)
            result.append(element)
    return result 


def Process(matrix):

    results = []
    operation = []

    # starting from last row and decide if we sum or multiplying
    for row in range(len(matrix)-1, -1, -1):
        print(f"Processing row {row} : {matrix[row]} ")
        for col in range(len(matrix[row])):
            value = matrix[row][col]
            if value == '+':
                print(f"Row {row} switching to SUM operation.")
                results.append(0)
                operation.append('+')   
            elif value == '*':

                print(f"Row {row} switching to MUL operation.")
                results.append(1)
                operation.append('*') 

            else:

                if operation[col] == '+':
                    results[col] += int(value)
                    print(f"\t\t {value} +++ {results[col]} ")

                elif operation[col] == '*':
                    results[col] *= int(value)
                    print(f"\t\t {value} * {results[col]}")

        print(f"After row {row} results: {results} ops:{operation}")

    return results  




def main():
    parser = argparse.ArgumentParser(description="Parse file lines with a character and a number.")
    parser.add_argument("filename", help="Input file to parse")
    args = parser.parse_args()

    # 1. Parse the input file
    matrix = ProcessInputfile(args.filename)
    print(matrix)

    # 2. Process data.
    results = Process(matrix)
    print(f"Results per row: {results}")

    total = 0
    for r in results:
        total += r

    print(f"Final maths : {total} ")


if __name__ == "__main__":
    main()