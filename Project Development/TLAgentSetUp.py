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
    # fileParser(fileName)

# def fileParser(fileName):

    # Open desired file
    f = open(fileName, "r")
    
    lanes = []
    trafficLights = []
    # Parse file to gather information about traffic lights, and instantiate their objects
    for x in f:
        # Gather info about individual traffic lights
        if "<junction" and "type=\"traffic_light\"" in x:
            # isolate individual TLs
            temp = x.split("id=\"")
            trafficLightName = temp[1].split("\"")     #Traffic Light name

            # get all lanes controlled by TL
            splitForlanes = temp[1].split("incLanes=\"")
            lanesBulk = splitForlanes[1].split("\"")
            lanesSplit = lanesBulk[0].split()

            # Split lanes into individual elements in a list
            for l in lanesSplit:
                lanes.append(l)

            # **ADD IN GETTING TL PHASES**
            trafficLights.append(TrafficLight(trafficLightName[0], lanes))
            lanes = []
        
        else:
            continue
    
        # Close file once finished
    f.close()

    return trafficLights
    
# main entry point
if __name__ == "__main__":
    run()