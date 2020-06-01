import os
import sys
import InitSetUp 
import OutputManager

import datetime
import timeit
import time

from Driver import Driver
import EvolutionaryLearner


# Importing needed python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")


from sumolib import checkBinary  # Checks for the binary in environ vars
import traci

if __name__ == "__main__":
    print("Working...")
    # --- TRAINING OPTIONS ---
    gui = True
    totalGenerations = 1
    individualRunsPerGen = 1  # Min number of training runs an individual gets per generation
    # ----------------------

    # Attributes of the simulation
    sumoNetworkName = "simpleNetwork.net.xml"
    maxGreenPhaseTime = 225
    maxYellowPhaseTime = 5
    maxSimulationTime = 10000
    runTimeSet = []


    # setting the cmd mode or the visual mode
    if gui == False:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    # initializations
    #sumoCmd = [sumoBinary, "-c", "intersection/tlcs_config_train.sumocfg", "--no-step-log", "true", "--waiting-time-memory", str(max_steps)]
    sumoCmd = [sumoBinary, "-c", "config_file.sumocfg", "--waiting-time-memory", "5", "--time-to-teleport", "-1"]
    generationRuntimes = []
    generations = 1

while generations <= totalGenerations:
    print("----- Start time:", datetime.datetime.now())
    setUpTuple = InitSetUp.run(sumoNetworkName, individualRunsPerGen)
    genStart = datetime.datetime.now()

    for tl in setUpTuple[1]:
        tl.setMaxRedPhaseTime(maxGreenPhaseTime, maxYellowPhaseTime)
        tl.initPhaseTimeSpentInRedArray()

    simulationStartTime = datetime.datetime.now()

    # Evolutionary learning loop 
    print("This simulation began at:", simulationStartTime)
    genStart = datetime.datetime.now()
    startTime = time.time()

    simRunner = Driver(sumoCmd, setUpTuple, maxGreenPhaseTime, maxYellowPhaseTime)

    print("Generation start time:", genStart)
    start = timeit.default_timer()
    simRuntime = simRunner.run()  # run the simulation
    stop = timeit.default_timer()
    print('Time: ', round(stop - start, 1))

    sys.stdout.flush()               

    print("Start time:", simulationStartTime, "----- End time:", datetime.datetime.now())
    print("This simulation began at:", simulationStartTime)
    generationRuntimes.append(simRuntime)
    generations += 1
print(generationRuntimes)
print("Average simulation time is", sum(generationRuntimes)/(generations-1))
    # Do something to save session stats here