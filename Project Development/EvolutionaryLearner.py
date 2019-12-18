import os
import sys
import PredicateSet as PredicateSet
import CoopPredicateSet as CoopPredicateSet

from Rule import Rule
from Individual import Individual
from random import randrange
from random import randint

    #  EVOLUTIONARY LEARNER ALGORITHM
# class EvolutionaryLearner:
    
    # How many of the top individuals to breed for new generation
global maxIndexToBreed
global maxChildrenToMutate
maxIndexToBreed = 4   
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
def rFit(simTime, sumOfRuleWeights):
    return runtimeFactor*(1/simTime) + ruleWeightFactor*(1-(1/sumOfRuleWeights))

    # FITNESS FUNCTION FOR ONE GENERATION
def fit(simTime, agentPools):
    ruleWeights = getSumRuleWeights(agentPools)
    fit = runtimeFactor*(1/simTime) + ruleWeightFactor*(1-(1/ruleWeights))

    return fit

    # CREATES NEW GENERATION AFTER A SIMULATION RUN AND UPDATES AGENT POOLS' INDIVIDUAL SET WITH NEW GEN
def createNewGeneration(agentPools):
    for ap in agentPools:
        individuals = ap.getIndividualsSet()
        individuals.sort(key=lambda x: x.getFitness(), reverse = True)


        newGenPool = individuals[0:maxIndexToBreed]
        print(newGenPool)
        children = []
            # Create children 
        for i in newGenPool:
            for partner in newGenPool:
                if i != partner:
                    child = crossover(i, partner)
                    child.updateFitness(rFit(((i.getLastRunTime() + partner.getLastRunTime())/2), child.getSumRuleWeights())) 
                    children.append(child)

            # Randomly mutate a random number of the children
        # ** THIS NEEDS TO BE UPDATED TO RESOLVE THE NEW RFIT VALUE****
        for i in range(randint(1, maxChildrenToMutate)):
            childToMutate = children[randrange(0, len(children))]
            children.append(mutate(childToMutate))
            children.remove(childToMutate)
        
            # Add children to new generation selection pool
        for c in children:
            newGenPool.append(c)
        
        newGenPool.sort(key=lambda x: x.getFitness(), reverse = True)
        newGeneration = newGenPool[0:maxIndividuals - 2] # Fill all but one spot of the new generation with the best children
        newGeneration.append(newGenPool[randrange(maxIndividuals - 1, len(newGenPool))])

        ap.updateIndividualsSet(newGeneration)
            
            # Randomly mutate a random number of the children
        for i in range(randint(1, maxChildrenToMutate)):
            childToMutate = children[randrange(len(children))]
            children.append(mutate(childToMutate))
            children.remove(childToMutate)

    # CREATE INDIVIDUALS WITH RANDOM RULES POPULATING THEIR RULE SETS BEFORE FIRST RUN
def initIndividuals(agentPool):
    individuals = []
    for x in range(maxIndividuals):    
        RS = []     # RS is a rule set with no shout-ahead predicates
        RSint = []  # RSint is a rule set with shout-ahead predicates
            # Populate a rule set
        for i in range(maxRules):
            RS.append(createRandomRule(agentPool, 0))
            RSint.append(createRandomRule(agentPool, 1))
        
        individuals.append(Individual(x+1, agentPool, RS, RSint))
    
    return individuals
    
    # CREATE A RANDOM RULE USING RANDOM PREDICATES AND AN AGENT POOL RELATED ACTION
def createRandomRule(agentPool, ruleType):
    conditions = [] # Conditions for a rule
        
        # RS rule
    if ruleType == 0:
            # Set conditions of rules as a random amount of random predicates
        for i in range(randint(1, maxRulePredicates)):
            newCond = PredicateSet.getRandomPredicate()
            if checkValidCond(newCond, conditions):
                conditions.append(newCond)
        
        # RSint rule
    elif ruleType == 1:
            # Set conditions of rules as a random amount of random predicates
        for i in range(randint(1, maxRulePredicates)):
            newCond = agentPool.getRandomRSintPredicate()
            if checkValidCond(newCond, conditions):
                conditions.append(newCond)

        # Get index of possible action. SUMO changes phases on indexes
    action = randrange(0, len(agentPool.getActionSet()))     # Set rule action to a random action from ActionSet pertaining to Agent Pool being serviced
    # print("The action is:", action)
    rule = Rule(ruleType, conditions, action, agentPool)

    return rule   
    
    # CREATE A CHILD RULE BY BREEDING TWO PARENT RULES
def crossover(indiv1, indiv2):
    identifier = str(indiv1.getID()) + "." + str(indiv2.getID())
    agentPool = indiv1.getAgentPool()

    superRS = indiv1.getRS() + indiv2.getRS()    
    superRS.sort(key=lambda x: x.getWeight(), reverse = True)
    
    superRSint = indiv1.getRSint() + indiv2.getRSint()    
    superRSint.sort(key=lambda x: x.getWeight(), reverse = True)

    newRS = [superRS[0], superRS[len(superRS)-1]]
    newRSint = [superRSint[0], superRSint[len(superRSint)-1]]

        # Ensure the same rule with different weights haven't been added to rule set. If they have, keep the one with the higher weight and mutate the other
    for rule in newRS:
        for r in newRS:
            if rule != r and rule.getConditions() == r.getConditions():
                if rule.getWeight > r.getWeight():
                    newRS.append(mutateRule(r))
                    newRS.remove(r)
                else:
                    newRS.append(mutateRule(rule))
                    newRS.remove(rule)

        # Ensure the same rule with different weights haven't been added to rule set. If they have, keep the one with the higher weight and mutate the other
    for rule in newRSint:
        for r in newRSint:
            if rule != r and rule.getConditions() == r.getConditions():
                if rule.getWeight > r.getWeight():
                    newRSint.append(mutateRule(r))
                    newRSint.remove(r)
                else:
                    newRSint.append(mutateRule(rule))
                    newRSint.remove(rule)

    return Individual(identifier, agentPool, newRS, newRSint)

def mutate(individual):
    chosenRule = individual.getRS()[randrange(0,len(individual.getRS()))]
    newRule = mutateRule(chosenRule)

    individual.getRS().append(newRule)
    individual.getRS().remove(chosenRule)

    return individual    
    
    # MUTATES A RULE A RANDOM NUMBER OF TIMES (MAX MUTATIONS IS USER-DEFINED)
def mutateRule(rule):
    maxNumOfMutations = 1 # user defined maximum number of mutations
    ruleCond = rule.getConditions()
    
        # Remove a random number of conditions and add a random number of random conditions
    for x in range(1, randint(1, maxNumOfMutations)):
        
        numCondToRemove = randrange(1, len(ruleCond))
        for i in range(numCondToRemove):
            ruleCond.remove(randrange(len(ruleCond)))
        
        numCondToAdd = randint(1, maxRulePredicates - len(ruleCond))
            
            # If rule is from RS
        if rule.getType() == 0:
            for i in range(numCondToAdd):
                newPredicate = PredicateSet.getRandomPredicate()  

                    # If new random predicate is valid, append it to the conditions list
                if checkValidCond(newPredicate, ruleCond):
                    ruleCond.append(newPredicate)
            
            # If rule is from RSint
        elif rule.getType() == 1:
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
def getSumRuleWeights(agentPools):
    weightSum = 0

    for ap in agentPools:
        individuals = ap.getIndividualsSet()    
        # For each individual, sum all their rule weights
        for i in individuals:
            ruleSet = i.getRS()    
            weightSum += sum(rule.getWeight() for rule in ruleSet)
    
    if weightSum == 0:
        weightSum = 2.2250738585072014e-308

    return weightSum

