# -*- coding: utf-8 -*-
"""
Initially done by Olivier Blazy
This does not aim to be anything wonderful
"""

import sys
import random
from time import sleep
import pickle
import os

import PrettyUI
import Monster

listyes = ["y","Y","O","o","yes","YES","oui","OUI","j","J","ja","JA"]
listno = ["n","N","no","NO","no","NO","nein","NEIN"]
yn = "("+PrettyUI.add_color("y",PrettyUI.OKGreen)+"/"+PrettyUI.add_color("n",PrettyUI.Critical)+")"


class Perso:
    defattr={
        "human"     :{"CON":(10,(1,2)), "STR":(10,(1,2)),"INT":(10,(1,2)),"WIS":(10,(1,2)),"DEX":(10,(1,2)),"LUC":(10,(1,2)),"STA":(10,(1,2)),"SPD":(10,(1,1)),"CHA":(10,(1,2)),"PER":(10,(1,2))},
        "undead"    :{"CON":(8,(0,2)), "STR":(11,(2,3)),"INT":(9,(1,1)),"WIS":(12,(0,1)),"DEX":(8,(1,1)),"LUC":(10,(1,2)),"STA":(14,(1,3)),"SPD":(8,(0,1)),"CHA":(10,(1,1)),"PER":(10,(1,2))},
        "elf"       :{"CON":(9,(0,1)), "STR":(8,(1,1)),"INT":(8,(2,3)),"WIS":(13,(3,4)),"DEX":(25,(3,6)),"LUC":(10,(3,4)),"STA":(11,(1,2)),"SPD":(12,(2,2)),"CHA":(11,(1,3)),"PER":(12,(1,3))},
        "orc"       :{"CON":(15,(2,3)), "STR":(10,(3,4)),"INT":(10,(0,1)),"WIS":(10,(0,1)),"DEX":(10,(0,1)),"LUC":(10,(0,1)),"STA":(15,(2,3)),"SPD":(10,(1,2)),"CHA":(10,(2,3)),"PER":(9,(0,2))},
        "ent"       :{"CON":(15,(3,3)), "STR":(10,(2,2)),"INT":(10,(1,2)),"WIS":(10,(0,1)),"DEX":(10,(0,1)),"LUC":(8,(0,1)),"STA":(12,(1,3)),"SPD":(10,(0,1)),"CHA":(12,(2,2)),"PER":(10,(1,1))},
        "goblin"    :{"CON":(15,(3,3)), "STR":(10,(2,2)),"INT":(10,(1,2)),"WIS":(10,(0,1)),"DEX":(10,(0,1)),"LUC":(8,(0,1)),"STA":(12,(1,3)),"SPD":(10,(0,1)),"CHA":(9,(1,3)),"PER":(12,(2,3))},
        "wolfy"     :{"CON":(14,(1,3)), "STR":(10,(2,3)),"INT":(10,(1,2)),"WIS":(10,(1,2)),"DEX":(10,(2,2)),"LUC":(12,(1,2)),"STA":(13,(2,3)),"SPD":(11,(1,3)),"CHA":(11,(1,2)),"PER":(11,(2,3))}
        }

    listattr=["CON","STR", "DEX", "INT","CHA", "WIS", "PER", "STA", "SPD", "LUC"]

    listrac=list(defattr.keys())

    minipic={
        "human"     :[" (~~~) "," |o o| ","(| . |) "," ( - ) "],
        "undead"    :[" (())) ","/|x x| ","/| . | ","\\( - ) "],
        "elf"       :[" /~~~/ "," |o o| ","\\| . |/"," \\ - / "],
        "ent"       :[" \\#|#/ ","~ \\|/  ","  )|( ~","  )|(  "],
        "goblin"    :["/(-'-)\\","\\/   \\/","/o. .o\\","\\  i  /"],
        "wolfy"     :[" /\\-/\\ ","((o o))","\\ /_\\ /"," \\_-_/ "],
        "orc"       :["<\\<,>/>","( 0 0 )","\\ ),( /"," \\=-=/ "],

    }



    listcard=["North","South","East","West"]

    deftal={
        "Jack of all trades":("When leveling up, each base stat is increased by one more",1),
        "MC Dodger":("Can't touch this!",1),
        "Resilient": ("It's just a scratch",1),
        "Divine Spark": ("Even death won't kill me!",1),
        "Smart Goblin": ("Money! Money! Money!",1),
        "Intangible": ("Not really there",1),
        "Giant": ("I would explain, but you are very small",1),
        "Bulky": ("I've seen many battles",1),
        "Clever": ("I've seen things beyond your comprehension",1),
        "Scholar": ("Books are my friends",1),
        "Etherborn": ("Magic is my ally",1),
        "Lucky": ("Heads i win, tails they lose",1),
        "Prepared": ("I always carry my potions with me",1),
        "Beginner's luck": ("I never found any Four Leaves Clover, they always have more", 1),
        "Backstabber": ("No matter how you face me, i'm going to stab you in the back",1),
        "Leprechaun": ("I'm lucky and i know it",1)
        }

    listtal=list(deftal.keys())

    '''
    CON : Max HP
    STR : Phys Damage
    INT : Max MP
    WIS : Magic Dodge
    Dex : Phys Dodge
    Luc : Used in encounters
    STA : Generic Damage Reduce
    SPD : Attack speed
    ??? : Magic Damage
    '''

    prettyname={
        "lpot":PrettyUI.add_color("Life Potion",PrettyUI.Life),
        "mpot":PrettyUI.add_color("Mana Potion",PrettyUI.Mana),
        "spdb":"🥾 Speed Boots",
        "dglo":"🧤 Dexterity Gloves",
        "what":"🎩 Wizard Hat",
        "lche":"🦺 Life Chest",
        "samu":"📿 Sage Amulet",
        "4lc":"🍀 Four leaf Clover",
        "sshi":"🔰 Small shield"
        }

    liststuff=list(prettyname.keys())
    liststuff.remove("lpot")
    liststuff.remove("mpot")

    def __init__(self,name,race,sex="x"):
        self.name   = name
        self.race   = race
        self.prace  = Perso.prace(race)
        self.attr={}
        for i in Perso.listattr:
            self.attr[i] = [Perso.defattr[race][i][0],0]
        self.xp     = 0
        self.lvl    = 1
        self.sex    = sex
        self.gold   = 0
        self.nbdod  = 0
        self.nbkill = 0
        self.nbinit = 0
        self.alive  = 1
        self.items  = []
        self.tallist= []
        self.bpd    = 0
        self.bmd    = 0
        self.brdc   = 0
        self.bhp    = 0
        self.bghp   = 0
        self.bmp    = 0
        self.bgmp   = 0
        self.bfa    = 0
        self.bchance= 0

        self.nbach  = 0
        self.lidod  = [5,10,25,50,100,250,500,1000]
        self.lifsa  = [5,10,25,50,100,250,500,1000]
        self.lifig  = [5,10,25,50,100,250,500,1000]
        self.quest  = [-1,-1,-1]  # reward is x*lvl, given when y=0, z is type 0 monster, 1 encounter, 2 dodge


        if race=="undead":
            self.alive += 1
        tal = random.choice(Perso.listtal)
        self.newtal(tal)
        self.welcom(tal)

    def prace(race):
        if race in PrettyUI.racecol:
            return PrettyUI.add_color(race, PrettyUI.racecol[race])
        return race

    def achiev(self,list,s="an"):
        list.pop(0)
        self.nbach += 1
        print("You completed {} achievement, here's a little boost for you".format(s))

    def welcom(self,tal):
        print ("Welcome {}. You are a young {} ready for an adventure. You have been blessed with {}. \n [{}]: {}. \n Here we go...".format(
                self.name, self.prace, PrettyUI.add_color(tal,PrettyUI.Talent), self.name, Perso.deftal[tal][0]))
        print("\n"+"*"*79)
        Perso.printlvl(self)
        print("*"*32+PrettyUI.seqspider()+"*"*32)
        self.fluff()

    def printtal(tallist):
        print("\n\tYou had the following talent{}:".format(PrettyUI.ans(len(tallist))))
        s="\t -  "
        s+=',\n\t -  '.join(tallist)+"."
        print(s)

    def printite(items):
        n=len(items)
        lit =[Perso.prettyname[x] for x in items]
        if n>0:
            print("\n\tYou had the following item{}:".format(PrettyUI.ans(n)))
            s="\t -  "
            s+=',\n\t -  '.join(lit)+"."
            print(s)

    def printattr(self):
        b=0
        s=""
        for i in Perso.listattr:
            b+=1
            if b%3==1:
                s+=" "+PrettyUI.add_color(Perso.minipic[self.race][b//3],PrettyUI.racecol[self.race])+"\t"
            s+=" "+i+" "+PrettyUI.padleft(self.attr[i][0])+"\t \t"
            if b%3==0:
                s+="\n"
        print(s)


    def newtal(self,tal,fill=True):
        Perso.listtal.remove(tal)
        if tal == "Divine Spark":
            self.alive +=1
        elif tal == "Smart Goblin":
            self.gold +=100
        elif tal == "Lucky":
            self.attr["LUC"][1]+=3
        elif tal == "Beginner's luck":
            self.attr["LUC"][0]+=10
        elif tal == "Backstabber":
            self.bfa += 2
        elif tal == "Leprechaun":
            self.bchance += 5
        elif tal == "Prepared":
            self.items.append("lpot")
            self.items.append("mpot")
        elif tal == "MC Dodger":
            self.bpd += 5
        elif tal == "Resilient":
            self.brdc += 2
        elif tal == "Intangible":
            self.bpd += 2
            self.bmd += 2
        elif tal == "Giant":
            self.bghp += 5
        elif tal == "Bulky" :
            self.bhp += 100
        elif tal == "Scholar":
            self.bgmp += 5
        elif tal == "Clever":
            self.bmp += 100
        elif tal == "Etherborn":
            self.bmd += 5
        elif tal == "Jack of all trades":
            for k in list(self.attr.keys()):
                self.attr[k][1]+=1
        self.tallist.append(tal)
        self.update(fill)

    def newitem(self,item,fill=True):
        Perso.liststuff.remove(item)
        if item == "spdb":
            self.attr["SPD"][0]+=3
        elif item == "dglo":
            self.attr["DEX"][0]+=3
        elif item == "what":
            self.attr["INT"][0]+=3
        elif item == "lche":
            self.attr["CON"][0]+=3
        elif item == "samu":
            self.attr["WIS"][0]+=3
        elif item == "4lc":
            self.attr["LUC"][0]+=3
        elif item == "sshi":
           self.attr["STA"][0]+=3
        self.items.append(item)
        self.update(False)

    def update(self,fill=True):  # Updates the dodge, red and so on for each level
       self.pdodge  = min(int((self.attr["DEX"][0])/self.lvl**0.5)+self.bpd,75)
       self.mdodge  = min(int((self.attr["WIS"][0])/self.lvl**0.5)+self.bmd,75)
       self.reduce  = min(int((max(0,self.attr["STA"][0] - self.lvl)/self.lvl)**0.4)+self.brdc,75)
       self.maxhp   = (15+self.bghp) * self.attr["CON"][0] +self.bhp
       self.maxmp   = (15+self.bgmp) * self.attr["INT"][0] +self.bmp
       self.chance  = min(75, int(10*(max(0,self.attr["LUC"][0]-self.lvl)**0.4))/10)
       self.fa      = min(int(self.attr["SPD"][0]/self.lvl**0.2+self.bfa),75)
       if fill:
           self.hp      = self.maxhp
           self.mp      = self.maxmp

    def __str__(self):
        return "{} ({}): {}: {} \t {}: {} \t {}: {}/{} \t \t {}: {}".format(
                self.name, PrettyUI.add_color(self.lvl,PrettyUI.racecol[self.race]), PrettyUI.add_color("Life",PrettyUI.Life),Perso.colhp(self.hp,self.maxhp), PrettyUI.add_color("Mana",PrettyUI.Mana), Perso.colhp(self.mp,self.maxmp),PrettyUI.add_color("XP",PrettyUI.XP), self.xp,
                Perso.xp2lvl(self.lvl), PrettyUI.add_color("Gold",PrettyUI.Gold), self.gold)

    def colhp(hp,mhp):
        if 10*hp > 9 *mhp:
            return PrettyUI.add_color(hp, PrettyUI.OKGreen)
        elif 10*hp < mhp:
            return PrettyUI.add_color(hp, PrettyUI.Danger)
        elif 3*hp < mhp:
            return PrettyUI.add_color(hp, PrettyUI.Critical)
        return str(hp)

    def nblife(self):
        s = PrettyUI.add_color("☥" * (self.alive-1),PrettyUI.Gold)
        s += PrettyUI.add_color("❤" * (self.items.count("lpot")),PrettyUI.Life)
        s += PrettyUI.add_color("✿" * (self.items.count("mpot")),PrettyUI.Mana)
        return s

    def printlvl(self):
        print ("[{} ({})] {} \t \t {} ⚔     {} 🤸     {} 💨     {} 🏆\n {}: {} \t  \t {}: {} \t \t {}: {} \n".format(
                self.name, self.prace, self.nblife(), PrettyUI.padleft(self.nbkill), PrettyUI.padleft(self.nbdod), PrettyUI.padleft(self.nbinit), PrettyUI.padleft(self.nbach), PrettyUI.add_color("Max Life",PrettyUI.Life), PrettyUI.padleft(self.maxhp), PrettyUI.add_color("Max Mana",PrettyUI.Mana), PrettyUI.padleft(self.maxmp), PrettyUI.add_color("Gold",PrettyUI.Gold), PrettyUI.padleft(self.gold)))

        self.printattr()

        print("\tP.Dodge: {}% \t \t M.Dodge: {}% \t\tC.dodge: {}% \n\tD.Reduce: {}% \t \t 1st.Att: {}% \t \t Chance: {}%".format(PrettyUI.padleft(self.pdodge,4),PrettyUI.padleft(self.mdodge,4),PrettyUI.padleft(self.pdodge*self.mdodge//10/10,4),PrettyUI.padleft(self.reduce,3),PrettyUI.padleft(self.fa,4), PrettyUI.padleft(self.chance,4)))

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
        self.xp  -= Perso.xp2lvl(self.lvl)
        self.lvl += 1
        for i in Perso.listattr:
            self.attr[i][0]+=self.attr[i][1]+random.randint(Perso.defattr[self.race][i][1][0],Perso.defattr[self.race][i][1][1])
        Perso.update(self)
        self.hp=self.maxhp
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n"+"*"*31 +" Congratulations *"+"*"*30)
        Perso.printlvl(self)
        print("*"*32+PrettyUI.seqspider()+"*"*32)
        self.fluff()
        sleep(1)

    def newxp(self,xp):
        self.xp+=xp
        if self.xp >= Perso.xp2lvl(self.lvl):
            Perso.lvlup(self)

    def damage(self,dam,name):
        self.hp -= int(dam * (1-self.reduce/100))
        if self.hp<=0:
            print ("Oh no, your character took lethal damage from the "+name+" :(")
            self.alive -=1
            if self.alive>0:
                self.hp = self.maxhp//2

    def dodge(self,t):
        hit = random.randint(0,100)
        res = [self.pdodge>hit,self.mdodge>hit,self.pdodge>hit or self.mdodge>hit][t]
        return res

    def roll(self,att,val=100):
        return random.randint(0,val) < att


    def handlefight(self):
        name, xp, dam, loot, dod = self.fight()
        if self.quest[2] == 0:
            self.quest[1] -= 1
        self.newxp(xp)
        self.nbkill+=1
        self.gold+= loot
        if not(dod):                                            # If not dodged
            if not(self.roll(self.fa,100+self.lvl)):            # If no sneak attack
                self.damage(dam,name)
                if self.alive > 0:
                    print("You fought "+random.choice(listmean)+" "+name+" and won "+str(xp)+" xp, took "+PrettyUI.givemeans(dam,"damage")+" and earned "+PrettyUI.givemeans(loot, "gold")+"!")
                else:
                    self.gold   -=1
                    self.nbkill -=1
                    return
            else:
                 print("You sneaked on "+random.choice(listmean)+" "+name+" and won "+str(xp)+" xp, you also earned "+PrettyUI.givemeans(loot, "gold")+"!")
                 self.nbinit += 1
        else:
            print("You fought a "+name+" and won "+str(xp)+" xp, avoided damage and earned "+str(loot)+" golds!")
            self.nbdod += 1
            if self.quest[2] == 1:
                self.quest[1] -= 1
        print(self)

    def checkachiev(self):
        if self.nbinit == self.lifsa[0]:
            self.bfa += 0.75
            self.achiev(self.lifsa,"a celerity")
        if self.nbkill == self.lifig[0]:
            self.attr[random.choice(Perso.listattr)][0] += 1
            self.achiev(self.lifig,"a slaying")
        if self.nbdod == self.lidod[0]:
            self.bpd += 0.5
            self.bmd += 0.5
            self.achiev(self.lidod,"a dodging")

    def checkquest(self,t=0.1):
        if self.quest[1] == 0:
            print("Congratulations, you have completed a "+Perso.quest_list[self.quest[2]]+"quest!")
            print("Here is "+str(self.lvl*self.quest[0])+PrettyUI.add_color(" Gold",PrettyUI.Gold)+" as a reward")
            self.quest[1] -= 1
            sleep(10*t)


    def handlencounter(self):
        print("\n")
        enclist=[self.alchemist,self.herbalist,self.healer,self.mspring,self.oracle,self.graal,self.osiris,self.blacksmith,self.vampireoverlord,self.scrollquest]
        a=random.choice(enclist)
        a()
        print("\n")


    def autopot(self):
        if "lpot" in self.items and self.hp < 0.2 * self.maxhp:
                print("Auto-using a "+PrettyUI.add_color("Life",PrettyUI.Life)+" potion")
                self.hp += int(0.4*self.maxhp)
                self.items.remove("lpot")

        if "mpot" in self.items and self.mp < 0.2 * self.maxmp:
                print("Auto-using a "+PrettyUI.add_color("Mana",PrettyUI.Mana)+" potion")
                self.mp += int(0.4*self.maxmp)
                self.items.remove("mpot")



    def fight(self):
        strinou = Monster.pickmonster(self.lvl)
        xp      = random.randint(max(0,strinou.xp-2),strinou.xp+self.lvl)
        dam     = random.randint(max(0,strinou.dam-5),strinou.dam+self.lvl)
        hit     = self.dodge(strinou.typ)
        loot    = random.randint(max(0,strinou.loot-5),strinou.loot+self.lvl)
        return (strinou.name,xp,dam,loot,hit)

    def get_race():
        request = 'Choose one of the following race: '
        l = [Perso.prace(x) for x in Perso.listrac]
        request += ', '.join(l) + ': '
        while True:
            ra = input(request)
            if ra not in Perso.defattr:
                PrettyUI.invalid_ans()
            else:
                return ra

    def reduc(self,price):
        race=random.choice(Perso.listrac)
        if self.race == race or self.race=="goblin":
            return int(0.9 * price),race
        return price,race

    def fluff(self):
        s=""
        box="*"*79
        if self.lvl == 1:
            s+=PrettyUI.center("It is a peaceful day, in Squirelia 🐿️")
            s+="\n"+box
        if self.lvl == 6:
            s+=("\t An invading {} army is coming from the {}, brace yourself".format(Perso.prace(random.choice(Perso.listrac)),random.choice(Perso.listcard)))
            s+="\n"+box
        elif self.lvl == 12:
            s+=PrettyUI.center("The army is gone, some spooky monsters are coming your way")
            s+="\n"+box
        elif self.lvl == 18:
            s+=PrettyUI.center("Whaaaat? They are now coming from space?")
            s+="\n"+box
        elif self.lvl == 22:
            s+=PrettyUI.center("Nagas, why does it have to be Nagas?")
            s+="\n"+box
        elif self.lvl == 24:
            s+=PrettyUI.center("Void enemies? I should have stayed in bed...")
            s+="\n"+box
        print(s)

    def herbalist(self):
          price = 200
          price,race = self.reduc(price)
          print("\t You encounter {} {} herbalist".format(random.choice(listshop),Perso.prace(race)))
          if "lpot" in self.items:
              print("Sadly, you already carry a "+PrettyUI.add_color("Life",PrettyUI.Life)+" potion "+PrettyUI.add_color("❤",PrettyUI.Life)+", they cannot sell you a new one")
          elif self.gold < price:
              print("Sadly, you don't have enough "+PrettyUI.add_color("Gold",PrettyUI.Gold)+", they cannot sell you a "+PrettyUI.add_color("Life",PrettyUI.Life)+" Potion")
          else:
              b=0
              while b<1:
                  tab1 =["Do you want to buy a", "Life potion ❤","for "+str(price)+" Gold (y/n)?"]
                  tab  =["Do you want to buy a", PrettyUI.add_color("Life",PrettyUI.Life)+" potion "+PrettyUI.add_color("❤",PrettyUI.Life),"for "+str(price)+" "+PrettyUI.add_color("Gold",PrettyUI.Gold)+" "+ yn+"?"]
                  ltabl=PrettyUI.box_strings(tab1,tab)
                  stra=PrettyUI.add_color("   .-|   ",PrettyUI.Life)+"\t"*3+ltabl[0]+"\n"
                  stra+=PrettyUI.add_color(" .-'-'-. ",PrettyUI.Life)+"\t"*3+ltabl[1]+"\n"
                  stra+=PrettyUI.add_color(" :-...-: ",PrettyUI.Life)+"\t"*3+ltabl[2]+"\n"
                  stra+=PrettyUI.add_color(" |;    |   ",PrettyUI.Life)+"\t"*3+ltabl[3]+"\n"
                  stra+=PrettyUI.add_color(" |;:   |   ",PrettyUI.Life)+"\t"*3+ltabl[4]+"\n"
                  stra+=PrettyUI.add_color(" |;:.._|   ",PrettyUI.Life)+"\t"*3+ltabl[5]+"\n"
                  stra+=PrettyUI.add_color(" `-...-'  ",PrettyUI.Life)+"\t"*3+ltabl[6]+"\n"
                  a=input(stra)
                  if a in listyes:
                      self.gold-=price
                      self.items.append("lpot")
                      print("Thank you! Be safe!")
                      b=1
                  elif a in listno:
                      print("Oh, a bold one... I'd say you'd come back crawling but we both know you won't")
                      b=1
                  else:
                      PrettyUI.invalid_ans()

    def alchemist(self):
           price = 150
           price,race = self.reduc(price)
           print("\t You encounter {} {} alchemist".format(random.choice(listshop),Perso.prace(race)))
           if "mpot" in self.items:
               print("Sadly, you already carry a "+PrettyUI.add_color("Mana",PrettyUI.Mana)+" potion "+PrettyUI.add_color("✿",PrettyUI.Mana)+", they cannot sell you a new one")
           elif self.gold < price:
               print("Sadly, you don't have enough "+PrettyUI.add_color("Gold",PrettyUI.Gold)+", they cannot sell you a "+PrettyUI.add_color("Mana",PrettyUI.Mana)+" Potion")
           else:
               b=0
               while b<1:
                   tab1 =["Do you want to buy a", "Mana potion ✿","for "+str(price)+" Gold (y/n)?"]
                   tab  =["Do you want to buy a", PrettyUI.add_color("Mana",PrettyUI.Mana)+" potion "+PrettyUI.add_color("✿",PrettyUI.Mana),"for "+str(price)+" "+PrettyUI.add_color("Gold",PrettyUI.Gold)+" "+ yn+"?"]
                   ltabl=PrettyUI.box_strings(tab1,tab)
                   stra=PrettyUI.add_color("   .-|   ",PrettyUI.Mana)+"\t"*3+ltabl[0]+"\n"
                   stra+=PrettyUI.add_color(" .-'-'-. ",PrettyUI.Mana)+"\t"*3+ltabl[1]+"\n"
                   stra+=PrettyUI.add_color(" :-...-: ",PrettyUI.Mana)+"\t"*3+ltabl[2]+"\n"
                   stra+=PrettyUI.add_color(" |;    |   ",PrettyUI.Mana)+"\t"*3+ltabl[3]+"\n"
                   stra+=PrettyUI.add_color(" |;:   |   ",PrettyUI.Mana)+"\t"*3+ltabl[4]+"\n"
                   stra+=PrettyUI.add_color(" |;:.._|   ",PrettyUI.Mana)+"\t"*3+ltabl[5]+"\n"
                   stra+=PrettyUI.add_color(" `-...-'  ",PrettyUI.Mana)+"\t"*3+ltabl[6]+"\n"
                   a=input(stra)
                   if a in listyes:
                       self.gold-=price
                       self.items.append("mpot")
                       print(PrettyUI.center("Thank you! Be safe!"))
                       b=1
                   elif a in listno:
                       print(PrettyUI.center("I understand, time is Mana!"))
                       b=1
                   else:
                       PrettyUI.invalid_ans()

    def healer(self):
           price = 150
           price,race = self.reduc(price)
           print("\t You encounter {} {} healer".format(random.choice(listshop),Perso.prace(race)))
           if self.hp >= self.maxhp:
               print("You are already at full "+PrettyUI.add_color("Life",PrettyUI.Life)+", you don't need their help")
           elif self.gold < price:
               print("Sadly, you don't have enough "+PrettyUI.add_color("Gold",PrettyUI.Gold)+", for their service")
           else:
               b=0
               while b<1:
                   tab1 =["Do you want to be healed back", "to full Life","for "+str(price)+" Gold (y/n)?"]
                   tab  =["Do you want to be healed back", "to full "+PrettyUI.add_color("Life",PrettyUI.Life),"for "+str(price)+" "+PrettyUI.add_color("Gold",PrettyUI.Gold)+" "+ yn+"?"]
                   ltabl=PrettyUI.box_strings(tab1,tab)
                   stra=PrettyUI.add_color("   ____(_",PrettyUI.Life)+"\t"*3+ltabl[0]+"\n"
                   stra+=PrettyUI.add_color("   |____|",PrettyUI.Life)+"\t"*3+ltabl[1]+"\n"
                   stra+=PrettyUI.add_color("   |  ☥ |",PrettyUI.Life)+"\t"*3+ltabl[2]+"\n"
                   stra+=PrettyUI.add_color("    \\__/  ",PrettyUI.Life)+"\t"*3+ltabl[3]+"\n"
                   stra+=" ========== "+"\t"*3+ltabl[4]+"\n"
                   stra+="   / () \   "+"\t"*3+ltabl[5]+"\n"
                   stra+="  /  ||  \  "+"\t"*3+ltabl[6]+"\n"
                   a = input(stra)
                   if a in listyes:
                       self.gold-=price
                       self.hp=self.maxhp
                       print(PrettyUI.center("Thank you! Be safe!"))
                       b=1
                   elif a in listno:
                       print(PrettyUI.center("Oh, a bold one... I'd say you'd come back crawling but we both know you won't"))
                       b=1
                   else:
                       PrettyUI.invalid_ans()

    def mspring(self):
            print(PrettyUI.center("You encounter a magic spring"))
            if self.mp >= self.maxmp:
                print("Sadly, you are already at Max "+PrettyUI.add_color("Mana",PrettyUI.Mana)+", the spring is useless")
            else:
                b=0
                while b<1:
                    tab1 =["Do you want to recover", "Mana","from the spring (y/n)?"]
                    tab  =["Do you want to recover", PrettyUI.add_color("Mana",PrettyUI.Mana),"from the spring "+yn+"?"]
                    ltabl=PrettyUI.box_strings(tab1,tab)
                    stra=PrettyUI.add_color("   .'''.'.'''.  ",PrettyUI.Mana)+"\t"*3+ltabl[0]+"\n"
                    stra+=PrettyUI.add_color("  ' .''.'.''. ' ",PrettyUI.Mana)+"\t"*3+ltabl[1]+"\n"
                    stra+=PrettyUI.add_color("    . . : . .   ",PrettyUI.Mana)+"\t"*3+ltabl[2]+"\n"
                    stra+=PrettyUI.add_color("  _'___':'___'_ ",PrettyUI.Mana)+"\t"*3+ltabl[3]+"\n"
                    stra+=" (_____________)"+"\t"*3+ltabl[4]+"\n"
                    stra+="     _)   (_    "+"\t"*3+ltabl[5]+"\n"
                    stra+="    (_______)   "+"\t"*3+ltabl[6]+"\n"
                    a=input(stra)
                    if a in listyes:
                        self.mp=self.maxmp
                        print(PrettyUI.center("Aaaah, what a delight!"))
                        b=1
                    elif a in listno:
                        print(PrettyUI.center("Ok, you know, there was no trap..."))
                        b=1
                    else:
                        PrettyUI.invalid_ans()

    def osiris(self):
                print(PrettyUI.center("You encounter a mystical god"))
                price = 2500
                if self.gold < price:
                    print("Sadly, you don't have enough "+PrettyUI.add_color("Gold",PrettyUI.Gold)+", for their service")
                else:
                    b=0
                    while b<1:
                        tab1 =["Do you want to buy", "to buy an Ankh ☥","for "+str(price)+" Gold (y/n)?"]
                        tab  =["Do you want to buy", "to buy an "+PrettyUI.add_color("Ankh ☥",PrettyUI.Gold),"for "+str(price)+" "+PrettyUI.add_color("Gold",PrettyUI.Gold)+" "+ yn+"?"]
                        ltabl=PrettyUI.box_strings(tab1,tab)
                        stra=PrettyUI.add_color(" .d88b. ",PrettyUI.Gold)+"\t"*3+ltabl[0]+"\n"
                        stra+=PrettyUI.add_color(" 88  88 ",PrettyUI.Gold)+"\t"*3+ltabl[1]+"\n"
                        stra+=PrettyUI.add_color(" '8bd8' ",PrettyUI.Gold)+"\t"*3+ltabl[2]+"\n"
                        stra+=PrettyUI.add_color("  '88'  ",PrettyUI.Gold)+"\t"*3+ltabl[3]+"\n"
                        stra+=PrettyUI.add_color(" o8888o ",PrettyUI.Gold)+"\t"*3+ltabl[4]+"\n"
                        stra+=PrettyUI.add_color("   88   ",PrettyUI.Gold)+"\t"*3+ltabl[5]+"\n"
                        stra+=PrettyUI.add_color("  d88b  ",PrettyUI.Gold)+"\t"*3+ltabl[6]+"\n"
                        a = input(stra)
                        if a in listyes:
                            self.alive+= 1
                            self.gold -= price
                            print(PrettyUI.center("Here it is. Don't worry, i'll see you later anyway!"))
                            b=1
                        elif a in listno:
                            print(PrettyUI.center("I can't wait to see you again"))
                            b=1
                        else:
                            PrettyUI.invalid_ans()

    def oracle(self):
          price = 2200
          price,race = self.reduc(price)
          print("\t You encounter {} {} oracle".format(random.choice(listshop),Perso.prace(race)))
          if  len(Perso.listtal) ==0:
              print(PrettyUI.center("You have nothing new to learn"))
          elif self.gold < price:
                    print("Sadly, you don't have enough "+PrettyUI.add_color("Gold",PrettyUI.Gold)+", for their service")
          else:
                    b=0
                    while b<1:
                        tab1 =["Do you want to buy", "a new random Talent","for "+str(price)+" Gold (y/n)?"]
                        tab  =["Do you want to buy", "a new random "+PrettyUI.add_color("Talent",PrettyUI.Talent),"for "+str(price)+" "+PrettyUI.add_color("Gold",PrettyUI.Gold)+" "+ yn+"?"]
                        ltabl=PrettyUI.box_strings(tab1,tab)
                        stra=PrettyUI.add_color("      ,,,,     ",PrettyUI.Talent)+"\t"*3+ltabl[0]+"\n"
                        stra+=PrettyUI.add_color("   ,########,  ",PrettyUI.Talent)+"\t"*3+ltabl[1]+"\n"
                        stra+=PrettyUI.add_color("  ############ ",PrettyUI.Talent)+"\t"*3+ltabl[2]+"\n"
                        stra+=PrettyUI.add_color(" |############|",PrettyUI.Talent)+"\t"*3+ltabl[3]+"\n"
                        stra+=PrettyUI.add_color("  ############ ",PrettyUI.Talent)+"\t"*3+ltabl[4]+"\n"
                        stra+=PrettyUI.add_color('   "########"  ',PrettyUI.Talent)+"\t"*3+ltabl[5]+"\n"
                        stra+=PrettyUI.add_color('      """"     ',PrettyUI.Talent)+"\t"*3+ltabl[6]+"\n"
                        a=input(stra)
                        if a in listyes:
                            tal=random.choice(Perso.listtal)
                            self.newtal(tal,False)
                            self.gold -= price
                            print("You learnt {}, congratulations".format(PrettyUI.add_color(tal,PrettyUI.Talent)))
                            b=1
                        elif a in listno:
                            print(PrettyUI.center("Some people are less talented than others"))
                            b=1
                        else:
                            PrettyUI.invalid_ans()

    def blacksmith(self):
          price = 1600
          price,race = self.reduc(price)
          print("\t You encounter {} {} blascksmith".format(random.choice(listshop),Perso.prace(race)))
          if  len(Perso.liststuff) ==0:
              print(PrettyUI.center("You have nothing new to buy"))
          elif self.gold < price:
                    print("Sadly, you don't have enough "+PrettyUI.add_color("Gold",PrettyUI.Gold)+", for their service")
          else:
                    b=0
                    while b<1:
                        tab1 =["Do you want to buy", "a new random Item","for "+str(price)+" Gold (y/n)?"]
                        tab  =["Do you want to buy", "a new random "+PrettyUI.add_color("Item",PrettyUI.Item),"for "+str(price)+" "+PrettyUI.add_color("Gold",PrettyUI.Gold)+" "+ yn+"?"]
                        ltabl=PrettyUI.box_strings(tab1,tab)
                        stra=""+"\t"*5+ltabl[0]+"\n"
                        stra+=PrettyUI.add_color(" .-------..___     ",PrettyUI.Item)+"\t"*3+ltabl[1]+"\n"
                        stra+=PrettyUI.add_color(" '-._     :_.-'    ",PrettyUI.Item)+"\t"*3+ltabl[2]+"\n"
                        stra+=PrettyUI.add_color("  .- ) _ ( --.     ",PrettyUI.Item)+"\t"*3+ltabl[3]+"\n"
                        stra+=" :  "+PrettyUI.add_color("'-' '-'",PrettyUI.Item)+"   :"+"\t"*4+ltabl[4]+"\n"
                        stra+="  '-.._____.-'  "+"\t"*3+ltabl[5]+"\n"
                        stra+=""+"\t"*5+ltabl[6]+"\n"
                        a=input(stra)
                        if a in listyes:
                            ite=random.choice(Perso.liststuff)
                            self.newitem(ite,False)
                            self.gold -= price
                            print("You bought {}, congratulations".format(PrettyUI.add_color(Perso.prettyname[ite],PrettyUI.Item)))
                            b=1
                        elif a in listno:
                            print(PrettyUI.center("Some people think it's better to travel light"))
                            b=1
                        else:
                            PrettyUI.invalid_ans()

    def graal(self):
          print("\t You found the "+PrettyUI.add_color("Graal",PrettyUI.Gold)+"!!")
          b=0
          while b<1:
              tab1 =["Do you want", "to try your luck","and grab it (y/n)?"]
              tab  =["Do you want", "to try your luck","and grab it "+yn+"?"]
              ltabl=PrettyUI.box_strings(tab1,tab)
              stra=PrettyUI.add_color("  _..,----,.._ ",PrettyUI.Gold)+"\t"*3+ltabl[0]+"\n"
              stra+=PrettyUI.add_color(" ;'-.,____,.-';",PrettyUI.Gold)+"\t"*3+ltabl[1]+"\n"
              stra+=PrettyUI.add_color(" |            |",PrettyUI.Gold)+"\t"*3+ltabl[2]+"\n"
              stra+=PrettyUI.add_color(" )            (",PrettyUI.Gold)+"\t"*3+ltabl[3]+"\n"
              stra+=PrettyUI.add_color("  \          / ",PrettyUI.Gold)+"\t"*3+ltabl[4]+"\n"
              stra+=PrettyUI.add_color("   `,.____.,'  ",PrettyUI.Gold)+"\t"*3+ltabl[5]+"\n"
              stra+=PrettyUI.add_color("    '------'   ",PrettyUI.Gold)+"\t"*3+ltabl[6]+"\n"
              a = input(stra)
              if a in listyes:
                  res = self.roll(self.chance)
                  if res:
                      print("You caught it! Behold an "+PrettyUI.add_color("extra",PrettyUI.Gold)+" life!")
                      self.alive += 1
                      self.hp = self.maxhp
                  else:
                      print(PrettyUI.center("Oh no, you failed and took some damage"))
                      self.hp -= (random.randint(15,40) * self.maxhp)//100
                      if self.hp <1:
                          self.hp = 1
                          print("Luckily, the "+PrettyUI.add_color("Graal",PrettyUI.Gold)+" prevented this damage from being lethal")
                  b=1
              elif a in listno:
                  print(PrettyUI.center("Some things are probably better left alone..."))
                  b=1
              else:
                  PrettyUI.invalid_ans()

    quest_list=["Fighting ","Dodging ","Adventuring "]

    def scrollquest(self):
          print("\t You found a "+PrettyUI.add_color("Scroll of Quest ",PrettyUI.SQuest)+"!!")
          if self.quest[1]>0:
              print("\t You are already on a "+PrettyUI.add_color("Quest ",PrettyUI.SQuest)+"!!")
              print("\t You need to go "+PrettyUI.add_color(Perso.quest_list[self.quest[2]],PrettyUI.SQuest)+str(self.quest[1])+" more times!!")
          else:
              r      = random.randint(0,2) # Enemies, Encounter, Dodger
              nb     = int(1.5*random.randint(10,20))
              reward = nb
              if r > 1:
                  nb = int(nb/1.8)
                  reward = int(1.8*reward)
              b=0
              while b<1:
                  tab1 =["Do you want", "to accept the quest of ",Perso.quest_list[r]+str(nb)+" times (y/n)?"]
                  tab  =["Do you want", "to accept the "+PrettyUI.add_color("quest",PrettyUI.SQuest)+" of ",Perso.quest_list[r]+str(nb)+" times "+yn+"?"]
                  ltabl=PrettyUI.box_strings(tab1,tab)
                  stra=PrettyUI.add_color("  ,-----------. ",PrettyUI.SQuest)+"\t"*3+ltabl[0]+"\n"
                  stra+=PrettyUI.add_color(" (_\\           \\",PrettyUI.SQuest)+"\t"*3+ltabl[1]+"\n"
                  stra+=PrettyUI.add_color("    |           |",PrettyUI.SQuest)+"\t"*3+ltabl[2]+"\n"
                  stra+=PrettyUI.add_color("    |           |",PrettyUI.SQuest)+"\t"*3+ltabl[3]+"\n"
                  stra+=PrettyUI.add_color("    |           |",PrettyUI.SQuest)+"\t"*3+ltabl[4]+"\n"
                  stra+=PrettyUI.add_color("   _|           |",PrettyUI.SQuest)+"\t"*3+ltabl[5]+"\n"
                  stra+=PrettyUI.add_color("  (_/_____(*)___/",PrettyUI.SQuest)+"\t"*3+ltabl[6]+"\n"
                  a = input(stra)
                  if a in listyes:
                      print("Here you go adventurer, "+PrettyUI.add_color("have fun",PrettyUI.SQuest)+"!")
                      self.quest=[reward,nb,r]
                      b=1
                  elif a in listno:
                      print(PrettyUI.center("Oh not interested? Ok..."))
                      b=1
                  else:
                      PrettyUI.invalid_ans()

    def vampireoverlord(self):
        gold = 500
        print(PrettyUI.center("You encounter a rich vampire"))
        b=0
        while b<1:
            tab1 =["Do you want to get bitten", "lose half your current Life","and get "+str(gold)+" Gold (y/n)?"]
            tab  =["Do you want to get bitten", "lose half your current "+PrettyUI.add_color("Life",PrettyUI.Life),"and get "+str(gold)+" "+PrettyUI.add_color("Gold",PrettyUI.Gold)+" "+ yn+"?"]
            ltabl=PrettyUI.box_strings(tab1,tab)
            stra=""+"\t"*4+ltabl[0]+"\n"
            stra+=PrettyUI.add_color("      _______",PrettyUI.Life)+"\t"*3+ltabl[1]+"\n"
            stra+=PrettyUI.add_color("    .'_/_|_\\_'.",PrettyUI.Life)+"\t"*3+ltabl[2]+"\n"
            stra+=PrettyUI.add_color("    \\`\\  |  /`/",PrettyUI.Life)+"\t"*3+ltabl[3]+"\n"
            stra+=PrettyUI.add_color("     `\\\\ | //'",PrettyUI.Life)+"\t"*3+ltabl[4]+"\n"
            stra+=PrettyUI.add_color("       `\\|/`",PrettyUI.Life)+"\t"*3+ltabl[5]+"\n"
            stra+=PrettyUI.add_color("         `"  ,PrettyUI.Life)+"\t"*3+ltabl[6]+"\n"
            a=input(stra)
            if a in listyes:
                self.hp -= self.hp //2
                self.gold += gold
                print(PrettyUI.center("Thanks for the meal"))
                b=1
            elif a in listno:
                print(PrettyUI.center("Why do i bother?"))
                b=1
            else:
                PrettyUI.invalid_ans()



def title():
   col = PrettyUI.racecol[random.choice(Perso.listrac)]
   os.system('cls' if os.name == 'nt' else 'clear')
   eye = PrettyUI.add_color("\"",PrettyUI.Gold)
   str =("   ____              "
    "    _       _      _"
    "_   __       ____   "
    "   ____      ____   "
    "\r\n "
    " / __"+eye+"| u      ___ "
    "    |"+eye+"|     |"+eye+"|   "
    "  \\ \\ / /    U |  "
    "_"+eye+"\\ u U|  _"+eye+"\\ uU"
    " /"+eye+"___|u \r\n "
    "<\\___ \\/      |_"+eye+""
    "_|  U | | u U | | u "
    "   \\ V /      \\| |"
    "_) |/ \\| |_) |/\\| "
    "|  _ / \r\n "
    " u___) |       | |  "
    "  \\| |/__ \\| |/__ "
    " U_|"+eye+"|_u      |  _ "
    "<    |  __/   | |_| "
    "|  \r\n "
    " |____/>>    U/| |\\"
    "u   |_____| |_____| "
    "  |_|        |_| \\_"
    "\\   |_|       \\___"
    "_|  \r\n "
    "  )(  (__).-,_|___|_"
    ",-.//  \\\\  //  \\"
    "\\.-,//|(_       // "
    "  \\\\_  ||>>_     _"
    ")(|_   \r\n "
    " (__)      \\_)-\' "
    "\'-(_/(_\")(\"_)(_\""
    ")(\"_)\\_) (__)     "
    "(__)  (__)(__)__)   "
    "(__)__) "
    "\n\n")
   return(str)


listmean = ["a mean","a wild","an horrible","a scary","a nasty","a cryptic","a bloody","an evil","a strong","a brooding"]
listshop = ["a traveling","a lost","a friendly","an exhausted","a curious","a clumsy","an interested","an enigmatic"]

def save_per_to_file(self):
    with open('Silly_save.sav', 'wb') as save_file:
        pickle.dump(self, save_file)

def load_per_from_file():
    with open('Silly_save.sav', 'rb') as load_file:
        per = pickle.load(load_file)
        return per

def play(t=0.2):
    print(title())
    b = False
    if os.path.isfile('./Silly_save.sav'):
        g = True
        while g:
            a = input("Save file detected do you want to load it "+yn+"?\n"+PrettyUI.add_bold(" "*9+"Refusing will overwrite it "))
            if a in listyes:
                b = True
                g = False
            elif a in listno:
                g = False
            else:
                PrettyUI.invalid_ans()

    if b :
        print("Loading...")
        global per
        per = load_per_from_file()

    else :
        n=input("Please, enter your character name: ")
        r=Perso.get_race()
        per=Perso(n,r)
    #    per.scrollquest()
    #per.printlvl()
    sleep(10*t)

    while (per.alive > 0):
    #    print(per.quest)
    #    sleep(1)
        per.handlefight()
        if per.alive > 0 and per.roll(per.nbkill % 17,20):
            per.handlencounter()
            if per.quest[2]==2:
                per.quest[1]-=1
        per.checkachiev()
        per.checkquest(t)
        per.autopot()
        sleep(2*t)
        if per.nbkill % 23 == 0:
            save_per_to_file(per)

    if per.alive <1:
        print("/"+"=-"*38+"=\\")
        print("Your lvl {} {} {} died :(".format(per.lvl, per.prace, per.name))
        per.printlvl()
        Perso.printtal(per.tallist)
        Perso.printite(per.items)
        print("\\"+"=-"*15+PrettyUI.seqspider()+"-"+"=-"*15+"=/")
        if os.path.isfile('./Silly_save.sav'):
            os.remove("./Silly_save.sav")
    else:
        print(PrettyUI.center("You stopped your adventure, good bye."))


t=0.1




if len(sys.argv) > 1:
    t=int(sys.argv[1])/10

play(t)
