# ------------------------------------------------------------------------------
# JockStack — GDScript port of the core algorithm
# Mirrors backend/jockstack.py exactly.
# Used as an offline fallback; the backend is authoritative for saved runs.
# ------------------------------------------------------------------------------
class_name JockStackAlgo


static func stack_jocks(numjocks: int) -> Array:
	if numjocks == 0:
		return []

	# Build size pool and shuffle
	var pool: Array[int] = []
	for i in range(numjocks):
		pool.append(i)
	pool.shuffle()

	var namepool: Array[String] = ["Wee", "Medium", "Big"]
	var jocks: Dictionary = {}  # size (int) -> name (String), for neighbour lookups
	var result: Array = []      # generation order — the display order

	for i in range(pool.size()):
		var jocksize: int = pool[i]

		# Sorted list of all sizes including the new one
		var existing: Array = jocks.keys()
		existing.append(jocksize)
		existing.sort()

		var jockpos: int = existing.find(jocksize)

		# Immediate neighbours
		var smallersize = null
		var smallername = null
		var biggersize = null
		var biggername = null

		if jockpos > 0:
			smallersize = existing[jockpos - 1]
			smallername = jocks[smallersize]

		if jockpos < existing.size() - 1:
			biggersize = existing[jockpos + 1]
			biggername = jocks[biggersize]

		# Name assignment — mirrors Python logic exactly
		var jockname: String
		if i == 0:
			jockname = "Jock"
		elif namepool.size() > 0:
			if smallername != null and biggername != null and "Medium" in namepool:
				jockname = "Medium-Sized Jock"
				namepool.erase("Medium")
			elif smallername == null and "Wee" in namepool:
				jockname = "Wee Jock"
				namepool.erase("Wee")
			elif biggername == null and "Big" in namepool:
				jockname = "Big Jock"
				namepool.erase("Big")
			else:
				jockname = _determine_jock_name(
					jocks, jocksize, smallersize, smallername, biggersize, biggername
				)
		else:
			jockname = _determine_jock_name(
				jocks, jocksize, smallersize, smallername, biggersize, biggername
			)

		jocks[jocksize] = jockname
		result.append({"size": jocksize, "name": jockname})

	return result


static func _determine_jock_name(
	jocks: Dictionary,
	jocksize: int,
	smallersize,
	smallername,
	biggersize,
	biggername
) -> String:
	if smallername != null:
		smallername = (smallername as String).replace(" ", "-")
	if biggername != null:
		biggername = (biggername as String).replace(" ", "-")

	var jocksizes: Array = jocks.keys()
	jocksizes.sort()
	var sizerange: int = int(jocksizes[-1]) - int(jocksizes[0])
	var numjocks: int = jocks.size()

	var offset_small: int = 0
	var offset_big: int = 0
	if smallersize != null:
		offset_small = jocksize - int(smallersize)
	if biggersize != null:
		offset_big = int(biggersize) - jocksize

	# Guard against division by zero (can only happen with 1 Jock, but be safe)
	var offpct_small: float = 0.0
	var offpct_big: float = 0.0
	if sizerange > 0:
		offpct_small = float(offset_small) / float(sizerange)
		offpct_big   = float(offset_big)   / float(sizerange)

	var muchbigger: bool = false
	var muchsmaller: bool = false
	if numjocks > 5:
		if offpct_small > 0.35:
			muchbigger = true
		if offpct_big > 0.35:
			muchsmaller = true

	var offset_dir: String = "small" if offpct_small > offpct_big else "big"

	var smalltxt: String = "Much-Smaller" if muchsmaller else "Smaller"
	var bigtxt: String   = "Much-Bigger"  if muchbigger  else "Bigger"

	if smallername == null:
		return "%s-Than-%s Jock" % [smalltxt, biggername]
	elif biggername == null:
		return "%s-Than-%s Jock" % [bigtxt, smallername]
	elif offset_dir == "big":
		return "No'-As-Big-As-%s-But-%s-Than-%s Jock" % [biggername, bigtxt, smallername]
	else:
		return "No'-As-Small-As-%s-But-%s-Than-%s Jock" % [smallername, smalltxt, biggername]
