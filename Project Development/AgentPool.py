import os
import sys
import inspect

import PredicateSet as PredicateSet
import CoopPredicateSet as CoopPredicateSet

import EvolutionaryLearner as EvolutionaryLearner
from TrafficLight import TrafficLight
from Rule import Rule
from random import randrange

class AgentPool:
                
        # INTIALIZE AGENT POOL VARIABLES
    def __init__(self, identifier, actionSet):
        self.id = identifier                                            # AgentPool name
        self.actionSet = actionSet                                      # A list of action names that can be applied by assigned TL's of the pool
        self.trafficLightsAssigned = []                                 # List of traffic lights using Agent Pool 
        self.individuals = []                   
        self.userDefinedRuleSet = [Rule(-1, ["emergencyVehicleApproachingVertical"], -1, self), Rule(-1, ["emergencyVehicleApproachingHorizontal"], -1, self), Rule(-1, ["maxGreenPhaseTimeReached"], -1, self), Rule(-1, ["maxYellowPhaseTimeReached"], -1, self)]
        self.initIndividuals()                                          # Populate Agent Pool's own rule set with random rules
        self.coopPredicates = CoopPredicateSet.getPredicateSet(self)    # Store Observations of communicated intentions here since they are agent specific

    def getID(self):
        return self.id

    def getActionSet(self):
        return self.actionSet
    
    def getCoopPredicates(self):
        return self.coopPredicates

    def getIndividualsSet(self):
        return self.individuals
    
    def updateIndividualsSet(self, individuals):
        self.individuals = individuals
    
    def initIndividuals(self):
        self.individuals = EvolutionaryLearner.initIndividuals(self)

    def getAssignedTrafficLights(self):
        return self.trafficLightsAssigned
        
    def addNewTrafficLight(self, trafficLight):
        self.trafficLightsAssigned.append(trafficLight)
        trafficLight.assignToAgentPool(self)

        # SELECTS AN INDIVIDUAL TO PASS TO A TRAFFIC LIGHT WHEN REQUESTED
    def selectIndividual(self):
        return self.getIndividualsSet()[randrange(0, len(self.getIndividualsSet()))] # Currently returning a random rule

        # RETURN RANDOM PREDICATE FROM coopPredicate LIST FOR A RULE IN RSint
    def getRandomRSintPredicate(self):
        return self.coopPredicates[randrange(len(self.coopPredicates))]

# def run():
#     ap = AgentPool("ap1", ["H_S_G", "H_S_Y", "H_L_G", "H_L_Y"])
#     for i in ap.getIndividualsSet():    
#         print("Individual", i.getID(), "has rules with the following conditions and actions:\n")
#         for r in i.getRuleSet():
#             print(r.getConditions(), "and the action is:", r.getAction(), "\n\n")

# if __name__ == "__main__":
#     run()