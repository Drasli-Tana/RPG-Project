# Code version 3.0.0  pour pouvoir s'y retrouver

import os

import logging as LG
import json as JS
import time as TI
import tkinter as TK
import tkinter.font as TF
import tkinter.messagebox as TM

import codes.Logger as CL
import codes.Shop.buyFrame as BF
import codes.Shop.sellFrame as SF

class Shop(TK.Tk):
    path = "ressources/data/stuff/"
    colors = {True: "#008040", False: "#800000"}
    def __init__(self, kwarg):
        super().__init__()
        self.attributes("-topmost", True)
        self.logger = kwarg.get("logger", CL.Logger())
        #self.bell()
        
        if "argent" in kwarg:
            self.money = kwarg.get("argent")
        else:
            raise TypeError("Missing parameter: argent")
        
        if "inventaire" in kwarg:
            self.inventaire = kwarg.get("inventaire")
        
        else:
            raise TypeError("Missing parameter: inventaire")
        
        self.geometry("+100+100")
        self.overrideredirect(True)
        
        self.font = TF.Font(family = "Courier New", size = 12)
        
        self._buyFrame = False
        
        self.createTitleBar()
        
        self.frame = TK.Frame(self)
        self.toggleButton()
        self._toggleState()
        
        
        self.bind("<KeyRelease-Escape>", lambda _: self.destroy())
        
    def toggleButton(self):
        """
        Ajoute une sorte d'interrupteur pour alterner entre les options
            d'achat et de vente
        """
        self.toggleCanvas = TK.Canvas(
            self, bg = "#FFFFFF", height = 40, highlightthickness = 0,
            bd = 0)
        self.toggleCanvas.grid(row = 1, column = 0, columnspan = 2,
                               sticky = "ew")
        
        self.toggleCanvas.create_rectangle(
            487 // 2 - 2, 0,
            487 // 2 + 2, 40, fill = "#000000")
        
        self.states = [
            self.toggleCanvas.create_rectangle(
                0, 0, 487 // 2 - 2, 40,
                fill = "#008040"),
            
            self.toggleCanvas.create_rectangle(
                487 // 2 + 3, 0, 487, 40,
                fill = "#800000")]
        
        self.toggleCanvas.create_text(
            487 //4, 20, text = "Achat",
            font = self.font, fill = "#FFFFFF")
        
        self.toggleCanvas.create_text(
            3 * (487 // 4), 20, text = "Vente",
            font = self.font, fill = "#FFFFFF")
        
        self.toggleCanvas.bind("<Button-1>", lambda _: self._toggleState())
        
    def destroy(self):
        """
        La seule utilité de cette méthode est d'afficher un message
        à la fermeture de la fenêtre
        """
        self.logger.log("Shop", "Leaving shop", 1)
        super().destroy()
    
    def _toggleState(self):
        """
        Permet d'alterner entre la fenêtre de vente et d'achat
        """
        self.frame.destroy()
        
        if self._buyFrame:
            self.frame = SF.SellFrame
            ratio = .5
        
        else:
            self.frame = BF.BuyFrame
            ratio = 1
        
        self._buyFrame = not self._buyFrame
        self.frame = self.frame(
            self, font = self.font, money = self.money,
            inventaire = self.inventaire, ratio = ratio)
        
        self.toggleCanvas.itemconfig(
            self.states[0], fill = self.colors[self._buyFrame])
        
        self.toggleCanvas.itemconfig(
            self.states[1], fill = self.colors[not self._buyFrame])
        
        self.frame.grid(row = 2, column = 0)
    
    def createTitleBar(self):
        """
        Cette méthode supprime la barre de titre par défaut de tkinter
            et la remplace par une barre de titre personnalisée
        """
        self.titleBar = TK.Frame(self, bd = 0, bg = "#000000")
        self.titleBar.grid(row = 0, column = 0, columnspan = 2,
                           sticky = "nsew")
        self.titleBar.columnconfigure(0, weight = 1)
        
        self.title = TK.Label(self.titleBar, text = "Boutique",
                              bg = "#000000", fg = "#FFFFFF",
                              font = ("Courier New", 20)) 
        self.title.grid(row = 0, column = 0, sticky = "nsew")
        
        self.quitButton = TK.Canvas(
            self.titleBar, width = 36, height = 36,
            bg = "#000000",
            highlightthickness = 0)
        
        self.quitButton.update()
        self.gif = TK.PhotoImage(
            file = "ressources/images/shop/gui/cross.gif")
        
        self.quitButton.create_image(18, 18, image = self.gif)
        self.quitButton.grid(row = 0, column = 1)
        
        self.title.bind("<Button-1>", lambda event: self._clicked(event))
        self.title.bind("<B1-Motion>", lambda event: self._drag(event))
        
        self.quitButton.bind("<Enter>", lambda _: self._mouseIn())
        self.quitButton.bind("<Leave>", lambda _: self._mouseOut())
        
        self.quitButton.bind("<ButtonRelease-1>",
                             lambda _: self.destroy())
    
    """
    Deux méthodes relatives à la barre de titre, permettant de 
        déplacer la fenêtre
    """
    def _clicked(self, event):
        self.lastCoos = [event.x, event.y]    
    
    def _drag(self, event):
        self.geometry(
            f"+{event.x_root - self.lastCoos[0]}" +
            f"+{event.y_root - self.lastCoos[1]}")

    """
    Deux méthodes relatives au bouton de fermeture:
        Ellses servent à changer la couleur de fond quand la
        souris le survole ou non.
    """
    def _mouseIn(self):
        self.quitButton.config(bg = "#FF0000")
    
    def _mouseOut(self):
        self.quitButton.config(bg = "#000000")
                               