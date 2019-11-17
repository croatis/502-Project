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
            ruleSet.append(makeRule(agentPool.getActionSet()))
        
        return ruleSet
    
    def makeRule(actionSet):
        conditions = [] # Conditions for a rule
        
        # Set conditions of rules as a random amount of random predicates
        for i in range(randrange(1, maxRulePredicates)):
            newCond = PredicateSet.getRandomPredicate()
            if checkValidCond(newCond, conditions):
                conditions.append(newCond)
        
        action = actionSet.getRandomAction() # Set rule action to a random action from ActionSet pertaining to Agent Pool being serviced
        rule = Rule(conditions, action)

        return rule                                                              

    def checkValidCond(cond, conditions):
        
        if "_" in cond:
            predicateType = cond.split("_")

            if predicateType[0] in conditions:
                return False
