import math 
import random
import sys
import argparse

sys.stdout = open("sed_string1_string2.txt", "w")

string1 = '#' + sys.argv[1]
string2 = '#' + sys.argv[2]

def assign_cost(char1, char2):
	#Vowel list to check if characters are vowels...
	vowel_list = ['a', 'e', 'i', 'o', 'u']
	accum = 0.0
	#Let us track to see if vowel or consonant
	track1 = 0 #Checks to see if char1 is vowel or consonant
	track2 = 0 #Checks to see if char2 is vowel or consonant

	i = 0
	if (char1 == char2):
		return accum
	
	while (i <= 4):
		if (char1 == vowel_list[i]):
			track1 = 1
			break
		i += 1
	
	j = 0
	while (j <= 4):
		if (char2 == vowel_list[j]):
			track2 = 1
			break
		j += 1
	if ((track1 == 1) and (track2 == 1)):
		accum += 0.5
		return accum
	elif ((track1 == 1 and track2 == 0) or (track1 == 0 and track2 == 1)):
		accum += 3.0
		return accum
	elif ((track1 == 0) and (track2 == 0)):
		accum += 0.6
		return accum


def initiate_values():
	entry_list = [[0 for i in range(len(string1))] for j in range(len(string2))]
	entry_list[0][0] = 0

	parents = [[0 for i in range(len(string1))] for j in range(len(string2))]
	for count1 in range(1, len(string1)):
	 	entry_list[0][count1] = entry_list[0][count1 - 1] + 2 
	 	parents[0][count1] = (0, count1-1)

	for count2 in range(1, len(string2)):
	 	entry_list[count2][0] = entry_list[count2 - 1][0] + 2
	 	parents[count2][0] = (count2-1, 0)


	
	for i in range(1, len(string2)):
		for j in range(1, len(string1)):
			e = entry_list[i][j-1] + 2
			s = entry_list[i-1][j] + 2
			d = entry_list[i-1][j-1] + assign_cost(string1[j], string2[i])
			entry_list[i][j] = min(s, e, d)
			if entry_list[i][j] == e:
				parents[i][j] = ((i, j-1))
			elif entry_list[i][j] == s:
				parents[i][j] = ((i-1, j))
			elif entry_list[i][j] == d:
				parents[i][j] = ((i-1, j-1))

	
	cur = (len(string2)-1, len(string1)-1)
	path = [cur]
	while cur[0] > 0 or cur[1] > 0:
		cur = parents[cur[0]][cur[1]]
		path = [cur] + path


	#PRINT THE LETTER CORRESPONDENCE
	print '-'*(5 * len(string1)) + '--'
	print('    ' + "    ".join(string1))
	print '-'*(5 * len(string1)) + '--'
	for n in range(0, len(string2)):
		store = string2[n] + '  '
		counter = 0
		sub_space = 0
		for i in path: 
			if i[0] == n and counter < 1: 
				store += '     '*i[1] + '%c:%c' % (string2[i[0]], string1[i[1]])
				sub_space = i[1]
				counter += 1
			elif i[0] == n and counter >= 1:
				store += '  '*(i[1] - sub_space) + '%c:%c' % (string2[i[0]], string1[i[1]])
				sub_space = i[1]
		print store		

	print '\n\n'
	#PRINT THE NUMBER CORRESPONDENCE
	print '-'*(5 * len(string1)) + '--'
	print('    ' + "    ".join(string1))
	print '-'*(5 * len(string1)) + '--'
	for n in range(0, len(string2)):
		store = string2[n] + '  '
		counter = 0
		sub_space = 0
		for i in path: 
			if i[0] == n and counter < 1: 
				store += '     '*i[1] + '%.1f' % entry_list[i[0]][i[1]]
				sub_space = i[1]
				counter += 1
			elif i[0] == n and counter >= 1:
				store += '  '*(i[1] - sub_space) + '%.1f' % entry_list[i[0]][i[1]]
				sub_space = i[1]
		print store


def execute():
	initiate_values()


execute()