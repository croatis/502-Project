# This script creates all the agents

import os
import sys
import optparse
import re

from TrafficLight import TrafficLight
from AgentPool import AgentPool
from Rule import Rule

def run(sumoNetworkName):
    tlAgentPoolList = []
    trafficLightDict = {}
    userDefinedRules = []
        
        # Parse user defined rules file and create rules for each
    f = open("UserDefinedRules.txt", "r")
        # Parse file to gather information about traffic lights, and instantiate their objects
    for x in f:
            # Ignore comment sections of input file
        if "//" in x:
            continue
            # For each user defined rule, create a rule with its conditions
        elif "udr" in x:
            ruleComponents = x.split(": ")
            ruleComponents = ruleComponents[1].split()
            userDefinedRules.append(Rule([ruleComponents[0]], -1, None)) # User defined rules have only defined conditions; actions are predefined in Driver.py and they apply to all Agent Pools
            print("The rule being added is:", ruleComponents[0], ".")
    f.close() # Close file before moving on

        
        # Get SUMO network file to parse
    # fileName = input("Please enter the name of the desired network file: ")

#ADD error checking for input (ensure it's a valid network file)

    # Open desired file
    f = open(sumoNetworkName, "r")
    
    lanes = []
    trafficLights = []
    tlPhases = {}
    # Parse file to gather information about traffic lights, and instantiate their objects
    for x in f:
            # Create an action set dictionary for each traffic light
        if "<tlLogic" in x:
            getTLName = x.split("id=\"")
            tlNameArray = getTLName[1].split("\"")
            tlPhases[tlNameArray[0]] = []
                
                # Count number of phases/actions a TL has; loop max is arbitrarily high given phase number uncertainty 
            for i in range(0, 1000):
                x = f.readline()
                    # For each phase, record its phase name
                if "<phase" in x:
                    phaseNameSplit = x.split("name=")
                    phaseName = phaseNameSplit[1].split("\"")
                    tlPhases[tlNameArray[0]].append(phaseName[1])
                else:
                    break

            # Gather info about individual traffic lights
        elif "<junction" and "type=\"traffic_light\"" in x:
                # Isolate individual TLs
            temp = x.split("id=\"")
            trafficLightName = temp[1].split("\"") #Traffic Light name

                # Get all lanes controlled by TL
            splitForlanes = temp[1].split("incLanes=\"")
            lanesBulk = splitForlanes[1].split("\"")
            lanesSplit = lanesBulk[0].split()

                # Split lanes into individual elements in a list
            for l in lanesSplit:
                lanes.append(l)

            trafficLights.append(TrafficLight(trafficLightName[0], lanes))
            lanes = []

        else:
            continue
    
    f.close() # Close file once finished

        # Set number of phases for each traffic light
    for x in tlPhases:
        for tl in trafficLights:
            if x == tl.getName():
                tl.setPhases(tlPhases[x])
    
        # Create and assign agent pools    FYI: THIS ASSUMES PHASE NUMBER = SAME POOL; LIKELY NOT TRUE
    agentPools = []
    for tl in trafficLights:
        apAssigned = False
            # If agent pool(s) already exist, check to see its ability to host the traffic light
        if len(agentPools) > 0:    
            for ap in agentPools:
                    # An agent pool can realistically host more than one traffic light iff at minimum all TL's using the pool share the same number of phases
                if tl.getPhases() == ap.getActionSet(): 
                    tl.assignToAgentPool(ap)
                    ap.addNewTrafficLight(tl)
                    apAssigned = True
                    break
        
        if apAssigned == False:
            apID = "AP" + str(len(agentPools) + 1) # Construct new agent ID
            agentPool = AgentPool(apID, tl.getPhases()) # Create a new agent pool for traffic light
            agentPool.addNewTrafficLight(tl) # Assign traffic light to agent pool 
            
            agentPools.append(agentPool) # Add new pool to agent pools list
        

    return (userDefinedRules, trafficLights, agentPools)
    
# main entry point
if __name__ == "__main__":
    run()