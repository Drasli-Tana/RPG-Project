# classe s'occupant du combat
# mais en gros ça sera le combat en version code comme la
# classe Inventaire comparé à la classe Affichage_graphisme

from random import randint
from math import*
import codes.Logger as CL
import pygame # juste pour le chrono, oui je suis flemmard

class Combat:
    def __init__(self, stats_joueur, lvl, nombre, attaquant = "player", logger=None):
        """
        pour l'instant un truc basique
        gère juste les pv et l'attaque
        """
        if logger is None:
            self.logger = CL.Logger()
        
        else:
            self.logger = logger
            
        self.logger.log("Combat", "Debut du combat")

        self.stats_joueurs = stats_joueur # un seul joueur pour le moment
        self.lvl_monstre = lvl
        self.nombre_monstre = nombre
        self.monstre = {}  # contiendra les stats de chaque monstre

        self.running = True
        self.attaquant = attaquant # qui commence en premier (player ou monstre)
        
        self.debug = False
        
        # nouveau ajout
        self.numero_tour_actuel = 0
        self.attaquant_actuel = attaquant
        # differencie monstre0 de monstre1 comparé à self.attaquant

        self.monstre_mort = {}

        self.log = []  # mettra en liste le texte à afficher

    def generateur_monstre(self):
        # pas aléatoire pour le moment et ne prend pas en compte la difficulté
        for i in range(1, self.nombre_monstre + 1):
            self.monstre["monstre" + str(i)] = {"PV": 3, "AT": 8, "PI": 1}

    def affichage_monstre(self, monstre = "all"):
        if monstre == "all":
            return self.monstre
        
        else:
            return self.monstre[monstre]

    def affichage_joueur(self):
        return self.stats_joueurs

    def tour(self, entite, cible):
        # entite peut être : "player" ou "monstreX" (X le numéro)
        # on gère le cas avec un joueur unique sans allier
        if entite == "player":
            self.attaquant_actuel = "player"
            if cible != "personne":
                if self.attaque_joueur(cible):
                    self.update_jeu()
                
        else:
            for i in self.monstre:
                self.attaquant_actuel = "monstre" + str(i)
                self.attaque_monstre(i)
            self.update_jeu()
            self.attaquant = "player"
        
        return cible != "personne"
    
    def getLogs(self):
        return self.log
    
    def clearLogs(self):
        self.log.clear()
    
    def rollDice(self, AT, PI):
        dice = randint(1, 20)
        if dice == 1:
            # Coup critique
            degats = self.stats_joueurs["PI"] * 2
        
        elif dice <= self.stats_joueurs["AT"]:
            degats = self.stats_joueurs["PI"]
        
        else:
            # J'ai pas envie d'intégrer maintenant les échecs
            degats = 0
        
        self.logger.log("Combat", f"Résultat du dé: {dice}", 0)
            
        return (dice, degats)

    def attaque_joueur(self, cible):
        # si la cible n'existe pas on redemande au joueur
        if self.targetExists(cible):
            degat = self.rollDice(
                self.stats_joueurs["AT"],
                self.stats_joueurs["PI"])[1]
            
            self.monstre[cible]["PV"] -= degat

            self.logger.log("Combat", f"Le joueur fait {degat} dégats à {cible}", 0)
            self.log.append(f"Le joueur fait {degat} dégats à {cible}")
            self.attaquant = "monstre"
            self.numero_tour_actuel += 1

    def attaque_monstre(self, monstre):
        # pour le moment fait juste perdre des pv à joueur
        degat = self.rollDice(
                self.monstre[monstre]["AT"],
                self.monstre[monstre]["PI"])[1]
        self.stats_joueurs["PV"] -= degat
        self.logger.log("Combat", f"{monstre} fait {degat} dégats au joueur", 0)
        self.log.append(f"{monstre} fait {degat} dégats au joueur")
    
    def targetExists(self, target):
        return target in self.monstre

    def update_jeu(self):
        # gère la fin du jeu et le cas où le monstre à des pv négatif

        liste_monstre = []  # pour éviter une erreur de dictionnaire
        for i in self.monstre:
            liste_monstre.append(i)

        for i in liste_monstre:
            if self.monstre[i]["PV"] <= 0:
                self.monstre_mort[i] = self.monstre[i]
                self.monstre.pop(i)
                self.logger.log("Combat", f"{i} est mort")
                self.log.append(i + "est mort")

        if len(self.monstre) == 0:
            self.running = False
            self.logger.log("Comabt", "Le joueur à gagné", 0)
            self.log.append("Le joueur à gagné")

        elif self.stats_joueurs["PV"] <= 0:
            self.running = False
            self.logger.log("Comabt", "Les monstres ont gagné", 0)
            self.log.append("Les monstres ont gagné")
        
        
        self.logger.log("Combat", "\nEtat du jeu:", 0)
        self.logger.log("Combat", f"Stats du joueur: {self.affichage_joueur()}", 0)
        for i in self.monstre:
            self.logger.log("Combat", f"{i} stats : {self.affichage_monstre(i)}", 0)

if __name__ == "__main__":
    print("---- Combat en version console ---- \n")
    stats_joueur = {"PV":20, "AT":4}
    nombre_monstre = randint(1,3)
    lvl = 1  # difficulté
    tour = "player" # celui qui commence

    jeu = Combat(stats_joueur, lvl, nombre_monstre, tour)
    jeu.generateur_monstre()
    jeu.update_jeu()

    running = True
    while running:
        clock = pygame.time.Clock()
        fps = 1

        running = jeu.running
        tour = jeu.attaquant
        
        print("\nc'est le tour de: ", tour)
        cible = None
        if tour == "player":
            cible = input("Entrer la cible à attaquer : \n")

        jeu.tour(tour, cible)
        running = jeu.running

        clock.tick(fps)
