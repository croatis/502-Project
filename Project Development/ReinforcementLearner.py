import os
import sys
import math
from Rule import Rule

global learningFactor           # Influences rate with which the weight value converges against the correct weight value
global discountRate             # Determines the emphasis on the importance of future evaluations 
global throughputFactor         # Determines the emphasis throughput has on the size of the reward
global waitTimeReducedFactor    # Determines the emphasis reduced waiting time has on the size of the reward

learningFactor = 0.5
discountRate = 0.5
throughputFactor = 1
waitTimeReducedFactor = 1

def updatedWeight(rule, nextRule, throughput, waitTimeReduced):
       # Returns the updated weight based on the Sarsa learning method
    updatedWeight = rule.getWeight() + (learningFactor*(determineReward(throughput, waitTimeReduced) + (discountRate*nextRule.getWeight() - rule.getWeight())))

    return updatedWeight * 0.0001 # Numbers are reduced by 90% to keep them managable

    # Function to determine the reward 
#*** Add in something for basing reward as performance relative to average rates in simulation maybe***
def determineReward(throughput, waitTimeReduced):
    return (throughputFactor*throughput + waitTimeReducedFactor*waitTimeReduced)

