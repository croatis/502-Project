#!/usr/bin/env python

import os
import sys
import optparse

import InitSetUp 
import PredicateSet 
import EvolutionaryLearner 
import ReinforcementLearner
from Rule import Rule

global maxGreenPhaseTime
global maxYellowPhaseTime
global userDefinedRules
global trafficLights
global rule
global nextRule

maxGreenPhaseTime = 225
maxYellowPhaseTime = 5


# Importing needed python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")


from sumolib import checkBinary  # Checks for the binary in environ vars
import traci

def get_options():
    opt_parser = optparse.OptionParser()
    opt_parser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = opt_parser.parse_args()
    return options


# CONTAINS MAIN TRACI SIMULATION LOOP
def run():
        # Run set-up script and acquire list of user defined rules and traffic light agents in simulation
    setUpTuple = InitSetUp.run()
    userDefinedRules = setUpTuple[0]
    trafficLights = setUpTuple[1]
    rule = None 
    nextRule = None

        # Assign each traffic light an individual from their agent pool for this simulation run, and a starting rule
    for tl in trafficLights:
        tl.assignIndividual()
        rule = applicableUserDefinedRule(tl, userDefinedRules) # Check user-defined rules
            
            # If no user-defined rules can be applied, get a rule from Agent Pool
        if rule == False:    
            rule = tl.getAssignedIndividual().selectRule(getValidRules(tl, tl.getAssignedIndividual())) # Get a rule from assigned rsIndividual
                # If rule conditions are satisfied, apply its action. Otherwise, do nothing.
            if evaluateRule(tl, rule):
                traci.trafficlight.setPhase(tl.getName(), rule.getAction())                
                print("Rule selected for", tl.getName(), ". It's conditions are:", rule.getConditions())    

        else:
            applyUserDefinedRuleAction(tl, traci.trafficlight.getPhaseName(tl.getName()), rule)

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
                carsWaitingAfter = carsWaitingCount(tl) 
                waitingTimeAfter = getWaitingTime(tl)
                    
                nextRule = applicableUserDefinedRule(tl, userDefinedRules) # Check if a user-defined rule can be applied
                   
                    # If no user-defined rules can be applied, get a rule from Agent Pool
                if nextRule == False:    
                    nextRule = tl.getAssignedIndividual().selectRule(getValidRules(tl, tl.getAssignedIndividual())) # Get a rule from assigned rsIndividual

                        # If applied rule isn't user-defined, update its weight
                    if rule not in userDefinedRules:
                        rule.updateWeight(ReinforcementLearner.updatedWeight(rule, nextRule, (tl.getCarsWaitingCount() - carsWaitingAfter), (tl.getWaitTime() - waitingTimeAfter)))
                        print("Rule with conditions:", rule.getConditions(), "now has a weight of:", rule.getWeight(), "\n\n")
                            
                            # If nextRule conditions are satisfied, apply its action. Otherwise, do nothing.
                    traci.trafficlight.setPhase(tl.getName(), nextRule.getAction())                
                    print("Rule selected for", tl.getName(), ". It's conditions are:", nextRule.getConditions())    

                else:
                    applyUserDefinedRuleAction(tl, traci.trafficlight.getPhaseName(tl.getName()), nextRule)
                    print("Applying action of", nextRule.getConditions())  

                    # Update values before proceeding
                rule = nextRule
                tl.setCarsWaitingCount(carsWaitingAfter)
                tl.setWaitTime(waitingTimeAfter)             
        
        step += 1  # Increment step in line with simulator

    traci.close()       # End simulation
    sys.stdout.flush()  
    
# RETRIEVE THE STATE OF THE INTERSECTION FROM SUMO
def getState(trafficLight):
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

def carsWaitingCount(trafficLight):
    state = getState(trafficLight)
    carsWaiting = 0
        # Count all vehicles in the state dictionary
    for lanes in state:
        carsWaiting += len(state[lanes])
    
    return carsWaiting

def getWaitingTime(trafficLight):
    waitTime = 0
        # Sum waiting time of each edge controlled by the traffic light
    for edge in trafficLight.getEdges():
        waitTime += traci.edge.getWaitingTime(edge)
    
    return waitTime

def getValidRules(trafficLight, individual):
    validRules = []

    for rule in individual.getRuleSet():
        if evaluateRule(trafficLight, rule):
            validRules.append(rule)
    
    return validRules

    # EVALUATE RULE VALIDITY (fEval)
def evaluateRule(trafficLight, rule):
        # For each condition, its parameters are acquired and the condition predicate is evaluated
    for cond in rule.getConditions():
        predicateSplit = cond.split("_")
        predicate = predicateSplit[0]

        predCall = getattr(PredicateSet, cond)(getPredicateParameters(trafficLight, predicate)) # Construct predicate fuction call
            # Determine validity of predicate
        if predCall == False:
            return False
    
    return True # if all predicates return true, evaluate rule as True
    
    # DETERMINE IF ANY USER DEFINED RULES ARE APPLICABLE
def applicableUserDefinedRule(trafficLight, userDefinedRules):
        # Evaluate each user define rule
    for rule in userDefinedRules:
            # For each rule, its parameters are acquired and the condition predicate is evaluated
        for cond in rule.getConditions():    
            if "emergencyVehicleApproaching" in cond:
                continue
            else:
                parameters = getPredicateParameters(trafficLight, cond)
                print("The parameters are:", parameters)
                predCall = getattr(PredicateSet, cond)(parameters[0], parameters[1], parameters[2]) # Construct predicate fuction call
                
                # Determine validity of predicate
            if predCall == True:
                print("User defined rule applicable:", rule.getConditions())
                return rule
    return False # if no user-defined predicates are applicable, return False

    # APPLIES USER DEFINED ACTIONS
def applyUserDefinedRuleAction(trafficLight, currPhaseName, rule):
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
def getPredicateParameters(trafficLight, predicate):
    if predicate == "longestTimeWaitedToProceedStraight":
            # Find max wait time for relevant intersection
        maxWaitTime = 0
        state = getState(trafficLight) # Retrieve state of specified intersection 
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
        state = getState(trafficLight) # Retrieve state of specified intersection 
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
        state = getState(trafficLight) # Retrieve state of specified intersection 
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
        state = getState(trafficLight) # Retrieve state of specified intersection 
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
        parameters.append(traci.trafficlight.getPhaseDuration(trafficLight.getName()) - (traci.trafficlight.getNextSwitch(trafficLight.getName()) - traci.simulation.getTime()))
        parameters.append(maxGreenPhaseTime)

        return parameters
    
    elif "maxYellowPhaseTimeReached" == predicate:
        parameters = []  
        parameters.append(traci.trafficlight.getPhaseName(trafficLight.getName())) # Get traffic light phase name
            
            # Get phase (G or Y) from phase name
        getPhase = parameters[0].split("_")
        parameters[0] = getPhase[2]
        
        parameters.append(traci.trafficlight.getPhaseDuration(trafficLight.getName()) - (traci.trafficlight.getNextSwitch(trafficLight.getName()) - traci.simulation.getTime()))
        parameters.append(maxYellowPhaseTime)

        return parameters        
# main entry point
if __name__ == "__main__":
    options = get_options()

    # check binary
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    # traci starts sumo as a subprocess and then this script connects and runs
    traci.start([sumoBinary, "-c", "config_file.sumocfg",
                             "--tripinfo-output", "tripinfo.xml"])
    run()

