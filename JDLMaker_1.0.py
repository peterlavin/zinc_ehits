#! /usr/bin/python
'''

Python script to generate JDl file for gLite job submission, takes three args...
1) The full file name of the receptor
2) The full file name of the file containing the ligands
3) the full file name of the clip-file

One variable is hardcoded here, e.g. the name of
patch file used in eHiTS installation on the WN.

IMPORTANT: The clipfile name here is made by replacing the characters 'rec' with 'lig'
in the first argument passed. This depends on the file naming scheme being
consistent.

IMPORTANT; the file name created from abridged arguments passed here are also
used in the executable pyehits_x.x.py. The file name used in the OutputSnabox must
be the same as the file to which the best_scores.txt are copied at the end of
the pyehits_x.x.py script.

'''

import os,commands,time
from os import sys

print 'Testing args, number of args passed was... ' + str(len(sys.argv)-1)

# verifying list of args passed (from jdl file when in grid)
if len(sys.argv) == 4:
    print sys.argv[1] + ' ' + sys.argv[2] + sys.argv[3] + '\n' 
else:
    print '\nWrong number of args, aborting NOW!\n\n Use the following args\n\n'
    print 'The full file name of the receptor'
    print 'The full file name of the file containing the ligands'
    print 'The full file name of the clip-file\n\n'
    sys.exit()

# Trimming file extensions from args to create path to best_scores.txt file
RecName = sys.argv[1][:-8]
LigName = sys.argv[2][:-7]

# This variable is used for the file in the OutputSandbox below
filenameBase = RecName + '_' + LigName
filename = filenameBase  + '.jdl'
print 'File name is ' + filename

# Creating the clip file name from sys.argv[1]
ClipName = sys.argv[3]


# creating actual jdl file
fn = open (filename, 'w')

# Creating the first four lines, these will not change frequently
fn.write('[\n  Type = "job";\n  JobType = "Normal";\n  Executable = "pyehits_1.0.py";\n')

# Creating the arguments line, this will change as files change,
# NB This makes one line, note no \n used except at the end.
fn.write('  Arguments = "eHiTS_2009.1_Cell.bin')
fn.write(' ')
fn.write(sys.argv[1])
fn.write(' ')
fn.write(sys.argv[2])
fn.write(' ')
fn.write(ClipName)
fn.write('";\n')

# The following line does not change regularly
fn.write('  StdOutput = "' + filenameBase +'_sim.out";\n  StdError = "' + filenameBase + '_sim.err";\n')

fn.write('  InputSandbox = {"pyehits_1.0.py","')
fn.write(sys.argv[1])
#fn.write('","')
#fn.write(sys.argv[2]) 
fn.write('","' + ClipName + '","patch-ehits-proxy.patch"')
fn.write('};\n')

# The OutputSandbox will change for each job, this makes a unique file name for each job,
# this line depends on the same flename being created here as is created for the output by
# the executable file (ie. pyehits.py)
fn.write('  OutputSandbox = {"')
fn.write(filenameBase)
fn.write('_sim.err","')
fn.write(filenameBase)
fn.write('_sim.out"')
#fn.write(filenameBase)
#fn.write('_BS_ehps3.txt","')
#fn.write(filenameBase)
#fn.write('_BP_ehps3.sdf"')
fn.write('};\n')




# This next 2 lines change as CE requirements change, so this will need editing before
# changing to PS3 resources.
#fn.write('  Requirements=(other.GlueCEInfoTotalCPUs>0 && RegExp("ps3", other.GlueCEUniqueID));\n')
fn.write('  Requirements = other.GlueCEUniqueID == "gridgate.cs.tcd.ie:2119/jobmanager-pbs-ps3";\n')

fn.write('  RetryCount = 3;\n]\n')

# Close the file after all writing is done
fn.close()

# For debug only, print the created file to the screen...
print '\n' + commands.getoutput('cat ' + filename) + '\n'

print '\n --- End of JDLMaker python script ---\n'


# END of file
