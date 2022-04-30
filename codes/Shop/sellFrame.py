'''
Created on 26 août 2021

@author: Thomas
'''
import tkinter as TK
import json as JS
import tkinter.messagebox as TM

import codes.Shop.baseFrame as BF

class SellFrame(BF.BaseFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sellButton = TK.Button(
            self, text = "Vendre", font = self.font,
            command = lambda: self.sell(), bg = "#800000",
            fg = self.foreground)
        
        self.sellButton.grid(
            row = 8, column = 0, columnspan=2, sticky = "ew")
        self.updateOpt()
        
    def sell(self):
        try:
            self.inventaire.delItem(self.nameStr.get())
        
        except AttributeError:
            TM.showerror("Shop", "Vous ne pouvez pas vendre une absence d'item.")
        
        else:
            self.money.value += self.price.get()
            TM.showinfo(
                "Shop",f"Vous avez vendu {self.nameStr.get()} " +
                f"pour {self.price.get()} PO")
            self.logger.log("Shop", f"Sold {self.nameStr.get()}", 0)
            self.updateOpt()
            
    def updateOpt(self):
        items = self.inventaire.getInventory().values()
        self.changeOpts([item["name"] for item in items])
                