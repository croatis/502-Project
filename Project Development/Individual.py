import os
import sys
from random import choice

class Individual:
    global epsilon = 0.5        # paramater between 0 and 1 used to determine importance of doing exploration (higher epsilon = more exploration)
    
        # INTIALIZE OBJECT VARIABLES
    def __init__(self, identifier, agentPool, ruleSet):
        self.id = identifier                    # AgentPool name
        self.ruleSet = ruleSet                  # Set of rules contained within individual
        self.selectedCount = 0                  # Number of times individual has been chosen during a training period                  
        self.agentPool = agentPool
        
    def getID(self):
        return self.id

    def getRuleSet(self):
        return self.ruleSet

        # RETURN A RULE BASED ON THEIR PROBABILITIES 
    def selectRule(self, validRules):
        ruleSets = subDivideValidRules(validRules)
        ruleSelectionList = []                      # A list of 100 valid rules. Number of times any one rule appears in list is relative to their probability of being selected 
            
            # Add a number of max weight rules to selection set relative to their probabilities
        for rule in ruleSets[0]:
            probability = int(getRuleProbabilityMax(rule)) * 100
            for i in range(probability + 1):
                ruleProbabilitiesList.append(rule)
        
            # Add a number of the rest of the rules to selection set relative to their probabilities
        for rule in ruleSets[1]:
            probability = int(getRuleProbabilityRest(rule)) * 100
            for i in range(probability + 1):
                ruleProbabilitiesList.append(rule)

        return random.choice(ruleSelectionList)


        # **** FLESH OUT TO RETURN A RULE ACCORDING TO EQUATIONS IN SHOUT AHEAD PAPER *********
    def selectRandomRule(self, validRules):
        return self.ruleSet[randrange(0, len(self.ruleSet))]    # Return a random rule

    def getSelectedCount(self):
        return self.selectedCount

    def selected(self):
        self.selectedCount += 1

    def getAgentPool(self):
        return self.agentPool

    def getRuleProbabilityMax(self, rule):
    
    def getRuleProbabilityRest(self, rule):
    
    def subDivideValidRules(self, validRules):
        rsMax = []
        ruleWeights = []

            # Add all the valid rule weights into a list to sort
        for rule in validRules:
            ruleWeights.append(rule.getWeight())
        
        ruleWeight.sort(reverse=True)   # Sort rule weights from highest to lowest

            # Add rules with highest weight into rsMax, and then remove them from primary list
        for rule in validRules:
            if rule.getWeight() == ruleWeight[0]:
                rsMax.append(rule)
                validRules.remove(rule)

        return (rsMax, validRules)       # Return the two rule sets (validRules now serves as rsRest)

        
