import os
import sys
import optparse
import traci

def run(agentPools):
    avgGenRuntime = 0
    finalGenRuntime = 0

    # Create new output file and add generation runtime information 
    f = open("simOutputData", "w")
    f.write("Final Generation Stats\n\nGeneration runtime:", finalGenRuntime, "\nAverage Generation runtime:", avgGenRuntime, "\n---------------------------\n\nBest Individuals per Agent Pool\n")

    for ap in agentPools:
        f.write("Agent Pool", ap.getID(), "\n")
        individuals = ap.getIndividualsSet()
        topIndividual = max(individuals, key=attrgetter('getFitness'))
        f.write("The top individual's RS and RSint sets contain the following rules (formatted as \"<conditions>, <action>\"):\n\n RS:\n")
        
        ruleCount = 1
        for rule in topIndividual.getRuleSet():
            f.write("Rule", ruleCount, ": <", rule.getConditions(), ">, <", rule.getAction(), ">\n\n")
            ruleCount += 1

        f.write("RSint:\n")
        ruleCount = 1
        for rule in topIndividual.getRuleSet():
            f.write("Rule", ruleCount, ": <", rule.getConditions(), ">, <", rule.getAction(), ">\n\n")
            ruleCount += 1

        f.write("*******\n")

if __name__ == "__main__":
    run()
