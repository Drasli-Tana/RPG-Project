# -*- coding: utf-8 -*-
# Code version 3.0.0
# class Inventaire en test
# ici code non graphique


class Inventaire:
    def __init__(self, classe, argent, taille = 3):
        """ classe qui va géré l'equipement et l'or du joueur """
        # selon la classe du personnage il aura pas les même objets
        # au lieu des None il y aura un dictionnaire avec
        # les caracteristiques de chaque objet
        self.argent = argent
        # self.inventaire = inventaire
        # L. 17: Ne marche pas: possibilité d'ajouter des clefs mais pas de
        # modifier les valeurs associées
        

        self.limit = taille + (
            1 if classe in ("guerrier", "orc") else 0)
        # on peut ajouter -1 pour les mages par exemple
        
        # selon le sac, le dictionnaire "backpack" sera plus ou moins grand
        # le joueur ne peut pas transporter plus que sa limite en objets
        # limite de base: 3 objets/ +1 si chevalier ou orc / +x selon force
        
        self.inventaire = {
            "sac": None,
            "main_principale": None,
            "main_secondaire": None,
            "bottes": None,
            "chapeau": None,  
            "ceinture": None,
            "anneau": None, 
            "amulette": None, 
            "plastron": None,
            "backpack": {None: self.limit}}
            # nombre d'espaces libres, vaut limite au départ
                
                    
        # On ajoute toutes les clefs nécessaires au dictionnaire

    def getInventory(self, emplacement = "all"):
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
    
    def getBackpack(self):
        return {
            key: self.inventaire["backpack"][key]
            for key in self.inventaire["backpack"]
            if key is not None} 
    
    def setBackpack(self, backpack: dict):
        self.inventaire["backpack"] = backpack

    def set_emplacement(self, emplacement, objet):
        """
        Change ce que porte le joueur dans <emplacement>
        """
        if emplacement not in self.inventaire:
            raise ValueError(f"L'emplacement: {emplacement} n'existe pas")
        self.inventaire[emplacement] = objet
    
    def addSlot(self, count = 1):
        if (self.limit + count <= 49):
            self.limit += count

    """ ---------------- Méthodes de gestion de l'argent ---------------- """
    def getArgent(self):
        return self.argent.value

    def setArgent(self, valeur):
        if self.argent.value + valeur < 0:
            raise ValueError("Impossible d'être à découvert!")
        
        else:
            with self.argent.get_lock():
                self.argent.value += valeur

    def addItem(self, item, data):
        backpack = self.inventaire["backpack"]
        if item in backpack or backpack[None] != 0:
            data["count"] = backpack.get(
                item, dict()).get("count", 0) + 1
            backpack[item] = data
            
            if item not in backpack:
                backpack[None] -= 1
        
        else:
            raise ArithmeticError("You've reached the inventory limit")
    
    def delItem(self, item):
        if item not in self.getBackpack():
            raise AttributeError(f"No item named {item}")
    
        else:
            data = dict(self.getBackpack())
            if data[item]["count"] == 1:
                del data[item]
            
            else:
                data[item]["count"] -= 1
            
            self.setBackpack(data)    
        