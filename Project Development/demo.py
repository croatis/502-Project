#!/usr/bin/env python

import os
import sys
import optparse

# we need to import some python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")


from sumolib import checkBinary  # Checks for the binary in environ vars
import traci

FOURARM_STR_NS_G = 0
FOURARM_STR_NS_Y = 1
FOURARM_LT_NS_G = 2
FOURARM_LT_NS_Y = 3
FOURARM_STR_EW_G = 4
FOURARM_STR_EW_Y = 5
FOURARM_LT_EW_G = 6
FOURARM_LT_EW_Y = 7


def get_options():
    opt_parser = optparse.OptionParser()
    opt_parser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = opt_parser.parse_args()
    return options

# SET IN SUMO THE CORRECT YELLOW PHASE
def _set_yellow_phase(self, old_action):
    yellow_phase = old_action * 2 + 1 # obtain the yellow phase code, based on the old action
    traci.trafficlight.setPhase("TL", yellow_phase)

# SET IN SUMO A GREEN PHASE
def _set_green_phase(self, action_number):
    if action_number == 0:
        traci.trafficlight.setPhase("TL", PHASE_NS_GREEN)
    elif action_number == 1:
        traci.trafficlight.setPhase("TL", PHASE_NSL_GREEN)
    elif action_number == 2:
        traci.trafficlight.setPhase("TL", PHASE_EW_GREEN)
    elif action_number == 3:
        traci.trafficlight.setPhase("TL", PHASE_EWL_GREEN)


# contains TraCI control loop
def run():
    
    step = 0
    edgeDensity = []
    edges = traci.edge.getIDList() 
    trafficLights = traci.trafficlight.getIDList()
    time = traci.simulation.getCurrentTime()

    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        # print(step)

        if step % 5 == 0:
            carsWaiting = traci.edge.getWaitingTime
            # print(carsWaiting)
            phase = traci.trafficlight.getPhase("4-arm")

            if phase + 1 == 8:
                traci.trafficlight.setPhase("4-arm", 0)
            else:
                traci.trafficlight.setPhase("4-arm", phase + 1)           
        else:
            pass

        step+=1
    
    fourArmLanes = traci.trafficlight.getControlledLanes("4-arm")
    print(fourArmLanes)

    traci.close()
    sys.stdout.flush()


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

