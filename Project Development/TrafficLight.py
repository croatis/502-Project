import os
import sys

class TrafficLight:

    def __init__ (self, tlType, name, lanes):
        self.tlType = tlType
        self.name = name
        self.lanes = lanes
        self.edges = []
        self._setEdges(self.lanes)


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



