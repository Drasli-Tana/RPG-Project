# Code version 3.0.0
# classe s'occupant de l'affichage graphique
# devrait gérer les combats et affichage de pnj

import pygame
from codes.Inventaire import*
from codes.Combat import*
import codes.Logger as CL
from random import randint
import codes.Player as CP

class Affichage_graphique:
    colors = {
        "black": (0, 0, 0),
        "white": (255, 255, 255),
        "red": (255, 0, 0),
        "green": (0, 255, 0),
        "blue": (0, 0, 255),
        "grey": (47, 47, 47)}
    
    ressourcePath = "ressources/images/"
    # enregistre les valeurs de couleurs (pour le texte)
    # Pas forcément utile, en ce qui me concerne, le tape
    #  directement les codes couleur quand j'en ai besoin
    
    def __init__(self, kwarg):
        self.combat_en_cours = False
        self.logger = kwarg.get("logger", CL.Logger(level = 0))
        
        if "player" in kwarg:
            self.personnage = kwarg.get("player")
        
        else:
            raise TypeError("Missing parameter: player")
        
        if "argent" in kwarg:
            self.argent = kwarg.get("argent")
        
        else:
            raise TypeError("Missing parameter: argent")
        
        self.images_item = kwarg.get("image_item")
        self.inventaire_player = kwarg.get("inventaire") # normalement ça marche
        self.stats = kwarg.get("stats")
        
        self.objets = {}
        self.texte = {}
        # Dictionnaire qui devrait contenir les images ou le texte à afficher
        # Forme d'une image:
        #     "name": {objet, (x, y), [portion de l'image à affiché], layer}
        # une image de layer 1 sera affiché après une image de layer 0
        
             
        # initialisation de la partie texte
        pygame.font.init()
        self.font_25 = pygame.font.SysFont(
            "ressources/data/font/antiquity-print.ttf", 24)

    def get_image(self, name = "all"):
        """
        Renvoie l'objet porté dans le slot donné
        
        Si le slot vaut "all", renvoie tous les objets
        Sinon: si le slot est un objet valide (porté), le renvoie,
               sinon, renvoie None
        """
        if name == "all":
            return self.objets
        
        else:
            return self.objets.get(name)

    def set_image(self, name, objet, position):
        """
         Change une image présente ou en ajoute une
        """
        self.objets[name] = {"objet": objet, "position": position}
    
    def loadImage(self, path):
        """
        Comme ce code revient très souvent, ça ira plus vite
          que de le retaper à chaque fois (et ça évite le copié collé)
          
        Charge une image spécifiée et la renvoie
        """
        return pygame.image.load(path).convert_alpha()
    
    def update_images(self):
        for i in self.objets:
            image = self.objets[i]
            self.screen.blit(image["objet"], image["position"])
            
    def get_texte(self, name = "all"):
        """
        Permet de récupérer le texte (cf. get_image)
        """
        if name == "all":
            return self.texte
        
        else:
            return self.texte.get(name)

    def set_texte(self, name, objet, position):
        """
          ajout de texte ou modification si déjà présent dans self.texte
          (cf. set_image)
          
        """
        self.texte[name] = {"objet": objet, "position": position}
    
    def getFont(self, path, size):
        return pygame.font.Font(path, size)

    def update_text(self):
        """
        Morceau de code très utilisé, donc il vaut mieux utiliser une fonc.
        """
        for i in self.texte:
            texte = self.texte[i]
            self.screen.blit(texte["objet"], texte["position"])
    
    def reinitialiser(self, image = True, texte = True):
        if image:
            self.objets = {}
        
        if texte:
            self.texte = {}

    def change_taille_image(self, name, nouvelle_taille):
        """
        Redimensionne une image se trouvant dans le slot name
        """
        self.objets[name]["taille"] = nouvelle_taille
        objet = self.objets[name]["objet"]
        objet = pygame.transform.scale(objet, nouvelle_taille)
        self.objets[name]["objet"] = objet
    
    """
    On peut aussi prédéfinir certain modèle tel que inventaire ou mode combat
      pour l'instant faire un combat ou ouvrir l'inventaire va lancer une
      nouvelle fenêtre
    """
    def inventaire(self, width = 600):
        # même si on change la taille on garde le ratio x = 2/3 y
        self.taille_fenetre = (width, int(width / 3 * 2))
        self.row = 7
        self.column = 7
        
        # sera nécessaire pour automatiser les positions et taille
        self.ratio = round(width / 600, 3)
        
        # le contenu de l'inventaire
        self.slots = [
            {
                "contenu": None,
                "position": (0, 0),
                "image": None
                }
            for i in range(self.row * self.column)]
            
        # pour gérer la limite d'inventaire
        loop  = self.inventaire_player.inventaire["equipements"]["rien"]
        for i in range(loop):
            self.slots[i]["contenu"] = "Vide"
        # si un slot vaut None alors le joueur ne le possède pas
        # si un slot vaut "rien" alors il n'y pas d'objet ici
        # si un slot contient un objet alors la valeur sera {objet}

        # vide = pas d'image, None = une croix, sinon il y a un objet
        # On aurait aussi pu utiliser None, False, et aute chose, ce serait plus simple
        
        for i in range(self.row):
            for j in range(self.column):
                self.slots[i * self.column + j]["position"] = (
                    int(17 * self.ratio + (40 * j * self.ratio)),
                    # Position dans chaque ligne. 
                    int(64 * self.ratio + (40 * i * self.ratio)))
                    #Position dans chaque colonne
                    
                #La première partie de chaque formule
                # (x * self.ratio) désigne le décalage par rapport au
                # coin en haut à gauche de la fenêtre 

        # création de la fenêtre
        self.screen = pygame.display.set_mode(self.taille_fenetre)
        pygame.display.set_caption("Inventaire")

        chemin = "ressources/images/inventaire/"

        # chargement des images
        image_principale = self.loadImage(chemin + "gui/" + "inventory_preset.png")

        self.set_image("background", image_principale, (0, 0))
        self.change_taille_image("background", (
            int(self.taille_fenetre[0]), int(self.taille_fenetre[1])))
        
        image_or = self.loadImage(chemin + "gui/" + "coin_04a.png")
        
        self.set_image("or", image_or, (17 * self.ratio, 15 * self.ratio))
        self.change_taille_image("or", (int(32 * self.ratio), int(32 * self.ratio)))
        
        # contenu de l'inventaire (ici les croix rouges)
        for i in range(self.row):
            for j in range(self.column):
                image = self.loadImage(chemin + "items/" + "croix_32x32.png")
                self.slots[i * self.column + j]["image"] = image
                
        pygame.display.flip()
        self.fenetre("Inventaire")
        
    def combat(self, width = 800):
        """
        C'est un sacré chantier
        """
        # même si on change la taille on garde le ratio x = 2/3 y
        self.taille_fenetre = (width, int(width / 3*2))
        self.width = self.taille_fenetre[0]
        self.height = self.taille_fenetre[1]
        # sera nécessaire pour automatiser les positions et taille
        self.ratio = round(self.width/800, 3)

        self.screen = pygame.display.set_mode(self.taille_fenetre)
        pygame.display.set_caption("Combat (ou gagne or)")

        # chargement des images
        chemin = "ressources/images/combat/"

        image_fond = self.loadImage(chemin + "fond_noir.png")
        self.set_image("fond_noir", image_fond, (0, 0))
        self.change_taille_image("fond_noir", (int(width), int(width*2/3)))

        self.font_25 = self.getFont(
            path = "ressources/data/font/Seagram tfb.ttf",
            size = int(25 * self.ratio))
        
        # chargement du texte
        self.font_30 = self.getFont(
            path = "ressources/data/font/Seagram tfb.ttf",
            size = int(30 * self.ratio))
        
        
        affichage_or = self.font_30.render(
            "Argent :" + str(self.argent.value) + "PO", False, (255, 255, 255))
        self.set_texte("or", affichage_or, (10*self.ratio, 45*self.ratio))
        
        affichage_lieu = self.font_25.render(
            "Lieu : Probablement le donjon", False, (255,255,255))
        self.set_texte("lieu", affichage_lieu, (10*self.ratio, 10*self.ratio))

        pygame.display.flip()
        self.combat_en_cours = True
        self.creation_combat = True # pour creer le combat une seule fois
        self.generateur_combats(self.stats, randint(2,4), 1) # en test
        # Attention, les dégâts, c'est les "PI", l'attaque sert au lancer
        # de dés pour déterminer si l'attaque rate ou non 
        self.cible_joueur = None # qui le joueur va attaquer
        self.cible_confirmer = False # si la cible est déja choisi
        self.affichage_etat_jeu = True
        self.update_image = True
        
        # ici on lancera le generateur de combat une fois prêt
        self.fenetre("Combat")
    
    def statistiques(self, width = 200):
        """
        Affiche une fenêtre de stats
        """
        # même si on change la taille on garde le ratio x = 2 y
        self.taille_fenetre = (width, int(width * 2))
        self.width = self.taille_fenetre[0]
        self.height = self.taille_fenetre[1]
        # sera nécessaire pour automatiser les positions et taille
        self.ratio = round(self.width/200, 3)

        self.screen = pygame.display.set_mode(self.taille_fenetre)
        pygame.display.set_caption("Stats du joueur")


        # chargement des images
        chemin = Affichage_graphique.ressourcePath + "stats_joueur/"

        image_fond = self.loadImage(chemin + "fond_noir.png")

        self.set_image("fond_noir", image_fond, (0, 0))
        self.change_taille_image(
            "fond_noir", (int(400*self.ratio), int(200*self.ratio)))

        image_PV = self.loadImage(chemin + "heart.png")

        self.set_image("PV", image_PV, (0, 0))
        self.change_taille_image(
            "PV", (int(30*self.ratio), int(30*self.ratio)))
                                                
        image_AT = self.loadImage(chemin + "sword_silver.png")
        
        self.set_image("AT", image_AT, (0, 50))
        self.change_taille_image(
            "AT", (int(30*self.ratio), int(30*self.ratio)))
                                                
        image_PA = self.loadImage(chemin + "orb_blue.png")

        self.set_image("PA", image_PA, (0, 100))
        self.change_taille_image(
            "PA", (int(30*self.ratio), int(30*self.ratio)))
                                                
        # chargement du texte
        self.font_25 = pygame.font.SysFont('Comic Sans MS', int(25 * self.ratio))

        affichage_PV = self.font_25.render(
            str(self.stats["PV"])+ " PV", False, (255, 255, 255))
        self.set_texte("PV", affichage_PV, (45*self.ratio, 0*self.ratio))
        
        affichage_AT = self.font_25.render(
            str(self.stats["AT"]) + " AT",False, (255, 255, 255))
        self.set_texte("AT", affichage_AT, (45*self.ratio, 50*self.ratio))
        
        affichage_PA = self.font_25.render(
            str(self.stats["PA"]) + " PA", False, (255, 255, 255))
        self.set_texte("PA", affichage_PA, (45*self.ratio, 100*self.ratio))
                                          
        self.fenetre("Statistiques")
        
    def generateur_combats(self, player_stats, nb_ennemie, lvl):
        # un truc simple pour le moment
        # lance la classe combat si aucun combat en cours
        # sera appeler chaque tour par la méthode combat dans update
        # se chargera uniquement de l'action en cours
        if self.creation_combat:
            if self.combat_en_cours:
                self.combat_instance = Combat(
                    player_stats, lvl, nb_ennemie)
                self.combat_instance.generateur_monstre()
                self.creation_combat = False
                self.tour_actuelle = 0 # le nombre de tour du combat 
        
        else:
            if self.combat_en_cours:
                # c'est ici qu'on dira aux monstres d'attaquer
                # et au joueur de jouer 
                # ainsi qu'actualiser les stats
                if self.affichage_etat_jeu:
                    self.combat_instance.update_jeu()
                    self.logger.log("Combat", "le combat est en attente", 0)
                    print("Tour de", self.combat_instance.attaquant_actuel)
                    self.affichage_etat_jeu = False
                
                if self.combat_instance.attaquant == "player":
                    # tour du joueur
                    if self.cible_confirmer:
                        self.combat_instance.tour(
                            "player", "monstre" + str(self.cible_joueur))
                        self.cible_joueur = None
                        self.cible_confirmer = False
                        
                    else:
                        self.combat_instance.tour("player", "personne")
                        # saute tour
                    
                else:
                    self.combat_instance.tour("monstre", None)
        
    def gere_combat(self):
        self.update("Combat")
        self.handle_input("Combat")
        self.generateur_combats(None, None, None)
        self.update("Combat")
    
    def _update_inventory(self):
        """
        Pour éviter de rendre illisible la méthode update,
            ça facilite le debugging si besoin
            
        """
        # reaffiche le texte en actualisant les variables
        affichage_or = self.font_25.render(str(self.argent.value), False, (0, 0, 0))
        self.set_texte("or", affichage_or, (60 * self.ratio, 24 * self.ratio))


        # reactualise les images de l'inventaire
        for i in range(self.row):
            for j in range(self.column):
                if self.slots[i*self.column + j]["contenu"] != "Vide":
                    image = self.slots[i*self.column + j]["image"]
                    position = self.slots[i*self.column + j]["position"]
                    self.screen.blit(image, position)
        
        chemin = "ressources\\images\\inventaire\\"
        # contenu de l'inventaire ici les objets (que 1 objet pour l'instant)
        # chantier en cours
        objets = self.inventaire_player.getInventory()
        liste_objet = [i for i in objets if i != "rien"]
        # Version simplifiée (et optimisée de ton code)
        # Oui, j'ai utilisé une boucle for, ça marche mieux, c'est fait pour
        # Et y'a pas besoin de bricolage pour faire -1 partout
        # Accessoirement, se met à jour quand on achète quelque chose
        
        for i in range(len(liste_objet)):
            if liste_objet[i] in self.images_item:
                place = self.images_item[liste_objet[i]]
            
            else:
                place = "notFound.png"
            
            image = self.loadImage(chemin + "items\\" + place)
            
            self.slots[i]["image"] = image
            self.slots[i]["contenu"] = liste_objet[i]
        
        for i in range(len(liste_objet),
                       self.inventaire_player.getLimit()):
            self.slots[i]["image"] = "rien"
            self.slots[i]["contenu"] = "Vide"
    
    def _update_combat(self):
        """
        Affichage des stats du joueur et des monstres
            et également du texte pour le moment
        """
        # actualisation
        # attention pour le moment il n'y as pas d'arguments
        # plus tard on demandera les stats de la classe player
        
        # -------------------------- stats du joueur ---------------------------
        text_player = self.font_25.render(
            "Stats du joueur", False, (255,255,255))
        
        self.set_texte(
            "Stats_player", text_player, (10 * self.ratio, 140 * self.ratio))
        
        statsPlayer = self.combat_instance.stats_joueurs
        strs = {
            "PV_player": f"PV: {statsPlayer['PV']}",
            "AT_player": f"AT: {statsPlayer['AT']}",
            "PI_player": f"PI: {statsPlayer['PI']}"}
        
        coordonnees = 40
        for elem in strs:
            text = self.font_25.render(strs[elem], False, self.colors["white"])
            
            self.set_texte(
                elem, text, (30 * self.ratio, coordonnees * self.ratio + 180))
            coordonnees += 40
        
        # ------------------------- stats des monstres -------------------------
        textMonster = self.font_25.render(
            "Stats des monstres :", False, self.colors["white"])
        
        self.set_texte(
            "Stats_monster", textMonster, (300 * self.ratio, 140 * self.ratio))
        
        nb_monstre = len(self.combat_instance.monstre)

        
        # efface les stats de monstre mort
        for i in self.combat_instance.monstre_mort:
            self.texte.pop(i)
            self.texte.pop("AT_" + i)
            self.texte.pop("PV_" + i)
            self.texte.pop("PI_" + i)
        
        self.combat_instance.monstre_mort.clear()
        # Plus efficace: c'est fait pour
        
        monstres = list(self.combat_instance.monstre.keys())
        stats = ["PV", "AT", "PI"]
        
        # Réécrit les stats de monstres
        for i in range(len(monstres)):
            currentMonster = monstres[i]
            nom_monstre = self.font_25.render(
                currentMonster.capitalize(), False,
                self.colors["white"])
            
            self.set_texte(currentMonster, nom_monstre,(
                330 * self.ratio, (40 * i + 180) * self.ratio))
            
            
            for statId in range(len(stats)):
                currentStat = stats[statId]
                targetStat = self.combat_instance.monstre[
                    currentMonster][currentStat]
                
                text = self.font_25.render(
                    f"{currentStat}_{targetStat}",
                    False, (255,255,255))
            
                self.set_texte(
                    currentStat + "_" + currentMonster, text, (
                        (90 * statId + 450) * self.ratio,
                        (40 * i + 180) * self.ratio))
                
            # texte concernant le tour actuelle 
            # si monstre: n° tour,  nom_monstre, son action
            # si joueur: n° tour,  choix de l'action + résultat action
            
            # nom de l'attaquant de ce tour
            attaquant = self.font_25.render(
                    f"Attaquant: {self.combat_instance.attaquant}",
                    False, self.colors["white"])
            self.set_texte("tour_attaquant", attaquant, 
                           (150 * self.ratio,
                            340 * self.ratio))
            
            # nom de la cible de ce tour
            cible = self.font_25.render(
                    f"Cible : {str(self.cible_joueur).capitalize()}",
                    False, self.colors["white"])
            self.set_texte("cible_joueur", cible, (
                400 * self.ratio,
                340 * self.ratio))
            
            # texte des dernières actions (5 la limite ?)
            # Plutot celles du dernier tour, et on les efface ensuite
            font_20 = self.getFont(
                "ressources\\data\\font\\Seagram tfb.ttf",
                int(20 * self.ratio))
            
            for i in range(len(self.combat_instance.log)):
                texte_final = self.combat_instance.log[i]
                texte_final = font_20.render(texte_final,
                    False, self.colors["white"])
                self.set_texte("texte_temporaire", texte_final, 
                    (100 * self.ratio,
                     380 * self.ratio + 25 * i * self.ratio))
                
                texte = self.texte["texte_temporaire"]
                self.screen.blit(texte["objet"], texte["position"])
                self.texte.pop("texte_temporaire")
                
                
        # numéro du tour actuelle
        nb_tour = self.font_25.render(
            f"Tour: {self.tour_actuelle}", False, self.colors["white"])
        
        self.set_texte(
            "nb_tour", nb_tour, (10 * self.ratio, 340 * self.ratio))
        
        logs = self.font_25.render("Log: ", False, self.colors["white"])
            
        self.set_texte("logs", logs, (10 * self.ratio, 380 * self.ratio))
        
    def update(self, interface):
        self.update_images()
        if interface == "Inventaire":
            self._update_inventory()

        elif interface == "Combat":
            # actualise le texte
            affichage_or = self.font_25.render(
                "Argent :" + str(self.argent.value), False, (255, 255, 255))
            
            self.set_texte(
                "or", affichage_or, (10 * self.ratio, 45 * self.ratio))
            
            if self.combat_en_cours:
                self._update_combat()
                    
        elif interface == "Statistiques":
            pass
        
        self.update_text()
        pygame.display.flip()
    
    def checkTarget(self):
        if self.combat_instance.targetExists(
            "monstre" + str(self.cible_joueur)):
            
            self.combat_instance.clearLogs()
            self.tour_actuelle += 1
            self.cible_confirmer = True
        
        else:
            self.cible_joueur = None
            self.cible_confirmer = False

    def handle_input(self, interface):
        # récupere les touches qui sont préssées
        pressed = pygame.key.get_pressed()
        
        """ # pour savoir à quoi correspond une touche clavier 
        for i in range(len(pressed)):
            if pressed[i] == 1:
                print(i)
        """
        if interface == "Combat":
            if pressed[pygame.K_UP]:
                self.argent.value += 1

            elif pressed[pygame.K_DOWN]:
                if self.argent.value > 0:
                    self.argent.value -= 1

            # pour choisir le monstre à attaquer
            elif pressed[pygame.K_1]:
                self.cible_joueur = 1
            
            elif pressed[pygame.K_2]:
                self.cible_joueur = 2
            
            elif pressed[pygame.K_3]:
                self.cible_joueur = 3
            
            elif pressed[pygame.K_4]:
                self.cible_joueur = 4
            
            elif pressed[pygame.K_5]:
                self.cible_joueur = 5
            
            elif pressed[pygame.K_SPACE]:
                self.checkTarget()
                
    def handle_mouse(self, interface):
        """
        méthode qui gère la souris (position et clic)
        principalement pour l'inventaire pour le moment
        """
        pass
        
    def fenetre(self, interface=None):
        #pygame.display.flip()
        # gérer les fps du jeu
        clock = pygame.time.Clock()
        fps = 24
        # 24 pour les vieux jeux,
        # 30 pour les PC pas très puissants
        # 60 pour un PC moyen, avec un écran valable
        # 61+ pour les machines puissantes, avec un écran qui suit

        # Boucle principale de la sous-fenêtre
        while True: 
            # Simulation d'une boucle 'do...while' dans d'autres langages
            try:
                events = [event.type for event in pygame.event.get()]
               
            except pygame.error:
                break
            
            else:
                # fermeture de la fenetre
                if pygame.QUIT in events:
                    break
                
                else:
                    if interface == "Combat":
                        self.gere_combat() # besoin car on attend des actions

                    else:
                        self.handle_input(interface) # gère touche clavier
                        # met à jour les images
                        self.update(interface)
        
            finally:
                clock.tick(fps)

        pygame.quit()
