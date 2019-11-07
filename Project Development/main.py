#!/usr/bin/env python

import os
import sys
import optparse

import TLAgentSetUp as TLAgentSetUp

# Importing needed python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")


from sumolib import checkBinary  # Checks for the binary in environ vars
import traci


# CONTAINS MAIN TRACI SIMULATION LOOP
def run():
    # Acquire agent pool dictionary 
    agentPool = TLAgentSetUp.run()
    print(agentPool) 
    
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
    print(traci.vehicle.getIDList())
    traci.close()
    sys.stdout.flush()
    
# RETRIEVE THE STATE OF THE INTERSECTION FROM SUMO
def _get_state(self, trafficLight):
    state = {}
    for lane in trafficLight.lanes():
        state[lane] = []

    for vehID in traci.vehicle.getIDList(): 
        laneID = traci.vehicle.getLaneID(vehID)
        
        if laneID in trafficLight.getLanes():
            lanePos = traci.vehicle.getLanePosition(vehID)
            lanePos = 750 - lanePos  # inversion of lane pos, so if the car is close to TL, lanePos = 0
            laneGroup = -1  # just dummy initialization
            validCar = False  # flag for not detecting cars crossing the intersection or driving away from it

            # distance in meters from the TLS -> mapping into cells
            if lanePos < 7:
                laneCell = 0
            elif lanePos < 14:
                laneCell = 1
            elif lanePos < 21:
                laneCell = 2
            elif lanePos < 28:
                laneCell = 3
            elif lanePos < 40:
                laneCell = 4
            elif lanePos < 60:
                laneCell = 5
            elif lanePos < 100:
                laneCell = 6
            elif lanePos < 160:
                laneCell = 7
            elif lanePos < 400:
                laneCell = 8
            elif lanePos <= 750:
                laneCell = 9

            # finding the lane where the car is located - _max is the "turn left only" lanes if iot exists
                
                # EDIT THIS TO MAKE DYNAMIC FOR ANY TL
            if laneID == "W2TL_0" or laneID == "W2TL_1" or laneID == "W2TL_2":
                laneGroup = 0
            elif laneID == "W2TL_3":
                laneGroup = 1
            elif laneID == "N2TL_0" or laneID == "N2TL_1" or laneID == "N2TL_2":
                laneGroup = 2
            elif laneID == "N2TL_3":
                laneGroup = 3
            elif laneID == "E2TL_0" or laneID == "E2TL_1" or laneID == "E2TL_2":
                laneGroup = 4
            elif laneID == "E2TL_3":
                laneGroup = 5
            elif laneID == "S2TL_0" or laneID == "S2TL_1" or laneID == "S2TL_2":
                laneGroup = 6
            elif laneID == "S2TL_3":
                laneGroup = 7

            if laneGroup >= 1 and laneGroup <= 7:
                vehPosition = int(str(laneGroup) + str(laneCell))  # composition of the two postion ID to create a number in interval 0-79
                validCar = True
            elif laneGroup == 0:
                vehPosition = laneCell
                validCar = True

            if validCar:
                state[vehPosition] = 1  # write the position of the car vehID in the state array

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

