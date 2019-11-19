#!/usr/bin/env python

import os
import sys
import optparse

import TLAgentSetUp as TLAgentSetUp
import PredicateSet as PredicateSet
import EvolutionaryLearner as EvolutionaryLearner
from Rule import Rule

global maxGreenPhaseTime
global maxYellowPhaseTime

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
    # Acquire agent pool dictionary 
    trafficLights = TLAgentSetUp.run()
 
        # Simulation loop 
    step = 0
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep() # Advance SUMO simulation one step (1 second)
            
            # Traffic Light agents reevaluate their state every 5 seconds
        if step % 5 == 0:
            for tl in trafficLights:


        else:
            pass

        step+=1

    traci.close()
    sys.stdout.flush()
    
# RETRIEVE THE STATE OF THE INTERSECTION FROM SUMO
def get_state(trafficLight):
    state = {}
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
                leftTurnLane = ""
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
    
    # EVALUATE RULE VALIDITY
def evaluateRule(trafficLight, rule):
    tlName = trafficLight.getName()

        # For each condition, its parameters are acquired and the condition predicate is evaluated
    for cond in rule.getConditions():
        predicateSplit = cond.split("_")
        predicate = predicateSplit[0]

        predCall = getattr(PredicateSet, cond)(getPredicateParameter(trafficLight, predicate)) # Construct predicate fuction call
            # Determine validity of predicate
        if predCall == False:
            return False
    
    return True # if all predicates return true, evaluate rule as True
    
    # EVALUATE USER-DEFINED RULE VALIDITY
def evaluateUserDefinedRule(trafficLight):
    userDefRules = trafficLight.getAgentPool().getUserDefinedRuleSet()


    # PROVIDE SIMULATION RELEVANT PARAMETERS
def getPredicateParameter(trafficLight, predicate):
    if predicate == "longestTimeWaitedToProceedStraight":
            # Find max wait time for relevant intersection
        maxWaitTime = 0
        state = get_state(trafficLight) # Retrieve state of specified intersection 
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
        state = get_state(trafficLight) # Retrieve state of specified intersection 
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
        state = get_state(trafficLight) # Retrieve state of specified intersection 
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
        state = get_state(trafficLight) # Retrieve state of specified intersection 
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

