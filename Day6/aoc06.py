import re
import sys
import argparse
from math import floor
from typing import List, Tuple

def ProcessInputfile(filename, keep_format=False) -> List[List]:
    print(f"Processing input file: {filename}")
    result = []

    keep_whitespace=True
    skip_empty=True
    with open(filename, 'r') as f:

        if keep_format:
            lines = f.readlines()
            result = parse_visual_columns(lines,
                                          keep_leading=True,
                                          keep_trailing=True)

        else:
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


def parse_visual_columns(lines: List[str],
                         keep_leading: bool = True,
                         keep_trailing: bool = False) -> List[List[str]]:
    """
    Parse visual columns from aligned text lines.
    - keep_leading: keep spaces that precede a token (leading spaces inside the column).
    - keep_trailing: keep spaces that follow a token (trailing spaces inside the column).
    Returns rows of tokens (slices from the original lines).
    """
    rows = [ln.rstrip('\n') for ln in lines if ln != '']
    if not rows:
        return []

    maxlen = max(len(r) for r in rows)
    padded = [r.ljust(maxlen) for r in rows]

    # separator positions: True if every row has a space at that column
    sep_mask = [all(row[i] == ' ' for row in padded) for i in range(maxlen)]

    # collapse contiguous True runs into separator intervals
    sep_ranges: List[Tuple[int,int]] = []
    i = 0
    while i < maxlen:
        if sep_mask[i]:
            start = i
            while i < maxlen and sep_mask[i]:
                i += 1
            sep_ranges.append((start, i - 1))
        else:
            i += 1

    # build slice intervals between separators
    slices: List[Tuple[int,int]] = []
    prev = 0
    for s, e in sep_ranges:
        if prev <= s - 1:
            slices.append((prev, s))   # end exclusive
        prev = e + 1
    if prev < maxlen:
        slices.append((prev, maxlen))

    # extract tokens per row with requested whitespace preservation
    result: List[List[str]] = []
    for row in padded:
        tokens = []
        for a, b in slices:
            tok = row[a:b]
            if not keep_leading:
                tok = tok.lstrip()
            if not keep_trailing:
                tok = tok.rstrip()
            tokens.append(tok)
        result.append(tokens)

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


def combine_column_chars(col_values: list[str]) -> list[int]:
    """
    Given a list of strings (one string per row for a single column),
    build numbers by concatenating characters top-to-bottom at each character index,
    strip surrounding spaces and convert to int.
    Example: ["1234", " 789"] -> ["1 ", "27", "38", "49"] -> [1,27,38,49]
    """
    if not col_values:
        return []

    maxlen = max(len(s) for s in col_values)
    out: list[int] = []
    for i in range(maxlen):
        tok = ''.join((s[i] if i < len(s) else ' ') for s in col_values)
        tok = tok.strip()
        if tok == '':
            continue
        else:
            out.append(tok)
    return out

def ProcessB(matrix):

    results = []
    operation = []
    column_numbers = []

    # get last row and setup operations
    op_row = matrix[len(matrix)-1]
    print(f"Processing operator row {op_row} : {op_row} ")
    for value in op_row:
        if  '+' in value:
            print(f"Row {value} switching to SUM operation.")
            results.append(0)
            operation.append('+')   
        elif '*' in value:
            print(f"Row {value} switching to MUL operation.")
            results.append(1)
            operation.append('*') 

    print(f"Initial results: {results} ops:{operation}")

    # now start to handle the strips.
    # gather numbers from each strip in the rows of each column.
    # skip last column as that is the operator row.
    for row in range(0, len(matrix) - 1):
        
        print(f"After row {row} results: {results} ops:{operation}")
        for col in range(len(matrix[row])):
            value = matrix[row][col]
            # breakdown numbers into list and update.
            if row == 0:
                # first row, setup list
                column_numbers.append( [] )

                column_numbers[col].append( value )
            else:
                # append to existing list
                column_numbers[col].append( value )
            print(f"Column {col} numbers so far: {column_numbers[col]} ")
        print(f"Column numbers collected: {column_numbers}")

    # now process each column number list to build final numbers into results
    for col in range(len(column_numbers)):
        col_vals = column_numbers[col] # list of strings for this column

        print(f"Processing column {col} values: {col_vals}")
        
        nums = combine_column_chars( col_vals )
        print(f"\t\tColumn {col} combined values: {nums}")

        for n in nums:
            if operation[col] == '+':
                results[col] += int(n)
                print(f"\t\t\t {n} +++ {results[col]} ")

            elif operation[col] == '*':
                results[col] *= int(n)
                print(f"\t\t\t {n} * {results[col]}")

    return results  


def main():
    parser = argparse.ArgumentParser(description="Parse file lines with a character and a number.")
    parser.add_argument("filename", help="Input file to parse")
    args = parser.parse_args()

    # 1. Parse the input file
    matrix = ProcessInputfile(args.filename, keep_format=True)
    print(matrix)

    # 2 Process data.
    results = ProcessB(matrix)
    print(f"Results per row: {results}")

    total = 0
    for r in results:
        total += r

    print(f"Final maths : {total} ")


if __name__ == "__main__":
    main()