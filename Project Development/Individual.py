import os
import sys
from numpy.random import choice

class Individual:
    global epsilon          # paramater between 0 and 1 used to determine importance of doing exploration (higher epsilon = more exploration)
    epsilon = 0.5      
    global fitness

        # INTIALIZE OBJECT VARIABLES
    def __init__(self, identifier, agentPool, RS, RSint):
        self.id = identifier                    
        self.RS = RS                  # Set of rules without observations of communicated intentions
        self.RSint = RSint                    # Set of rules with observations of communicated intentions
        self.selectedCount = 0                  # Number of times individual has been chosen during a training period                  
        self.agentPool = agentPool              # AgentPool name
        self.fitness = 0
        self.lastRunTime = 2.2250738585072014e-308
        self.ruleWeightSum = 0

        # RETURN INDIVIDUAL IDENTIFIER
    def getID(self):
        return self.id

        # RETURN INDIVIDUAL'S RULE SET
    def getRS(self):
        return self.RS

        # RETURN INDIVIDUAL'S RULE SET
    def getRSint(self):
        return self.RSint
    
        # INCREMENT selectedCount BY ONE FOR EVOLUTIONARY LEARNING PURPOSES
    def selected(self):
        self.selectedCount += 1

        # RESET selectedCount TO ZERO
    def resetSelectedCount(self):
        self.selectedCount = 0

        # RETURN selectedCount 
    def getSelectedCount(self):
        return self.selectedCount
    
        # RETURN INDIVIDUAL'S FITNESS SCORE
    def getFitness(self):
        return self.fitness
        
        # UPDATE INDIVIDUAL'S FITNESS SCORE
    def updateFitness(self, fitness):
        self.fitness += fitness
        
        # RESET INDIVIDUAL'S FITNESS SCORE FOR EACH NEW GENERATION
    def resetFitness(self):
        self.fitness = 0

        # RETURN THE LENGTH OF THE LAST RUN THE INDIVIDUAL PARTICIPATED IN
    def getLastRunTime(self):
        return self.lastRunTime

        # UPDATE THE LENGTH OF THE LAST RUN THE INDIVIDUAL PARTICIPATED IN
    def updateLastRunTime(self, runtime):
        self.lastRunTime = runtime

        # RETURN SUM OF ALL WEIGHTS IN A RULE SET
    def getSumRuleWeights(self):        
        ruleSet = self.getRS()    
        self.ruleWeightSum = sum(rule.getWeight() for rule in ruleSet)
        
        if self.ruleWeightSum == 0:
            self.ruleWeightSum = 2.2250738585072014e-308

        return self.ruleWeightSum

        # RETURN A RULE FROM RS BASED ON THEIR PROBABILITIES 
    def selectRule(self, validRules):
        if len(validRules) == 0:
            return -1
        
        ruleSets = self.subDivideValidRules(validRules)
        rules = []
        probabilities = []  
        
        print("Valid rule sets contain:", ruleSets)

            # Add a number of max weight rules to selection set relative to their probabilities
        for rule in ruleSets[0]:
            probability = self.getRuleProbabilityMax(rule, ruleSets[0], ruleSets[1])
            rules.append(rule)
            probabilities.append(probability)

            #If rsRest contains elements too, calculate their probabilities
        if len(ruleSets[1]) > 0:  
                # Acquire sum of weights in rsRest
            sumOfWeights = self.getSumOfWeights(ruleSets[1])
            
            # If sum of weights is 0, assign a weight based on the available probability left
            if sumOfWeights == 0:
                print("Sum of weights is 0")
                probability = (1-sum(probabilities))/len(ruleSets[1])
                    
                    # If sum of weights is 0, assign equal part of the remaining probability to each rule
                for rule in ruleSets[1]:
                    rules.append(rule)
                    probabilities.append(probability)
            else:
                    # If sum of weights is NOT 0, individually calculate probabilities 
                for rule in ruleSets[1]:
                    probability = self.getRuleProbabilityRest(rule, probabilities, sumOfWeights, ruleSets[1])
                    rules.append(rule)
                    probabilities.append(probability)

        # print("Probabilities have a sum of:", sum(probabilities))
        if sum(probabilities) == 0:
            for i in range(len(probabilities)):
                probabilities[i] = 1/len(probabilities)
            # print("Probabilities have been edited and have a sum of:", sum(probabilities))
        for rule in rules:
            print(rule, "has a weight of", rule.getWeight())
        print("Prob set contains", probabilities)
        print("Rule set contains", rules)
        rule = choice(rules, 1, p = probabilities)  # Returns a list (of size 1) of rules based on their probabilities
        
        print("Rule chosen is", rule[0])
        return rule[0]  # Choice function returns an array, so we take the only element in it
            
        # RETURN A RULE FROM RSint BASED ON THEIR PROBABILITIES 
    def selectCoopRule(self, validRules):
        if len(validRules) == 0:
            return -1
        
        ruleSets = self.subDivideValidRules(validRules)

        if len(ruleSets[0]) > 0:  
            rules = []
            probabilities = []  
                # Add a number of max weight rules to selection set relative to their probabilities
            for rule in ruleSets[0]:
                probability = int(self.getRuleProbabilityMax(rule, ruleSets[0], ruleSets[1])) 
                # print("Rule with conditions:", rule.getConditions(), "is in the MAX GROUP with probability", probability, "\n\n")
                rules.append(rule)
                probabilities.append(probability)
            
            #If rsRest contains elements too, calculate their probabilities
        if len(ruleSets[1]) > 0:  
                # Acquire sum of weights in rsRest
            sumOfWeights = self.getSumOfWeights(ruleSets[1])
            
            # If sum of weights is 0, assign a weight based on the available probability left
            if sumOfWeights == 0:
                print("Sum of weights is 0")
                probability = (1-sum(probabilities))/len(ruleSets[1])
                    
                    # If sum of weights is 0, assign equal part of the remaining probability to each rule
                for rule in ruleSets[1]:
                    rules.append(rule)
                    probabilities.append(probability)
            else:
                    # If sum of weights is NOT 0, individually calculate probabilities 
                for rule in ruleSets[1]:
                    probability = self.getRuleProbabilityRest(rule, probabilities, sumOfWeights, ruleSets[1])
                    rules.append(rule)
                    probabilities.append(probability)
        
        # print("Probabilities have a sum of:", sum(probabilities))
        if sum(probabilities) == 0:
            for i in range(len(probabilities)):
                probabilities[i] = 1/len(probabilities)
            # print("Probabilities have been edited and have a sum of:", sum(probabilities))
        rule = choice(rules, 1, p = probabilities)  # Returns a list (of size 1) of rules based on their probabilities
        
        return rule[0]  # Choice function returns an array, so we take the only element in it

        # RETURN A RANDOM RULE FROM RS
    def selectRandomRule(self, validRules):
        return self.RS[randrange(0, len(self.ruleSet))]    # Return a random rule

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
    def getRuleProbabilityRest(self, rule, probabilities, sumOfWeights, rsRest):
        weight = rule.getWeight()
        
        print("Rule with weight", rule.getWeight(), "has a probability of", epsilon*(weight/sumOfWeights))
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
                # print(rule, "has a weight of", rule.getWeight(), "and the highest weight is:", ruleWeights[0])
                rsMax.append(rule)
                validRules.remove(rule)

        # print("RSMax contains:", rsMax, "\nRSRest contains:", validRules)
        return (rsMax, validRules)       # Return the two rule sets (validRules now serves as rsRest)

        
