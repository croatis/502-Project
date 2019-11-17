# This script creates all the agents

import os
import sys
import optparse
import re

from TrafficLight import TrafficLight

def run():
    tlAgentPoolList = []
    trafficLightDict = {}
    global tlAgentPools

        # Get network file to parse
    fileName = input("Please enter the name of the desired network file: ")

#ADD error checking for input (ensure it's a valid network file)

    # Open desired file
    f = open(fileName, "r")
    
    lanes = []
    trafficLights = []
    tlPhases = {}
    # Parse file to gather information about traffic lights, and instantiate their objects
    for x in f:
            # Create an action set dictionary for each traffic light
        if "<tlLogic" in x:
            getTLName = x.split("id=\"")
            tlNameArray = getTLName[1].split("\"")
            tlPhases[tlNameArray[0]] = 0
                # Count number of phases/actions a TL has; loop max is arbitrarily high given phase number uncertainty 
            for i in range(0, 1000):
                x = f.readline()
                if "<phase" in x:
                    tlPhases[tlNameArray[0]] += 1
                else:
                    break

            # Gather info about individual traffic lights
        elif "<junction" and "type=\"traffic_light\"" in x:
                # Isolate individual TLs
            temp = x.split("id=\"")
            trafficLightName = temp[1].split("\"")     #Traffic Light name

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
    
    return trafficLights
    
# main entry point
if __name__ == "__main__":
    run()