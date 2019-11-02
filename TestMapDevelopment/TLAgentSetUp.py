# This script creates all the agents

import os
import sys
import optparse
import re

def run():
    setUp()

def setUp():
        # Get network file to parse
    fileName = input("Please enter the name of the desired network file: ")
        #ADD error checking for input (ensure it's a valid network file)

    # Open desired file
    f = open(fileName, "r")
    
    tlAgentPools = []
    trafficLightDict = {}
    edges = []
     # Parse file to gather information
    for x in f:
        # Determine agent pools
        if "<tlLogic" in x:
            temp = x.split("id=\"")
            trafficLightType = temp[1].split("\"")
            tlAgentPools.append(trafficLightType[0])

        # Gather info about individual traffic lights
        elif "<junction" and "type=\"traffic_light\"" in x:
            # isolate individual TLs
            temp = x.split("id=\"")
            trafficLightName = temp[1].split("\"")     #Traffic Light name; a key
            
            # get all edges controlled by TL
            splitForEdges = temp[1].split("incLanes=\"")
            edgesBulk = splitForEdges[1].split("\"")
            edgesSplit = edgesBulk[0].split()

            # Split edges into individual elements in a list
            for e in edgesSplit:
                edges.append(e)

            # Add traffic light and corresponding edges into the TL dictionary
            trafficLightDict.update({trafficLightName[0]: edges})
        
        else:
            continue
    
    for x in trafficLightDict:
        print(x, ": ", trafficLightDict[x])

    # print(tlAgentPools)
    # print(trafficLightNames)

    # main entry point
if __name__ == "__main__":
    run()