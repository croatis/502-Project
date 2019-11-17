import os
import sys
import PredicateSet as PredicateSet
import Rule as Rule
from random import randrange

    #  EVOLUTIONARY LEARNER ALGORITHM
class EvolutionaryLearner:

    global maxRulePredicates = 3
    global maxRules = 5

        # CREATE RANDOM RULES FOR RULE SETS BEFORE FIRST RUN
    def initRuleSet(agentPool):
        ruleSet = [] # Rule sets are lists of rules

        for i in range(maxRules):
            ruleSet.append(createRandomRule(agentPool))
        
        return ruleSet
        
        # CREATE A RANDOM RULE USING RANDOM PREDICATES AND AN AGENT POOL RELATED ACTION
    def createRandomRule(agentPool):
        conditions = [] # Conditions for a rule
        
        # Set conditions of rules as a random amount of random predicates
        for i in range(randrange(1, maxRulePredicates)):
            newCond = PredicateSet.getRandomPredicate()
            if checkValidCond(newCond, conditions):
                conditions.append(newCond)
        
        action = randrange(0, len(agentPool.getActionSet())) # Set rule action to a random action from ActionSet pertaining to Agent Pool being serviced
        rule = Rule(conditions, action, agentPool)

        return rule   
        
        # CREATE A CHILD RULE BY BREEDING TWO PARENT RULES
    def breed(rule1, rule2):
            # Seperate the conditions and actions of each parent for combination
        conditionSet1 = rule1.getConditions()
        conditionSet2 = rule2.getConditions()
        condLen1 = len(conditionSet1)
        condLen2 = len(conditionSet2)
        
        childConditions = []
        childAction = -1
            
            # Determine how many conditions the child will have; random quantity between number of parents' conditions
        if condLen1 > condLen2:
            numOfChildCond = randrange (condLen2, condLen1)
        else: 
            numOfChildCond = randrange (condLen2, condLen1)
            
            # Populate child conditions with predicates from its two parents
        for x in range(numOfChildCond):
            chooseParent = randrange(1,2) # Randomly decide which parent contributes a predicate this iteration

            if chooseParent == 1:
                childConditions.append(conditionsSet1[randrange(0, condLen1)]) # Assign random predicate from parent/rule1 
            else:
                childConditions.append(conditionsSet1[randrange(0, condLen2)]) # Assign random predicate from parent/rule1 
            
            # Determine whose action the child will take
        actionToChoose = randrange(1, 2) 
        if actionToChoose == 1:
            childAction = rule1.getAction()
        else:
            childAction = rule2.getAction()

        return Rule(childConditions, childAction)
        
        # MUTATES A RULE A RANDOM NUMBER OF TIMES (MAX MUTATIONS IS USER-DEFINED)
    def mutate(rule):
        
        # MUTATES A RULE A SPECIFIED NUMBER OF TIMES 
    def mutate(rule, numOfMutations):
        ruleCond = rule.getConditions()
        
        for x in range(0, numOfMutations):
            newPredicate = PredicateSet.getRandomPredicate()
                
                # If new random predicate is valid, replace a random existing one with it
            if checkValidCond(newPredicate, ruleCond):
                ruleCond[randrange(0, len(ruleCond))] = newPredicate
            else:
                x -= 1 # if condition is not valid, decrement x by 1 to redo loop iteration

            # Change action a specified % of the time 
        if randrange(0, 25) == 1:

        # ENSURE UNIQUE PREDICATE TYPES IN CONDITIONS 
    def checkValidCond(cond, conditions):        
        predicateType = cond.split("_")
            
            #If predicate type already exists in conditions, return false
        if predicateType[0] in conditions:
            return False 
        else:
            return True
