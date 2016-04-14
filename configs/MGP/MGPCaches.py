#########################
#The caches derived from Basecaches.
from m5.objects import Cache
from m5.objects import NMRU

class L1Cache(Cache):
    assoc           =2
    hit_latency     =2
    response_latency=2
    mshrs           =4
    tgts_per_mshr   =20
    #is_top_level	=True

    ###################
    def __init__(self, options=None):
        super(L1Cache, self).__init__()
        pass

    def connectCPU(self, cpu):
        #need to define this in a derived class
        raise NoImplementedError

    def connectBus(self, bus):
        self.mem_side	= bus.slave


class L1ICache(L1Cache):
    size        ='16kB'

    ##################
    def __init__(self, options=None):
        super(L1ICache, self).__init__(options)

        if options and options.l1i_size:
            self.size	=options.l1i_size

    def connectCPU(self, cpu):
        self.cpu_side	=cpu.icache_port

class L1DCache(L1Cache):

    size        ='64kB'
    tags        =NMRU()

    def __init__(self, options=None):
        super(L1DCache, self).__init__(options)

        if options and options.l1d_size:
            self.size	=options.l1d_size

    def connectCPU(self, cpu):
        self.cpu_side	=cpu.dcache_port

class L2Cache(Cache):
    size            ='256kB'
    assoc           =8
    hit_latency     =20
    response_latency=20
    mshrs           =20
    tgts_per_mshr   =12

    #####################
    def __init__(self, options=None):
        super(L2Cache, self).__init__()

        if options and options.l2_size:
            self.size	= options.l2_size

    def connectCPUSideBus(self, bus):
        self.cpu_side	=bus.master

    def connectMemSideBus(self, bus):
        self.mem_side	=bus.slave
