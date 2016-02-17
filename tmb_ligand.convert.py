#! usr/bin/env python
# Aug 23
# Code is written only to hanlde sdf files with 2 mols, ie the for i in range(0,2) loop over file.
# would need to count mols ($$$$) in file.
import os, sys
from os import chdir, listdir, path
                                                                                                                     
sourcepath = '/home/lavinp/fightmalaria/ligand_files/smi_2blks/'
destpath = '/home/lavinp/fightmalaria/ligand_files/smi_tmb_2blks/'
                                                                                                                     
sourcelist = listdir(sourcepath)
                                                                                                                     
for entry in sourcelist:
        infile = sourcepath + entry
        outfile = destpath + entry[:-4] + '.tmb'
        print infile, outfile, 'conversion'
                                                                                                                     
        if os.path.exists(destpath + outfile) == True:
                print ' ----------- Removing existing ', outfile
                os.system('rm ' + destdir + outfile)
                                                                                                                     
        os.system('touch ' + outfile)
        for i in range(0,2):
                os.system('/home/lavinp/fightmalaria/ehits_install/eHiTS_6.2/Linux/bin/convert ' + infile + ' ligand_' + str(i) + '.tmb -mol ' + str(i) + ' -config /home/lavinp/fightmalaria/ehits_install/eHiTS_6.2/data/parameters.cfg')
                print 'cat ligand_' + str(i) + '.tmb >> ' + outfile
                os.system('cat ligand_' + str(i) + '.tmb >> ' + outfile)
        os.system('rm ligand_0.tmb')
        os.system('rm ligand_1.tmb')
                                                                                                                     

