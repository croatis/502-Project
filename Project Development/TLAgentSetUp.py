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
    # Parse file to gather information
    for x in f:
        # Determine agent pools
        if "<tlLogic" in x:
            temp = x.split("id=\"")
            trafficLightType = temp[1].split("\"")
            
            if "(" in trafficLightType:
                isolateAgentName = trafficLightType.split("(")
                trafficLightType = isolateAgentName[0]
            
            tlAgentPoolList.append(trafficLightType[0])

        # Gather info about individual traffic lights
        elif "<junction" and "type=\"traffic_light\"" in x:
            # isolate individual TLs
            temp = x.split("id=\"")
            trafficLightName = temp[1].split("\"")     #Traffic Light name; a key
            
            # get all lanes controlled by TL
            splitForlanes = temp[1].split("incLanes=\"")
            lanesBulk = splitForlanes[1].split("\"")
            lanesSplit = lanesBulk[0].split()

            # Split lanes into individual elements in a list
            for e in lanesSplit:
                lanes.append(e)

            # Add traffic light and corresponding lanes into the TL dictionary
            trafficLightDict.update({trafficLightName[0]: lanes})
            lanes = []
        
        else:
            continue
    
    # for x in trafficLightDict:
    #     print(x, ": ", trafficLightDict[x])

        # Close file once finished
    f.close()

# def createAgentPools():
    tlAgentPools = {}

    for agentPool in tlAgentPoolList:
        tlAgentPools[agentPool] = []
    
    for tl in trafficLightDict:
        for ap in tlAgentPoolList:
            if tl in ap:
                newTL = TrafficLight(ap, tl, trafficLightDict[tl])
                tlAgentPools[ap].append(newTL)
                newTL = TrafficLight(ap, tl, trafficLightDict[tl])
                tlAgentPools[ap].append(newTL)                

        # print("tlAgentPools conains this: ", tlAgentPools)

    
    for x in tlAgentPools:
        tl = tlAgentPools[x]
        print("Pool", x, "contains: \n", "Traffic light", tl[0].getName(), "of type", tl[0].getType(), "with lanes", tl[0].getLanes(), "\n")
# main entry point
if __name__ == "__main__":
    run()