#! /usr/bin/python

'''
----------------------------------------------------------------------------

This script runs eHiTS, takes four args in the following order...
1) eHiTS_binary_file
2) receptor 
3) ligand 
4) clipfile

It is designed to be used as the executable file for grid job submissions
and is used with a JDL file and the other appropriate files matchig the
above args.

NB, this file should not change from one eHiTS run to the next, 
all changes are made in the individual .jdl file for each job.

When the version of eHiTS is changed, a new patch file is needed and a
new md5sum value. The location of the ehits.lic will also need editing.

Author: Peter Lavin, lavinp@scss.tcd.ie, May 2010 

----------------------------------------------------------------------------
'''

import os, commands, time
from os import sys



''' function to copy files to grid storage 
passed the name of the file as argument '''
def gStoreCopy(filename):
    print 'Attempting to copy ' + filename + ' to grid-storage'
    commands.getoutput('lcg-cr --vo gene file:' + filename + \
    ' -l lfn:/grid/gene/malaria/results/' + filename)
    cpShRetVal = commands.getoutput('echo $?')
    if cpShRetVal != '0':
        print '\nExiting for non-zero return from gStoreCopy for ' + \
        filename + '\n'
        sys.exit(1) 

''' methods to verify presence of copied files on grid storage
passed the name of the file as argument, boolean returned '''
def verifyCopy(filename):
    lsResult = commands.getoutput('lcg-ls lfn:/grid/gene/malaria/' + \
    'results/' + filename)
    verShRetVal = commands.getoutput('echo $?')
    if verShRetVal != '0':
        print '\nExiting for non-zero return from verifyCopy ' + \
        filename + '\n'
        sys.exit(1)

    if lsResult == 'lfn:/grid/gene/malaria/results/' + filename:
        print 'Presence verified on grid storage of ' + filename
        return True
    else:
        print 'Exiting, grid storage verification failed for ' + filename
        return False

def GetInHMS(sec):
    sec = int(sec)
    dd,  remainder = divmod(sec, 60*60*24)
    hh, remainder = divmod(remainder, 60*60)
    mm, seconds = divmod(remainder, 60)
    if dd == 0:
        return "%d hours %d mins " % (hh, mm)
    return "%d day(s) %d hours %d mins" % (dd, hh, mm)


print '\nScript pyehits.py starting at timestamp:  '
print commands.getoutput('date')
startJob = commands.getoutput('date -u +%s')

print 'Testing args, len is... ' + str(len(sys.argv))


''' Verifying list of args passed (from jdl file when in grid) '''
if len(sys.argv) == 5:
    print sys.argv[1] + ' ' + sys.argv[2] + ' ' + sys.argv[3] + \
    ' ' + sys.argv[4] 
else:
    print 'Wrong number of args, aborting NOW!'
    sys.exit(1)


''' Routine command line opertaions, useful for debug '''
print commands.getoutput('which python')
print commands.getoutput('python -V')
print commands.getoutput('/bin/hostname')
print '---------------------------\n'



''' Copies the binary file from the grid storage element (SE) '''
print commands.getoutput('lcg-cp --vo gene lfn:/grid/gene/malaria' +
'/ehits/' + sys.argv[1] + ' file:' + sys.argv[1])
shellRetVal = commands.getoutput('echo $?')
if shellRetVal != '0':
    print '\nExiting for non-zero return from fetching eHiTS binary\n'
    sys.exit(1)




'''Checks here for existance of the file copied, abort if not present '''
if os.path.exists(sys.argv[1]):
    print 'eHiTS binary now on WN, md5sum is...'
    print commands.getoutput('md5sum ' + sys.argv[1]) + '\n'
else:
    print 'eHiTS binary not found, aborting'
    sys.exit(1)


''' Comparing known good md5sum for binary file '''
if ('38cb94b59a383fc9967c0479e687a23d  eHiTS_2009.1_Cell.bin' \
== commands.getoutput('md5sum ' + sys.argv[1])):
    print 'md5 sums are the same...'
    print commands.getoutput('md5sum ' + sys.argv[1]) + '\n'
else:
    print 'md5 sums are different -this is BAD!!!'
    print commands.getoutput('ls -l ' + sys.argv[1])
    print commands.getoutput('ls -lh ' + sys.argv[1])
    print commands.getoutput('file ' + sys.argv[1])
    print commands.getoutput('md5sum ' + sys.argv[1])
    sys.exit(1)





''' Copies the ligand file from the grid storage element (SE) '''
print commands.getoutput('lcg-cp --vo gene lfn:/grid/gene/malaria/' + \
'ligands/' + sys.argv[3] + ' file:' + sys.argv[3])
shellRetVal = commands.getoutput('echo $?')
if shellRetVal != '0':
    print '\nExiting for non-zero return from fetching ligand file\n'
    sys.exit(1)




''' Checks for presence of downloaded ligand file, counts ligands
for debug Checks here for existance of the file copied, abort if not
present. '''
if os.path.exists(sys.argv[3]):
    print 'Ligand file found, ligand ($$$$) count is...'
    print commands.getoutput('cat ' + sys.argv[3]  + \
        ' | grep \$\$\$ | wc -l') + ' ligands\n'
else:
    print 'Required ligand file ' + sys.argv[3] + \
    ' not found, aborting'
    sys.exit(1)




''' Changes permissions to executable for the downloaded ehits
binary '''
print commands.getoutput('chmod 700 ' + sys.argv[1])


'''  Installs eHiTS from the binary (using an argument) '''
print commands.getoutput('./'+ sys.argv[1] + ' ./')


''' Running patch on ehits.sh script to set proxy at the top of,
top of file. NB this line and patch file is specific
to each version of eHiTS !!! BEWARE !!! '''
print '\nPrint of attempt to patch ehits.sh...\n' + \
commands.getoutput('patch < patch-ehits-proxy.patch ' + \
'eHiTS_2009.1/ehits.sh')


''' Printing md5 for patched ehits.sh file '''
print '\nmd5 of patched ehits.sh...\n' + \
commands.getoutput('md5sum eHiTS_2009.1/ehits.sh')


''' verifying one part of the patch changes '''
print '\nPrint to examine the SBS_PROXY settings in ehits.sh'
print commands.getoutput('cat eHiTS_2009.1/ehits.sh | ' \
'grep -n SBS_PROXY_NAME= ')


''' Print to examine proxy setting on grid WN '''
print '\nPrint of cmd... env | grep -i proxy for WN...\n'
print commands.getoutput('env | grep -i proxy')
print '\n'


''' Creating ehits.lic file in the binary install directory '''
commands.getoutput('echo kjshwe34ju > eHiTS_2009.1/ehits.lic')


''' Cat to verify license string is in place '''
print '\nPrint of ehits.lic after insertion...\n' + \
commands.getoutput('cat eHiTS_2009.1/ehits.lic ')


''' Print out of files now present on WN, may be useful for debug '''
print '\nPrinting contents of dir on WN...\n' + \
commands.getoutput('ls -l')
print '---------------------------'

ehits_command = './ehits.sh -receptor ' + sys.argv[2] + \
' -ligand ' + sys.argv[3] + ' -clip ' + sys.argv[4]  + \
' -workdir ./'

print '\nNow starting eHits with command line:\n\n' \
+ ehits_command +' \n'


''' Create a file for output of ehits command '''
commands.getoutput('touch ehOut.txt')
commands.getoutput(ehits_command + ' > ehOut.txt')

print commands.getoutput('cat ehOut.txt | head -n 16')
print '\n -- The above 16 and next 8 lines are the abridged ' + \
'eHiTS program output -- \n'
print commands.getoutput('cat ehOut.txt | tail -n 8')

print '\neHits has now ended:\n'




''' Running command to stop ehits (although already finished)
This is precautionary, aimed to clean up any remaining processes
still running after a crash, etc. '''
commands.getoutput('./stop_ehits.sh')




''' Trimming file extensions from args to create path to
best_scores.txt file '''
RecPath = sys.argv[2][:-4]
LigPath = sys.argv[3][:-4]


''' Use part of the filenames to make job specific 
best_scores.txt file '''
RecName = sys.argv[2][:-8]
LigName = sys.argv[3][:-7]


''' Make the file base name '''
filenameBase = RecName + '_' + LigName


''' Append the remainder bit
# Troubleshooting; these filenames should match the files
in the jdl file OutputSandbox '''
fullBestScoresFilename = filenameBase  + '_BS_ehps3.txt'
fullehitsBestFilename = filenameBase  + '_BP_ehps3.sdf'


''' For debug of naming of best_scores file '''
print 'Full Best Scores Filename is...\n' + fullBestScoresFilename
print '\nFull Best Poses Filename is...\n' + fullehitsBestFilename

''' Line count on the results file  '''
print '\n\nNumber of lines found in ORIGINAL best_scores.txt'
print 'in the eHiTS directory structure...'
print commands.getoutput('cat results/' + RecPath  +'/' + \
LigPath  + '/best_scores.txt | wc -l')
print '\n'

print '\nPrinting head of ORIGINAL best_scores.txt (3 lines)\n'
print commands.getoutput('cat results/' + RecPath  +'/' + \
LigPath  + '/best_scores.txt | head -n 3')
print '\n'


''' copies text from the eHiTS best_scores.txt to a file, plus the
best poses (sdf) file. These files have the same names as is
specified in the jdl file for this unique job. '''

commands.getoutput('cat results/' + RecPath  +'/' + LigPath  + \
'/best_scores.txt > ' + fullBestScoresFilename)
commands.getoutput('cat results/' + RecPath  +'/' + LigPath  + \
'/ehits_best.sdf > ' + fullehitsBestFilename)


''' Counting lines and cat-ing 3 lines from the result files  '''
print 'Result files should now be ready for copy to grid-storage.'


''' Line count on the result files ready for copy to storage  '''
print 'Number of lines found in ' + fullBestScoresFilename + ' ready to copy.'
print commands.getoutput('cat ' + fullBestScoresFilename  + ' | wc -l')
print '\n'

print '\nPrinting head of ' + fullBestScoresFilename + ' (3 lines)\n'
print commands.getoutput('cat ' + fullBestScoresFilename  + ' | head -n 3')
print '\n'


print 'Number of lines found in ' + fullehitsBestFilename 
print commands.getoutput('cat ' + fullehitsBestFilename + ' | wc -l')
print '\n'

print '\nPrinting head of ' + fullehitsBestFilename + ' (3 lines)\n'
print commands.getoutput('cat ' + fullehitsBestFilename + ' | head -n 3')
print '\n'



''' Copying the two results files out, then verifying success '''
gStoreCopy(fullBestScoresFilename)
gStoreCopy(fullehitsBestFilename)


''' Calls a function to verify the file is now on grid-storage '''
if not verifyCopy(fullBestScoresFilename):
    sys.exit(1)

if not verifyCopy(fullehitsBestFilename):
    sys.exit(1)


''' Setting the variable problemTarFile in case needed  '''
problemTarFile = filenameBase  + '_PROBLEM.tar'



''' Grep sim.out for ehits problem string
then get the error file for return to UI '''

''' Dealing with a problem reported by the ehits output  '''
problemTarFile = filenameBase  + '_PROBLEM.tar'
problem = commands.getoutput('cat ehOut.txt | ' + \
'grep -e "program finished with problems" | wc -l')
print '\n\n ***** Problem result is ' + problem + ' *****\n\n'
if problem == '1':
    commands.getoutput('touch ' + problemTarFile )
    commands.getoutput('tar cvf ' + problemTarFile + ' logs/')
    commands.getoutput('tar tvf ' + problemTarFile)
    ''' Calls a function to copy the filename
    passed to grid storage  '''
    gStoreCopy(problemTarFile)
    ''' Calls a function to verify the file is now on grid-storage '''
    if not verifyCopy(problemTarFile):
        sys.exit(1)
   


''' For debug of licence issues, prints some license data '''
print '\nGetting ls -l of license/ dir...\n'
print commands.getoutput('ls -l license/')
print '\nGetting cat of file in license/ dir...\n'
print commands.getoutput('cat license/eHiTS* | tail -n 5')

 

print '\nEnd of pyehits.py at timestamp: '
print commands.getoutput('date') + '\n'
endJob = commands.getoutput('date -u +%s')
duration = (int(endJob)-int(startJob))


''' Print out the time taken from beginning to end
of this script '''
print 'Job duration was ' + GetInHMS(duration) + '\n\n'


# END of file
