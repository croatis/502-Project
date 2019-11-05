import os
import sys

class TrafficLight:

    def __init__ (self, tlType, name, edges):
        self.tlType = tlType
        self.name = name
        self.edges = edges

    def getType(self):
        return self.tlType

    def getName(self):
        return self.name

    def getEdges(self):
        return self.edges

