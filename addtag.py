#! /usr/bin/python
import os
from os import sys
import shutil

srcFileName = sys.argv[1]

# Copy the original file to a temp one
shutil.copy(srcFileName, "tempfile.sdf")

# Use a part of the orig file name to make the new one
destFileName = srcFileName[:-4] + "_tagged.sdf" 
print "\nOutput file will be called " + destFileName + "\n"

# Open the two file, dest and the input (temp) file
destination = open(destFileName, "w")
source = open( "tempfile.sdf", "r" )

# Inerate over every line in the file...
for line in source:
    destination.write( line )
    # When a line is found starting with ZINC, this is a first line of new ligand, store this
    if line.startswith("ZINC"):
        ZINCvariable = line
        ZINCvariable = ZINCvariable.replace("\n","")
    # When the end of a ligand is found, insert the tag syntax, clear the ZINCvariable
    if line.startswith("M  END"):
        destination.write("\n" + "> <fm_tagname>" + "\n" + ZINCvariable + "\n\n")
        ZINCvariable = ""

# Close files opened, remove the temp file - DONE!
source.close()
os.remove("tempfile.sdf")
destination.close()

