# Code version 3.0.0
# j'ai enlevé la classe animation_sprite pour le moment
# je la remettrai plus tard dans le jeu

import pygame
import json as JS
import random as RD

from codes.animation_sprite import*

class Player(pygame.sprite.Sprite): #Animation_sprite):
    """
    Classe en test, d'après Hamza
    """
    chemin = "ressources\\images\\personnages\\"
    # Le chemin vers les images
    personnage = {
        "mage":      chemin + "mage_2.png",
        "orc":       chemin + "orc.png",
        "chevalier": chemin + "chevalier.png",
        "sorcière":  chemin + "sorcière.png"}
    # dictionnaire contenant tous les personnages possibles

    def __init__(self, x, y, name = "mage", frames = 3):
        """
            x, y: coordonnées dans le plan
            name: la "classe" du personnage
            frames: Nombre d'images disponibles par animation
                (pour le déplacement)
        """
        super().__init__()
        self.classe = name
        self.inventaire = None

        # On crée ou charge les stats de base du personnage
        with open(
            "ressources/data/statsPlayer.json", "r", encoding="utf-8"
            ) as file:
            self.stats = JS.load(file)[name]

            self.stats["description"] = "".join(self.stats["description"])

        for caract in ["COU", "AD", "FO", "INT"]:
            self.stats[caract] = RD.randint(1, 6) + 7


        self.sprite_sheet = pygame.image.load(Player.personnage[name])

        # paramétrage de l'image du personnage
        # là on laisse comme ça mais il faudra généraliser si on ajoute monstre
        self.image = self.get_image(0, 0)
        self.image.set_colorkey([0, 0, 0]) # enlever le fond noir du perso
        self.rect = self.image.get_rect()
        self.position = [x,y]
        self.frame_actuelle = 0
        self.frames = frames

        # reaction lors de collision
        self.feet = pygame.Rect(0, 0, self.rect.width*0.5, 12 )
        self.old_position = self.position.copy()

        self.speed = 4 # default: 4
        self.coefficient = 0 # pour ralentir fps de l'animation
        # au départ pas d'animation lors de la création du perso
        self.anime = False

        self.old_direction = "down"

    def save_location(self):
        self.old_position = self.position.copy()
    
    def getStats(self):
        return self.stats

    def animation_deplacement(self, direction, old_direction):
        self.coefficient += 0.3 # default: 0.16
        # pour ralentir fps de l'animation

        self.frame_actuelle = 32 * (round(self.coefficient) % 3)

        self.images = {
            "down":  self.get_image(self.frame_actuelle, 0),
            "left":  self.get_image(self.frame_actuelle, 32),
            "right": self.get_image(self.frame_actuelle, 64),
            "up":    self.get_image(self.frame_actuelle, 96),
             }
        
        self.coefficient %= 3

        #  ce que j'ai ajouté, permet de s'arrêter pour le joueur
        self.anime = direction != "stop"
        
        if not self.anime:
            self.frame_actuelle = 0
            y = {"down": 0, "left": 32, "right": 64, "up": 96}[old_direction]
            self.images["stop"] = self.get_image(32, y)

        if self.anime and direction != old_direction:
            self.old_direction = direction
            
        return self.images[direction]

    def change_animation(self, direction):
        """
        Change l'image du personnage en fonction de la direction
        """
        self.image = self.animation_deplacement(direction, self.old_direction)
        self.image.set_colorkey([0, 0, 0])

    def getClass(self):
        return self.classe

    def getInventaire(self):
        return self.inventaire_player

    def __str__(self):
        return "It's a custom player"

    """
    Déplacement du personnage
    """
    def move_right(self):
        self.position[0] += self.speed
        self.change_animation("right")

    def move_left(self):
        self.position[0] -= self.speed
        self.change_animation("left")

    def move_up(self):
        self.position[1] -= self.speed
        self.change_animation("up")

    def move_down(self):
        self.position[1] += self.speed
        self.change_animation("down")

    def move_stop(self):
        # pour que le joueur ne s'arrete pas en deplacement
        if self.anime:
            self.change_animation("stop")
    
    def move_back(self):
        self.position = self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom
    
    def get_image(self, x, y):
        # découpage et sélection de l'image du perso
        image = pygame.Surface([32, 32])
        image.blit(self.sprite_sheet, (0,0), (x, y, 32, 32))

        return image

    def setInventaire(self, inventaire):
        self.inventaire_player = inventaire

    # les mêmes noms qu'inventaire mais bon...
    def get_possessions(self, emplacement = "all"):
        return self.inventaire_player.get_possessions(emplacement)

    def set_emplacement(self, emplacement, nouveau_objet):
        self.inventaire_player.set_emplacement(emplacement, nouveau_objet)

