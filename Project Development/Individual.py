import os
import sys
import random

class Individual:
    global epsilon          # paramater between 0 and 1 used to determine importance of doing exploration (higher epsilon = more exploration)
    global minProbability   # minimum probability a rule can have for being selected
    epsilon = 0.5      
    minProbability = 1  
    
        # INTIALIZE OBJECT VARIABLES
    def __init__(self, identifier, agentPool, ruleSet):
        self.id = identifier                    # AgentPool name
        self.ruleSet = ruleSet                  # Set of rules contained within individual
        self.selectedCount = 0                  # Number of times individual has been chosen during a training period                  
        self.agentPool = agentPool
        
        # RETURN INDIVIDUAL IDENTIFIER
    def getID(self):
        return self.id

        # RETURN INDIVIDUAL'S RULE SET
    def getRuleSet(self):
        return self.ruleSet
    
        # INCREMENT selectedCount BY ONE FOR EVOLUTIONARY LEARNING PURPOSES
    def selected(self):
        self.selectedCount += 1
        
        # RETURN selectedCount 
    def getSelectedCount(self):
        return self.selectedCount

        # RETURN A RULE BASED ON THEIR PROBABILITIES 
    def selectRule(self, validRules):
        if len(validRules) == 0:
            return -1
        
        ruleSets = self.subDivideValidRules(validRules)
        ruleSelectionList = []                      # A list of valid rules. Number of times any one rule appears in list is relative to their probability of being selected 

        if len(ruleSets[0]) > 0:    
                # Add a number of max weight rules to selection set relative to their probabilities
            for rule in ruleSets[0]:
                probability = int(self.getRuleProbabilityMax(rule, ruleSets[0])) * 100
                print("Rule with conditions:", rule.getConditions(), "is in the MAX GROUP with probability", probability, "\n\n")
                for i in range(probability + 1):
                    ruleSelectionList.append(rule)
        
        if len(ruleSets[1]) > 0:    
                # Add a number of the rest of the rules to selection set relative to their probabilities
            for rule in ruleSets[1]:
                probability = int(self.getRuleProbabilityRest(rule, ruleSets[1])) * 100
                print("Rule with conditions:", rule.getConditions(), "is in the REST GROUP with probability", probability, "\n\n")
                for i in range(probability + 1):
                    ruleSelectionList.append(rule)

        print("The rule selection list has", len(ruleSelectionList), "rules in it!")
        return random.choice(ruleSelectionList)

        # RETURN A RANDOM RULE FROM INDIVIDUAL RULE SET
    def selectRandomRule(self, validRules):
        return self.ruleSet[randrange(0, len(self.ruleSet))]    # Return a random rule

        # RETURN AGENT POOL THE INDIVIDUAL BELONGS TO
    def getAgentPool(self):
        return self.agentPool

        # RETURN PROBABILITY OF SELECTION FOR A RULE IN rsMax
    def getRuleProbabilityMax(self, rule, rsMax):
        weight = rule.getWeight()
        
            #Set weight to smallest number in Python to avoid dividing by 0
        if weight == 0:
            weight = 2.2250738585072014e-308

        return max(minProbability, ((1-epsilon)*(weight/(weight*len(rsMax)))))
    
        # RETURN PROBABILITY OF SELECTION FOR A RULE IN rsRest
    def getRuleProbabilityRest(self, rule, rsRest):
        weight = rule.getWeight()
        
        #Set weight to smallest number in Python to avoid dividing by 0
        if weight == 0:
            weight = 2.2250738585072014e-308
        
        return max(minProbability, (epsilon*(weight/self.getSumOfWeights(rsRest))))

        # RETURN SUM OF ALL WEIGHTS IN A RULE SET
    def getSumOfWeights(self, setOfRules):
        weightSum = 0
            
            # Sum the weights of all the rules in the set
        for rule in setOfRules:
            weightSum += rule.getWeight()
        
        if weightSum == 0:
            weightSum = 2.2250738585072014e-308

        return weightSum

        # SEPERATE RULES INTO rsMax AND rsRest 
    def subDivideValidRules(self, validRules):
        rsMax = []
        ruleWeights = []

            # Add all the valid rule weights into a list to sort
        for rule in validRules:
            ruleWeights.append(rule.getWeight())
        
        ruleWeights.sort(reverse=True)   # Sort rule weights from highest to lowest

            # Add rules with highest weight into rsMax, and then remove them from primary list
        for rule in validRules:
            if rule.getWeight() == ruleWeights[0]:
                rsMax.append(rule)
                validRules.remove(rule)

        return (rsMax, validRules)       # Return the two rule sets (validRules now serves as rsRest)

        
