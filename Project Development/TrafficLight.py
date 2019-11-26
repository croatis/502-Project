import os
import sys

class TrafficLight:

    global assignedIndividual

    def __init__ (self, name, lanes):
        self.name = name
        self.lanes = lanes
        self.edges = []
        self._setEdges(self.lanes)
        self.phases = 0
        self.carsWaiting = 0
        self.waitTime = 0

        # RETURNS THE TRAFFIC LIGHT'S NAME
    def getName(self):
        return self.name

        # RETURNS THE NUMBER OF LANES CONTROLLED BY THE TRAFFIC LIGHT
    def getLanes(self):
        return self.lanes

        # RETURNS THE NUMBER OF EDGES CONTROLLED BY THE TRAFFIC LIGHT
    def getEdges(self):
        return self.edges
        
        # SETS THE NUMBER OF EDGES CONTROLLED BY THE TRAFFIC LIGHT
    def _setEdges(self, lanes):
        # Determine edges from lanes
        for l in lanes:
            # Isolate edge name from lane name
            edge = l.split("_")
            
            # Ensure edge being added to list isn't a duplicate or retains "LTL" designation
            if edge[1] == "LTL":
                edgeName = edge[0] + "_LTL"
                if edgeName not in self.edges:
                    self.edges.append(edgeName)
            
            elif edge[0] not in self.edges:
                self.edges.append(edge[0])
            
            else:
                print("Unprocessable edge detected:", edge)

                
       
        # RETURNS THE PHASES AVAILBLE TO THE TRAFFIC LIGHT
    def getPhases(self):
        return self.phases
        
        # SETS THE PHASES AVAILBLE TO THE TRAFFIC LIGHT
    def setPhases(self, phases):
        self.phases = phases

        # RETURNS THE AGENT POOL OF THE TRAFFIC LIGHT
    def getAgentPool(self):
        return self.agentPool
        
        # ASSIGNS THE TRAFFIC LIGHT TO AN AGENT POOL
    def assignToAgentPool(self, agentPool):
        self.agentPool = agentPool

        # RETURNS THE RULE SET INDIVIDUAL CURRENTLY BEING USED BY THE TRAFFIC LIGHT FOR A SIM RUN
    def getAssignedIndividual(self):
        return self.assignedIndividual

        # ASSIGNS A RULE SET INDIVIDUAL CURRENTLY BEING USED BY THE TRAFFIC LIGHT FOR A SIM RUN
    def assignIndividual(self):
        self.assignedIndividual = self.agentPool.selectIndividual()
        self.assignedIndividual.selected() # Let Individual know it's been selected

        # RETURNS THE TOTAL NUMBER OF CARS WAITING AT THE TRAFFIC LIGHT'S INTERSECTION
    def getCarsWaitingCount(self):
        return self.carsWaiting
    
        # SETS THE TOTAL NUMBER OF CARS WAITING AT THE TRAFFIC LIGHT'S INTERSECTION
    def setCarsWaitingCount(self, carsWaiting):
        self.carsWaiting = carsWaiting

        # RETURNS THE TOTAL WAIT TIME OF CARS WAITING AT THE TRAFFIC LIGHT'S INTERSECTION
    def getWaitTime(self):
        return self.waitTime
    
        # SETS THE TOTAL WAIT TIME OF CARS WAITING AT THE TRAFFIC LIGHT'S INTERSECTION
    def setWaitTime(self, waitTime):
        self.waitTime = waitTime