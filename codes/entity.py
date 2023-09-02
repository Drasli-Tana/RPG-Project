"""
Created on 25 mars 2022

@author: Thomas
"""
import os
import json as JS
import random as RD

import codes.inventaire as CI

class Entity:
    def __init__(self, **kwargs):
        # On crée ou charge les stats de base du personnage
        self.classe = kwargs.get("name", "orc")
        self.inventaire = None
        self.stats = self.loadData(kwargs.get(
            "save",
            os.path.join(
                "ressources", "data", "entities", f"{self.classe}.json"
            )))
        
        self.stats["xp"] = self.stats.get("xp", 0)

        for caract in ["COU", "AD", "FO", "INT"]:
            self.stats[caract] = self.stats.get(
                caract, RD.randint(1, 6) + 7)
    
    def __str__(self):
        return f"{self.classe}: {self.stats}"
            
    def loadData(self, path):
        with open(path, mode = "r") as file:
            return JS.load(file)

    def getClass(self):
        return self.classe
    
    def getInventaire(self):
        return self.inventaire

    def setInventaire(self, inventaire: CI.Inventaire):
        self.inventaire = inventaire
    
    def getStats(self):
        return self.stats

    
    