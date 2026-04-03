# ------------------------------------------------------------------------------
# JockStack — core algorithm
# Explore the algebra of Jocks' names, relative to other Jocks.
# Inspired by the Nac Mac Feegle, with thanks to Sir Terry Pratchett.
# ------------------------------------------------------------------------------
import random


def stack_jocks(numjocks: int) -> dict:
    """
    Generate a stack of numjocks Jocks, naming each based on its relative
    position among its neighbours.

    Returns a dict keyed by size (int), value is the Jock's name (str).
    The dict is not ordered — callers should sort by key if display order matters.
    """
    jockpool = list(range(numjocks))
    random.shuffle(jockpool)

    namepool = ["Wee", "Medium", "Big"]
    jocks = {}

    for i, jocksize in enumerate(jockpool):
        # Build a sorted list of all sizes so far + the new one
        existing = sorted([x for x in jocks] + [jocksize])
        jockpos = existing.index(jocksize)

        # Find immediate neighbours
        if jockpos == 0:
            smallersize = None
            smallername = None
        else:
            smallersize = existing[jockpos - 1]
            smallername = jocks[smallersize]

        if jockpos == len(existing) - 1:
            biggersize = None
            biggername = None
        else:
            biggersize = existing[jockpos + 1]
            biggername = jocks[biggersize]

        # Assign a name
        if i == 0:
            jockname = "Jock"
        elif len(namepool) > 0:
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
                jockname = determine_jock_name(
                    jocks, jocksize, smallersize, smallername, biggersize, biggername
                )
        else:
            jockname = determine_jock_name(
                jocks, jocksize, smallersize, smallername, biggersize, biggername
            )

        jocks[jocksize] = jockname

    return jocks


def determine_jock_name(
    jocks: dict,
    jocksize: int,
    smallersize,
    smallername,
    biggersize,
    biggername,
) -> str:
    """
    Name a Jock based on his size relative to his immediate neighbours.
    Names reference the neighbours' names, hyphenating internal spaces.
    """
    if smallername:
        smallername = smallername.replace(" ", "-")
    if biggername:
        biggername = biggername.replace(" ", "-")

    jocksizes = sorted(jocks.keys())
    sizerange = jocksizes[-1] - jocksizes[0]
    numjocks = len(jocks)

    offset_small = jocksize - smallersize if smallersize is not None else 0
    offset_big = biggersize - jocksize if biggersize is not None else 0

    offpct_small = offset_small / sizerange
    offpct_big = offset_big / sizerange

    muchbigger = False
    muchsmaller = False
    if numjocks > 5:
        if offpct_small > 0.35:
            muchbigger = True
        if offpct_big > 0.35:
            muchsmaller = True

    offset_dir = "small" if offpct_small > offpct_big else "big"

    smalltxt = "Much-Smaller" if muchsmaller else "Smaller"
    bigtxt = "Much-Bigger" if muchbigger else "Bigger"

    if not smallername:
        return f"{smalltxt}-Than-{biggername} Jock"
    elif not biggername:
        return f"{bigtxt}-Than-{smallername} Jock"
    elif offset_dir == "big":
        return f"No'-As-Big-As-{biggername}-But-{bigtxt}-Than-{smallername} Jock"
    else:
        return f"No'-As-Small-As-{smallername}-But-{smalltxt}-Than-{biggername} Jock"
