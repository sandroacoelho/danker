#!/usr/bin/python3
#    danker - PageRank on Wikipedia/Wikidata
#    Copyright (C) 2017  Andreas Thalhammer
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import time

dictionary = {}

def init(leftSorted, startValue):
	previous = 0
	currentCount = 1
	with open(leftSorted, encoding="utf-8") as f:
		for line in f:
			current = int(line.split("\t")[0])
			receiver = int(line.split("\t")[1])

			# always take care of inlinks
			data = dictionary.get(receiver, (0, startValue, []))
			data[2].append(current)
			dictionary[receiver] = data[0], data[1], data[2]

			# now take care of counts
			if (current == previous):
				# increase counter
				currentCount = currentCount + 1
			else:
				if (previous != 0):
					# store previousQID and reset counter
					prev = dictionary.get(previous, (0, startValue, []))
					dictionary[previous] = currentCount, prev[1], prev[2]
					currentCount = 1
			previous = current
		# write last bunch
		if (previous != 0):	
			prev = dictionary.get(previous, (0, startValue, []))
			dictionary[previous] = currentCount, prev[1], prev[2]

def danker(iterations, damping, startValue):
	for i in range(0, iterations):
		print(str(i + 1) + ".", end="", flush=True, file=sys.stderr)
		k = list(dictionary.keys())
		k.sort()
		for i in k:
			current = dictionary.get(i)
			dank = 1 - damping
			dictionary[i] = current[0], dank, current[2]
			m = current[2]
			m.sort()
			for j in m:
				inDank = dictionary.get(j)
				dank = dank + (damping * inDank[1] / inDank[0])
	#			print(str(i) + '\t' + str(j) + '\t' + str(dank))
				dictionary[i] = current[0], dank, current[2]
	print("", file=sys.stderr)

if __name__ == '__main__':
	leftSorted = sys.argv[1]
	damping = float(sys.argv[2])
	iterations = int(sys.argv[3])
	startValue = float(sys.argv[4])
	start = time.time()
	init(leftSorted, startValue)
	danker(iterations, damping, startValue)
	for i in dictionary.keys():
		print(str(i) + "\t" + str(dictionary[i][1]))
	print("Computation of PageRank on '" + leftSorted + "' took " + str(int(100 * (time.time() - start)) / 100) + " seconds.", file=sys.stderr)
