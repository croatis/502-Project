import os
import sys

class Rule:

    def __init__(self, conditions, action):
        self.conditions = conditions
        self.action = action
    
    def getConditions(self):
        return self.conditions

    def getAction(self):
        return self.action