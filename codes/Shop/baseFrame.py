'''
Created on 25 août 2021

@author: Thomas
'''
import tkinter as TK
import json as JS

class BaseFrame(TK.Frame):
    foreground = "#FFFFFF"
    background = "#000000"
    def __init__(self, master, font = None, money = None, 
                 inventaire = None, *cnf, **kwarg):
        super().__init__(master, cnf)
        self.logger = master.logger 
        self.font = font
        self.money = money
        self.inventaire = inventaire
        self.price = TK.DoubleVar(self)
    
        if "ratio" in kwarg:
            self.ratio = kwarg["ratio"]
        
        else:
            self.ratio = 1
        # Dévaluation du prix (vente)
        
        with open("ressources/data/items.json", 'r') as file:
            self.dictFiles = JS.load(file)
        
        self.items = list(self.dictFiles.keys())
        self.config(bg = self.background)
        
        self.nameFrame = TK.Frame(
            self,
            bg = self.background,
            highlightthickness = 0)
        self.nameStr = TK.StringVar(self.nameFrame, self.items[0])
        self.name1 = TK.Label(
            self.nameFrame, text = "Nom: ", font = self.font,
            bg = self.background, 
            fg = self.foreground,
            highlightthickness = 0)
        
        self.nameFrame.grid(row = 1, column = 0, columnspan = 2,
                            sticky = "nsew")
        self.name1.grid(row = 0, column = 0)

        self.nameFrame.columnconfigure(1, weight = 1)
        
        self.options = TK.OptionMenu(
            self.nameFrame, self.nameStr, *self.items,
            command=lambda _: self.update())
        
        self.options.config(
            font=self.font, bg = "#474747", fg = self.foreground,
            highlightthickness = 1, highlightbackground = self.background,
            bd = 0, activebackground = "#474747",
             activeforeground = self.foreground)
        
        self.options.grid(row = 0, column = 1, sticky = "nsew")
        self.options["menu"].config(
            bg = self.background,
            fg = self.foreground)
        
        self.baseBonus()
        self.baseSlot()
        self.baseEffect()
        self.baseDesc()
        self.baseUsage()
        self.basePrice()
        self.update()
    
    def baseSlot(self):
        self.slot1 = TK.Label(
            self.slotFrame, text = "Slot: ", font = self.font,
            bg = self.background, 
            fg = self.foreground,
            highlightthickness = 0)
        
        self.slot2 = TK.Label(
            self.slotFrame, font = self.font,
            textvariable = self.slotStr,
            bg = self.background, 
            fg = self.foreground,
            highlightthickness = 0)
        
        self.slotFrame.grid(row = 3, column = 0, columnspan = 2)
        self.slot1.grid(row = 0, column = 0)
        self.slot2.grid(row = 0, column = 1)
    
    def baseDesc(self):
        self.descFrame = TK.Frame(self,
            bg = self.background, 
            highlightthickness = 0)
        self.desc1 = TK.Label(
            self.descFrame, text = f"{'Description:':16s}", font = self.font,
            bg = self.background, 
            fg = self.foreground,
            highlightthickness = 0)
        
        self.desc2 = TK.Text(
            self.descFrame, font = self.font, width = 30,
            height = 3, wrap = "word",
            bg = self.background, 
            fg = self.foreground,
            highlightthickness = 0)
        
        self.scrollbar2 = TK.Scrollbar(
            self.descFrame, orient="vertical", command=self.desc2.yview,
            relief = "flat",
            bg = self.background, 
            highlightthickness = 0)
        
        
        self.desc2.config(yscrollcommand=self.scrollbar2.set,
                          state = "disabled")
        
        self.descFrame.grid(row = 5, column = 0, columnspan = 2)
        self.desc1.grid(row = 0, column = 0)
        self.desc2.grid(row = 0, column = 1)
        self.scrollbar2.grid(row = 0, column = 2, sticky = "ns")
    
    def changeOpts(self, sequence):
        self.options.destroy()
        sequence.insert(0, "</>")
        
        self.options = TK.OptionMenu(
            self.nameFrame, self.nameStr, *sequence,
            command=lambda _: self.update())
        
        self.options.config(
            font=self.font, bg = "#474747", fg = self.foreground,
            highlightthickness = 1, highlightbackground = self.background,
            bd = 0, activebackground = "#474747",
             activeforeground = self.foreground)
        
        self.options.grid(row = 0, column = 1, sticky = "nsew")
        self.options["menu"].config(
            bg = self.background,
            fg = self.foreground)
            
        self.nameStr.set(sequence[0])
        self.update()
    
    def baseUsage(self):
        self.useFrame = TK.Frame(self,
            bg = self.background, 
            highlightthickness = 0)
        self.use1 = TK.Label(
            self.useFrame, text = "Utilisable par: ", font = self.font,
            bg = self.background, 
            fg = self.foreground,
            highlightthickness = 0)
        
        self.use2 = TK.Text(
            self.useFrame, font = self.font, width = 30,
            height = 3, wrap = "word",
            bg = self.background, 
            fg = self.foreground,
            highlightthickness = 0)
        
        self.scrollbar3 = TK.Scrollbar(
            self.useFrame, orient="vertical", command=self.use2.yview,
            relief = "flat",
            bg = self.background, 
            highlightthickness = 0)
        
        
        self.use2.config(yscrollcommand=self.scrollbar3.set,
                          state = "disabled")
        
        self.useFrame.grid(row = 6, column = 0, columnspan = 2)
        self.use1.grid(row = 0, column = 0)
        self.use2.grid(row = 0, column = 1)
        self.scrollbar3.grid(row = 0, column = 2, sticky = "ns")
    
    def basePrice(self):
        self.priceFrame = TK.Frame(self,
            bg = self.background, 
            highlightthickness = 0)
        self.price1 = TK.Label(
            self.priceFrame, text = "Prix: ", font = self.font,
            bg = self.background, 
            fg = self.foreground,
            highlightthickness = 0)
        
        self.price2 = TK.Label(
            self.priceFrame, font = self.font, textvariable = self.price,
            bg = self.background, 
            fg = self.foreground,
            highlightthickness = 0)
        
        self.priceFrame.grid(row = 7, column = 0, columnspan = 2)
        self.price1.grid(row = 0, column = 0)
        self.price2.grid(row = 0, column = 1)
        
    def baseBonus(self):
        self.protectionFrame = TK.Frame(self)
        self.stat = TK.StringVar(self.protectionFrame, "Protection: ")
        self.protectionStr = TK.StringVar(self.protectionFrame)
        
        self.protection1 = TK.Label(
            self.protectionFrame, textvariable = self.stat,
            font = self.font,
            bg = self.background, 
            fg = self.foreground,
            highlightthickness = 0)
        
        self.protection2 = TK.Label(
            self.protectionFrame, font = self.font,
            textvariable = self.protectionStr,
            bg = self.background, 
            fg = self.foreground,
            highlightthickness = 0)
        
        self.protectionFrame.grid(row = 2, column = 0, columnspan = 2)
        self.protection1.grid(row = 0, column = 0)
        self.protection2.grid(row = 0, column = 1)
        
        self.slotFrame = TK.Frame(self)
        self.slotStr = TK.StringVar(self.slotFrame)
    
    def baseEffect(self):
        self.effectFrame = TK.Frame(self,
            bg = self.background,
            highlightthickness = 0)
        self.effect1 = TK.Label(
            self.effectFrame, text = f"{'Effet(s):':16s}", font = self.font,
            bg = self.background, 
            fg = self.foreground,
            highlightthickness = 0)
        
        self.effect2 = TK.Text(
            self.effectFrame, font = self.font, width = 30,height = 3,
            bg = self.background, 
            fg = self.foreground,
            highlightthickness = 0)
        
        self.scrollbar1 = TK.Scrollbar(
            self.effectFrame, orient="vertical", 
            command=self.effect2.yview, relief = "flat",
            bg = self.background, 
            highlightthickness = 0)
        
        self.scrollbar1.grid(row = 0, column = 2, sticky = "ns")
        self.effect2.config(yscrollcommand=self.scrollbar1.set,
                                state = "disabled")
        
        self.effectFrame.grid(row = 4, column = 0, columnspan = 2)
        self.effect1.grid(row = 0, column = 0)
        self.effect2.grid(row = 0, column = 1)
    
    def update(self):
        if self.nameStr.get() in self.dictFiles:
            with open(self.dictFiles[self.nameStr.get()]) as file:
                attribute = JS.load(file)
                
                self.nameStr.set(attribute["name"])
                try:
                    self.protectionStr.set(str(attribute["protection"]))
                
                except KeyError:
                    self.stat.set("Dégâts: ")
                    self.protectionStr.set(
                        str(attribute["degats"][0]) + "D6 + " +
                        str(attribute["degats"][1]))
                
                else:
                    self.stat.set("Protection: ")
                
                self.slotStr.set(attribute["slot"].capitalize())                
                
                self.effect2.config(state = "normal")
                self.effect2.delete(1.0, TK.END)
                effets = [
                    str(i) + ": " + str(attribute["effet"][i])
                    for i in attribute["effet"]]
                
                self.effect2.insert(1.0, "\n".join(effets))            
                self.effect2.config(state = "disabled")
                
                
                self.desc2.config(state = "normal")
                self.desc2.delete(1.0, TK.END)
                self.desc2.insert(1.0, attribute["tooltip"].rstrip())
                self.desc2.config(state="disabled")
                
                self.use2.config(state = "normal")
                self.use2.delete(1.0, TK.END)
                self.use2.insert(1.0, "\n".join(
                    [i.capitalize() for i in attribute["usable"]
                     if attribute["usable"][i]]))
                self.use2.config(state = "disabled")
                    
                self.price.set(attribute["prix"] * self.ratio)
        
        else:
            self.protectionStr.set("</>")
            self.slotStr.set("</>")
           
            self.effect2.config(state = "normal")
            self.effect2.delete(1.0, TK.END)        
            self.effect2.config(state = "disabled")
            
            self.desc2.config(state = "normal")
            self.desc2.delete(1.0, TK.END)
            self.desc2.config(state = "disabled")
            
            self.use2.config(state = "normal")
            self.use2.delete(1.0, TK.END)
            self.use2.config(state = "disabled")
                
            self.price.set("</>")
            
            