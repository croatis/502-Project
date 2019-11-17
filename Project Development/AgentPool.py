import os
import sys
import inspect

from PredicateSet import PredicateSet
from EvolutionaryLearner import EvolutionaryLearner

class AgentPool:
    global _agentRuleSet = []
    global _sharedRuleSet = []
    global _userDefinedRuleSet = []

    def __init__(self, actionSet):
        self.actionSet = actionSet
        self.setAgentRuleSet()

    def getActionSet():
        return actionSet

    def setAgentRuleSet():
        agentRuleSet = EvolutionaryLearner.initRuleSet(self.actionSet)

    def fit():
        continue    

def run():
    methodList = inspect.getmembers(PredicateSet, predicate=inspect.isroutine)
    print(methodList)

if __name__ == "__main__":
    run()