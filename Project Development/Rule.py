import os
import sys

class Rule:

    def __init__(self, conditions, action, agentPool):
        self.conditions = conditions    # Set of predicates that determine if rule is true
        self.action = action            # Action to carry out if all conditions are true 
        self.agentPool = agentPool      # Agent pool rule originated from (used for updating actions of rule)
        self.weight = 0                 # Weight of rule (used during a TL agent's process of selecting a rule)
        self.timesSelected = 0          # Keep track of how many times a rule was selected

    def getConditions(self):
        return self.conditions
        
        # UPDATE RULE CONDITIONS
    def setConditions(self, conditions):
        self._conditions = conditions

    def getAction(self):
        return self.action
        
        # UPDATE RULE ACTION
    def setAction(self, action):
        self._action = action
    
    def getAgentPool(self):
        return self._agentPool
        
        # UPDATE AGENT POOL RULE ORIGINATED FROM
    def setAgentPool(self, agentPool):
        self.agentPool = agentPool
    
    def getWeight(self):
        return self.weight
        
        # UPDATE WEIGHT OF RULE AFTER SIMULATION RUN
    def updateWeight(self, weight):
        self.weight = weight
    
    def selected(self):
        self.timesSelected += 1
    
    def getTimesSelected(self):
        return self.timesSelected
    