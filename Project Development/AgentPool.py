import os
import sys
import inspect

from PredicateSet import PredicateSet
from EvolutionaryLearner import EvolutionaryLearner

class AgentPool:
    global _agentRuleSet = []
    global _sharedRuleSet = []
    global _userDefinedRuleSet = []

        # Intialize object variables
    def __init__(self, actionSet):
        self._actionSet = actionSet # a integer specifying number of actions available to AgentPool
        self._agentRuleSet()

    def getActionSet(self):
        return _actionSet

    def getAgentRuleSet(self):
        return _agentRuleSet
    
    def _setAgentRuleSet(self):
        _agentRuleSet = EvolutionaryLearner.initRuleSet(self)

    def fit(self):
        continue    

def run():
    methodList = inspect.getmembers(PredicateSet, predicate=inspect.isroutine)
    print(methodList)

if __name__ == "__main__":
    run()