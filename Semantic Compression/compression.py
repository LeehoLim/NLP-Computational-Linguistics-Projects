import math 
import random
import sys
import argparse
import matplotlib.pyplot as draw

sys.stdout = open("output.txt", "w")

def count_key(alphabet):
	letters = list(set(alphabet))
	[x for x in letters if ' ' not in x]
	empfreq = dict.fromkeys(letters, None)
	totalcount = 0.0
	for key in empfreq:
		count = 0
		
		for word in alphabet:
			if (key in word):
				count += 1
				totalcount += 1
		empfreq[key] = count

	for key in empfreq:
		empfreq[key] = empfreq[key] / totalcount


	return empfreq		

#http://code.activestate.com/recipes/52306-to-sort-a-dictionary/
#Taken sorting code from this site
def accumulatedict(alphabet):
	countfreq = 0
	newdict = {}
	for letter, value in sorted(alphabet.items()):
		newdict[letter] = countfreq
		countfreq += value

	return newdict	

def subinterval_phoneme(accalph, alphabet):
	newdict = {}
	for letter, value in sorted(accalph.items()):
		newdict[letter] = [value, value + alphabet[letter]]
	return newdict


def forward_interval(al_int):
	newdict = {}
	wordlist = []
	file = open('TomSawyer.dx1', 'r')
	i = 0
	for word in file:
		actualLine = word.strip().lower()
		actualLine = actualLine.split(" ")
		actualLine = actualLine[0]
		actualLine += "#"

		lower = 0
		upper = 1
		for i in range(len(actualLine)):
			oldlower = lower
			lower = lower + (upper - lower) * al_int[actualLine[i]][0]
			upper = oldlower + (upper - oldlower) * al_int[actualLine[i]][1]

		newdict[actualLine] = [lower, upper]

	return newdict


def backward_interval(al_int):
	newdict = {}
	wordlist = []
	file = open('TomSawyer.dx1', 'r')
	i = 0
	for word in file:
		actualLine = "#"
		actualLine += word.strip().lower()
		actualLine = actualLine.split(" ")
		actualLine = actualLine[0]

		lower = 0
		upper = 1
		for i in range(len(actualLine) - 1, 0, -1):
			oldlower = lower
			lower = lower + (upper - lower) * al_int[actualLine[i]][0]
			upper = oldlower + (upper - oldlower) * al_int[actualLine[i]][1]

		newdict[actualLine] = [lower, upper]

	return newdict


def strip_hash(back_int, for_int):
	newdict = {}

	for key, value in back_int.items():
		newkey = key.strip("#")
		newdict[newkey] = value

	for key, value in for_int.items():
		newkey2 = key.strip("#")
		newdict[newkey2].append(value[0])
		newdict[newkey2].append(value[1])

	return newdict
	        



def execute():
	alphabet = []
	file = open('TomSawyer.dx1', 'r')
	for line in file:
		actualLine = line.strip().lower()
		actualLine = actualLine.split(" ")
		actualLine = actualLine[0]
		#actualLine = line.strip(" ").lower()
		#actualLine = line.strip("\t").lower()
		result = ''.join([i for i in actualLine if not i.isdigit()])
		alphabet += result
		alphabet += "#"



	a = count_key(alphabet)
	frequency_up_to = accumulatedict(a)
	subint = subinterval_phoneme(frequency_up_to, a)
	wordintervals = forward_interval(subint)
	backwardintervals = backward_interval(subint)

	hashstrip = strip_hash(wordintervals, backwardintervals)
#	finaloutput = combine_output(wordintervals, backwardintervals)


	for word, value in sorted(hashstrip.items()):
		if (len(word) >= 17):
			print "%s  %.12f  %.12f  %.12f  %.12f" %(word, value[0], value[1], value[2], value[3])
		elif (len(word) >= 8):
			print "%s\t    %.12f  %.12f  %.12f  %.12f" %(word, value[0], value[1], value[2], value[3])	
		else:
			print "%s\t\t    %.12f  %.12f  %.12f  %.12f" %(word, value[0], value[1], value[2], value[3])

	xcoor = []
	ycoor = []
	for word, value in sorted(hashstrip.items()):
		xcoor.append(value[0])
		ycoor.append(value[2])

	graph = draw.Figure()
	graph.set_canvas(draw.gcf().canvas)
	draw.plot(xcoor, ycoor, 'ro', ms=3)
	draw.axis([0, 1.15, 0, 1.15])
	draw.title('Tom Sawyer Dict Graph', y=1.04)
	draw.xlabel('Forward Calculation', labelpad=15)
	draw.ylabel('Backward Calculation', labelpad=10)
	graph.savefig('Graph.pdf', format='pdf')




execute()
