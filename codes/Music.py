import os

import logging as LG
import multiprocessing as MP
import playsound as PS
import random as RD
import time as TI
import codes.Logger as CD

class Music(MP.Process):
    def __init__(self, path = "ressources/sound/music/ambiance/"):
        """
        Rien de très complexe
        
        On commence par appeler le constructeur de la classe Process
        on fait ensuite une liste des musiques qui se trouvent dans
        le dossier de ressources (au format *.mp3)
        """
        super().__init__()
        
        self.path = path
        self.display = CD.Utils()
        self.sounds = [i for i in os.listdir(self.path) if i.endswith(".mp3")]
    
    def run(self):
        """
        Redéfinition de la méthode run, avec un effet semblable à:
            MP.Process(target=<function>)
        
        Ne sert qu'à lancer la boucle
        """
        self.running = True
        while self.running:
            if RD.randint(1, 10) == 1: 
                # 1 chance sur 10 de lancer la musique/seconde
                music = self.path + RD.choice(self.sounds) 
                self.display.debug(
                    "Music", f"Now playing: {music}"
                    )
                PS.playsound(music)
            
            else:
                TI.sleep(1)
    
    def terminate(self, *args, **kwargs):
        """
        Redéfinition de la méthode terminate, pour ajouter une sortie
        propre de la boucle
        """
        self.running = False
        return super().terminate(*args, **kwargs)
    
    def kill(self, *args, **kwargs):
        """
        Idem
        """
        self.running = False
        return super().kill(*args, **kwargs)

if __name__ == "__main__":
    a = Music()
    print("Creating new Process")
    a.start()
