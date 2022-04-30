import time as TI
import multiprocessing as MP
from ctypes import windll
import _queue
import os 
import json

class Logger(MP.Process):
    levels = {
        0: "DEBUG",
        1: "INFO",
        2: "WARNING",
        3: "ERROR",
        4: "CRITICAL"}
    
    def __init__(self, level=1):
        super().__init__()
        self.check = 0    # Utilisé par les checkPoints
        self.toWrite = MP.Queue()
        self.running = True
        self.level = level  # Le niveau d'affichage des logs
        self.log("Logger", "Initialised logger by Thomas", 1)
        
        self.quit = self.createLine("Logger", "Shutting down the logger", 1)
        
    def createLine(self, thread, message, level):
        return f"[Thread {thread}/{Logger.levels.get(level)}] {message}\n"
    
    def run(self):
        with open("ressources/data/logger/alphabet.json", mode="r") as file:
            self.checkpoints = json.load(file)
        
        date = TI.strftime("%d-%m-%Y")
        self.filename = "logs/" + date
        fichiers = len([fichier for fichier in os.listdir("logs/")
                         if date in fichier])
        
        if fichiers > 0:
            self.filename += "_" + str(fichiers)
        
        self.filename += ".log"
        
        while self.running:
            ligne = self.toWrite.get(block=True)
            if ligne == self.quit:
                self.running = False
            
            #TI.sleep(.05)            
            with open(self.filename, mode="a") as file:
                file.write(ligne)
                print(ligne, end="")
                    
    def log(self, thread, message, level=1):
        if level >= self.level:
            ligne = self.createLine(thread, message, level)
            self.toWrite.put(ligne)
        
    def stop(self):
        self.toWrite.put(self.quit)
        
        
    """
    Deux méthodes permettant un debuging (un peu) plus simple:
        On appelle une méthode, et un compteur s'incrémente pour
        Signaler un point atteint dans le code (doit être appelé
        manuellement)
        
        On peut aussi choisir de ne pas augmenter le compteur, dans une
        boucle par exemple
    
    Si le nom du point de passage (oui, c'est la traduction de checkpoint)
        n'est pas spécifié, utilise les lettres de l'alphabet aéronautique
        (parce que c'est plus drôle) sous la forme X-X-X, avec autant de X
        que nécessaire -> si le compteur augmente, il faudra de plus en plus
        de lettres. Minimum: une lettre
    """
    def _get26Pow(self, number):
        if number < 26:
            return [number]
        
        else:
            return self._get26Pow(number // 26 - 1) + [number % 26]
        
    def checkpoint(self, name=None, increaseCount=True):
        if name is None:
            name = "-".join(
                [self.checkpoints[i] for i in self._get26Pow(self.check)])
        
        print(f"Checkpoint {name}")        
        if increaseCount:
            self.check += 1
        
if __name__ == "__main__":
    a = Logger()
    a.start()
    for i in range(64):
        a.checkpoint()
    
    a.log("Test", "Un simple texte", 4)
    
    
    