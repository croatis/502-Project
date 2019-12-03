import os
import sys
import PredicateSet as PredicateSet
from Rule import Rule
from Individual import Individual
from random import randrange
from random import randint

    #  EVOLUTIONARY LEARNER ALGORITHM
# class EvolutionaryLearner:

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
ruleWeightFactor = 0.5

    # FITNESS FUNCTION FOR ONE SIMULATION SET
def fit(simTime, agentPools):
    ruleWeights = getSumRuleWeights(agentPools)
    fit = runtimeFactor*(1/simTime) + ruleWeightFactor*(1-(1/ruleWeights))

    createNewGeneration(individuals)
    return fit

def createNewGeneration(agentPools):
    pass

    # RETURN SUM OF ALL WEIGHTS IN A RULE SET
def getSumRuleWeights(agentPools):
    weightSum = 0

    for ap in agentPools:
        individuals = ap.getIndividualsSet()    
        # For each individual, sum all their rule weights
        for i in individuals:
            ruleSet = i.getRuleSet()    
                # Sum the weights of all the rules in the set
            for rule in ruleSet:
                weightSum += rule.getWeight()
    
    if weightSum == 0:
        weightSum = 2.2250738585072014e-308

    return weightSum

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
def breed(rule1, rule2):
        # Seperate the conditions and actions of each parent for combination
    conditionsSet1 = rule1.getConditions()
    conditionsSet2 = rule2.getConditions()
    condLen1 = len(conditionsSet1)
    condLen2 = len(conditionsSet2)
    
    childConditions = []
    childAction = -1
        
        # Determine how many conditions the child will have; random quantity between number of parents' conditions
    if condLen1 > condLen2:
        numOfChildCond = randint(condLen2, condLen1)
    
    elif condLen1 == condLen2 and condLen1 > 1:
        numOfChildCond = randint(1, condLen1)
    
    elif condLen1 == condLen2 and condLen1 == 1:
        numOfChildCond = 1

    else: 
        numOfChildCond = randint(condLen1, condLen2)

        # Populate child conditions with predicates from its two parents
    for x in range(numOfChildCond):
        chooseParent = randint(1,2) # Randomly decide which parent contributes a predicate this iteration

        if chooseParent == 1:
            childConditions.append(conditionsSet1[randrange(condLen1)]) # Assign random predicate from parent/rule1 

        else:
            childConditions.append(conditionsSet2[randrange(condLen2)]) # Assign random predicate from parent/rule1 

        # Determine whose action the child will take
    actionToChoose = randint(1, 2) 
    if actionToChoose == 1:
        childAction = rule1.getAction()
    else:
        childAction = rule2.getAction()

    return Rule(childConditions, childAction)
    
    # MUTATES A RULE A RANDOM NUMBER OF TIMES (MAX MUTATIONS IS USER-DEFINED)
def mutate(rule):
    maxNumOfMutations = 10 # user defined maximum number of mutations
    ruleCond = rule.getConditions()
    
        # Do a random number of mutations; no more than maximum specified
    for x in range(1, randint(maxNumOfMutations)):
        mutationType = randint(2) # Randomly determine if mutation is an addition, removal or replacement of predicate
        
            # Predicate addition mutation
        if mutationType == 0:
            if len(ruleCond) < maxRulePredicates:
                newPredicate = PredicateSet.getRandomPredicate() # Get a new random predicate
                
                # If new random predicate is valid, append it to the conditions list
            if checkValidCond(newPredicate, ruleCond):
                ruleCond.append(newPredicate)

            # Predicate removal mutation 
        elif mutationType == 1:
            if len(ruleCond) > 1:
                del(ruleCond[randint(len(ruleCond))]) # Delete predicate at random location in conditions list
            
            # Random predicate replacement mutation     
        else:
            newPredicate = PredicateSet.getRandomPredicate()
                
                # If new random predicate is valid, replace a random existing one with it
            if checkValidCond(newPredicate, ruleCond):
                ruleCond[randrange(len(ruleCond))] = newPredicate # Replace random predicate with new predicate
            else:
                x -= 1 # if condition is not valid, decrement x by 1 to redo loop iteration
    
    rule.setConditions(ruleCond) # set rule's new conditions

        # Change action a specified % of the time to a random, permitted action 
    if randrange(0, 25) == 1:
        rule.setAction(randrange(0, len(rule.getAgentPool().getActionSet())))
    
    return rule

    # ENSURE UNIQUE PREDICATE TYPES IN CONDITIONS 
def checkValidCond(cond, conditions):        
    predicateType = cond.split("_")
        
        #If predicate type already exists in conditions, return false
    if predicateType[0] in conditions:
        return False 
    else:
        return True
