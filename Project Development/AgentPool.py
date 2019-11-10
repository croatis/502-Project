import os
import sys
import inspect
import PredicateSet as PredicateSet

class AgentPool:

    def __init__():
        self.isInit = 1

    def ownRuleSet():
        elementList = []
    
    def sharedRuleSet():
        elementList = []
    
    def userDefinedRuleSet():
        elementList = []
    

def run():
    methodList = inspect.getmembers(PredicateSet, predicate=inspect.isroutine)
    print(methodList)

if __name__ == "__main__":
    run()