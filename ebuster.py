import operator
import sys
import random
from astropy.table import Table, Column
from colorama import init, Fore, Back, Style
from datetime import datetime

init() #Colorama Initialization
info = """\nEntropy Buster v1.1 (https://binsmash.com/tools/ebuster) by Xorus
Usage: ebuster.py [Options] {target}
Example: ebuster.py -t ./strings -v
------------------- 

##GENERAL##
-h, --help - Display the help menu.
-v, --verbose - Increase scan information
-o {outfile}, --output {outfile} - Specify a file to write to.

##SCAN OPTIONS##
-t {file}, --text {file} - Perform a scan over a group of texts.
-p, --pattern - Perform a pattern scan over a group of texts.
-l, --left - Perform left-side expansion on text to pad strings
-r, --right - Perform right-side expansion on text to pad strings

##MIMIC OPTIONS##
-mW {number} {outputfile} - Generate new strings in the file randomly based on character weights.
-mU {number} {outputfile} - Generate new strings in the file randomly."""

vtext = "[" + Fore.YELLOW + Style.BRIGHT + "VERBOSE" + Style.RESET_ALL + "] "
bitconstant = 8 #ASCII Default
encoding = "ASCII"

class ParamBlock:
	verbose = False
	pattern = False
	padright = True
	mimicun = False
	mimicwe = False
	mimicpi = False
	mimic = False

	ohandle = None
	bintarg = ""
	txttarg = ""
	mimicnum = 0
	mimicfile = ""


def Main():
	binscan = False
	txtscan = False
	params = ParamBlock()
	if len(sys.argv) < 2:
		print(info)
		return

	index = 0
	for x in sys.argv:
		if x == "-h" or x == "--help":
			print(info)
			return
		if x == "-v" or x == "--verbose":
			params.verbose = True

		if x == "-p" or x == "--pattern":
			params.pattern = True
		if x == "-mU" or x == "-mW" or x == "-mP":
			ispiping = False
			if x == "-mU":
				params.mimicun = True
				params.mimicwe = False
				params.mimicnum = int(sys.argv[index+1])
				for y in sys.argv:
					if y == "-mP":
						ispiping = True

				if ispiping == False:
					params.mimicfile = sys.argv[index+2]
			if x == "-mW":
				params.mimicwe = True
				params.mimicun = False
				params.mimicnum = int(sys.argv[index+1])
				for y in sys.argv:
					if y == "-mP":
						ispiping = True

				if ispiping == False:
					params.mimicfile = sys.argv[index+2]
			#if x == "-mP":
			#	params.mimicpi = True

			params.mimic = True
			params.mimicpi = False

		#if x == "-b" or x == "--binary":
		#	binscan = True
		#	bintarg = sys.argv[index+1]

		if x == "-t" or x == "--text":
			txtscan = True
			params.txttarg = sys.argv[index+1]

		if x == "-r" or x == "--right":
			params.padright = True

		if x == "-l" or x == "--left":
			params.padright = False

		if x == "-o" or x == "--output":
			params.ofile = sys.argv[index+1]
			params.ohandle = open(ofile,"w")
		index += 1


	if txtscan and binscan:
		print ("Unable to perform a binary and text scan at the same time.")
		return


	if txtscan:
		TextScan(params.txttarg, params)
	#elif binscan:
	#	BinaryScan(binarg, pattern, verbose, padright)










#Wrapper for Print that allows for parameters to be passed along with forced ohandles and verbose.
def wPrint(s, verbose, ohandle, params, e = "\n"):
	if params.mimicpi == False:
		if verbose:
			print(vtext + s, end=e)
			if ohandle != None:
				if e == "\n":
					ohandle.write("[VERBOSE] " + s + "\n")
				else:
					ohandle.write("[VERBOSE] " + s)
		else:
			print(s, end=e)
			if ohandle != None:
				if e == "\n":
					ohandle.write(s + "\n")
				else:
					ohandle.write(s)








#########################################################
#                                                       #
#                  TEXT SCANNING SECTION                #
#                                                       #
#                                                       #
#                                                       #
#########################################################
def Text_Pattern(patterninput, uniquecharacters, params):
	s = "Possible Patterns:\n\t"
	hexchars = list(range(48,57+1)) + list(range(65,70+1)) + list(range(97,122+1))
	l = len(patterninput)

	if patterninput[l-2:l] == "==" or patterninput[l-1:l] == "=":
		s += "Base64\n"

	if l == 32:
		f = False
		for pos in uniquecharacters:
			for x in pos:
				if ord(x) not in hexchars:
					f = True
					break
			if f == True:
				break
		if f == False:
			s += "MD2/MD4/MD5\n"

	if l == 40:
		f = False
		for pos in uniquecharacters:
			for x in pos:
				if ord(x) not in hexchars:
					f = True
					break
			if f == True:
				break
		if f == False:
			s += "SHA-1\n"

	if l == 64:
		f = False
		for pos in uniquecharacters:
			for x in pos:
				if ord(x) not in hexchars:
					f = True
					break
			if f == True:
				break
		if f == False:
			s += "SHA-256\n"

	if l == 128:
		f = False
		for pos in uniquecharacters:
			for x in pos:
				if ord(x) not in hexchars:
					f = True
					break
			if f == True:
				break
		if f == False:
			s += "SHA-512\n"
	wPrint(s, False, params.ohandle, params)






def Text_PadString(highestlength, params, tarray):
	paddedstrings = []
	if params.verbose:
		wPrint("Highest and lowest lengths don't match. Padding strings.", params.verbose, params.ohandle, params)

	if params.padright:
		if params.verbose:
			wPrint("Padding right side.", params.verbose, params.ohandle, params)
		for x in [list(tarray[x]) for x in range(0,len(tarray))]:
			if len(x) < highestlength:
				padamount = highestlength - len(x) - 1
				for i in range(0, padamount+1):
					x.append("\x00")
			paddedstrings.append(x)

	else:
		if params.verbose:
			wPrint("Padding left side.", params.verbose, params.ohandle, params)
		for x in [list(tarray[x]) for x in range(0,len(tarray))]:
			if len(x) < highestlength:
				padamount = highestlength - len(x)-1
				for i in range(0, padamount+1):
					x.insert(0, "\x00")
			paddedstrings.append(x)

	return paddedstrings






def Text_UniqueCharacterScan(highestlength, tarray, statics, params):
	if params.verbose:
		wPrint("Performing character scan", params.verbose, params.ohandle, params)

	uniquecharacters = []
	highestcharacters = []
	lowestcharacters = []
	uniquenum = 0

	for i in range(0, highestlength):
		uniquecharacters.append([])
		lowestchar = 999999999
		highestchar = 0
		for line in [list(tarray[x]) for x in range(0,len(tarray))]:
			if len(line) > i:
				if(ord(line[i]) < lowestchar):
					lowestchar = ord(line[i])
				if(ord(line[i]) > highestchar):
					highestchar = ord(line[i])

				if line[i] not in uniquecharacters[i]:
					uniquecharacters[i].append(line[i])
					uniquenum += 1

		highestcharacters.append(highestchar)
		lowestcharacters.append(lowestchar)

	for i in range(0, highestlength):
		uniquecharacters[i].sort()

	if params.verbose:
		wPrint("Unique Character Readout", params.verbose, params.ohandle, params)
	for x in range(0, len(uniquecharacters)):
		if len(uniquecharacters[x]) == 1:
			statics += 1
		if params.verbose: ##FIX
			wPrint("| ", params.verbose, params.ohandle, params, "")
			for k in uniquecharacters[x]:
				if k != "\x00":
					wPrint(k + " ", False, params.ohandle, params, "")
			wPrint("", False, params.ohandle, params)

	return (uniquecharacters, statics)







def Text_GeneratePatternString(uniquecharacters, params):
	if params.verbose:
		wPrint("Generating Pattern Readout", params.verbose, params.ohandle, params)

	patternstring = ""
	coloredpatternstring = ""
	for q in uniquecharacters:
		if len(q) > 1:
			patternstring += "?"
			coloredpatternstring += Fore.YELLOW + Style.BRIGHT
			coloredpatternstring += "?"
			coloredpatternstring += Fore.RESET + Style.RESET_ALL
		else:
			patternstring += q[0]
			coloredpatternstring += Fore.GREEN + Style.BRIGHT
			coloredpatternstring += q[0]
			coloredpatternstring += Fore.RESET + Style.RESET_ALL

	return (patternstring, coloredpatternstring)









def TotalGuesses(bitlength, unknowns):
	s = 0
	speed = 1000
	for x in range(0, bitlength):
		s += 2 ** x
	f = s ** (unknowns/bitlength)
	if (f/speed) > 60: #Seconds
		if (f/speed)/60 > 60: #Minutes 
			if(f/speed)/60/60 > 24: #More than 24 hours
				if (f/speed)/60/60/24 > 7: #More than 7 days
					if(f/speed)/60/60/24/7 > 30: #More than 1 month
						if(f/speed)/60/60/24/7/30 > 12:
							return (str('%.3f'%((f/speed)/60/60/24/7/30)) + "y", f)
						else:
							return (str('%.3f'%((f/speed)/60/60/24/7)) + "mo", f)
					else:
						return (str('%.3f'%((f/speed)/60/60/24)) + "w", f)
				else:
					return (str('%.3f'%((f/speed)/60/60/24)) + "d", f)
			else:
				return (str('%.3f'%((f/speed)/60/60)) + "h", f)
		else:
			return (str('%.3f'%((f/speed)/60)) + "m", f)
	else:
		return (str('%.3f'%((f/speed))) + "s", f)

	return ("", 0)






def Text_GenerateCharacterWeight(lines, uniquecharacters, highestlength, params):
	if params.verbose:
		wPrint("Generating character weights", params.verbose, params.ohandle, params)

	cweight = []
	scweight = []

	for i in range(0, highestlength):
		cweight.append([])
		for l in lines:
			found = False
			for q in cweight[i]:
				if "\x00" in q:
					cweight[i].remove(q)
				if len(q) > 0:
					if l[i] == q[0]:
						q[1] = str(int(q[1]) + 1)
						found = True
						break
			if found == False:
				cweight[i].append([l[i], "1"])

	#Hacky fix to make all digits the same length for order.
	#Otherwise, if one number has less digits than the others then it will appear first.
	for q in range(0, highestlength):
		hposlen = 0
		for char in range(0, len(cweight[q])):
			if len(cweight[q][char][1]) > hposlen:
				hposlen = len(cweight[q][char][1])

		for char in range(0, len(cweight[q])):
			if len(cweight[q][char][1]) < hposlen:
				cweight[q][char][1] = '0'*(hposlen - len(cweight[q][char][1])) + cweight[q][char][1]


	hlen = 0
	for x in range(0, highestlength):
		scweight.append([])
		scweight[x] = sorted(cweight[x], key=lambda g: g[1], reverse=True)
		i = 0
		ltotal = 0
		for ltot in range(0, len(scweight[x])):
			ltotal += int(scweight[x][ltot][1])

		for g in scweight[x]:
			val = float(g[1])
			if float(val/ltotal)*100.00 >= 10.00:
				g[1] = str('%.3f'%(float(val/ltotal)*100.00)) + "%"
			else:
				g[1] = str('0' + '%.3f'%(float(val/ltotal)*100.00)) + "%"
			scweight[x][i] = ':'.join(g[0:2])
			i += 1

		if len(scweight[x]) > hlen:
			hlen = len(scweight[x])

	for x in range(0, highestlength):
		while len(scweight[x]) < hlen:
			scweight[x].append("")

	return Table(scweight,names=(["Position: " + str(s) for s in range(0,highestlength)]))






def Text_Mimic(weighttable, lowestlength, highestlength, params):
	rlength = 0	
	colprob = []

	for i in range(0, len(weighttable.colnames)):
		colprob.append([])
		for y in weighttable["Position: " + str(i)]:
			if len(y) >= 2:
				probability = y.split(':')
				probability[1] = probability[1].replace('%','')
				colprob[i].append([probability[0], float(probability[1])])
	
	mimiclines = []
	for m in range(0, params.mimicnum):
		random.seed(datetime.now())
		if lowestlength < highestlength:
			rlength = random.randrange(lowestlength,highestlength+1)
			#print("Generated length:" + str(rlength))
		else:
			rlength = highestlength

		s = ""
		i = 0

		if params.mimicwe == True:
			while len(s) < rlength:
				for cid in range(0, len(colprob[i])):
					p = colprob[i][cid][1]
					r = random.uniform(0, 100)
					if r <= p:
						s += colprob[i][cid][0]
						i+=1
						break

					if cid == colprob[i]:
						cid = 0
		elif params.mimicun == True:
			while len(s) < rlength:
				tl = len(colprob[i])
				r = random.randint(0, tl-1)
				s += colprob[i][r][0]
				i+=1

		mimiclines.append(s)

	if params.mimicpi == False:
		o = None
		try:
			o = open(params.mimicfile, "a")
		except:
			wPrint("File " + params.mimicfile + " does not exist. Creating file.", params.verbose, params.ohandle, params)
			o = open(params.mimicfile, "w+")

	if len(mimiclines) > 100 and params.verbose:
		wPrint("Printing a maximum of 100 lines to console.", params.verbose, params.ohandle, params)

	i = 0
	if params.mimicpi == False:
		for l in mimiclines:
			o.write(str(l) + "\n")
			if params.verbose and i < 100:
				wPrint(str(l), params.verbose, params.ohandle, params)
	else:
		for l in mimiclines:
			print(l)




			

def TextScan(target, params):
	uniquecharacters = []	
	tarray = []
	characters = []
	lowestlength = 9999999
	highestlength = 0
	statics = 0

	if params.verbose:
		wPrint("Loading: " + target, params.verbose, params.ohandle, params)
	handle = open(target, "r")
	for line in handle:
		line = line.strip('\n')
		tarray.append(line)
		characters.append(list(line))
		if len(line) < lowestlength:
			lowestlength = len(line)
			if params.verbose:
				wPrint("New lowest length of " + str(lowestlength), params.verbose, params.ohandle, params)
		if len(line) > highestlength:
			highestlength = len(line)
			if params.verbose:
				wPrint("New highest length of " + str(highestlength), params.verbose, params.ohandle, params)

	if highestlength != lowestlength:
		paddedstrings = Text_PadString(highestlength, params, tarray)
	else:
		paddedstrings = tarray

	cscan = Text_UniqueCharacterScan(highestlength, tarray, statics, params)
	uniquecharacters = cscan[0]
	statics = cscan[1]

	patternstring = Text_GeneratePatternString(uniquecharacters, params)

	wtable = Text_GenerateCharacterWeight(paddedstrings, uniquecharacters, highestlength, params)

	wPrint("", False, params.ohandle, params)
	wPrint("+---Text Attributes---+", False, params.ohandle, params)
	wPrint("Final pattern string:" + patternstring[1], False, params.ohandle, params)
	if params.pattern:
		Text_Pattern(patternstring[0], uniquecharacters, params)
	#wPrint("Selected Encoding:" + encoding)
	if highestlength != lowestlength:	
		wPrint("Minimum string length: " + str(lowestlength), False, params.ohandle, params)
		wPrint("Maximum string length: " + str(highestlength), False, params.ohandle, params)
		wPrint("Average string length: " + str((highestlength + lowestlength) / 2), False, params.ohandle, params)
	else:
		wPrint("String length: " + str(highestlength), False, params.ohandle, params)
	wPrint("", False, params.ohandle, params)
	wPrint("+---Bit Information---+", False, params.ohandle, params)
	if highestlength != lowestlength:
		wPrint("Highest bits:" + str(bitconstant * highestlength), False, params.ohandle, params)
		wPrint("Lowest bits:" + str(bitconstant * lowestlength), False, params.ohandle, params)
	else:
		wPrint("Total bits:" + str(bitconstant * highestlength), False, params.ohandle, params)
	wPrint("Total static bits:" + str(bitconstant * statics), False, params.ohandle, params)
	unknownbits = 0
	if highestlength != lowestlength:
		unknownbits = (bitconstant * highestlength) - bitconstant * statics
		wPrint("Highest unknown bits:" + str(((bitconstant * highestlength) - bitconstant * statics)), False, params.ohandle, params)
		wPrint("Lowest unknown bits:" + str(((bitconstant * lowestlength) - bitconstant * statics)), False, params.ohandle, params)
	else:
		unknownbits = (bitconstant * highestlength) - bitconstant * statics
		wPrint("Unknown bits:" + str(((bitconstant * highestlength) - bitconstant * statics)), False, params.ohandle, params)
	wPrint("Number of unknown bit guesses:", False, params.ohandle, params)
	wPrint("\t" + Fore.GREEN + Style.BRIGHT + "ASCII" + Style.RESET_ALL + " " + str(TotalGuesses(8,unknownbits)[1]), False, params.ohandle, params)
	wPrint("\t\t" + Fore.GREEN + Style.BRIGHT + "Estimated Time:" + Style.RESET_ALL + " " + str(TotalGuesses(8,unknownbits)[0]), False, params.ohandle, params)


	wPrint("", False, params.ohandle, params)
	wPrint("" + Fore.RED + Style.BRIGHT + "Estimated Time based on 1000 guesses per second." + Style.RESET_ALL, False, params.ohandle, params)

	wPrint("", False, params.ohandle, params)
	wPrint("+---Character weights---+", False, params.ohandle, params)

	if params.mimicpi == False:
		print(wtable)
		if params.ohandle != None:
			wtable.write(params.ohandle, format='ascii.fixed_width')

	if params.mimic:
		wPrint("\nGenerating " + str(params.mimicnum) + " similar strings.", False, params.ohandle, params)
		Text_Mimic(wtable, lowestlength, highestlength, params)	
		wPrint("Finished generating " + str(params.mimicnum) + " similar strings.", False, params.ohandle, params)
		print("")




Main()
