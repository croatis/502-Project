import os
import sys
import inspect

import PredicateSet as PredicateSet
import EvolutionaryLearner as EvolutionaryLearner
from TrafficLight import TrafficLight
from Rule import Rule
from random import randrange

class AgentPool:
    
    global rsIndividuals                        # AgentPool's set of Rule Set Individuals containing a set of rules
        
        # Intialize object variables
    def __init__(self, identifier, actionSet):
        self.id = identifier                    # AgentPool name
        self.actionSet = actionSet              # An integer specifying number of actions available to AgentPool
        self.trafficLightsAssigned = []         # List of traffic lights using Agent Pool 
        self.individuals = []                   
        self.userDefinedRuleSet = [Rule(["emergencyVehicleApproachingVertical"], -1, self), Rule(["emergencyVehicleApproachingHorizontal"], -1, self), Rule(["maxGreenPhaseTimeReached"], -1, self), Rule(["maxYellowPhaseTimeReached"], -1, self)]
        self.initIndividuals()                      # Populate Agent Pool's own rule set with random rules

    def getID(self):
        return self.id

    def getActionSet(self):
        return self.actionSet

    def getIndividualsSet(self):
        return self.rsIndividuals
    
    def initIndividuals(self):
        self.rsIndividuals = EvolutionaryLearner.initRSIndividuals(self)

    def getAssignedTrafficLights(self):
        return self.trafficLightsAssigned
        
    def addNewTrafficLight(self, trafficLight):
        self.trafficLightsAssigned.append(trafficLight)
        trafficLight.assignToAgentPool(self)

        # SELECTS AN INDIVIDUAL TO PASS TO A TRAFFIC LIGHT WHEN REQUESTED
    def selectIndividual(self):
        return self.getIndividualsSet()[randrange(0, len(self.getIndividualsSet()))] # Currently returning a random rule

    def fit(self):
        pass  
        
# def run():
#     ap = AgentPool("ap1", ["H_S_G", "H_S_Y", "H_L_G", "H_L_Y"])
#     for i in ap.getIndividualsSet():    
#         print("Individual", i.getID(), "has rules with the following conditions and actions:\n")
#         for r in i.getRuleSet():
#             print(r.getConditions(), "and the action is:", r.getAction(), "\n\n")

# if __name__ == "__main__":
#     run()