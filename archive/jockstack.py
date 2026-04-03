# ------------------------------------------------------------------------------
# JockStack
# Explore the algebra of Jocks' names, relative to other Jocks.
# ------------------------------------------------------------------------------
import random
import sys
import argparse

# --------------------------------------------------------------------------
# Argument parsing
# --------------------------------------------------------------------------
def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("num", nargs="?", type=int, default=0, help="number of Jocks")
    parser.add_argument("--debug", dest="debug", action="store_true", help="show detailed information")
    parser.set_defaults(debug=False)
    args = parser.parse_args()
    return args

# ------------------------------------------------------------------------------
# Main
# ------------------------------------------------------------------------------
def main(num, display=True):
    # --------------------------------------------------------------------------
    # Gather ye input, which is an integer between 1 and 1000
    # --------------------------------------------------------------------------
    if (not display) and num == 0:
        numjocks = 0
    elif num > 0:
        numjocks = num
    else:
        numjocks = None
        while not numjocks:
            i = input("\nHow many Jocks may ye be wantin'?\n")
            try:
                i = int(i)
                if i == 0:
                    print("\nYe must have at least one Jock, Bigjob! Try again!")
                if i < 1001:
                    numjocks = i
                else:
                    print("\nTa' can onlie be one t'ousan! Put a smaller number!")
            except:
                print("\nCrivins! Ye need to be giving us a number, you scunner!")

    if display:
        print(f"\nYe've selected {numjocks} Jocks, and tha's what ye'll be gettin'!")

    # --------------------------------------------------------------------------
    # Do the stacking of the Jocks
    # --------------------------------------------------------------------------
    jocks = stack_jocks(numjocks)

    # --------------------------------------------------------------------------
    # Compile the output text
    # --------------------------------------------------------------------------
    stack = []
    if len(jocks) == 0:
        stack.append("T'ere hain't na Jocks here, Bigjob!")
    else:
        stack.append(f"T'ere are to be {numjocks} jocks this time!")
        for jock in jocks:
            line = f"Oi! We be {jocks[jock]}."
            stack.append(line)
        stack.append("...and t'at's all the Jocks t'are!")

    # --------------------------------------------------------------------------
    # Show the output on the screen and return it
    # --------------------------------------------------------------------------
    if display:
        for line in stack:
            print(line)

    return "\n".join(stack)

# ------------------------------------------------------------------------------
# Do the business 
# ------------------------------------------------------------------------------
def stack_jocks(numjocks, debug=False):
    # --------------------------------------------------------------------------
    # There will be that many Jocks added; arrange them by size and then shuffle
    # to randomize the order in which they will be added to the stack
    # --------------------------------------------------------------------------
    jockpool = list(range(numjocks))
    random.shuffle(jockpool)

    # --------------------------------------------------------------------------
    # The first few Jocks will receive specific names
    # --------------------------------------------------------------------------
    namepool = ["Wee","Medium","Big"]

    # --------------------------------------------------------------------------
    # Add each Jock in turn, determining his name based on his position. Build
    # up a dict of their names, keyed by position
    # --------------------------------------------------------------------------
    jocks = {}
    debuginit = True
    for i, jocksize in enumerate(jockpool):
        # ----------------------------------------------------------------------
        # Get a list of existing Jocks, then add the new Jock to it and sort,
        # so we can find New Jock's position.
        # ----------------------------------------------------------------------
        existing = [x for x in jocks]
        existing.append(jocksize)
        existing = sorted(existing)
        jockpos = existing.index(jocksize)

        # ----------------------------------------------------------------------
        # Find New Jock's immediate neighbors
        # ----------------------------------------------------------------------
        if jockpos == 0:
            smallersize = None
            smallername = None
        else:
            smallersize = existing[jockpos-1]
            smallername = jocks[smallersize]

        if jockpos == len(existing)-1:
            biggersize = None
            biggername = None
        else:
            biggersize = existing[jockpos+1]
            biggername = jocks[biggersize]

        # ----------------------------------------------------------------------
        # For debug
        # ----------------------------------------------------------------------
        if debug:
            if debuginit: 
                print("Jocksizes in order:")
                print(jockpool)
                debuginit=False
            print("")
            print("="*80)
            print(f"Iteration:   {i}")
            print(f"Jocksize:    {jocksize}")
            print(f"Existing:    {existing}")
            print(f"Jocks:       {jocks}")
            print(f"Jockpos:     {jockpos}")
            print(f"Smallersize: {smallersize}")
            print(f"Biggersize:  {biggersize}")
            print(f"Smallername: {smallername}")
            print(f"Biggername:  {biggername}")
            print(f"Namepool:    {namepool}")

        # ----------------------------------------------------------------------
        # Make Jock's name
        # First Jock is just Jock
        # First few additions receive Wee, Medium, Big as appropriate until they
        # are used.
        # Medium will end up one one side of Jock or the other, depending on
        # whehter Big or Wee shows up first.
        # ----------------------------------------------------------------------
        if i == 0:
            jockname = "Jock"
        elif len(namepool)>0:
            if smallername and biggername and "Medium" in namepool:
                jockname = "Medium-Sized Jock"
                namepool.remove("Medium")
            elif not smallername and "Wee" in namepool:
                jockname = "Wee Jock"
                namepool.remove("Wee")
            elif not biggername and "Big" in namepool:
                jockname = "Big Jock"
                namepool.remove("Big")
            else:
                jockname = determine_jock_name(jocks, jocksize, smallersize, smallername, biggersize, biggername, debug=debug)
        else:
            jockname = determine_jock_name(jocks, jocksize, smallersize, smallername, biggersize, biggername, debug=debug)

        # ----------------------------------------------------------------------
        # Add this Jock to the list of Jocks
        # ----------------------------------------------------------------------
        jocks[jocksize] = jockname

    # --------------------------------------------------------------------------
    # Finish
    # --------------------------------------------------------------------------
    return jocks

# ------------------------------------------------------------------------------
# Jock's name depends on the names of those immediately larger or smaller.
# ------------------------------------------------------------------------------
def determine_jock_name(jocks, jocksize, smallersize, smallername, biggersize, biggername, debug=False):
    # --------------------------------------------------------------------------
    # Each entry will only have the space at the final Jock, all else will be 
    # hyphenated
    # --------------------------------------------------------------------------
    if smallername:
        smallername = smallername.replace(" ","-")
    if biggername:
        biggername = biggername.replace(" ","-")

    # --------------------------------------------------------------------------
    # Figure out the offsets between this Jock and his neighbors
    # --------------------------------------------------------------------------
    jocksizes = sorted([x for x in jocks])
    sizerange = jocksizes[-1] - jocksizes[0]
    numjocks = len(jocks)

    offset_small = 0
    offset_big = 0
    if smallersize:
        offset_small = jocksize - smallersize
    if biggersize:
        offset_big = biggersize - jocksize

    offpct_small = offset_small / sizerange
    offpct_big = offset_big / sizerange

    # --------------------------------------------------------------------------
    # Determine if new Jock is much bigger or smaller
    # --------------------------------------------------------------------------
    muchbigger = False
    muchsmaller = False
    if numjocks > 5:
        if offpct_small > 0.35:
            muchbigger = True
        if offpct_big > 0.35:
            muchsmaller = True

    if offpct_small > offpct_big:
        offset_dir = "small"
    else:
        offset_dir = "big"

    # --------------------------------------------------------------------------
    # Set the size-words
    # --------------------------------------------------------------------------
    smalltxt = "Smaller"
    bigtxt = "Bigger"

    if muchsmaller:
        smalltxt = "Much-Smaller"
    if muchbigger:
        bigtxt = "Much-Bigger"

    # --------------------------------------------------------------------------
    # Make the name based on position
    # --------------------------------------------------------------------------
    if not smallername:
        name = f"{smalltxt}-Than-{biggername} Jock"
    elif not biggername:
        name = f"{bigtxt}-Than-{smallername} Jock"
    else:
        if offset_dir == "big":
            name = f"No'-As-Big-As-{biggername}-But-{bigtxt}-Than-{smallername} Jock"
        else:
            name = f"No'-As-Small-As-{smallername}-But-{smalltxt}-Than-{biggername} Jock"

    # --------------------------------------------------------------------------
    # For debug
    # --------------------------------------------------------------------------
    if debug:
        print("-----------------------")
        print("offsets")
        print("-----------------------")
        #print(numjocks, smallersize, jocksize, biggersize, offset_small, offset_big, offpct_small, offpct_big)
        print(f"{numjocks} Jocks so far")
        print(f"Size range is {sizerange}")
        print("Sizes:".ljust(20)    ,  str(smallersize).center(10), str(jocksize).center(10), str(biggersize).center(10))
        print("Offset:".ljust(25)   ,  str(offset_small).center(10) , str(offset_big).center(10))
        print("Offpct:".ljust(25)   ,  str(round(offpct_small, 2)).center(10) , str(round(offpct_big, 2)).center(10))
        print(f"Offsetdir: {offset_dir}")
        print(f"Muchsmaller: {muchsmaller}")
        print(f"Muchbigger: {muchbigger}")


    # --------------------------------------------------------------------------
    # Send back the final name
    # --------------------------------------------------------------------------
    return name

# ------------------------------------------------------------------------------
# Run
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    args = cli()
    num = args.num
    main(num)



