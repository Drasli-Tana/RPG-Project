# Code version 3.0.0
import multiprocessing as MP
import subprocess as SP
import tkinter as Tk # si jamais on a besoin
import importlib as IL
import sys

import os 
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame
import random as RD
import json as JS

import codes.Logger as CL
from codes.Game import Game

# j'ai ajouté un nouveau dictionnaire pour les images
def fenetre_principale(**kwarg):
    game = Game(kwarg)
    game.run()

def loadJsonStuff(path = "./", logger = None):
    tree = [i for i in os.listdir(path) if os.path.isdir(path + i) or i.endswith(".json")]
    for i in tree:
        if os.path.isdir(path + i):
            loadJsonStuff(path + i + "/", logger)
        
        else:
            with open(path + i) as file:
                data = JS.load(file)
                try:
                    name = data["name"]
                
                except KeyError:
                    logger.log(
                        "Shop", f"Skipped invalid file: {path + i}", 0)
                
                else:
                    logger.log(
                        "Shop", f"Successfully loaded file: {path + i}", 0)
                    
                    with open("ressources/data/items.json") as file2:
                        listFiles = JS.load(file2)
                    
                    listFiles.update({name: path + i})
                    
                    with open("ressources/data/items.json", 'w') as file2:
                        JS.dump(listFiles, file2, indent = 4)


if __name__ == "__main__":
    debug = True
    # Passer en mode debug? Devrait être désactivé par défaut, et sera déplacé
    # dans un fichier de configuration dans une future mise à jour
    pygame.init()
    
    logger = CL.Logger(level=(0 if debug else 1))
    
    argent = MP.Value('f', RD.randrange(1, 30))
    # gros bricolage en cours
    manager = MP.Manager()
    inv = manager.dict()
    images_item = manager.dict()
    
    logger.log("Main", "Initializing main Process")
    
    logger.log("Shop", "Loading Item files")
    with open("ressources/data/items.json", "w") as file:
        JS.dump({}, file, indent = 4)
    
    loadJsonStuff("ressources/data/stuff/", logger)
    logger.log("Shop", "Loaded Item files")
    
    # en phase de test
    processus_1 = MP.Process(
        target = fenetre_principale,
        kwargs = {
            "argent": argent,
            "inventaire": inv,
            "images_item": images_item,
            "logger": logger
            })
    
    processus_1.start()
    logger.start()
    processus_1.join()
    
    logger.stop()
    del os.environ['PYGAME_HIDE_SUPPORT_PROMPT']
    