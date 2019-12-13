import os
import sys
from numpy.random import choice

class Individual:
    global epsilon          # paramater between 0 and 1 used to determine importance of doing exploration (higher epsilon = more exploration)
    epsilon = 0.5      
    
        # INTIALIZE OBJECT VARIABLES
    def __init__(self, identifier, agentPool, ruleSet):
        self.id = identifier                    
        self.ruleSet = ruleSet                  # Set of rules contained within individual
        self.selectedCount = 0                  # Number of times individual has been chosen during a training period                  
        self.agentPool = agentPool              # AgentPool name
        self.fitness = 0
        self.lastRunTime = 2.2250738585072014e-308
        self.ruleWeightSum = 0

        # RETURN INDIVIDUAL IDENTIFIER
    def getID(self):
        return self.id

        # RETURN INDIVIDUAL'S RULE SET
    def getRuleSet(self):
        return self.ruleSet
    
        # INCREMENT selectedCount BY ONE FOR EVOLUTIONARY LEARNING PURPOSES
    def selected(self):
        self.selectedCount += 1

        # RESET selectedCount TO ZERO
    def resetSelectedCount(self):
        self.selectedCount = 0

        # RETURN selectedCount 
    def getSelectedCount(self):
        return self.selectedCount
    
    def getFitness(self):
        return self.fitness
    
    def updateFitness(self, fitness):
        self.fitness = fitness

    def getLastRunTime(self):
        return self.lastRunTime
    
    def updateLastRunTime(self, runtime):
        self.lastRunTime = runtime

        # RETURN SUM OF ALL WEIGHTS IN A RULE SET
    def getSumRuleWeights(self):        
        ruleSet = self.getRuleSet()    
        self.ruleWeightSum = sum(rule.getWeight() for rule in ruleSet)
        
        if self.ruleWeightSum == 0:
            self.ruleWeightSum = 2.2250738585072014e-308

        return self.ruleWeightSum

        # RETURN A RULE BASED ON THEIR PROBABILITIES 
    def selectRule(self, validRules):
        if len(validRules) == 0:
            return -1
        
        ruleSets = self.subDivideValidRules(validRules)

        if len(ruleSets[0]) > 0:  
            rules = []
            probabilities = []  
                # Add a number of max weight rules to selection set relative to their probabilities
            for rule in ruleSets[0]:
                probability = int(self.getRuleProbabilityMax(rule, ruleSets[0], ruleSets[1])) 
                print("Rule with conditions:", rule.getConditions(), "is in the MAX GROUP with probability", probability, "\n\n")
                rules.append(rule)
                probabilities.append(probability)
            
            for rule in ruleSets[1]:
                probability = int(self.getRuleProbabilityRest(rule, probabilities, ruleSets[1])) 
                print("Rule with conditions:", rule.getConditions(), "is in the REST GROUP with probability", probability, "\n\n")
                rules.append(rule)
                probabilities.append(probability)
        
        print("Probabilities have a sum of:", sum(probabilities))
        if sum(probabilities) == 0:
            for i in range(len(probabilities)):
                probabilities[i] = 1/len(probabilities)
            print("Probabilities have been edited and have a sum of:", sum(probabilities))
        rule = choice(rules, 1, p = probabilities)  # Returns a list (of size 1) of rules based on their probabilities
        return rule[0]
    
    #     # CODE PROVIDED BY DAVID (https://stackoverflow.com/users/53192/david)
    # def weighted_choice(self, items):
    #     """returns a function that fetches a random item from items

    #     items is a list of tuples in the form (item, weight)"""
    #     weight_total = sum((item[1] for item in items))
    #     def choice(uniform = random.uniform):
    #         n = uniform(0, weight_total)
    #         for item, weight in items:
    #             if n < weight:
    #                 return item
    #             n = n - weight
    #         return item
    #     return choice

        # RETURN A RANDOM RULE FROM INDIVIDUAL RULE SET
    def selectRandomRule(self, validRules):
        return self.ruleSet[randrange(0, len(self.ruleSet))]    # Return a random rule

        # RETURN AGENT POOL THE INDIVIDUAL BELONGS TO
    def getAgentPool(self):
        return self.agentPool

        # RETURN PROBABILITY OF SELECTION FOR A RULE IN rsMax
    def getRuleProbabilityMax(self, rule, rsMax, rsRest):
        weight = rule.getWeight()

        if len(rsRest) == 0:
            return 1/len(rsMax)
            
            # Avoid dividing by zero
        if weight == 0:
            weight = 2.2250738585072014e-308 

        return ((1-epsilon)*(weight/(weight*len(rsMax))))
    
        # RETURN PROBABILITY OF SELECTION FOR A RULE IN rsRest
    def getRuleProbabilityRest(self, rule, probabilities, rsRest):
        weight = rule.getWeight()
        sumOfWeights = self.getSumOfWeights(rsRest)
        
        # If sum of weights is 0, assign a weight based on the available probability left
        if sumOfWeights == 0:
            return (1-sum(probabilities))/len(rsRest)
        
        return epsilon*(weight/sumOfWeights)

        # RETURN SUM OF ALL WEIGHTS IN A RULE SET
    def getSumOfWeights(self, setOfRules):       
        return sum(rule.getWeight() for rule in setOfRules)

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
                print(rule, "has a weight of", rule.getWeight(), "and the highest weight is:", ruleWeights[0])
                rsMax.append(rule)
                validRules.remove(rule)

        print("RSMax contains:", rsMax, "\nRSRest contains:", validRules)
        return (rsMax, validRules)       # Return the two rule sets (validRules now serves as rsRest)

        
