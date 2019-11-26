import os
import sys
from Rule import Rule
from random import randrange
from random import randint

global learningFactor
global discountRate

learningFactor = 0.1
discountRate = 0.1

def updateWeight(rule, nextRule, results):
        # Returns the updated weight based on the Sarsa learning method
    return (rule.getWeight() + learningFactor*(determineReward(rule,results) + (discountRate*nextRule.getWeight() - rule.getWeight())))

    # Function to determine the reward 
#*** Add in something for basing reward as performance relative to average rates in simulation maybe***
def determineReward(throughput, waitingTimeReduced):

