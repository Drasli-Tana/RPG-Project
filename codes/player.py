# Code version 3.0.0
# j'ai enlevé la classe animation_sprite pour le moment
# je la remettrai plus tard dans le jeu

import os

import pygame

import codes.entity as CE
from codes.animation_sprite import *

class Player(pygame.sprite.Sprite):
    resourcePath = "ressources/images/personnages/"
    def __init__(self, x, y, name = "mage", frames = 3):
        """
            x, y: coordonnées dans le plan
            name: la "classe" du personnage
            frames: Nombre d'images disponibles par animation
                (pour le déplacement)
        """
        super().__init__()
        self.entity = CE.Entity(name=name)

        self.sprite_sheet = pygame.image.load(
            os.path.join(
                Player.resourcePath,
                self.entity.getClass() + ".png"))

        # paramétrage de l'image du personnage
        # là on laisse comme ça mais il faudra généraliser si on ajoute monstre
        self.image = self.get_image(0, 0)
        self.rect = self.image.get_rect()
        self.feet = pygame.Rect(0, 0, self.rect.width*0.5, 12)
        
        self.position = [x, y]

        # reaction lors de collision
        self.save_location()
        
        # Loading graphic data
        
        self.speed = 6 # default: 4
        
        self.progress = 0 # pour ralentir fps de l'animation
        # au départ pas d'animation lors de la création du perso

        self.old_direction = "down"
    
    def getClass(self):
        return self.entity.getClass()
    
    def setInventaire(self, inventaire):
        self.entity.setInventaire(inventaire)
    
    def getStats(self):
        return self.entity.getStats()

    def save_location(self):
        self.old_position = self.position.copy()

    def change_animation(self, direction):
        """
        Change l'image du personnage en fonction de la direction
        """
        verticalOffset = {"down": 0, "left": 32, "right": 64, "up": 96}
        # Depending of the direction of the sprite, add an offset
        # to the line on the spritesheet
        
        self.progress += 0.3 # default: 0.3
        # pour ralentir fps de l'animation
        
        self.images = {id: self.get_image(
            32 * (round(self.progress) % 3), verticalOffset[id])
            for id in verticalOffset}
            
        self.images["stop"] = self.get_image(
            32, verticalOffset[self.old_direction])
        
        self.progress %= 3
        
        if direction != "stop":
            self.old_direction = direction 
        
        self.image = self.images[direction]

    """
    Déplacement du personnage
    """
    def get_image(self, x, y):
        # découpage et sélection de l'image du perso
        image = pygame.Surface([32, 32])
        image.blit(self.sprite_sheet, (0,0), (x, y, 32, 32))
        image.set_colorkey([0, 0, 0]) # enlever le fond noir du perso
        
        return image
        
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
        # pour que l'entité ne s'arrete pas en deplacement
        self.change_animation("stop")

    def move_back(self):
        self.position = self.old_position
        self.update()

    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom


    # les mêmes noms qu'inventaire mais bon...
    def get_possessions(self, emplacement = "all"):
        return self.inventaire_player.get_possessions(emplacement)

    def set_emplacement(self, emplacement, nouveau_objet):
        self.inventaire_player.set_emplacement(emplacement, nouveau_objet)

