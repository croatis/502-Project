#!/usr/bin/env python

import os
import sys
import optparse

import TLAgentSetUp as TLAgentSetUp
import PredicateSet as PredicateSet

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
    agentPool = TLAgentSetUp.run()
    predicateSet = PredicateSet.run()
    
    fourArmTrafficLights = agentPool["four-arm"]
    trafficLight = fourArmTrafficLights[0]

    step = 0
    edgeDensity = []
    edges = traci.edge.getIDList() 
    trafficLights = traci.trafficlight.getIDList()
    time = traci.simulation.getTime()

    # Simulation loop 
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        # print(step)
        # Changes TL phase every 5 steps
        if step % 5 == 0:
            PredicateSet.verticalPhaseIsGreen(traci.trafficlight.getPhase("four-arm"))
            carsWaiting = traci.edge.getWaitingTime
            # print(carsWaiting)
            phase = traci.trafficlight.getPhase("four-arm")

            if phase + 1 == 8:
                traci.trafficlight.setPhase("four-arm", 0)
            else:
                traci.trafficlight.setPhase("four-arm", phase + 1)           
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

    for vehID in traci.vehicle.getIDList(): 
        laneID = traci.vehicle.getLaneID(vehID)
        if laneID in trafficLight.getLanes():
            if traci.vehicle.getSpeed(vehID) == 0:
                if "_LT" in laneID:
                    vehID = vehID + "_L"
                else:
                    vehID = vehID + "_S"
        
            state[laneID].append(vehID)
            
    return state

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

