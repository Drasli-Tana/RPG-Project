"""
Created on 25 mars 2022

@author: Thomas
"""
class Entity(pygame.Sprite):
    chemin = "ressources\\images\\personnages\\"
    # Le chemin vers les images
    personnage = {
        "mage": chemin + "mage.png",
        "orc": chemin + "orc.png",
        "chevalier": chemin + "chevalier.png",
        "sorcière": chemin + "sorcière.png",
        "paladin": chemin + "paladin.json"}
    # dictionnaire contenant tous les personnages possibles
    def __init__(self, **kwargs):
        super().__init__()
        self.classe = kwargs.get("name", "orc")
        self.inventaire = None
        
        typeEntity = kwargs.get("type", "monster")
        with open(f"ressources/data/entities/{typeEntity}/{self.classe}.json",
                  mode = "r") as file:
            
            self.stats = JS.load(file)

            self.stats["description"] = "".join(self.stats["description"])

            for caract in ["COU", "AD", "FO", "INT"]:
                self.stats[caract] = RD.randint(1, 6) + 7
            
            