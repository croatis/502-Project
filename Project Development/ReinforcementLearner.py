import os
import sys
from Rule import Rule

global learningFactor           # Influences rate with which the weight value converges against the correct weight value
global discountRate             # Determines the emphasis on the importance of future evaluations 
global throughputFactor         # Determines the emphasis throughput has on the size of the reward
global waitTimeReducedFactor    # Determines the emphasis reduced waiting time has on the size of the reward

learningFactor = 0.1
discountRate = 0.1
throughputFactor = 1
waitTimeReducedFactor = 1

def updatedWeight(rule, nextRule, throughput, waitTimeReduced):
       # Returns the updated weight based on the Sarsa learning method
    updatedWeight = rule.getWeight() + learningFactor*(determineReward(throughput, waitTimeReduced) + (discountRate*nextRule.getWeight() - rule.getWeight()))
        
        # Ensure no rules have negative weights
    if updatedWeight < 0:
        return 0
    else:
        return updatedWeight

    # Function to determine the reward 
#*** Add in something for basing reward as performance relative to average rates in simulation maybe***
def determineReward(throughput, waitTimeReduced):
    return (throughputFactor*throughput + waitTimeReducedFactor*waitTimeReduced)

