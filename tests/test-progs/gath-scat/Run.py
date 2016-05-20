#!/usr/local/bin/python
###################################################
#Script to run the gem5 with different parameters
#Author: shawnless.xie@gmail.com

import matplotlib.pyplot as plt
import numpy as np
import subprocess
import sys
###################################################
# Basic files needed
gemRootDir  = "../../../"
configFile  = gemRootDir + "configs/example/se.py"
gemExeFile  = gemRootDir + "build/ARM/gem5.opt"


##################################################
# Cache related parameters.
# The default cache paramters

cpu_type   = 'detailed'
cacheline_size      = '64'

l1i_size   = '32kB'
l1i_assoc  = '2'
l1d_size   = '32kB'
l1d_assoc  = '2'

l2_size    = '512kB'
l2_assoc   = '2'

def getCachePara():
    """set the cache parameters'command string for gem5
    """
    cmdString = ['--cpu-type='          +cpu_type]+\
                ['--caches']            +\
                ['--ruby']              +\
                ['--cacheline_size='    +cacheline_size]  +\
                ['--l1i_size='          +l1i_size] +\
                ['--l1i_assoc='         +l1i_assoc] +\
                ['--l1d_size='          +l1d_size] +\
                ['--l1d_assoc='         +l1d_assoc] +\
                ['--l2_size='           +l1d_size] +\
                ['--l2_assoc='          +l2_assoc]

    return cmdString



##################################################
#

def runGem5(configOpt,binFile):
    """ Call the Gem5 executables "
        @configOpt: the options for the configuation
                script
        @binFile: a list of bin files  with
                coresspoding arguments to the gem5.
        @return: the return code of the gem5
    """
    Cmd = [gemExeFile, configFile] + configOpt +  binFile;

    try:
        print "===>   Running gem5 with '%s'"% (" ").join(Cmd)
        return subprocess.check_output( Cmd, stderr=subprocess.STDOUT )

    except subprocess.CalledProcessError as err:
        print "=================================="
        print "Error !!!!!!"
        print err.output
##################################################
# Get the cache statistics

def getCacheStat(statFile):
    """ read the static file and get the hit/miss
        rate of the caches.
        @statFile: full file name of the gem5 output
        @return: a list with desired:
    """
    print "===>   Readting statistics from '%s'"%statFile
    cacheStat=dict()
    for line in open(statFile).readlines():
        if "L1Dcache.demand_hits"  in line:
            cacheStat['l1d_hit'] = int( line.split()[1] );
        elif "L1Dcache.demand_misses"  in line:
            cacheStat['l1d_miss'] =int( line.split()[1] );
        elif "L1Icache.demand_hits"  in line:
            cacheStat['l1i_hit'] = int( line.split()[1] );
        elif "L1Icache.demand_misses"  in line:
            cacheStat['l1i_miss'] = int( line.split()[1] );
        elif "L2cache.demand_hits"  in line:
            cacheStat['l2_hit'] = int( line.split()[1] );
        elif "L2cache.demand_misses"  in line:
            cacheStat['l2_miss'] = int( line.split()[1] );
        elif "sim_ticks"              in line:
            cacheStat['time(ns)'] = float( line.split()[1] )/1000000.0;
        elif "swp_count"              in line:
            cacheStat['swp_count'] = int( line.split()[1] )


    return cacheStat

#################################################
# Plot the cache miss rates

def plotCacheMiss( cacheStat):
    """
    """
    assert( len(cacheStat) == 6 )

    l1i_miss=cacheStat['l1i_miss']/ \
             float(cacheStat['l1i_miss'] + cacheStat['l1i_hit'])
    l1d_miss=cacheStat['l1d_miss']/ \
             float(cacheStat['l1d_miss'] + cacheStat['l1d_hit'])
    l2_miss =cacheStat['l2_miss'] / \
             float(cacheStat['l2_miss']  + cacheStat['l2_hit'] )

    xLabels =['L1 I Cache','L1 D Cache','L2 Cache']
    xN      =range(3)
    yValues =[l1i_miss, l1d_miss, l2_miss];

    # get the current figure and axes
    fig, ax= plt.subplots()

    # plot the bar figure and set the label
    plt.bar(xN, yValues, align='center')
    plt.xticks(xN, xLabels)

    plt.title('The miss rate for the three caches')

    plt.ylabel('miss rate')
    ax.set_ylim([0.0, 1.0])

    # Add the lables
    for i, v in enumerate(yValues):
        ax.text(i, v + 0.025, "%.2f"%v , color='blue', fontweight='bold')

    # show the figure
    plt.show()

##############################
# The help funciton 
def Help():
    print "Run.py binfile"
    exit(1);

##############################
# Print the statistics
def printStat( statDict ):

    (binFile, cacheStat) =  statDict.items()[0];
    row_format='{:<12}'*( len(cacheStat) + 1 )
    print  row_format.format("",  *cacheStat.keys() )
    print  "="*80

    #Value seperated by comma
    for (binFile, cacheStat) in statDict.items():
        Val = [ "{:,}".format(v) for v in cacheStat.values() ]
        print  row_format.format(binFile[:-4], *Val) 

if __name__  == '__main__':

    if len(sys.argv) < 2:
        Help()


    statDict = dict()

    for binFile in sys.argv[1:]:
        binCmd =  ["-c", binFile ]

        runGem5(getCachePara(), binCmd)

        statDict[ binFile ] =  getCacheStat("./m5out/stats.txt")


    printStat( statDict )

    #plotCacheMiss( cacheStat );





