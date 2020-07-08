#!/usr/bin/env python
#encoding:utf-8
"""
filecopyTool.py
Show progress bar while copying large file
https://github.com/dbr/checktveps/blob/1be8f4445fbf766eba25f98f78ec52e955571608/autoPathTv.py#L64-153
"""
import os, sys, re
import shutil


def cursor_vis(text, hide=False, show=False):
    
    HIDE = chr(27)+'[?25l' # l-> low, doesn't show the cursor on the terminal
    SHOW = chr(27)+'[?25h' # h-> high, show the cursor on the terminal
    
    if hide:
        return HIDE + text
    elif show:
        return text + SHOW
    else:
        return HIDE + text + SHOW

def colour(text,colour="red"):
    nocolour=False
    if nocolour: # Colour no supported, return plain text
        return text
    #end if

    c = {'red':'[31m',
         'green':'[32m',
         'blue':'[34m',
        }
        
    CLR=chr(27)+'[0m' # Clear formatting
    if not colour in c.keys():
        raise ValueError("Invalid colour")
    else:
        return chr(27)+c[colour] + text + CLR
    #end if
#end colour


class ProgressBar:
    """From http://code.activestate.com/recipes/168639/"""
    def __init__(self, minValue = 0, maxValue = 10, totalWidth=12):
        self.progBar = "[]"   # This holds the progress bar string
        self.min = minValue
        self.max = maxValue
        self.span = maxValue - minValue
        self.width = totalWidth
        self.amount = 0       # When amount == max, we are 100% done 
        self.updateAmount(0)  # Build progress bar string

    def updateAmount(self, newAmount = 0):
        if newAmount < self.min: newAmount = self.min
        if newAmount > self.max: newAmount = self.max
        self.amount = newAmount

        # Figure out the new percent done, round to an integer
        diffFromMin = float(self.amount - self.min)
        percentDone = (diffFromMin / float(self.span)) * 100.0
        percentDone = round(percentDone)
        percentDone = int(percentDone)

        # Figure out how many hash bars the percentage should be
        allFull = self.width - 2
        numHashes = (percentDone / 100.0) * allFull
        numHashes = int(round(numHashes))

        # build a progress bar with hashes and spaces
        self.progBar = "[" + '#'*numHashes + ' '*(allFull-numHashes) + "]"

        # figure out where to put the percentage, roughly centered
        percentPlace = (len(self.progBar) / 2) - len(str(percentDone)) 
        percentString = str(percentDone) + "%"

        # slice the percentage into the bar
        self.progBar = (self.progBar[0:percentPlace] + percentString
                        + self.progBar[percentPlace+len(percentString):])

    def __str__(self):
        return str(self.progBar)


def copy_with_prog(src_file, dest_file, overwrite = False, block_size = 65536):
    if not overwrite:
        if os.path.isfile(dest_file):
            raise IOError("File exists, not overwriting")
    
    # Get absolute paths
    src_file = os.path.abspath(src_file)
    dest_file = os.path.abspath(dest_file)
    
    # Open src and dest files, get src file size
    src = open(src_file, "rb")
    dest = open(dest_file, "wb")

    src_size = os.stat(src_file).st_size
    
    # Set progress bar
    prgb = ProgressBar(totalWidth = 79, maxValue = src_size)
    
    # Start copying file
    cur_block_pos = 0 # a running total of current position
    while True:
        cur_block = src.read(block_size)
        
        # Update progress bar
        prgb.updateAmount(cur_block_pos)
        cur_block_pos += block_size
        
        sys.stdout.write(
            cursor_vis('\r%s' % str(prgb), hide=True)
        )
        
        # If it's the end of file
        if not cur_block:
            # ..write newline to prevent messing up terminal
            sys.stdout.write(cursor_vis('\n', show=True))
            break
        else:
            # ..if not, write the block and continue
            dest.write(cur_block)
    #end while

    # Close files
    src.close()
    dest.close()

    # Check output file is same size as input one!
    dest_size = os.stat(dest_file).st_size

    if dest_size != src_size:
        raise IOError(
            "New file-size does not match original (src: %s, dest: %s)" % (
            src_size, dest_size)
        )
