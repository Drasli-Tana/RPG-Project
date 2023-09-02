"""
Created on 2 sept. 2023

@author: Thomas
"""
import random

class MyClass(object):
    def __init__(self, stats: dict):
        self.tooltip = stats.get("tooltip", "item.tooltip")
        self.damages = stats.get("degats", [0, 1])
        self.price = stats.get("prix", 0)
        self.name = stats.get("name", "item.name")
        self.slot = stats.get("slot", None)
        self.user = stats.get("usable") 
    
    def itemDamage(self):
        return random.randrange(1, 7)*self.damages[0] + self.damages[1]        