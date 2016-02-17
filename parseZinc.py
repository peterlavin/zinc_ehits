#! /usr/bin/python
from os import sys

######################################################
# Script takes two args, source file and block size
# Parses the source file in to files the size of the 
# block size.
#
#
# TODO Incorporate name of source file in to the output file names
#
######################################################


if len(sys.argv) == 3:
    print sys.argv[1] + ' ' + sys.argv[2] + '\n'
else:
    print '\nWrong number of args, aborting NOW!\n'
    sys.exit()


srcFileName = sys.argv[1]
# Adding one decimal place to allow rounding of numFiles calculation
blkSize = int(sys.argv[2])
blkSizeFl = sys.argv[2] + ".0"
blkSizeFl = float(blkSizeFl)

# Open the source file
source= open(srcFileName,"r")

# open the file, read and count ligands, close.
totLigs = 0
for line in source:
   if line.startswith("$$$$"):
      totLigs = totLigs + 1
source.close()
print 'Total ligand count is ' +  str(totLigs)

# Number of file to be generated is...
numFiles = round(totLigs/blkSizeFl)
numFiles = int(numFiles)
print 'Number of files will be ' + str(numFiles)


# Open the source= again, for processing this time
source= open(srcFileName, "r")

ligC = 0
fileCount = 1
totC = 0
posLig = 0

destFile = open(str(fileCount) + ".sdf", "w")

for line in source:
   destFile.write(line)
   if line.startswith("$$$$"):
      ligC = ligC + 1
      totC = totC + 1
   if ligC == blkSize:
      if fileCount < numFiles:
         print 'Total count is now ' + str(totC) + ' File count is ' + str(fileCount)
         fileCount = fileCount + 1
         # Close the now full destination file and open a new one
         # NB this is assigned to the same source variable.
         destFile.close()
         destFile = open(str(fileCount) + ".sdf", "w")
         #print 'Local lig count is ' + str(ligC)
      # Reset the ligand count to zero for next file
      ligC = 0


print 'Total count at end is ' + str(totC) + ' File count is ' + str(fileCount)

