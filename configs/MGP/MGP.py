######################
# This is the script for MGP memory system simulation.
# Author: shawnless.xie@gmail.com


######################
import m5
from m5.objects import *
from MGPCaches	import *
#from caches	import *
from optparse	import OptionParser

######################
#Construct the Options
parser	= OptionParser()
parser.add_option('--l1i_size', help="L1 instruction cache size")
parser.add_option('--l1d_size', help="L1 data cache size")
parser.add_option('--l2_size',  help="Unified L2 cache size")

(options, args) = parser.parse_args()

#Create the system objects.
system= System()
system.clk_domain=SrcClockDomain()
system.clk_domain.clock='1GHz'
system.clk_domain.voltage_domain= VoltageDomain()

#the memory models
system.mem_mode 	= 'timing'
system.mem_ranges 	= [AddrRange('512MB')]

#the CPU parameters.
system.cpu		= TimingSimpleCPU()

# What is the mem bus type ?
system.membus		= SystemXBar()

#connect the cpu port directily to memory bus.
system.cpu.icache	=L1ICache(options)
system.cpu.dcache	=L1DCache(options)

system.cpu.icache.connectCPU(system.cpu)
system.cpu.dcache.connectCPU(system.cpu)

system.l2bus		=L2XBar()
system.cpu.icache.connectBus(system.l2bus)
system.cpu.dcache.connectBus(system.l2bus)

system.l2cache		=L2Cache(options)
system.l2cache.connectCPUSideBus(system.l2bus)
system.l2cache.connectMemSideBus(system.membus)

#Create the interrupt controller
system.cpu.createInterruptController()

#connect the system port, the backdoor port ?
system.system_port	=system.membus.slave

#connect the memory controller.
system.mem_ctrl		=DDR3_1600_x64()
system.mem_ctrl.range	=system.mem_ranges[0]
system.mem_ctrl.port	=system.membus.master



######################
#Create the process and workload
process			=LiveProcess()
process.cmd		=['tests/test-progs/hello/bin/ARM/linux/hello']
system.cpu.workload	=process
system.cpu.createThreads()

root			=Root(full_system=False,system=system)
m5.instantiate()

print	"Beginning simulation"
exit_event		=m5.simulate()

print	"Exiting @tic %i because %s" % (m5.curTick(), exit_event.getCause())


