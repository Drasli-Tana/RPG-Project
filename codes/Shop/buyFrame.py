'''
Created on 25 août 2021

@author: Thomas
'''
import tkinter as TK
import json as JS
import tkinter.messagebox as TM

import codes.Shop.baseFrame as BF

class BuyFrame(BF.BaseFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.buyButton = TK.Button(
            self, text = "Acheter", font = self.font,
             command = lambda: self.buy(), bg = "#008040",
             fg = self.foreground)
        
        self.buyButton.grid(
            row = 8, column = 0, columnspan = 2, sticky = "ew")
        
    def buy(self):
        if self.price.get() <= self.money.value:
            # j'ai un peu modifié le code ici
            if self.inventaire is not None:
                try:
                    self.addItem(self.nameStr.get())
                
                except ArithmeticError:
                    TM.showerror(
                        "Boutique",
                        f"Vous ne pouvez pas acheter: {self.nameStr.get()}\n" +
                        "Raison: Pas assez de place")
                
                else:
                    TM.showinfo(
                        "Boutique", f"Vous avez acheté: {self.nameStr.get()}")
                    self.money.value -= self.price.get()
                    
        
        else:
            TM.showerror(
                "Boutique",
                f"Vous ne pouvez pas acheter: {self.nameStr.get()}\n" +
                "Raison: Pas assez d'argent")
    
    def addItem(self, name):
        # ajoute l'objet dans equipement de l'inventaire
        # name sera la clé et bonus les stats ajoutées
        bonus = self.get_bonus(name)
        self.inventaire.addItem(name, bonus)
        
        self.logger.log("Shop", f"Added {name} to inventory", 0)
        self.logger.log("Shop", "Current inventory:", 0)
        slots = [
            i for i in self.inventaire.getInventory().keys()
            if i != "backpack"]
        
        for i in slots:
            self.logger.log(
                "Shop", f"\t{i:16s}: " +
                f"{self.inventaire.getInventory()[i]}", 1)
        
        self.logger.log("Shop", "\tSac à dos:", 1)
        
        for i in self.inventaire.getBackpack():
            self.logger.log(
                "Shop", f"\t - {i}: " +
                f"{self.inventaire.getBackpack()[i]}", 1)
        
    def get_bonus(self, name):
        # renvoie le bonus en stats de l'item
        # il s'agit d'effet dans le json
        with open(
            self.dictFiles[name], "r", encoding="utf-8"
            ) as file:
            bonus = JS.load(file)
            
            return bonus
        
