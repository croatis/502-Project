import os
import sys
import inspect

import PredicateSet as PredicateSet
import EvolutionaryLearner as EvolutionaryLearner
from TrafficLight import TrafficLight
from Rule import Rule
from random import randrange

class AgentPool:
    
    global ruleSet                              # AgentPool's own rule set
    global communicatedRuleSet                  # Set of communicated intentions from other agents (shout-ahead)
    global userDefinedRuleSet                   # Set of user defined rules that are always selected if true 

        # Intialize object variables
    def __init__(self, identifier, actionSet):
        self.id = identifier                    # AgentPool name
        self.actionSet = actionSet              # An integer specifying number of actions available to AgentPool
        self.trafficLightsAssigned = []         # List of traffic lights using Agent Pool 
        self.ruleSet = []                   
        self.communicatedRuleSet = []       
        self.userDefinedRuleSet = [Rule(["emergencyVehicleApproachingVertical"], 0, self), Rule(["emergencyVehicleApproachingHorizontal"], 0, self), Rule(["maxGreenPhaseTimeReached"], 0, self), Rule(["maxYellowPhaseTimeReached"], 0, self)]
        self.initRuleSet()                      # Populate Agent Pool's own rule set with random rules

    def getID(self):
        return self.id

    def getActionSet(self):
        return self.actionSet

    def getRuleSet(self):
        return self.ruleSet
    
    def initRuleSet(self):
        self.ruleSet = EvolutionaryLearner.initRuleSet(self)

    def getAssignedTrafficLights(self):
        return self.trafficLightsAssigned
    
    def getuserDefinedRuleSet(self):
        return self.userDefinedRuleSet
    
        # ***FINISH IMPLEMENTING**************************************************************************
    def setUserDefinedRuleActions(self):
        for rule in userDefRules:
            for predicate in rule.getConditions():    
                if "emergencyVehicleApproaching" in predicate:
                    continue
    
    def addNewTrafficLight(self, trafficLight):
        self.trafficLightsAssigned.append(trafficLight)
        trafficLight.assignToAgentPool(self)

        # SELECTS A RULE TO PASS TO A TRAFFIC LIGHT WHEN REQUESTED
    def selectRule(self):
        return self.getRuleSet()[randrange(0, len(self.getRuleSet()))] # Currently returning a random rule

    def fit(self):
        pass  
        
# def run():
#     methodList = inspect.getmembers(PredicateSet, predicate=inspect.isroutine)
#     print(methodList)

# if __name__ == "__main__":
#     run()