class datacenter:

    def __init__(self, nr, ncpus):
        self.nr = nr
        self.ncpus = ncpus

    def createRacks(self):
        ''' create racks and number of cpus defined through the class constructor  '''
        import numpy as np
        self.rackarray = np.arange(self.nr)
        self.cpuarray = np.arange(self.ncpus)
        self.racks = ['r'+str(self.rackarray[i]) for i in self.rackarray]
        self.cpus = ['p'+str(self.cpuarray[i]) for i in self.cpuarray]
        print(f'{len(self.cpus)} cpus for {self.nr} racks were created successfully!')
        return {'racks': self.racks, 'cpus': self.cpus}

    def allocateCpus(self, rkscpus, *kwargs):
        ''' supported only ordered methods for kwargs '''
        import numpy as np
        if 'ordered' in list(kwargs):
            nrks = len(self.racks)
            
            rkscpus = {}
            for k, v in zip(self.racks, np.array_split(self.cpus, nrks)):
                rkscpus[k] = v

            return rkscpus
            
    def simulateBlocks(self, blks):
        ''' creates {blks} number of blocks for given number of racks and cups '''
        blocks = len(self.cpus)//blks
        rem = len(self.cpus)%blks
        total = blocks + rem
        self.tblocks = ['b'+str(i) for i in range(total)]
        return self.tblocks
        
    def allocateCpusToBlocks(self):
        ''' allocates data to blocks '''
        import numpy as np
        self.bcpus = {}
        for k, v in zip(self.tblocks, np.array_split(self.cpus, len(self.tblocks))):
            self.bcpus[k] = v
        return self.bcpus
    
    def simulateData(self, nb, *kwargs):
        self.nb = nb
        ''' creates data in (supports only gbs) '''
        if 'gb' in kwargs:
            self.data = nb * (10**9)
            print(f'Created {self.nb} gigs of data')
            return self.data

    def allocateData(self, data):
        ''' allocates data to blocks '''
        import numpy as np

        self.blockbychunk = {}
        for k, v in zip(self.bcpus.keys(), self.bcpus.values()):
            self.blockbychunk[k] = data/len(v)

        self.databycpus = {}
        for k, v in zip(self.bcpus.values(), self.blockbychunk.values()):
            for i in k:
                self.databycpus[i] = v
                
        out = {'blocks by cpus':self.bcpus, 'data chunks per processor': self.databycpus}
        return out

    def printBlocksByProcessors(self, config):
        ''' prints blocks by cps '''

        for i in config['blocks by cpus'].items():
            print(i)

    def printProcessorsByChunks(self, config):
        ''' prints blocks by cps '''

        for i in config['data chunks per processor'].items():
            print(i)
    
    def totalDataCenterSize(self, config):
        ''' calculates data center capacity by memory size '''
        total = 0

        for i in config['data chunks per processor'].values():
            total += i
        print(f'The total memory required for data center is {len(self.bcpus.keys())} blocks times {len(self.cpus)} processors')
        return total * 10**(-9)

class rackawareness(datacenter):

    def __init__(self, nr, ncpus):
        datacenter.__init__(self, nr, ncpus)

    def establishRA(self, data, nb):

        import time
        
        self.nb = nb
        
        rkscpus = self.createRacks()
        alloc = self.allocateCpus(rkscpus, 'ordered')
        blocks = self.simulateBlocks(nb)
        self.allocateCpusToBlocks()
        data = self.simulateData(data, 'gb')
        self.config = self.allocateData(data)
        print('Trying to aware ...')
        time.sleep(1)
        print("Established awareness! Try 'print(config)' to know rack-awareness")
        return self.config

    def reConfigureDC(self, punchP):

        import time
        import numpy as np
        
        self.punchP = punchP
        
        print(f"do you like to punch '{self.punchP}'? Y/N")
        i = input()
        if i in ('y', 'Y'):
            print('Trying to reconfigure data center. Please wait ...')

        time.sleep(1)
        
        if self.punchP in self.config['data chunks per processor'].keys():
            print("Found the processor")

            
    def safeFailOver(self):
        ''' identifies proper device and remakes the blk '''

        import numpy as np
        import time
        
        procvalue = self.config['data chunks per processor'][self.punchP]

        self.availableprocs = []

        for k, v in self.config['data chunks per processor'].items():
            if k != self.punchP and v == procvalue:
                self.availableprocs.append(k)

        print(f'Found below procs suitable for {self.punchP}')
        
        for k in self.availableprocs:
            print(k)

        self.suitableproc = np.random.choice(self.availableprocs, 1)
        time.sleep(1)

        print(f'The suitable proc for {self.punchP} is found to be {self.suitableproc}')

        print('Trying to reconfigure the block...')

        time.sleep(1)
        
        self.block = {}

        for k, v in self.bcpus.items():
            for i in v:
                if i == self.punchP:
                    v = v.tolist()
                    v.remove(i)
                    v.append(self.suitableproc)
                    self.block[k] = v
                    
        return self.block       

    def faultTolerance(self):
        ''' calculates fault-tolerance '''
        value = 0
        for k1, v1 in self.config['data chunks per processor'].items():
            for k2, v2 in self.block.items():
                for i in v2:
                    if k1 == i:
                        value += v1
        fault_t = 1 - (value/self.data)
        return fault_t
                
##
##if __name__ == '__main__':
##    dc = datacenter(2, 10)
##    rkscpus = dc.createRacks()
##    alloc = dc.allocateCpus(rkscpus, 'ordered')
##    
##    blocks = dc.simulateBlocks(3)
##    dc.allocateCpusToBlocks()
##    data = dc.simulateData(5, 'gb')
##    config = dc.allocateData(data)
####    print(config) 
####    ra.printBlocksByProcessors(config)
####    ra.printProcessorsByChunks(config)
####    dc.totalDataCenterSize(config)
##
##    ra = rackawareness(2, 10)
##    config = ra.establishRA(5, 3)
##    ra.reConfigureDC('p8')
##    block = ra.safeFailOver()
##    print(ra.faultTolerance())
##    
##    
