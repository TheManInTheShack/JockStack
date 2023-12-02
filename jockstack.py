# ------------------------------------------------------------------------------
# JockStack
# Explore the algebra of Jocks' names, relative to other Jocks.
# ------------------------------------------------------------------------------
import random

# ------------------------------------------------------------------------------
# Main
# ------------------------------------------------------------------------------
def main():
    # --------------------------------------------------------------------------
    # Gather ye input, which is an integer between 1 and 1000
    # --------------------------------------------------------------------------
    print("")

    numjocks = None
    while not numjocks:
        i = input("How many Jocks may ye be wantin'?\n")
        try:
            i = int(i)
            if i == 0:
                print("Ye must have at least one Jock, Bigjob!")
            if i < 1001:
                numjocks = i
                print("")
            else:
                print("Ta' can onlie be one t'ousan!")
        except:
            print("Crivins! Ye need to be giving us a number, you scunner!")

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
        # First Jock is just Jock, he already introduced himself
        # ----------------------------------------------------------------------
        if i == 0:
            print(f"{jocksize}  Oi! We be Jock!")
            jocks[jocksize] = "Jock"
            continue

        # ----------------------------------------------------------------------
        # Find New Jock's immediate neighbors
        # ----------------------------------------------------------------------
        if jockpos == 0:
            smallerpos = None
            smallername = None
        else:
            smallerpos = existing[jockpos-1]
            smallername = jocks[smallerpos]

        if jockpos == len(existing)-1:
            biggerpos = None
            biggername = None
        else:
            biggerpos = existing[jockpos+1]
            biggername = jocks[biggerpos]

        # ----------------------------------------------------------------------
        # Make Jock's name
        # First few additions receive Wee, Medium, Big as appropriate until they
        # are used.
        # Medium will end up one one side of Jock or the other, depending on
        # whehter Big or Wee shows up first.
        # ----------------------------------------------------------------------
        if len(namepool)>0:
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
                jockname = determine_jock_name(smallername, biggername)
        else:
            jockname = determine_jock_name(smallername, biggername)

        # ----------------------------------------------------------------------
        # For debug
        # ----------------------------------------------------------------------
        if False:
            if debuginit: 
                print("Jocksizes in order:")
                print(jockpool)
                debuginit=False
            print("")
            print(f"Iteration:   {i}")
            print(f"Jocksize:    {jocksize}")
            print(f"Existing:    {existing}")
            print(f"Jocks:       {jocks}")
            print(f"Jockpos:     {jockpos}")
            print(f"Smallerpos:  {smallerpos}")
            print(f"Biggerpos:   {biggerpos}")
            print(f"Smallername: {smallername}")
            print(f"Biggername:  {biggername}")
            print(f"Namepool:    {namepool}")

        # ----------------------------------------------------------------------
        # Introduce new Jock and add him to the list
        # ----------------------------------------------------------------------
        print("")
        print(f"{jocksize}  Oi! We be '{jockname}'")
        jocks[jocksize] = jockname

    # --------------------------------------------------------------------------
    # Finish
    # --------------------------------------------------------------------------
    print("\n...and t'at's all the Jocks t'are!")

# ------------------------------------------------------------------------------
# Jock's name depends on the names of those immediately larger or smaller.
# ------------------------------------------------------------------------------
def determine_jock_name(smallername, biggername):
    # --------------------------------------------------------------------------
    # Each entry will only have the space at the final Jock, all else will be 
    # hyphenated
    # --------------------------------------------------------------------------
    if smallername:
        smallername = smallername.replace(" ","-")
    if biggername:
        biggername = biggername.replace(" ","-")

    # --------------------------------------------------------------------------
    # Make and return the name based on position
    # --------------------------------------------------------------------------
    if not smallername:
        return f"Smaller-Than-{biggername} Jock"
    elif not biggername:
        return f"Bigger-Than-{smallername} Jock"
    else:
        return f"No'-As-Big-As-{biggername}-But-Bigger-Than-{smallername} Jock"

# ------------------------------------------------------------------------------
# Run
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    main()



