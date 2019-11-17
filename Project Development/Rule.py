import os
import sys

class Rule:

    def __init__(self, conditions, action, agentPool):
        self._conditions = conditions
        self._action = action
        self._agentPool = agentPool

    def getConditions(self):
        return self._conditions
    
    def setConditions(self, conditions):
        self._conditions = conditions

    def getAction(self):
        return self._action

    def setAction(self, action):
        self._action = action
    
    def getAgentPool(self):
        return self._agentPool

    def setAgentPool(self, agentPool):
        self._agentPool = agentPool
    