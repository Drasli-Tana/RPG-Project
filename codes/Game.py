# je vais suivre la même strecture que dans la vidéo
# Code version 3.0.0
import json as JS
import multiprocessing as MP

import pygame
import pyscroll  # nécessaire sinon trop galère
import pytmx

import codes.inventaire as CI
import codes.Logger as CL
import codes.Music as CM
from codes.player import *  # importation de la classe Player
import codes.Shop.Shop as SP
import codes.Affichage_graphique as AG

def invWin(**kwargs):
    """
    Un sacré bricolage, mais permet d'ouvrir l'inventaire
    """
    win = AG.Affichage_graphique(kwargs)
    win.inventaire()

def combatWin(**kwargs):
    fenetre = AG.Affichage_graphique(kwargs)
    fenetre.combat()
    
def statWin(**kwargs):
    fenetre = AG.Affichage_graphique(kwargs)
    fenetre.statistiques()

def shopWin(**kwargs):
    win = SP.Shop(kwargs)
    win.mainloop()

class Game:
    def __init__(self, kwarg):
        # bricolage en cours ne pas toucher !
        
        self.logger = kwarg.get("logger", CL.Logger(level = 0))
        
        if "argent" in kwarg:
            self.argent = kwarg.get("argent")
        
        else:
            raise TypeError("Missing parameter: argent")
        
        if "images_item" in kwarg:
            self.images_item = kwarg.get("images_item")
        
        else:
            raise TypeError("Missing parameter: images_item")
    
        # j'améliorerai après
        
        with open("ressources/images/itemName.json") as file:
            # Ça marchera mieux comme ça (plus facile à modifier
            images = JS.load(file)
            
        for i in images:
            self.images_item[i] = images[i]       
        # du très grand bricolage (comme d'habitude)
        
        # Possibilité de mettre en plein écran version à voir
        self.screen = pygame.display.set_mode((800,600))
        self.tmxPath = "ressources\\data\\tmx\\"
        pygame.display.set_caption("Jeu RPG v 3.0.1")
        
        
        self.subprocess = {
            "inventory": None,
            "combat": None,
            "boutique": None,
            "stats": None}

        # chargement de la carte format tmx
        map_accueil = self.tmxPath + "accueil.tmx"

        tmx_data = pytmx.util_pygame.load_pygame(map_accueil)
        map_data = pyscroll.data.TiledMapData(tmx_data)
        # gère les différents calques
        map_layer = pyscroll.orthographic.BufferedRenderer(
            map_data, self.screen.get_size())

        # réglage du zoom
        # il faudrait qu'il dépend de la taille de l'écran donc à voir
        map_layer.zoom = 2

        # génére le joueur et récupére la position de spawn dans la map
        player_position = tmx_data.get_object_by_name("spawn_player")
        
        self.player = Player(player_position.x, player_position.y, name="guerrier")
        self.inventaire = CI.Inventaire(self.player.getClass(), self.argent)
        self.player.setInventaire(self.inventaire)
        
        # génére une liste de collision
        self.walls = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y,
                    obj.width, obj.height))

        # regroupe les calques et se positionne sur l'un d'eux (default)
        self.group = pyscroll.PyscrollGroup(map_layer = map_layer,
                     default_layer = 0)
        self.group.add(self.player, layer = 3) 
        # ajout du personnage dans l'image
        
        entriesNames = {
            "Entree-Armurerie": self.switch_armurerie,
            "Entree-Taverne": self.switch_taverne,
            "Entree-Maison": self.switch_maison_joueur,
            "Entree-Donjon": self.switch_donjon,
            "Entree-Foret": self.switch_foret}
        self.entries = {}
        
        for entry in entriesNames.keys():
            # On liste toutes les entrées de la map, auxquelles on associe
            # un rectangle de "collision", et la méthode appelée le cas
            # échéant 
            currEntry = tmx_data.get_object_by_name(entry)
            # On charge les données de la zone d'entrée
            self.entries[entry] = [
                pygame.Rect(
                    currEntry.x, currEntry.y,
                    currEntry.width, currEntry.height),
                # On crée le rectangle, et on y associe le nom de l'entrée
                entriesNames[entry]
                # Idem pour le callback
                ]
            

        # la map dans laquelle se situe le joueur actuellement
        self.map = "accueil"
        self.old_map = None
        
        self.playSound = False
        if self.playSound:
            self.music = CM.Music()
            self.music.start()

    def handle_input(self):
        # récupere les touches qui sont préssées
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]:
            self.player.move_up()

        elif pressed[pygame.K_DOWN]:
            self.player.move_down()

        elif pressed[pygame.K_LEFT]:
            self.player.move_left()

        elif pressed[pygame.K_RIGHT]:
            self.player.move_right()
            
        else:
            # on gère les moments ou aucune touche n'est préssé
            self.player.move_stop()
        
        events = [
            event for event in pygame.event.get(pygame.KEYUP)
            ]
        
        for event in events:
            if event.key == pygame.K_e:
                self.openWin("inventory")
            
            elif event.key == pygame.K_c:
                self.openWin("combat")
            
            elif event.key == pygame.K_b:
                self.openWin("boutique")
            
            elif event.key == pygame.K_s:
                self.openWin("stats")
                
    def switch_map(self, map, scale=1.6, player_layer=4):
        self.map = map
        
        tmx_data = pytmx.util_pygame.load_pygame(
            self.tmxPath + map + ".tmx")
        
        map_layer = pyscroll.orthographic.BufferedRenderer(
            pyscroll.data.TiledMapData(tmx_data),
            self.screen.get_size())
        
        map_layer.zoom(scale)
        self.walls = [
            pygame.Rect(obj.x, obj.y, obj.width, obj.height)
            for obj in tmx_data.objects
            if obj.type == "collision"]
        
        self.group = pyscroll.PyscrollGroup(
            map_layer=map_layer, default_layer=0)
        
        self.group.add(self.player, layer = player_layer)
        spawn_map = tmx_data.get_object_by_name("Spawn-" + map.capitalize())
        
        self.player.position[0] = spawn_map.x
        self.player.position[1] = spawn_map.y
        
        sortie_map = tmx_data.get_object_by_name("Sortie-" + map.capitalize())
        self.sortie_map_rect = pygame.Rect(
            sortie_map.x, sortie_map.y,
            sortie_map.width, sortie_map.height)

    def switch_armurerie(self):
        """
        Affiche l'armurerie
        """
        map_armurerie = self.tmxPath + "armurerie.tmx"
        self.map = "armurerie"

        tmx_data = pytmx.util_pygame.load_pygame(map_armurerie)
        map_data = pyscroll.data.TiledMapData(tmx_data)
        # gert les différents calques
        map_layer = pyscroll.orthographic.BufferedRenderer(
            map_data, self.screen.get_size())

        # réglage du zoom
        # il faudrait qu'il dépend de la taille de l'écran donc à voir
        map_layer.zoom = 1.7
        
        # génére une liste de collision
        self.walls = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(
                    obj.x, obj.y,obj.width, obj.height))


        # regroupe les calques et se positionne sur l'un d'eux (default)
        self.group = pyscroll.PyscrollGroup(
            map_layer = map_layer, default_layer = 0)
        self.group.add(self.player, layer = 2)
         # ajout du personnage dans l'image

        # lieu de spawn
        spawn_armurerie = tmx_data.get_object_by_name(
            "spawn_entree_armurerie")
        self.player.position[0] = spawn_armurerie.x
        self.player.position[1] = spawn_armurerie.y

        # sortie de la taverne
        sortie_armurerie = tmx_data.get_object_by_name(
            "sortie_armurerie")
        self.sortie_armurerie_rect = pygame.Rect(
            sortie_armurerie.x, sortie_armurerie.y,
            sortie_armurerie.width, sortie_armurerie.height)
    
    def switch_foret(self):
        """
        Affiche la forêt
        """
        new_map = self.tmxPath + "foret.tmx"
        self.map = "foret"
        
        tmx_data = pytmx.util_pygame.load_pygame(new_map)
        map_data = pyscroll.data.TiledMapData(tmx_data)
        # gère les différents calques
        map_layer = pyscroll.orthographic.BufferedRenderer(
            map_data, self.screen.get_size())

        # réglage du zoom
        # il faudrait qu'il dépend de la taille de l'écran donc à voir
        map_layer.zoom = 2
        
        
        # génére une liste de collision
        self.walls = []
        self.groot = None
        self.warpList = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(
                    obj.x, obj.y,obj.width, obj.height))
            
            elif obj.type == "groot":
                self.groot = pygame.Rect(
                    obj.x, obj.y,
                    obj.width, obj.height)
            
            elif obj.type == "warp":
                self.warpList.append(
                    [pygame.Rect(
                        obj.x, obj.y, obj.width, obj.height),
                        obj.target])
                

        # regroupe les calques et se positionne sur l'un d'eux (default)
        self.group = pyscroll.PyscrollGroup(
            map_layer = map_layer, default_layer = 0)
        self.group.add(self.player, layer = 4)
        # ajout du personnage dans l'image

        # lieu de spawn
        spawn_foret = tmx_data.get_object_by_name("Spawn")
        self.player.position[0] = spawn_foret.x
        self.player.position[1] = spawn_foret.y
        

        # sortie de la foret
        sortie_foret = tmx_data.get_object_by_name("Retour")
        self.sortie_foret_rect = pygame.Rect(
            sortie_foret.x, sortie_foret.y,
            sortie_foret.width, sortie_foret.height)
    
    def warp(self, direction = 'w'):
        """
        Sert à téléporter le joueur d"un bout à l'autre du chemin de la forêt 
        """
        tmx_data = pytmx.util_pygame.load_pygame(self.tmxPath + "foret.tmx")
        if direction == 'w':
            self.player.position[0] = 336 + 17
        
        elif direction == 'e':
            self.player.position[0] = 1808 - 24

    def switch_taverne(self):
        """
        Affiche la taverne
        """
        map_taverne = self.tmxPath + "taverne.tmx"
        self.map = "taverne"

        tmx_data = pytmx.util_pygame.load_pygame(map_taverne)
        map_data = pyscroll.data.TiledMapData(tmx_data)
        # gert les différents calques
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data,
                    self.screen.get_size())

        # réglage du zoom
        # il faudrait qu'il dépend de la taille de l'écran donc à voir
        map_layer.zoom = 1.6


        # génére une liste de collision
        self.walls = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y,
                    obj.width, obj.height))


        # regroupe les calques et se positionne sur l'un d'eux (default)
        self.group = pyscroll.PyscrollGroup(map_layer = map_layer,
                     default_layer = 3)
        self.group.add(self.player)  # ajout du personnage dans l'image

        # lieu de spawn
        spawn_taverne = tmx_data.get_object_by_name("spawn_entree_taverne")
        self.player.position[0] = spawn_taverne.x
        self.player.position[1] = spawn_taverne.y

        # sortie de la taverne
        sortie_taverne = tmx_data.get_object_by_name("sortie_taverne")
        self.sortie_taverne_rect = pygame.Rect(sortie_taverne.x,
            sortie_taverne.y, sortie_taverne.width, sortie_taverne.height)

    def switch_accueil(self):
        """
        Affiche la map principale
        """
        map_accueil = self.tmxPath + "accueil.tmx"
        self.map = "accueil"


        tmx_data = pytmx.util_pygame.load_pygame(map_accueil)
        map_data = pyscroll.data.TiledMapData(tmx_data)
        # gert les différents calques
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data,
                    self.screen.get_size())

        # réglage du zoom
        # il faudrait qu'il dépend de la taille de l'écran donc à voir
        map_layer.zoom = 2


        # génére une liste de collision
        self.walls = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y,
                    obj.width, obj.height))


        # regroupe les calques et se positionne sur l'un d'eux (default)
        self.group = pyscroll.PyscrollGroup(map_layer = map_layer,
                     default_layer = 0)
        self.group.add(self.player, layer = 4)  # ajout du personnage dans l'image


        # lieu de spawn
        if self.old_map == "armurerie":
            spawn_accueil = tmx_data.get_object_by_name("Sortie-Armurerie")
            self.player.position[0] = spawn_accueil.x
            self.player.position[1] = spawn_accueil.y
        
        elif self.old_map == "taverne":
            spawn_accueil = tmx_data.get_object_by_name("Sortie-Taverne")
            self.player.position[0] = spawn_accueil.x - 10
            self.player.position[1] = spawn_accueil.y - 15
        
        elif self.old_map == "maison_joueur":
            spawn_accueil = tmx_data.get_object_by_name("Sortie-Maison")
            self.player.position[0] = spawn_accueil.x 
            self.player.position[1] = spawn_accueil.y 
        
        elif self.old_map == "donjon":
            spawn_accueil = tmx_data.get_object_by_name("Sortie-Donjon")
            self.player.position[0] = spawn_accueil.x 
            self.player.position[1] = spawn_accueil.y 
        
        elif self.old_map == "foret":
            spawn_accueil = tmx_data.get_object_by_name("Sortie-Foret")
            self.player.position[0] = spawn_accueil.x 
            self.player.position[1] = spawn_accueil.y 

        self.update()
        
    def switch_maison_joueur(self):
        map_maison_joueur = self.tmxPath + "maison_joueur.tmx"
        self.map = "maison_joueur"

        tmx_data = pytmx.util_pygame.load_pygame(
            map_maison_joueur)
        map_data = pyscroll.data.TiledMapData(tmx_data)
        # gère les différents calques
        map_layer = pyscroll.orthographic.BufferedRenderer(
            map_data, self.screen.get_size())

        # réglage du zoom
        # il faudrait qu'il dépend de la taille de l'écran donc à voir
        map_layer.zoom = 1.6

        # génére une liste de collision
        self.walls = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(
                    pygame.Rect(
                        obj.x, obj.y, obj.width, obj.height))


        # regroupe les calques et se positionne sur l'un d'eux (default)
        self.group = pyscroll.PyscrollGroup(map_layer = map_layer,
                     default_layer = 4)
        self.group.add(self.player)  # ajout du personnage dans l'image

        # lieu de spawn
        spawn_maison_joueur = tmx_data.get_object_by_name("spawn_entree"
            +"_maison_joueur")
        self.player.position[0] = spawn_maison_joueur.x
        self.player.position[1] = spawn_maison_joueur.y

        # sortie de la taverne
        sortie_maison = tmx_data.get_object_by_name("sortie_maison"
            +"_joueur")
        self.sortie_maison_rect = pygame.Rect(
            sortie_maison.x, sortie_maison.y,
            sortie_maison.width, sortie_maison.height)
            
        self.update() 
    
    def switch_donjon(self):
        map_donjon = self.tmxPath + "donjon.tmx"
        self.map = "donjon"

        tmx_data = pytmx.util_pygame.load_pygame(
            map_donjon)
        map_data = pyscroll.data.TiledMapData(tmx_data)
        # gère les différents calques
        map_layer = pyscroll.orthographic.BufferedRenderer(
            map_data, self.screen.get_size())

        # réglage du zoom
        # il faudrait qu'il dépend de la taille de l'écran donc à voir
        map_layer.zoom = 1.6

        # génére une liste de collision
        self.walls = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(
                    pygame.Rect(
                        obj.x, obj.y, obj.width, obj.height))


        # regroupe les calques et se positionne sur l'un d'eux (default)
        self.group = pyscroll.PyscrollGroup(
            map_layer = map_layer, default_layer = 0)
        self.group.add(self.player, layer = 6)  # ajout du personnage dans l'image

        # lieu de spawn
        spawn_player_donjon = tmx_data.get_object_by_name(
            "spawn_player_donjon")
        self.player.position[0] = spawn_player_donjon.x
        self.player.position[1] = spawn_player_donjon.y

        # sortie de la taverne
        sortie_donjon = tmx_data.get_object_by_name("sortie_donjon")
        self.sortie_donjon_rect = pygame.Rect(
            sortie_donjon.x, sortie_donjon.y,
            sortie_donjon.width, sortie_donjon.height)
            
        self.update()

    def update(self):
        self.group.update()
        # vérification de l'entrée dans un bâtiment

        if self.map == "accueil":
            for collide in self.entries:
                if self.player.feet.colliderect(self.entries[collide][0]):
                    self.oldmap = "accueil"
                    self.entries[collide][1]()

        
        if self.map == "armurerie":
            if self.player.feet.colliderect(self.sortie_armurerie_rect):
                self.old_map = "armurerie"
                self.switch_accueil() # - accueil

        if self.map == "taverne":
            if self.player.feet.colliderect(self.sortie_taverne_rect):
                self.old_map = "taverne"
                self.switch_accueil() # - accueil
                
        if self.map == "maison_joueur":
            if self.player.feet.colliderect(self.sortie_maison_rect):
                self.old_map = "maison_joueur"
                self.switch_accueil() # - accueil
                
        if self.map == "donjon":
            if self.player.feet.colliderect(self.sortie_donjon_rect):
                self.old_map = "donjon"
                self.switch_accueil() # - accueil
        
        if self.map == "foret":
            if self.player.feet.colliderect(self.sortie_foret_rect):
                self.old_map = "foret"
                self.switch_accueil() # - accueil
            
            for warp in self.warpList:
                if self.player.feet.colliderect(warp[0]):
                    self.warp(warp[1])

        # verification des collisions
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls) > -1:
                sprite.move_back()

    
    def openWin(self, window = "inventory"):
        if window in self.subprocess.keys():
            if window == "inventory":
                target = invWin
            
            elif window == "combat":
                target = combatWin
            
            elif window == "boutique":
                target = shopWin
            
            elif window == "stats":
                # en test
                target = statWin
            
            if (self.subprocess[window] is None or
                not self.subprocess[window].is_alive()):
                self.subprocess[window] = MP.Process(
                    target=target,
                    kwargs={
                        "player": self.player.getClass(),
                        "argent": self.argent,
                        "stats":  self.player.getStats(),
                        "inventaire": self.inventaire,
                        "images_item": self.images_item,
                        "logger": self.logger})
                        
                self.subprocess[window].start()
            
            else:
                self.subprocess[window].terminate()
    
    def run(self):
        # gérer les fps du jeu
        clock = pygame.time.Clock()
        fps = 24

        running = True

        # Boucle principale du jeu
        while running:

            self.player.save_location()
            # gert les touches claviers
            self.handle_input()
            # met à jour l'affichage du groupe image
            self.update()
            # la caméra cible le joueur
            self.group.center(self.player.rect.center)


            # on dessine les calques (affichage de la map)
            self.group.draw(self.screen)
            pygame.display.flip()  # actualise la fenêtre

            # fermeture de la fenetre
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False


            clock.tick(fps)
        
        # On ferme toutes les fenêtres
        for i in self.subprocess.keys():
            if self.subprocess[i] is not None:
                self.subprocess[i].terminate()
        
        if self.playSound:
            self.music.terminate()
        
        pygame.quit()
        
        