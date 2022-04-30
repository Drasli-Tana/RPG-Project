# -*- coding: utf-8 -*-
# Code version 3.0.0
# class Inventaire en test
# ici code non graphique


class Inventaire:
    def __init__(self, classe, argent, inventaire, taille = 3):
        """ classe qui va géré l'equipement et l'or du joueur """
        # selon la classe du personnage il aura pas les même objets
        # au lieu des None il y aura un dictionnaire avec
        # les caracteristiques de chaque objet
        
        self.argent = argent
        self.inventaire = inventaire
        # self.inventaire = inventaire
        # L. 17: Ne marche pas: possibilité d'ajouter des clefs mais pas de
        # modifier les valeurs associées
        
        if classe in ("chevalier", "orc"):
            self.limit = taille + 1
        
        else:
            self.limit = taille + 0
            # on peut ajouter -1 pour les mages par exemple
        # selon le sac, le dictionnaire "equipement" sera plus ou moins grand
        # le joueur ne peut pas transporter plus que sa limite en objets
        # limite de base: 3 objets/ +1 si chevalier ou orc / +x selon force
        
        possession = {
            "sac": None,
            "main_principale": None,
            "main_secondaire": None,
            "bottes": None,
            "chapeau": None,  
            "ceinture": None,
            "anneau": None, 
            "amulette": None, 
            "plastron": None,
            "equipements": {
                "rien": self.limit
                },
            # nombre de vide, vaut limite au départ
            }
        
        self.inventaire.update(possession)
        # On ajoute toutes les clefs nécessaires au dictionnaire

    def get_possessions(self, emplacement = "all"):
        """
        retourne l'objet porté à un certain emplacement ou tous les objets
        """
        if emplacement == "all":
            return self.inventaire
        
        else:
            if emplacement in self.inventaire:
                return self.inventaire[emplacement]

            else:
                raise ValueError(f"L'emplacement: {emplacement} n'existe pas")
    
    def getLimit(self):
        return self.limit
    
    def getInventory(self):
        return {i: self.inventaire["equipements"][i]
                for i in self.inventaire["equipements"]
                if i != "rien"}

    def set_emplacement(self, emplacement, nouveau_objet):
        """
        Change ce que porte le joueur dans <emplacement>
        """
        if emplacement not in self.inventaire:
            raise ValueError(f"L'emplacement: {emplacement} n'existe pas")
        self.inventaire[emplacement] = nouveau_objet
    
    def addSlot(self, count = 1):
        self.limit += count

    """ ---------------- Méthodes de gestion de l'argent ---------------- """
    def get_argent(self):
        return self.argent.value

    def set_argent(self, valeur):
        if self.argent.value + valeur < 0:
            raise ValueError("Impossible d'être à découvert!")
        
        else:
            with self.argent.get_lock():
                self.argent.value += valeur

    def addItem(self, item, data):
        a = dict(self.inventaire["equipements"])
        if item in self.inventaire["equipements"]:
            data["count"] = a[item]["count"] + 1
            a[item] = data
            
        elif len(self.inventaire["equipements"]) <= self.limit:
            a[item] = data
            a[item]["count"] = 1
        
        else:
            raise ArithmeticError("You've reached the inventory limit")
        
        self.inventaire["equipements"] = a
    
    def delItem(self, item):
        if item not in self.inventaire["equipements"]:
            raise AttributeError(f"No item named {item}")
    
        else:
            data = dict(self.inventaire["equipements"])
            if data[item]["count"] == 1:
                del data[item]
            
            else:
                data[item]["count"] -= 1
            
            self.inventaire["equipements"] = data    
        