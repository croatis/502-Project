import os
import sys
import inspect

import PredicateSet as PredicateSet
import EvolutionaryLearner as EvolutionaryLearner
from TrafficLight import TrafficLight

class AgentPool:
    
    global ruleSet
    global sharedRuleSet 
    global userDefinedRuleSet 

        # Intialize object variables
    def __init__(self, identifier, actionSet):
        self.id = identifier
        self.actionSet = actionSet # a integer specifying number of actions available to AgentPool
        self.trafficLightsAssigned = []
        self.ruleSet = []
        self.communicatedRuleSet = []
        self.userDefinedRuleSet = []
        self.initRuleSet()

    def getID(self):
        return self.id

    def getActionSet(self):
        return self.actionSet

    def getRuleSet(self):
        return self.ruleSet
    
    def initRuleSet(self):
        self.ruleSet = EvolutionaryLearner.initRuleSet(self)

    def addNewTrafficLight(self, trafficLight):
        self.trafficLightsAssigned.append(trafficLight)
        trafficLight.assignToAgentPool(self)

    def getAssignedTrafficLights(self):
        return self.trafficLightsAssigned
    
    def getNumber(self):
        return self.number

    def fit(self):
        pass  
        
# def run():
#     methodList = inspect.getmembers(PredicateSet, predicate=inspect.isroutine)
#     print(methodList)

# if __name__ == "__main__":
#     run()