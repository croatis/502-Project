import os
import sys
import inspect

import PredicateSet as PredicateSet
import EvolutionaryLearner as EvolutionaryLearner
from TrafficLight import TrafficLight

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
        self.userDefinedRuleSet = ["emergencyVehicleApproachingVertical", "emergencyVehicleApproachingHorizontal", "maxGreenPhaseTimeReached", "maxYellowPhaseTimeReached"]
        self.initRuleSet()                      # Populate Agent Pool's own rule set with random rules

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
    
    def getuserDefinedRuleSet(self):
        return self.userDefinedRuleSet

    def fit(self):
        pass  
        
# def run():
#     methodList = inspect.getmembers(PredicateSet, predicate=inspect.isroutine)
#     print(methodList)

# if __name__ == "__main__":
#     run()