import os
import sys
import PredicateSet as PredicateSet
from Rule import Rule
from Individual import Individual
from random import randrange
from random import randint

    #  EVOLUTIONARY LEARNER ALGORITHM
# class EvolutionaryLearner:
    
    # How many of the top individuals to breed for new generation
global maxIndexToBreed
global maxChildrenToMutate
maxIndexToBreed = 6   
maxChildrenToMutate = 5

    # Specifications for making Individuals and Rules
global maxRulePredicates
global maxRules
global maxIndividuals

maxRulePredicates = 3
maxRules = 10
maxIndividuals = 5

    # How much runtime and rule weights matter when determining fitness of a simulation run
global runtimeFactor        
global ruleWeightFactor

runtimeFactor = 1
ruleWeightFactor = 1
    
    # FITNESS FUNCTION FOR AN INDIVIDUAL AFTER ONE SIMULATION RUN/EPISODE
def rFit(simTime, individual):
    ruleWeights = getSumRuleWeights(individual)
    rFit = runtimeFactor*(1/simTime) + ruleWeightFactor*(1-(1/ruleWeights))

    return rFit

    # FITNESS FUNCTION FOR ONE GENERATION
def fit(simTime, agentPools):
    ruleWeights = getSumRuleWeightsAP(agentPools)
    fit = runtimeFactor*(1/simTime) + ruleWeightFactor*(1-(1/ruleWeights))

    return fit

    # Creates new generation after a simulation run
def createNewGeneration(agentPools):
    for ap in agentPools:
        individuals = ap.getIndividualsSet()
        individuals.sort(key=lambda, x: x.getFitness(), reverse = True)

        newGenPool = [individuals[0], individuals[maxIndexToBreed]]
        children = []
            # Create children 
        for i in newGenPool:
            for partner in newGenPool:
                if i != partner:
                    children.append(crossover(i, partner))
            
            # Randomly mutate a random number of the children
        for i in range(randint(maxChildrenToMutate)):
            childToMutate = children[randrange(len(children))]
            children.append(mutate(childToMutate))
            children.remove(childToMutate)

    # CREATE INDIVIDUALS WITH RANDOM RULES POPULATING THEIR RULE SETS BEFORE FIRST RUN
def initRSIndividuals(agentPool):
    individuals = []
    for x in range(maxIndividuals):    
        ruleSet = [] # Rule sets are lists of rules
            # Populate a rule set
        for i in range(maxRules):
            ruleSet.append(createRandomRule(agentPool))
        
        individuals.append(Individual(x+1, agentPool, ruleSet))
    
    return individuals
    
    # CREATE A RANDOM RULE USING RANDOM PREDICATES AND AN AGENT POOL RELATED ACTION
def createRandomRule(agentPool):
    conditions = [] # Conditions for a rule
    
        # Set conditions of rules as a random amount of random predicates
    for i in range(randint(1, maxRulePredicates)):
        newCond = PredicateSet.getRandomPredicate()
        if checkValidCond(newCond, conditions):
            conditions.append(newCond)
        
        # Get index of possible action. SUMO changes phases on indexes
    action = randrange(0, len(agentPool.getActionSet()))     # Set rule action to a random action from ActionSet pertaining to Agent Pool being serviced
    print("The action is:", action)
    rule = Rule(conditions, action, agentPool)

    return rule   
    
    # CREATE A CHILD RULE BY BREEDING TWO PARENT RULES
def crossover(indiv1, indiv2):
    identifier = indiv1.getID() + indiv2.getID()
    agentPool = indiv1.getAgentPool()

    superRuleSet = indiv1.getRuleSet() + indiv2.getRuleSet()    
    superRuleSet.sort(key=lambda x: x.getWeight(), reverse = True)

    newRuleSet = [superRuleSet[0], superRuleSet[maxRules-1]]

        # Ensure the same rule with different weights haven't been added to rule set. If they have, keep the one with the higher weight and mutate the other
    for rule in newRuleSet:
        for r in newRuleSet:
            if rule != r and rule.getConditions() == r.getConditions():
                if rule.getWeight > r.getWeight():
                    newRuleSet.append(mutateRule(r))
                    newRuleSet.remove(r)
                else:
                    newRuleSet.append(mutateRule(rule))
                    newRuleSet.remove(rule)

    return Individual(identifier, agentPool, newRuleSet)

def mutate(individual):
    chosenRule = individual.getRuleSet()[randrange(0,len(individual.getRuleSet()))]
    newRule = mutateRule(chosenRule)

    individual.getRuleSet().append(newRule)
    individual.getRuleSet().remove(chosenRule)    
    
    # MUTATES A RULE A RANDOM NUMBER OF TIMES (MAX MUTATIONS IS USER-DEFINED)
def mutateRule(rule):
    maxNumOfMutations = 1 # user defined maximum number of mutations
    ruleCond = rule.getConditions()
    
        # Remove a random number of conditions and add a random number of random conditions
    for x in range(1, randint(maxNumOfMutations)):
        
        numCondToRemove = randrange(1, len(ruleCond))
        for i in range(numCondToRemove):
            ruleCond.remove(randrange(len(ruleCond)))
        
        numCondToAdd = randint(1, maxRulePredicates - len(ruleCond))
        for i in range(numCondToAdd):
            newPredicate = PredicateSet.getRandomPredicate()  

                # If new random predicate is valid, append it to the conditions list
            if checkValidCond(newPredicate, ruleCond):
                ruleCond.append(newPredicate)
    
    rule.setConditions(ruleCond) # set rule's new conditions
    rule.setAction(rule.getAgentPool().getActionSet()[randrange(0, len(rule.getAgentPool().getActionSet()))])
    rule.updateWeight(0)

    return rule

    # ENSURE UNIQUE PREDICATE TYPES IN CONDITIONS 
def checkValidCond(cond, conditions):        
    predicateType = cond.split("_")
        
        #If predicate type already exists in conditions, return false
    if predicateType[0] in conditions:
        return False 
    else:
        return True

    # RETURN SUM OF ALL WEIGHTS IN A RULE SET
def getSumRuleWeightsAP(agentPools):
    weightSum = 0

    for ap in agentPools:
        individuals = ap.getIndividualsSet()    
        # For each individual, sum all their rule weights
        for i in individuals:
            ruleSet = i.getRuleSet()    
            weightSum += sum(rule.getWeight() for rule in ruleSet)
    
    if weightSum == 0:
        weightSum = 2.2250738585072014e-308

    return weightSum

    # RETURN SUM OF ALL WEIGHTS IN A RULE SET
def getSumRuleWeights(individuals):
    weightSum = 0
    
    ruleSet = i.getRuleSet()    
    weightSum = sum(rule.getWeight() for rule in ruleSet)
    
    if weightSum == 0:
        weightSum = 2.2250738585072014e-308

    return weightSum