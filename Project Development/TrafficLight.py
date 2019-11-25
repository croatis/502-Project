import os
import sys

class TrafficLight:

    global assignedIndividual

    def __init__ (self, name, lanes):
        self.name = name
        self.lanes = lanes
        # self.numofPhases = numOfPhases
        self.edges = []
        self._setEdges(self.lanes)
        self.phases = 0


    def getType(self):
        return self.tlType

    def getName(self):
        return self.name

    def getLanes(self):
        return self.lanes

    def getEdges(self):
        return self.edges
    
    def _setEdges(self, lanes):
        # Determine edges from lanes
        for l in lanes:
            # Isolate edge name from lane name
            edge = l.split("_")
            
            # Ensure edge being added to list isn't a duplicate 
            if edge[0] in self.edges:
                continue
            else:
                self.edges.append(edge[0])

    def getPhases(self):
        return self.phases
    
    def setPhases(self, phases):
        self.phases = phases

    def getAgentPool(self):
        return self.agentPool
    
    def assignToAgentPool(self, agentPool):
        self.agentPool = agentPool

    def getAssignedIndividual(self):
        return self.assignedIndividual
    
    def assignIndividual(self):
        assignedIndividual = self.agentPool.selectIndividual()
        

