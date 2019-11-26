import os
import sys
from random import randrange

class Individual:
    
        # Intialize object variables
    def __init__(self, identifier, ruleSet):
        self.id = identifier                    # AgentPool name
        self.ruleSet = ruleSet                  # Set of rules contained within individual
        self.selectedCount = 0                  # Number of times individual has been chosen during a training period                  

    def getID(self):
        return self.id

    def getRuleSet(self):
        return self.ruleSet

        # **** FLESH OUT TO RETURN A RULE ACCORDING TO EQUATIONS IN SHOUT AHEAD PAPER *********
    def selectRule(self):
        return self.ruleSet[randrange(0, len(self.ruleSet))]    # Return a random rule


    def getSelectedCount(self):
        return self.selectedCount

    def selected(self):
        self.selectedCount += 1
