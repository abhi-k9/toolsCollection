#!/usr/bin/env python3
# *_* coding: utf-8 *_*

"""
File comparer.

Checks output from the test program against a verified output.

The presence of all the lines from the verified output text file is checked in the test 
executable output. This allows extra lines in the output due to debugging messages,
without causing the test to fail.

Numerical fields are treated differently by allowing slight variation in its value from the
verified one. This accomodates small variations due to external factors.
"""

__author__ = "Abhijit Kale"


import sys
from math import isclose

def check_if_num(word): 
    """Check if the input is a number. Removes commas if any.
    
    PARAMETERS
    ----------
    word: str
        Word to be checked.

    RETURNS
    -------
        A tuple with a bool `True` and the number as float if converted. Otherwise, returns tuple with bool `False` and the original word. 
    """

    try:
        num = float(word.replace(',', ''))
        return (True, num)
    except ValueError:
        return (False, word)

        
def num_aware_line_compare(line1, line2, abs_tol=5.0):
    """Compares two lines. Numeric fields any are checked with tolerence
    
    PARAMETERS
    ----------
    line{1, 2}: str
        Lines to be compared.

    RETURNS
    -------
        Boolean indicatinf if the lines match.
    """
    for (word1, word2) in zip(line1.split(), line2.split()):
        r1 = check_if_num(word1)
        r2 = check_if_num(word2)
        if r1[0] and r2[0]:
            if not isclose(r1[1], r2[1], abs_tol=abs_tol):
                print(word1," != ", word2)
                return False
        else:
            if word1 != word2:
                print(word1," != ", word2)
                return False

    return True


if __name__ == "__main__":

    with open(sys.argv[2], 'r') as verified_file, open(sys.argv[1], 'r') as out_file:
        ver_lines = verified_file.readlines()
        out_lines = out_file.readlines()

        prev_out_line_num = -1
        for ver_line_num in range(len(ver_lines)):
            
            for out_line_num in range(prev_out_line_num + 1, len(out_lines)):
                if num_aware_line_compare(ver_lines[ver_line_num], out_lines[out_line_num]):
                    prev_out_line_num = out_line_num
                    print(prev_out_line_num)
                    break
            else:  # Verified line not found in the output file.
                print("Files do not match")
                sys.exit(-1)

    print("Files match")       
    sys.exit(0) # Files match.
