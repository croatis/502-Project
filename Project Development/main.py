import os
import sys
import InitSetUp 

import datetime
import timeit

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

    # --- TRAINING OPTIONS ---
    gui = False
    totalGenerations = 1
    gamma = 0.75
    batch_size = 100
    memory_size = 50000
    path = "./model/model_1_5x400_100e_075g/"  # nn = 5x400, episodes = 300, gamma = 0.75
    # ----------------------

    # Attributes of the simulation
    sumoNetworkName = "simpleNetwork.net.xml"
    maxGreenPhaseTime = 225
    maxYellowPhaseTime = 5


    # setting the cmd mode or the visual mode
    if gui == False:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    # initializations
    #sumoCmd = [sumoBinary, "-c", "intersection/tlcs_config_train.sumocfg", "--no-step-log", "true", "--waiting-time-memory", str(max_steps)]
    sumoCmd = [sumoBinary, "-c", "config_file.sumocfg", "--tripinfo-output", "tripinfo.xml"]
        
    print("PATH:", path)
    print("----- Start time:", datetime.datetime.now())
    setUpTuple = InitSetUp.run(sumoNetworkName)
    simRunner = Driver(sumoCmd, setUpTuple, maxGreenPhaseTime, maxYellowPhaseTime)
    episode = 0
    generations = 0
    allIndividualsTested = False

    # Evolutionary learning loop 
    while generations < totalGenerations:
        print('----- GENERATION {} of {}'.format(generations+1, totalGenerations))

        # Prepare for next simulation run
        allIndividualsTested = False
        for ap in setUpTuple[2]:
            for i in ap.getIndividualsSet():
                i.resetSelectedCount()
                print("Generation includes Individual:", i.getID())

        # Reinforcement learning loop
        while not allIndividualsTested:
            print('----- Episode {}'.format(episode+1))
            start = timeit.default_timer()
            resultingAgentPools = simRunner.run()  # run the simulation
            stop = timeit.default_timer()
            print('Time: ', round(stop - start, 1))
            episode += 1

            untested = []
            for ap in resultingAgentPools:
                for i in ap.getIndividualsSet():
                    if i.getSelectedCount() == 0:
                        untested.append(True)
                    else:
                        untested.append(False)
            
            if True not in untested:
                allIndividualsTested = True
                for ap in resultingAgentPools:
                    for i in ap.getIndividualsSet():
                        print(i, "has a selected count of:", i.getSelectedCount())

        for ap in setUpTuple[2]:
            for i in ap.getIndividualsSet():
                i.resetSelectedCount()
                print("Generation includes Individual:", i.getID())
        
        if generations + 1 < totalGenerations:
            EvolutionaryLearner.createNewGeneration(setUpTuple[2])     # Update agent pools with a new generation of individuals
        generations += 1        

    print("----- End time:", datetime.datetime.now())
    print("PATH:", path)
    # Do something to save session stats here