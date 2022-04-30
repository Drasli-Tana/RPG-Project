# classe s'occupant des animations
# code version 0.2.5
# on va pas l'utiliser pour le moment

import pygame

class Animation_sprite(pygame.sprite.Sprite):
    def __init__(self, x, y, name, frames):
        super().__init__()
    """
    def animation_deplacement(self, direction):

        # on va limiter les fps de l'animation
        # c'est du bricolage mais bon...
        fps = 12
        #clock = pygame.time.Clock()
        # lance l'animation si aucune en court
        self.frame_actuelle += 32
        self.images = {"down":self.get_image(0+self.frame_actuelle, 0),
                      "left":self.get_image(0+self.frame_actuelle, 32),
                      "right":self.get_image(0+self.frame_actuelle, 64),
                      "up":self.get_image(0+self.frame_actuelle, 96)}

        if self.frame_actuelle == (self.frames-1)*32:
            self.frame_actuelle = 0

        #clock.tick(fps)
        return self.images[direction]

    """