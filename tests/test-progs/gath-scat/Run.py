###################################################
#Script to run the gem5 with different parameters
#Author: shawnless.xie@gmail.com


import numpy as np
import matplotlib.pyplot as plt

import subprocess

###################################################
# Basic files needed 
gemRootDir  = "../../../"
configFile  = gemRootDir + "configs/example/se.py"
gemExeFile  = gemRootDir + "build/ARM/gem5.opt"


##################################################
# Cache related parameters.
# The default cache paramters

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
    cmdString = ['--caches']            +\
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
        @return: a list with three elments:
                 ('l1_icache', l1i_miss_rate)
                 ('l1_dcache', l1d_miss_rate)
                 ('l2_cache',  l2_miss_rate)
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


    return cacheStat

#################################################
# Plot the cache miss rates

def plotCacheMiss( cacheStat):
    """
    """
    assert( len(cacheStat) == 6 )

    l1i_miss=cacheStat['l1i_miss']/float(cacheStat['l1i_miss'] + cacheStat['l1i_hit']) 
    l1d_miss=cacheStat['l1d_miss']/float(cacheStat['l1d_miss'] + cacheStat['l1d_hit']) 
    l2_miss =cacheStat['l2_miss'] /float(cacheStat['l2_miss']  + cacheStat['l2_hit'] ) 

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

if __name__  == '__main__':
    binFile =  ["-c", "./helloworld"]

    runGem5(getCachePara(),binFile)

    cacheStat = getCacheStat("./m5out/stats.txt")

    plotCacheMiss( cacheStat );





