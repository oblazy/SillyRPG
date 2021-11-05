# -*- coding: utf-8 -*-
"""
Initially done by Olivier Blazy
This does not aim to be anything wonderful
"""

import random
import time


class Perso:
    defattr={
        "human":{"CON":(10,2), "STR":(10,2),"INT":(10,2),"WIS":(10,2),"DEX":(10,2),"LUC":(10,2),"STA":(10,2)}}
    
    listattr=["CON","STR","INT","WIS","DEX","LUC","STA"]
    
    def __init__(self,name,race="human",sex="x"):
        self.name=name
        self.race=race
        self.attr={}
        for i in Perso.listattr:
            self.attr[i]=Perso.defattr[race][i][0]
        self.hp=self.attr["CON"] *10
        self.xp=0
        self.lvl=0
        self.sex=sex
        self.alive=1
        self.gold=0
        if race=="undead":
            self.alive =2
   
    def __str__(self):
        return "{}: health {}/{} \t \t lvl: {} \t \t xp: {}/{} \t \t gold: {}".format(
                self.name, self.hp, 10*self.attr["CON"],self.lvl, self.xp, 
                Perso.xp2lvl(self.lvl), self.gold)
       
   
    def printlvl(self):
        print ("{}: race: {} \n health {}/{} \n STR {} \t \t INT {}  \t \t WIS {} \n DEX {}  \t \t LUC {} \t \t STA {}".format(
                self.name, self.race, self.hp, 10*self.attr["CON"],self.attr["STR"], self.attr["INT"], self.attr["WIS"], self.attr["DEX"], self.attr["LUC"], self.attr["STA"]))
    
    def xp2lvl(lvl):
        '''
        

        Parameters
        ----------
        lvl : int

        Returns
        -------
        The amount of xp needed between lvl and lvl +1
        Why this formula? Because!

        '''
        return 3 * (lvl**2 - 5 * lvl +8)
        
    def lvlup(self):
        self.xp -= Perso.xp2lvl(self.lvl)
        self.lvl += 1
        for i in Perso.listattr:
            self.attr[i]+=random.randint(0,Perso.defattr[self.race][i][1])
        self.hp=self.attr["CON"] *10
        print("*** Congratulations ***")
        Perso.printlvl(self)
        
    def newxp(self,xp):
        self.xp+=xp
        if self.xp >= Perso.xp2lvl(self.lvl):
            Perso.lvlup(self)
            
    def damage(self,dam,name):
        self.hp -= dam
        if self.hp<=0:
            print ("Oh no, your character took lethal damage from a "+name)
            self.alive-=1
            
    def fight(self):
        strinou=Mon.pickmonster(self.lvl)
        xp=random.randint(max(0,strinou.xp-2),strinou.xp+self.lvl)
        dam = random.randint(max(0,strinou.dam-5),strinou.dam+self.lvl)
        loot = random.randint(max(0,strinou.loot-5),strinou.loot+self.lvl)
        return (strinou.name,xp,dam,loot)
        
        
class Mon:
    
    defmon= {"cryptographer":(3,4,1,3), "moth":(1,1,0,0), "bear":(6,7,0,0), "mage":(10,10,1,4), "demon":(13,12,2,3)} # Name, base xp, base dmg, phy|mag|chaos, loot
    limon = list(defmon.keys())
                 
    def __init__(self,name,c):
        self.name=name
        self.xp=c[0]
        self.dam=c[1]
        self.typ=c[2]
        self.loot=c[3]
    
    def relslice(lvl):
        '''     

        Parameters
        ----------
        lvl : int, user level.

        Returns
        -------
        list of appropriate monster names.

        '''
        
        l = len(Mon.limon)
        minslice=min(max(0,lvl-2),l-1)
        maxslice=(min(l, lvl+2))
        return Mon.limon[minslice:maxslice]
    
    def pickmonster(lvl):
        '''
        Parameters
        ----------
        lvl : int

        Returns
        -------
        monstrinou : a valid monster for the lvl range

        '''
        name = random.choice(Mon.relslice(lvl))
        c = Mon.defmon[name]
        monstrinou = Mon(name,c)
        return monstrinou
        
def play(t=0.2):
    n=input("Enter your character name: ")
    per=Perso(n)
    Perso.printlvl(per)
#    b='y'
    while (per.alive >0):
        name, xp, dam, loot = Perso.fight(per)
        print("You fought a "+name+" and won "+str(xp)+" xp, took "+str(dam)+" damage and earned "+str(loot)+" gold!")
        Perso.newxp(per,xp)
        Perso.damage(per,dam,name)
        per.gold+= loot
#        Perso.lvlup(per)
        print(per)
        time.sleep(t)
#        b=input("Do you want to fight a monster? y/n: ")
    if per.alive <1:
        print("Your lvl {} character {} woke up shocked, with {} gold".format(per.lvl, per.name, per.gold))
        Perso.printlvl(per)
    else:
        print("You stopped your adventure, good bye.")
        
play()