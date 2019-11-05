import os
import sys

class TrafficLight:

    def __init__ (self, tlType, name, lanes):
        self.tlType = tlType
        self.name = name
        self.lanes = lanes

    def getType(self):
        return self.tlType

    def getName(self):
        return self.name

    def getLanes(self):
        return self.lanes

