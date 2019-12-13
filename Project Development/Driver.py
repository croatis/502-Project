#!/usr/bin/env python

import os
import sys
import optparse
import traci

import PredicateSet 
import EvolutionaryLearner 
import ReinforcementLearner
from Rule import Rule
from Intention import Intention

class Driver:

    global userDefinedRules
    global trafficLights
    global rule
    global nextRule

    def __init__(self, sumoCmd, setUpTuple, maxGreenPhaseTime, maxYellowPhaseTime):
        self.sumoCmd = sumoCmd
        self.setUpTuple = setUpTuple
        self.maxGreenPhaseTime = maxGreenPhaseTime
        self.maxYellowPhaseTime = maxYellowPhaseTime

    # CONTAINS MAIN TRACI SIMULATION LOOP
    def run(self):
        traci.start(self.sumoCmd)   # Start SUMO. Comment out if running Driver as standalone module.

            # Run set-up script and acquire list of user defined rules and traffic light agents in simulation
        userDefinedRules = self.setUpTuple[0]
        trafficLights = self.setUpTuple[1]
        rule = None 
        nextRule = None

            # Assign each traffic light an individual from their agent pool for this simulation run, and a starting rule
        for tl in trafficLights:
            tl.assignIndividual()

            rule = self.applicableUserDefinedRule(tl, userDefinedRules) # Check user-defined rules
                
                # If no user-defined rules can be applied, get a rule from Agent Pool
            if rule == False:    
                rule = tl.getAssignedIndividual().selectRule(self.getValidRules(tl, tl.getAssignedIndividual())) # Get a rule from assigned rsIndividual
                    
                    # if no valid rule applicable, apply the Do Nothing rule.
                if rule == -1:
                    print("No valid rule. Do Nothing action applied.") 
                    tl.doNothing()  # Update traffic light's Do Nothing counter

                else:       
                        # If rule conditions are satisfied, apply its action. Otherwise, do nothing.
                    if self.evaluateRule(tl, rule):
                        traci.trafficlight.setPhase(tl.getName(), rule.getAction())                
                        print("Rule selected for", tl.getName(), ". It's conditions are:", rule.getConditions())    
            
            else:
                self.applyUserDefinedRuleAction(tl, traci.trafficlight.getPhaseName(tl.getName()), rule)

        for tl in trafficLights:
            i = tl.getAssignedIndividual()
            for rule in i.getRuleSet():
                print("\nRule with conditions", rule.getConditions(), "has a starting weight of:", rule.getWeight(), "\n\n")

            # Simulation loop 
        step = 0
        carsWaitingAfter = 0
        waitingTimeAfter = 0
        while traci.simulation.getMinExpectedNumber() > 0:
            traci.simulationStep() # Advance SUMO simulation one step (1 second)
                
                # Traffic Light agents reevaluate their state every 5 seconds
            if step % 5 == 0:  
                    # For every traffic light in simulation, select and evaluate new rule from its agent pool
                for tl in trafficLights:
                    carsWaitingAfter = self.carsWaitingCount(tl) 
                    waitingTimeAfter = self.getWaitingTime(tl)
                        
                    nextRule = self.applicableUserDefinedRule(tl, userDefinedRules) # Check if a user-defined rule can be applied
                    
                        # If no user-defined rules can be applied, get a rule from Agent Pool
                    if nextRule == False:    
                        nextRule = tl.getNextRule(self.getValidRules(tl, tl.getAssignedIndividual()), traci.simulation.getTime()) # Get next rule to be applied to tl

                            # if no valid rule applicable, apply the Do Nothing rule.
                        if nextRule == -1:
                            # print("No valid rule. Do Nothing action applied.") 
                            tl.doNothing()  # Update traffic light's Do Nothing counter
                            break

                        else: 
                            print("In else. Rule is", rule)
                                # If applied rule isn't user-defined, update its weight
                            if rule not in userDefinedRules:
                                if rule != -1:
                                    print("Rule", rule, "with conditions:", rule.getConditions(), "is getting its weight updated\n\n")
                                    rule.updateWeight(ReinforcementLearner.updatedWeight(rule, nextRule, (tl.getCarsWaitingCount() - carsWaitingAfter), (tl.getWaitTime() - waitingTimeAfter)))
                                    
                                    # If nextRule conditions are satisfied, apply its action.
                                traci.trafficlight.setPhase(tl.getName(), nextRule.getAction())                
                                # print("Rule selected for", tl.getName(), ". It's conditions are:", nextRule.getConditions())    

                    else:
                        self.applyUserDefinedRuleAction(tl, traci.trafficlight.getPhaseName(tl.getName()), nextRule)
                        # print("Applying action of", nextRule.getConditions())  

                        # Update values before proceeding
                    print("Last rule was", rule, "and the next rule is:", nextRule)
                    rule = nextRule
                    tl.setCarsWaitingCount(carsWaitingAfter)
                    tl.setWaitTime(waitingTimeAfter)             
            
            step += 1  # Increment step in line with simulator
            
            # Update the fitnesses of the individuals involved in the simulation based on their fitnesses
        simRunTime = traci.simulation.getTime()
        for tl in trafficLights:
            print(tl.getName(), "has these communicated intentions:", tl.getCommunicatedIntentions())
            i = tl.getAssignedIndividual()
            i.updateLastRunTime = simRunTime
            i.updateFitness(EvolutionaryLearner.rFit(simRunTime, i.getSumRuleWeights()))
            print(i, "has a fitness value of:", i.getFitness())
            # for rule in i.getRuleSet():
            #     print("Rule with conditions", rule.getConditions(), "has an end weight of:", rule.getWeight(), "\n\n")

        traci.close()       # End simulation
        
        return self.setUpTuple[2] # Returns all the agent pools to the main module
        # sys.stdout.flush()

        
    # RETRIEVE THE STATE OF THE INTERSECTION FROM SUMO
    def getState(self, trafficLight):
        state = {}
        leftTurnLane = ""
        for lane in trafficLight.getLanes():
            state[lane] = []

            # Loop to determine which vehicles are waiting at an intersection
        for vehID in traci.vehicle.getIDList(): 
            laneID = traci.vehicle.getLaneID(vehID)
            tlLanes = trafficLight.getLanes()
            
            # Operate only on vehicles in a lane controlled by traffic light 
            if laneID in tlLanes:
                    # Determine left turn lane if it exists
                if "_LTL" in laneID:
                    maxLaneNum = 0
                    for lane in tlLanes:
                        if lane == laneID:
                            laneSplit = lane.split("_")
                            if int(laneSplit[2]) > maxLaneNum:
                                leftTurnLane = lane
                
                    # If vehicle is stopped, append relevant identifier to it
                if traci.vehicle.getSpeed(vehID) == 0:    
                    if leftTurnLane == laneID:
                        vehID = vehID + "_L"
                    else:
                        vehID = vehID + "_S"
                
                    state[laneID].append(vehID)
                
        return state

    def carsWaitingCount(self, trafficLight):
        state = self.getState(trafficLight)
        carsWaiting = 0
            # Count all vehicles in the state dictionary
        for lanes in state:
            carsWaiting += len(state[lanes])
        
        return carsWaiting

    def getWaitingTime(self, trafficLight):
        waitTime = 0
            # Sum waiting time of each edge controlled by the traffic light
        for edge in trafficLight.getEdges():
            waitTime += traci.edge.getWaitingTime(edge)
        
        return waitTime

    def getValidRules(self, trafficLight, individual):
        validRules = []

        for rule in individual.getRuleSet():
            if self.evaluateRule(trafficLight, rule):
                validRules.append(rule)
        
        return validRules

        # EVALUATE RULE VALIDITY (fEval)
    def evaluateRule(self, trafficLight, rule):
            # For each condition, its parameters are acquired and the condition predicate is evaluated
        for cond in rule.getConditions():
            predicateSplit = cond.split("_")
            predicate = predicateSplit[0]

            predCall = getattr(PredicateSet, cond)(self.getPredicateParameters(trafficLight, predicate)) # Construct predicate fuction call
                # Determine validity of predicate
            if predCall == False:
                return False
        
        return True # if all predicates return true, evaluate rule as True
        
        # DETERMINE IF ANY USER DEFINED RULES ARE APPLICABLE
    def applicableUserDefinedRule(self, trafficLight, userDefinedRules):
            # Evaluate each user define rule
        for rule in userDefinedRules:
                # For each rule, its parameters are acquired and the condition predicate is evaluated
            for cond in rule.getConditions():    
                if "emergencyVehicleApproaching" in cond:
                    continue
                else:
                    parameters = self.getPredicateParameters(trafficLight, cond)
                    predCall = getattr(PredicateSet, cond)(parameters[0], parameters[1], parameters[2]) # Construct predicate fuction call
                    
                    # Determine validity of predicate
                if predCall == True:
                    # print("User defined rule applicable:", rule.getConditions())
                    return rule
        return False # if no user-defined predicates are applicable, return False

        # APPLIES USER DEFINED ACTIONS
    def applyUserDefinedRuleAction(self, trafficLight, currPhaseName, rule):
            # If max green phase time reached, switch phase to yellow in same direction
        if rule.getConditions()[0] == "maxGreenPhaseTimeReached":
            currPhase = traci.trafficlight.getPhaseName(trafficLight.getName())
            currPhase[5] = "Y"
            traci.trafficlight.setPhase(trafficLight.getName(), currPhase)
            
            # If max yellow phase time reached, switch to next phase in the schedule 
        elif rule.getConditions()[0] == "maxYellowPhaseTimeReached":
            if traci.trafficlight.getPhase(trafficLight.getName()) == (len(trafficLight.getPhases()) - 1):
                traci.trafficlight.setPhase(trafficLight.getName(), 0)
            else:
                traci.trafficlight.setPhase(trafficLight.getName(), traci.trafficlight.getPhase(trafficLight.getName()) + 1)


        # PROVIDE SIMULATION RELEVANT PARAMETERS
    def getPredicateParameters(self, trafficLight, predicate):
        if predicate == "longestTimeWaitedToProceedStraight":
                # Find max wait time for relevant intersection
            maxWaitTime = 0
            state = self.getState(trafficLight) # Retrieve state of specified intersection 
            for lane in state:
                if lane in trafficLight.getLanes():
                    for veh in state[lane]:
                        if "_S" in veh:
                            vehIDSplit = veh.split("_")
                            vehID  = vehIDSplit[0]
                            if traci.vehicle.getWaitingTime(vehID) > maxWaitTime:
                                maxWaitTime = traci.vehicle.getWaitingTime(vehID)
            return maxWaitTime

        elif predicate == "longestTimeWaitedToTurnLeft":
                # Find max wait time for relevant intersection
            maxWaitTime = 0
            state = self.getState(trafficLight) # Retrieve state of specified intersection 
            for lane in state:
                if lane in trafficLight.getLanes():
                    for veh in state[lane]:
                        if "_L" in veh:
                            vehIDSplit = veh.split("_")
                            vehID  = vehIDSplit[0]
                            if traci.vehicle.getWaitingTime(vehID) > maxWaitTime:
                                maxWaitTime = traci.vehicle.getWaitingTime(vehID)
            return maxWaitTime

        elif predicate == "numCarsWaitingToProceedStraight":
            carsWaiting = 0
            state = self.getState(trafficLight) # Retrieve state of specified intersection 
            for lane in state:
                if lane in trafficLight.getLanes():
                    for veh in state[lane]:
                        if "_S" in veh:
                            vehIDSplit = veh.split("_")
                            vehID  = vehIDSplit[0]
                            if traci.vehicle.getWaitingTime(vehID) > 0:
                                carsWaiting += 1

            return carsWaiting

        elif predicate == "numCarsWaitingToTurnLeft":
            carsWaiting = 0
            state = self.getState(trafficLight) # Retrieve state of specified intersection 
            for lane in state:
                if lane in trafficLight.getLanes():
                    for veh in state[lane]:
                        if "_L" in veh:
                            vehIDSplit = veh.split("_")
                            vehID  = vehIDSplit[0]
                            if traci.vehicle.getWaitingTime(vehID) > 0:
                                carsWaiting += 1

            return carsWaiting
        
        elif predicate == "timeSpentInCurrentPhase":
            return traci.trafficlight.getPhaseDuration(trafficLight.getName())
        
        elif "verticalPhaseIs" in predicate or "horizontalPhaseIs" in predicate or "northSouthPhaseIs" in predicate or "southNorthPhaseIs" in predicate or "eastWestPhaseIs" in predicate or "westEastPhaseIs" in predicate:
            return traci.trafficlight.getPhaseName(trafficLight.getName()).split("_")

        elif "maxGreenPhaseTimeReached" == predicate:
            parameters = []
            parameters.append(traci.trafficlight.getPhaseName(trafficLight.getName()))
            
                # Get phase (G or Y) from phase name
            getPhase = parameters[0].split("_")
            parameters[0] = getPhase[2]
            
            parameters.append(traci.trafficlight.getPhaseDuration(trafficLight.getName()) - (traci.trafficlight.getNextSwitch(trafficLight.getName()) - traci.simulation.getTime()))
            parameters.append(self.maxGreenPhaseTime)

            return parameters
        
        elif "maxYellowPhaseTimeReached" == predicate:
            parameters = []  
            parameters.append(traci.trafficlight.getPhaseName(trafficLight.getName())) # Get traffic light phase name
                
                # Get phase (G or Y) from phase name
            getPhase = parameters[0].split("_")
            parameters[0] = getPhase[2]
            
            parameters.append(traci.trafficlight.getPhaseDuration(trafficLight.getName()) - (traci.trafficlight.getNextSwitch(trafficLight.getName()) - traci.simulation.getTime()))
            parameters.append(self.maxYellowPhaseTime)

            return parameters 


# main entry point
if __name__ == "__main__":

    # traci starts sumo as a subprocess and then this script connects and runs
    traci.start([sumoBinary, "-c", "config_file.sumocfg",
                            "--tripinfo-output", "tripinfo.xml"])
    run()

