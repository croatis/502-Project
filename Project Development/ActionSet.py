import os
import sys
from random import randrange

class ActionSet:

    def __init__(agentPool, numOfActions):
        self.agentPool = agentPool
        self.actionSet = numOfActions
    
    def getAgentPoolName():
        return self.agentPool
        
    def getRandomAction():
        return randrange(self.actionSet)