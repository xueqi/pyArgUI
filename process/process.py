'''
Created on May 12, 2017

@author: xueqi
'''

class Process(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        self.pid = None
        self.terminate = None
        self.status = "WAIT"
    

class ProcessManager(object):
    def __init__(self):
        self.processes = []
    
    def addProcess(self, p):
        self.processes.append(p)
    
    def deleteProcess(self, p):
        self.processes.remove(p)
    
    def deleteProcessByPid(self, pid):
        for p in range(len(self.processes) - 1, -1, -1):
            if p.pid == pid:
                self.processes.remove(p)

    def terminate(self, p):
        p.terminate()
    

