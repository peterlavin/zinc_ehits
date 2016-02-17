#! /usr/bin/python
from os import sys
'''
This script is for parsing large ligand files and depends on the
$$$$ to denote the end of each ligand.

It takes three arguments...
1. The input file name.
2. The required number of ligands in the output files.
3. A user defined string (with no spaces) which will be used
to identify the source of the ligands at a later date.
For practical purposes, this should be as short as possible.

Author Peter Lavin, lavinp@cs.tcd.ie

'''


if len(sys.argv) == 4:
    print 'Parameters passed are:\nInput file is\t\t' + \
    sys.argv[1] + '\nBlock Size is\t\t' + sys.argv[2] + \
    '\nUser ID for files\t' +  sys.argv[3] + '\n'
else:
    print '\nWrong number of args, aborting NOW!\n'
    print 'Use the following args...\n\ninput file name\n' + \
    'block size\nUser defined name to appear in all files ' + \
    'with NO spaces.\n'
    sys.exit()


srcFileName = sys.argv[1]
# Adding one decimal place to allow rounding of numFiles calculation
blkSize = int(sys.argv[2])
blkSizeFl = sys.argv[2] + ".0"
blkSizeFl = float(blkSizeFl)

# Making a variable from the user defined name
userDefName = sys.argv[3] + '-IN'


# Open the source file
source = open(srcFileName,"r")

# open the file, read and count ligands, close.
totLigs = 0
for line in source:
    if line.startswith("$$$$"):
        totLigs = totLigs + 1
source.close()
print 'Total ligand count is ' +  str(totLigs)

if totLigs < blkSize:
    print '\n !!!!!!  Number of ligands is less than the ' + \
    'block size chosen !!!!!!\n'
    sys.exit(1)

# Number of file to be generated is...
'''
If the blkSize divides evenly in to the totLigs value, 
then simple division is sufficient to find the number of 
files required. If (as is more likely), there is a remainder, the
float value is used, then one added. The result is then changed to
integer (the egg box problem).
'''
if totLigs % blkSize == 0:
    numFiles = totLigs/blkSize
else:
    numFiles = int((totLigs/blkSizeFl) +1)

print 'Number of files will be ' + str(numFiles)


# Number of ligands left over before writing the last file is...
remainder = totLigs % blkSize
print 'Remainder will be ' + str(remainder)


# Open the source = again, for processing this time
source = open(srcFileName, "r")

ligC = 0
fileCount = 1
totC = 0
posLig = 0

fileName = str(totC + 1).zfill(8) + '-' + str(totC + blkSize).zfill(8) + \
'-' + userDefName

destFile = open(fileName + ".sdf", "w")

for line in source:
    destFile.write(line)
    if line.startswith("$$$$"):
        ligC = ligC + 1
        totC = totC + 1
    if ligC == blkSize:
        if fileCount < numFiles:
            print 'Total count is now ' + str(totC) + ' File count is ' + \
            str(fileCount)
            fileCount = fileCount + 1
            # Close the now full destination file and open a new one
            # NB this is assigned to the same source variable.
            destFile.close()
         
            if fileCount == numFiles:
                destFileName = str(totC + 1).zfill(8) + '-' + \
                str(totC + remainder).zfill(8) + '-' + userDefName
            else:
                destFileName = str(totC + 1).zfill(8) + '-' + \
                str(totC + blkSize).zfill(8) + '-' + userDefName

            destFile = open(str(destFileName) + ".sdf", "w")
            # Reset the ligand count to zero for next file
            ligC = 0


print 'Total count at end is ' + str(totC) + ' File count is ' + \
str(fileCount)

