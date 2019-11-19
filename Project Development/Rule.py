import os
import sys

class Rule:

    def __init__(self, conditions, action, agentPool):
        self.conditions = conditions
        self.action = action
        self.agentPool = agentPool

    def getConditions(self):
        return self.conditions
    
    def setConditions(self, conditions):
        self._conditions = conditions

    def getAction(self):
        return self.action

    def setAction(self, action):
        self._action = action
    
    def getAgentPool(self):
        return self._agentPool

    def setAgentPool(self, agentPool):
        self.agentPool = agentPool
    