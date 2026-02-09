
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk

            
class Game:
    def __init__(self):
        self.Spieler=2
        self.Wurf=[]
        self.Score=[]
        self.restart=False
        self.actualPlayer=0
        self.finish=False
        self.throw=[]
        self.Playerfinished=0
        self.Multiplier=[]
        self.NextPlayer1=False
        self.NextThrow=False
        self.Miss=False
        self.kreset=False
        self.kreset1=False
        self.k=0
        self.Multiplier1=1
        self.Score1=0
        self.boolthrow=0
        self.PThrow=(0,1)
        self.Mode=1
        self.root=root
        self.save=0
        self.save1=0
        self.save2=0
        self.save3=0
        self.NextScore=False
        self.save4=0
        self.s=""
        self.s1=""
        self.end=False
        self.p=False
        

    def GetScore(self):
        
        if(self.Playerfinished>=self.Spieler or self.finish==True):
            self.throw.clear()
            self.Multiplier.clear()
            self.finish=True
            self.end=True
            label4.configure(text="Game ended")
            
            return
        
        self.save1=0
        self.save2=0
        self.NextScore=True ##########    sollte nachher gelöscht und durch     self.NextScore, Score1, Multiplier1 =f()    ersetzt werden
                                        #f() ... Name der Funktion, man kann hier einen beliebigen Namen wählen
        # wenn zum Beispiel Triple 20 getroffen wurde:   Rückgabewert von f() -->      (True,20,3)
         
        # self.NextScore,Score1,Multiplier1=f()
        #f() soll die Daten über Schnittstelle in folgendem Format zurückgeben tuple(bool,int,int)
        # mit Funktion ersetzen, die den Rückgabetyp tuple mit folgenden Werten besitzt: (bool,int,int) erster int ist Score, zweiter int ist Multiplier--> self.NextScore, Score1, Multiplier1=Rückgabewert der Funktion
        #sollte True zurückgeben, wennn sich ein neuer Dart im Bild befindet, wenn er außerhalb der Dartscheibe liegt --> Score1 & Multiplier 1=0,0
        #sollte False zurückgeben, wenn kein neuer Dart entdeckt wurde
        if((self.NextScore==True) and (self.save!=1)):
            self.save=1                         
            Score1=int(input("Geben Sie den Score an:")) #sollte gelöscht werden
            if(self.finish==True):
                self.throw.clear()
                self.Multiplier.clear()
                self.finish=True
                self.end=True
                label4.configure(text="Game ended")
                
                return
            else:
                
                Multiplier1=int(input("Geben Sie den Multiplier an: ")) #sollte gelöscht werden
                
                self.PThrow=(Score1,Multiplier1)
                if(self.Mode==1):
                    self.root.after(20,self.NormalSchleife)
                
            
                elif(self.Mode==2):
                    self.root.after(20,self.DoubleSchleife)
                
                elif(self.Mode==3):
                    self.root.after(20,self.SSchleife)
                
                else:
                    self.root.after(20,self.ASchleife)
                
        
        elif(self.save==1):
            if(self.finish==True):
                self.throw.clear()
                self.Multiplier.clear()
                self.finish=True
                self.end=True
                label4.configure(text="Game ended")
                
                return
            else:
                pass    
        else:
            if(self.Miss==True):
                self.save=1
                self.Miss=False
                self.PThrow=(0,1)
                if(self.Mode==1):
                    self.root.after(20,self.NormalSchleife)
                elif(self.Mode==2):
                    self.root.after(20,self.DoubleSchleife)
                elif(self.Mode==3):
                    self.root.after(20,self.SSchleife)
                else:
                    self.root.after(20,self.ASchleife)
            else:
                self.root.after(20,self.GetScore)
        

    def miss(self):
        self.Miss=True    
        self.NextScore=False
        return 

    def GameEnd(self):
        self.finish=True
        
    def GetLoserPlayer(self):               
        for u in range(self.Spieler):
            if(self.Score[u]==0):
                pass
            else:
                return u
    def GetLoserPlayerG1(self):             
        for u in range(self.Spieler):
            if(self.Score[u]==26):
                pass
            else:
                return u

    def NextP(self):                   
        self.NextPlayer1=True
        return
        
    def NextPlayer(self):
        
        self.save2=0
        self.save1=0
        self.save3=0
        
        
        if(self.Playerfinished>=self.Spieler or self.finish==True):
            self.throw.clear()
            self.Multiplier.clear()
            self.finish=True
            label4.configure(text="Game ended")
            self.end=True
            return
        
        elif((self.NextPlayer1==True)and(self.save!=1)):
            
            self.save=1  
            if((self.actualPlayer+1)<self.Spieler):             
                self.actualPlayer=self.actualPlayer+1
            else:
                self.actualPlayer=0
            self.NextPlayer1=False
            label4.configure(text="")
            self.s=""
            label3.configure(text="Player {}".format((self.actualPlayer)+1))
            
            self.s1="Score:\n"
            for b in range(self.Spieler):
                if(((self.Score[b]==0)and(self.Mode==1 or self.Mode==2))or((self.Score[b]==26)and(self.Mode==3 or self.Mode==4))):
                    self.s1=self.s1+"\nPlayer: {}  You are finished".format((b+1))
                elif(self.Mode==1 or self.Mode==2):
                    self.s1=self.s1+"\nPlayer: {}  Score: {}".format((b+1),self.Score[b])
                else:
                    self.s1=self.s1+"\nPlayer: {}  NextGoalScore: {}".format((b+1),self.Score[b])
            label5.configure(text=self.s1)
            
            if(self.Mode==1):
                
                self.root.after(20,self.HerunterspielenModeNormal)
            elif(self.Mode==2):
               
                self.root.after(20,self.HerunterspielenModeDouble)
            elif(self.Mode==3):
                
                self.root.after(20,self.AroundTheClockSimple)
            else:
                
                self.root.after(20,self.AroundTheClockAdvanced)
                
        elif(self.save==1):
            pass
        else:
            
            self.save=0
            self.root.after(20,self.NextPlayer)

    def NextPlayer2(self):
        self.save2=0
        self.save1=0
        if(self.save!=1):
            self.save=1
            
            if((self.actualPlayer+1)<self.Spieler):             
                self.actualPlayer=self.actualPlayer+1
            else:
                self.actualPlayer=0
            self.NextPlayer1=False
            label4.configure(text="")
            self.s=""
            label3.configure(text="Player {}".format((self.actualPlayer)+1))
            self.s1="Score:\n"
            for b in range(self.Spieler):
                if(((self.Score[b]==0)and(self.Mode==1 or self.Mode==2))or((self.Score[b]==26)and(self.Mode==3 or self.Mode==4))):
                    self.s1=self.s1+"\nPlayer: {}  You are finished".format((b+1))
                elif(self.Mode==1 or self.Mode==2):
                    self.s1=self.s1+"\nPlayer: {}  Score: {}".format((b+1),self.Score[b])
                else:
                    self.s1=self.s1+"\nPlayer: {}  NextGoalScore: {}".format((b+1),self.Score[b])
            label5.configure(text=self.s1)
            if(self.Mode==1):
                self.root.after(20,self.HerunterspielenModeNormal)
            elif(self.Mode==2):
                self.root.after(20,self.HerunterspielenModeDouble)
            elif(self.Mode==3):
                self.root.after(20,self.AroundTheClockSimple)
            else:
                self.root.after(20,self.AroundTheClockAdvanced)
        else:
            pass
        
    def Herunterspielen(self,Spieleranzahl,Punkte,DoubleOut):
        self.Playerfinished=0
        self.p=False
        self.s=""
        label4.configure(text="")
        label3.configure(text="Player 1")
        self.save=0
        self.save1=0
        self.save2=0
        self.end=False
        if(self.save4!=1):
            self.save4=1
            self.finish=False
            if(Spieleranzahl<2):
                self.Spieler=4
            else:
                self.Spieler=Spieleranzahl
            self.Score.clear()
            self.actualPlayer=0
            self.throw.clear()
            self.Multiplier.clear()
            self.Playerfinished=0
            for i in range(Spieleranzahl):
                self.Score.append(None)
        
            for j in range(self.Spieler):
                if(Punkte>100):
                    self.Score[j]=Punkte
                else:
                    self.Score[j]=501
                    
            self.s1="Score:\n"
            for b in range(self.Spieler):
                if(((self.Score[b]==0)and(self.Mode==1 or self.Mode==2))or((self.Score[b]==26)and(self.Mode==3 or self.Mode==4))):
                    self.s1=self.s1+"\nPlayer: {}  You are finished".format((b+1))
                else:
                    self.s1=self.s1+"\nPlayer: {}  Score: {}".format((b+1),self.Score[b])
            label5.configure(text=self.s1)
            
            if(DoubleOut==False):
                self.Mode=1
                self.root.after(20,self.HerunterspielenModeNormal)
            else:
                self.Mode=2
                self.root.after(20,self.HerunterspielenModeDouble)
        else:
            pass
        


    def HerunterspielenModeNormal(self):
        self.p=False
        self.save4=0
        self.save1=0
        self.save=0
        if(self.save2!=1):
            if(self.Playerfinished>=self.Spieler):
                
                self.throw.clear()
                self.Multiplier.clear()
                label4.configure(text="Game ended")
                return
            self.save2=1
            self.save1=0
            self.save=0               
            if(self.finish==True):
                self.throw.clear()
                self.Multiplier.Clear()
                label4.configure(text="Game ended")
                return
            self.throw.clear()
            self.Multiplier.clear()
            if(self.Score[self.actualPlayer]==0):
                self.root.after(20,self.NextPlayer2)
                
            
            self.k=0
            self.root.after(20,self.ModeNormalSchleife)
        else:
            self.k=self.k+1
            self.root.after(20,self.ModeNormalSchleife)
        

    def NormalSchleife(self):
        
        self.save=0
        self.save1=0
        self.save3=0
        if(self.save2!=1): 
            
            self.save2=1
            Score, Multiplier=self.PThrow
            
            
            if(Score==0):
                self.throw.append(0)
                self.s=self.s+(("\nPlayer: {}  Throw{}: Miss").format((self.actualPlayer+1),(self.k+1)))
                label4.configure(text="{}".format(self.s))
            elif(self.finish==True or self.Playerfinished>=self.Spieler):
                self.throw.clear()
                self.Multiplier.clear()
                label4.configure(text="Game ended")
                return
            else:
                self.throw.append((Score*Multiplier))
                self.Multiplier.append(Multiplier)
                self.s=self.s+(("\nPlayer: {}  Throw{}: {}  Multiplier: {}  Score: {}").format((self.actualPlayer+1),(self.k+1),Score,Multiplier,(Multiplier*Score)))
                label4.configure(text="{}".format(self.s))
                
            if(self.k==0):
                if(self.Score[self.actualPlayer]-(self.throw[0])<0):
                    self.Score[self.actualPlayer]=self.Score[self.actualPlayer]
                    self.s=self.s+("\n\nPlayer: Player{}    Your Score got resettet       Score: {}".format((self.actualPlayer+1),self.Score[self.actualPlayer]))
                    self.s=self.s+("\nZiehe die Dartpfeile heraus\nKlicke dann auf NextPlayer")
                    label4.configure(text="{}".format(self.s))
                    self.throw.clear()
                    self.Multiplier.clear()
                    self.root.after(20,self.NextPlayer)
                elif(self.Score[self.actualPlayer]-(self.throw[0])==0):
                    self.Score[self.actualPlayer]=0
                    self.Playerfinished=self.Playerfinished+1
                    if(self.Playerfinished>=self.Spieler):
                        self.throw.clear()
                        self.Multiplier.clear()
                        self.finish=True
                        label4.configure(text="Game ended")
                        return
                    else:
                        self.s=self.s+("\n\nPlayer: Player{}  Score: You finished {}st/nd/rd/th".format((self.actualPlayer+1),self.Playerfinished))
                        self.s=self.s+("\nZiehe die Dartpfeile heraus\nKlicke dann auf NextPlayer")
                        label4.configure(text="{}".format(self.s))
                        self.throw.clear()
                        self.Multiplier.clear()
                        if(self.Playerfinished>=(self.Spieler-1)):
                            self.throw.clear()
                            self.Multiplier.clear()
                            label4.configure(text="Game ended")
                            self.finish=True
                            
                            
                            return
                        else:
                            self.throw.clear()
                            self.Multiplier.clear()
                            self.root.after(20,self.NextPlayer)
                else:
                    self.k=self.k+1
                    self.root.after(20,self.ModeNormalSchleife)
                    
                        
                                  
            elif(self.k==1):
                if(self.Score[self.actualPlayer]-(self.throw[0]+self.throw[1])<0):
                    self.s=self.s+("\n\nPlayer: Player{}    Your Score got resettet       Score: {}".format((self.actualPlayer+1),self.Score[self.actualPlayer]))
                    self.s=self.s+("\nZiehe die Dartpfeile heraus\nKlicke dann auf NextPlayer")
                    label4.configure(text="{}".format(self.s))
                    self.Score[self.actualPlayer]=self.Score[self.actualPlayer]
                    self.k=0
                    self.throw.clear()
                    self.Multiplier.clear()
                    self.root.after(20,self.NextPlayer)
                elif(self.Score[self.actualPlayer]-(self.throw[0]+self.throw[1])==0):
                    self.Score[self.actualPlayer]=0
                    self.Playerfinished=self.Playerfinished+1
                    if(self.Playerfinished>=self.Spieler):
                        
                        self.throw.clear()
                        self.Multiplier.clear()
                        self.finish=True
                        label4.configure(text="Game ended")
                        return
                    else:
                        self.s=self.s+("\nPlayer: Player{}  Score: You finished {}st/nd/rd/th\n\n".format((self.actualPlayer+1),self.Playerfinished))
                        self.s=self.s+("\nZiehe die Dartpfeile heraus\nKlicke dann auf NextPlayer")
                        label4.configure(text="{}".format(self.s))
                        self.throw.clear()
                        self.Multiplier.clear()
                        self.k=-1
                        if(self.Playerfinished>=(self.Spieler-1)):
                            self.throw.clear()
                            self.Multiplier.clear()
                            self.finish=True
                            label4.configure(text="Game ended")
                            
                            return
                        else:
                            self.throw.clear()
                            self.Multiplier.clear()
                            self.root.after(20,self.NextPlayer)
                else:
                    self.k=self.k+1
                    self.root.after(20,self.ModeNormalSchleife)
                    
            else:
                self.root.after(20,self.MNS)
            

            
            
            
        else:  
            pass
        
    def MNS(self):
        self.save=0
        self.save2=0
        self.save3=0
        if(self.save1!=1):
            
            
            
            self.save1=1
            if(self.finish==True):
                self.throw.clear()
                self.Multiplier.clear()
                label4.configure(text="Game ended")
                return
            elif(self.Score[self.actualPlayer]-(self.throw[0]+self.throw[1]+self.throw[2])<0):
                self.Score[self.actualPlayer]=self.Score[self.actualPlayer]
                self.s=self.s+("\n\nPlayer: Player{}    Your Score got resettet       Score: {}".format((self.actualPlayer+1),self.Score[self.actualPlayer]))
                self.s=self.s+("\nZiehe die Dartpfeile heraus\nKlicke dann auf NextPlayer")
                label4.configure(text="{}".format(self.s))
                self.root.after(20,self.NextPlayer)
                
                
            elif(self.Score[self.actualPlayer]-(self.throw[0]+self.throw[1]+self.throw[2])==0):
                self.Score[self.actualPlayer]=self.Score[self.actualPlayer]-(self.throw[0]+self.throw[1]+self.throw[2])
                self.Playerfinished=self.Playerfinished+1
                if(self.Playerfinished>=self.Spieler):
                    
                    self.throw.clear()
                    self.Multiplier.clear()
                    self.finish=True
                    label4.configure(text="Game ended")
                    return
                else:
                    self.s=self.s+("n\nPlayer: Player{}  Score: You finished {}st/nd/rd/th".format((self.actualPlayer+1),self.Playerfinished))
                    self.s=self.s+("\nZiehe die Dartpfeile heraus\nKlicke dann auf NextPlayer")
                    label4.configure(text="{}".format(self.s))
                    self.throw.clear()
                    self.Multiplier.clear()
                    self.root.after(20,self.NextPlayer)
            else:
                self.Score[self.actualPlayer]=self.Score[self.actualPlayer]-(self.throw[0]+self.throw[1]+self.throw[2])
                self.s=self.s+("\n\nPlayer: Player{}  Score: {}".format((self.actualPlayer+1),self.Score[self.actualPlayer]))
                self.s=self.s+("\nZiehe die Dartpfeile heraus\nKlicke dann auf NextPlayer")
                label4.configure(text="{}".format(self.s))
                self.throw.clear()
                self.Multiplier.clear()
                self.root.after(20,self.NextPlayer)
            
        else:
            pass
        
        
        
    def ModeNormalSchleife(self):
        self.save2=0
        self.save=0
        if(self.Playerfinished>=self.Spieler):
            self.throw.clear()
            self.Multiplier.clear()
            self.finish=True
            label4.configure(text="Game ended")
            return
        elif(self.Score[self.actualPlayer]==0 and self.save1!=1):
            self.root.after(20,self.NextPlayer2)
            self.save1=1
            
        elif(self.save1!=1):
            self.save1=1
            if((self.k<3)and(self.finish==False)):
                if(self.end==True):
                    self.throw.clear()
                    self.Multiplier.clear()
                    self.finish=True
                    label4.configure(text="Game ended")
                    return
                else:
                    self.root.after(20,self.GetScore)
                    self.save1=1
            
            
            else:
                if(self.finish==True):
                    self.throw.clear()
                    self.Multiplier.clear()
                    label4.configure(text="Game ended")       
                    
                    return
                else:
                    
                    self.root.after(20,self.HerunterspielenModeNormal)
                    
            
        else:
            pass
            

    def HerunterspielenModeDouble(self):
        self.p=False
        self.save4=0
        self.save3=0
        self.save1=0
        self.save=0
        if(self.save2!=1):
            self.save2=1
            if(self.finish==False):
                self.throw.clear()
                self.Multiplier.clear()
                if(self.Score[self.actualPlayer]==0):
                    self.root.after(20,self.NextPlayer2)
                else:
                    
                    self.k=0
                    self.root.after(20,self.ModeDoubleSchleife)
            else:
            
                self.throw.clear()
                self.Multiplier.clear()
                label4.configure(text="Game ended")
                return
        else:
            pass

    def DoubleSchleife(self):
        self.save=0
        self.save1=0
        self.save3=0
        if(self.save2!=1): 
            
            self.save2=1
            Score, Multiplier=self.PThrow
            if(Score==0):
                self.throw.append(0)
                self.Multiplier.append(1)
                self.s=self.s+(("\nPlayer: {}  Throw{}: Miss").format((self.actualPlayer+1),(self.k+1)))
                label4.configure(text="{}".format(self.s))
            elif(self.finish==True):
                self.k=2
            else:
                self.throw.append(Score*Multiplier)
                self.Multiplier.append(Multiplier)
                self.s=self.s+(("\nPlayer: {}  Throw{}: {}  Multiplier: {}  Score: {}").format((self.actualPlayer+1),(self.k+1),Score,Multiplier,(Multiplier*Score)))
                label4.configure(text="{}".format(self.s))

            if(self.k==0):
                if((self.Score[self.actualPlayer]-(self.throw[0])<0)or((self.Score[self.actualPlayer]-(self.throw[0])<1)and(self.Multiplier[0]!=2))or(((self.Score[self.actualPlayer]-(self.throw[0])<1)and(self.Score[self.actualPlayer]-(self.throw[0])>0))and(self.Multiplier[0]==2))):
                    self.Score[self.actualPlayer]=self.Score[self.actualPlayer]
                    self.s=self.s+("\n\nPlayer: Player{}    Your Score got resettet       Score: {}".format((self.actualPlayer+1),self.Score[self.actualPlayer]))
                    self.s=self.s+("\nZiehe die Dartpfeile heraus\nKlicke dann auf NextPlayer")
                    label4.configure(text="{}".format(self.s))        
                    
                    self.throw.clear()
                    self.Multiplier.clear()
                    self.root.after(20,self.NextPlayer)
                    
                            
                elif((self.Score[self.actualPlayer]-(self.throw[0])==0)and(self.Multiplier[0]==2)):
                    self.Score[self.actualPlayer]=0
                    self.Playerfinished=self.Playerfinished+1
                    if(self.Playerfinished>=self.Spieler):
                        self.throw.clear()
                        self.Multiplier.clear()
                        self.finish=True
                        label4.configure(text="Game ended")
                        return
                                
                    else:
                        self.s=self.s+("\n\nPlayer: Player{}  Score: You finished {}st/nd/rd/th".format((self.actualPlayer+1),self.Playerfinished))
                        self.s=self.s+("\nZiehe die Dartpfeile heraus\nKlicke dann auf NextPlayer")
                        label4.configure(text="{}".format(self.s))
                        self.throw.clear()
                        self.Multiplier.clear()
                        
                        if(self.Playerfinished>=(self.Spieler-1)):
                            self.throw.clear()
                            self.Multiplier.clear()
                            self.finish=True
                            label4.configure(text="Game ended")
                            return
                        else:
                                    
                            self.root.after(20,self.NextPlayer)
                else:
                    self.k=self.k+1
                    self.root.after(20,self.ModeDoubleSchleife)
                    
                                
                              
            elif(self.k==1):
                if((self.Score[self.actualPlayer]-(self.throw[0]+self.throw[1])<0)or((self.Score[self.actualPlayer]-(self.throw[0]+self.throw[1])<1)and(self.Multiplier[1]!=2))or(((self.Score[self.actualPlayer]-(self.throw[0]+self.throw[1])<1)and(self.Score[self.actualPlayer]-(self.throw[0]+self.throw[1])>0))and(self.Multiplier[0]==2))):
                    self.s=self.s+("\n\nPlayer: Player{}    Your Score got resettet       Score: {}".format((self.actualPlayer+1),self.Score[self.actualPlayer]))
                    self.s=self.s+("\nZiehe die Dartpfeile heraus\nKlicke dann auf NextPlayer")
                    label4.configure(text="{}".format(self.s))
                    self.Score[self.actualPlayer]=self.Score[self.actualPlayer]
                    self.root.after(20,self.NextPlayer)
                    self.throw.clear()
                    self.Multiplier.clear()
                    self.root.after(20,self.NextPlayer)
                            
                elif((self.Score[self.actualPlayer]-(self.throw[0]+self.throw[1])==0)and(self.Multiplier[1]==2)):
                    self.Score[self.actualPlayer]=0
                    self.Playerfinished=self.Playerfinished+1
                    if(self.Playerfinished>=self.Spieler):
                        self.throw.clear()
                        self.Multiplier.clear()
                        self.finish=True
                        label4.configure(text="Game ended")
                        return
                                
                                
                    else:
                        self.s=self.s+("\n\nPlayer: Player{}  Score: You finished {}st/nd/rd/th".format((self.actualPlayer+1),self.Playerfinished))
                        self.s=self.s+("\nZiehe die Dartpfeile heraus\nKlicke dann auf NextPlayer")
                        label4.config(text="{}".format(self.s))
                        if(self.Playerfinished>=(self.Spieler-1)):
                            self.throw.clear()
                            self.Multiplier.clear()
                            self.finish=True
                            label4.configure(text="Game ended")
                            return
                        else:
                            self.throw.clear()
                            self.Multiplier.clear()
                            self.k=-1
                            self.root.after(20,self.NextPlayer)
                else:
                    self.k=self.k+1
                    self.root.after(20,self.ModeDoubleSchleife)
                 
            else:
                self.k=self.k+1
                self.root.after(20,self.MDS)
        else:
            pass
        

    def MDS(self):
        self.save=0
        self.save2=0
        self.save3=0
        if(self.save1!=1):
            print(10)
            self.save1=1
            if(self.finish==True):
                self.root.after(20,self.HerunterspielenModeDouble)
            elif(((self.Score[self.actualPlayer]-(self.throw[0]+self.throw[1]+self.throw[2]))==0)and(self.Multiplier[2]==2)):
                self.Score[self.actualPlayer]=self.Score[self.actualPlayer]-(self.throw[0]+self.throw[1]+self.throw[2])
                self.Playerfinished=self.Playerfinished+1
                if(self.Playerfinished>=self.Spieler):
                    self.throw.clear()
                    self.Multiplier.clear()
                    self.finish=True
                    label4.configure(text="Game ended")
                    return
                else:
                    self.s=self.s+("\n\nPlayer: Player{}  Score: You finished {}st/nd/rd/th".format((self.actualPlayer+1),self.Playerfinished))
                    self.s=self.s+("\nZiehe die Dartpfeile heraus\nKlicke dann auf NextPlayer")
                    label4.configure(text="{}".format(self.s))
                    if(self.Playerfinished>=(self.Spieler-1)):
                        self.throw.clear()
                        self.Multiplier.clear()
                        self.finish=True
                        label4.configure(text="Game ended")
                        return

                    else:
                        self.root.after(20,self.NextPlayer)

            elif((self.Score[self.actualPlayer]-(self.throw[0]+self.throw[1]+self.throw[2]))>=1):
                self.Score[self.actualPlayer]=self.Score[self.actualPlayer]-(self.throw[0]+self.throw[1]+self.throw[2])
                self.s=self.s+("\n\nPlayer: Player{}  Score: {}".format((self.actualPlayer+1),self.Score[self.actualPlayer]))
                self.s=self.s+("\nZiehe die Dartpfeile heraus\nKlicke dann auf NextPlayer")
                label4.configure(text="{}".format(self.s))
                self.root.after(20,self.NextPlayer)

            else:
                self.Score[self.actualPlayer]=self.Score[self.actualPlayer]
                self.s=self.s+("\n\nPlayer: Player{}    Your Score got resettet       Score: {}".format((self.actualPlayer+1),self.Score[self.actualPlayer]))
                self.s=self.s+("\nZiehe die Dartpfeile heraus\nKlicke dann auf NextPlayer")
                label4.configure(text="{}".format(self.s))
                self.root.after(20,self.NextPlayer)

        
    def ModeDoubleSchleife(self):
        self.save2=0
        self.save=0
        self.save3=0
        if(self.Playerfinished>=self.Spieler):
            self.throw.clear()
            self.Multiplier.clear()
            self.finish=True
            label4.configure(text="Game ended")
            return
        if(self.save1!=1):
            self.save1=1
            if((self.k<3)and(self.finish==False)):
                if(self.Score[self.actualPlayer]==0):   
                    if((self.actualPlayer+1)<self.Spieler):
                        self.actualPlayer=self.actualPlayer+1
                    else:
                        self.actualPlayer=0
                if(self.end==True):
                    self.throw.clear()
                    self.Multiplier.clear()
                    self.finish=True
                    label4.configure(text="Game ended")
                    return
                else:
                    self.root.after(20,self.GetScore)      
            
            else:
                self.root.after(20,self.HerunterspielenModeDouble)
        else:
            pass









    def Start_AroundTheClock(self,Spieleranzahl,simple):
        self.p=False
        label4.configure(text="")
        label3.configure(text="Player 1")
        self.end=False
        self.s=""
        label4.configure(text="{}".format(self.s))
        self.save=0
        self.save1=0
        self.save2=0
        self.save3=0
        self.k=0
        if(self.save4!=1):
            self.save4=1
            self.Score.clear()
            self.actualPlayer=0
            self.Playerfinished=0

            self.finish=False
            
            if(Spieleranzahl<2):
                self.Spieler=4
            else:
                self.Spieler=Spieleranzahl
            for a in range(self.Spieler):
                self.Score.append(1)
                
            self.s1="Score:\n"
            for b in range(self.Spieler):
                if(((self.Score[b]==0)and(self.Mode==1 or self.Mode==2))or((self.Score[b]==26)and(self.Mode==3 or self.Mode==4))):
                    self.s1=self.s1+"\nPlayer: {}  You are finished".format((b+1))
                else:
                    self.s1=self.s1+"\nPlayer: {}  NextGoalScore: {}".format((b+1),self.Score[b])
            label5.configure(text=self.s1)
            
            if(simple==True):
                self.Mode=3
                self.root.after(20,self.AroundTheClockSimple)
            else:
                self.Mode=4
                self.root.after(20,self.AroundTheClockAdvanced)
        else:
            pass
        
            

    def AroundTheClockSimple(self):
        self.p=False
        self.save=0
        self.save4=0
        self.save2=0
        self.save3=0
        
        if(self.finish==False):
            if(self.save1!=1):
                self.save1=1
                self.throw.clear()
                self.Multiplier.clear()
                self.k=0

                self.root.after(20,self.SimpleSchleife)
            else:
                pass

        else:
            self.throw.clear()
            self.Multiplier.clear()
            self.finish=True
            label4.configure(text="Game ended")
            return

    def SSchleife(self):
        self.save=0
        self.save2=0
        self.save3=0
        if(self.save1!=1):
            Score, Multiplier=self.PThrow
            if(Score==0):
                self.throw.append(0)
                self.Multiplier.append(0)
                self.Score[self.actualPlayer]=self.Score[self.actualPlayer]
                self.s=self.s+(("\nPlayer: {}  Throw{}: Miss").format((self.actualPlayer+1),(self.k+1)))
                self.s=self.s+"\nPlayer: {}  NextGoalScore: {}\n".format((self.actualPlayer+1),self.Score[self.actualPlayer])
                label4.configure(text="{}".format(self.s))
            elif(self.finish==True):
                self.throw.clear()
                self.Multiplier.clear()
                self.finish=True
                label4.configure(text="Game ended")
                return
            else:
                self.throw.append(Score)
                self.Multiplier.append(Multiplier)
                        
            
                if(self.Score[self.actualPlayer]==26):
                    self.k=-1
                    self.s=self.s+("\nZiehe die Dartpfeile heraus\nKlicke dann auf NextPlayer")
                    label4.configure(text="{}".format(self.s))
                    self.root.after(20,self.NextPlayer)
                elif(self.throw[self.k]==self.Score[self.actualPlayer]):
                    if((self.Score[self.actualPlayer])<25):
                        if(self.Score[self.actualPlayer]<=19):
                            self.Score[self.actualPlayer]=self.Score[self.actualPlayer]+1
                            
                        else:
                            self.Score[self.actualPlayer]=25
                        self.s=self.s+(("\nPlayer: {}  Throw{}: {}  Multiplier: {}\nNextGoalSector: {}\n").format((self.actualPlayer+1),(self.k+1),Score,Multiplier,self.Score[self.actualPlayer]))
                        label4.configure(text="{}".format(self.s))
                    else:
                        self.Score[self.actualPlayer]=26
                        self.Playerfinished=self.Playerfinished+1
                        if(self.Playerfinished>=self.Spieler):
                            self.throw.clear()
                            self.Multiplier.clear()
                            self.finish=True
                            label4.configure(text="Game ended")
                            return
                        else:
                            self.s=self.s+("n\nPlayer: Player{}  Score: You finished {}st/nd/rd/th".format((self.actualPlayer+1),self.Playerfinished))
                            self.s=self.s+("\nZiehe die Dartpfeile heraus\nKlicke dann auf NextPlayer")
                            label4.configure(text="{}".format(self.s))
                            if(self.Playerfinished>=(self.Spieler-1)):
                                self.throw.clear()
                                self.Multiplier.clear()
                                self.finish=True
                                label4.configure(text="Game ended")
                                return
                            else:
                                self.k=-1
                                self.throw.clear()
                                self.Multiplier.clear()
                                self.root.after(20,self.NextPlayer)
                                    

                            
                else:
                    self.Score[self.actualPlayer]=self.Score[self.actualPlayer]
                    self.s=self.s+(("\nPlayer: {}  Throw{}: {}  Multiplier: {}\nYou got resettet   NextGoalSector: {}\n").format((self.actualPlayer+1),(self.k+1),Score,Multiplier,self.Score[self.actualPlayer]))
                    label4.configure(text="{}".format(self.s))
            if(self.k==2):
                self.k=-1
                self.throw.clear()
                self.Multiplier.clear()
                if(self.finish==False):
                    self.s=self.s+("\nZiehe die Dartpfeile heraus\nKlicke dann auf NextPlayer")
                    
                    label4.configure(text="{}".format(self.s))
                    self.root.after(20,self.NextPlayer)
            else:
                self.k=self.k+1
                self.root.after(20,self.SimpleSchleife)
        else:
            pass
        
    def SimpleSchleife(self):
        self.save=0
        self.save1=0
        self.save3=0
        if(self.save2!=1):
            self.save2=1
            if((self.k<3)and(self.finish==False)):
                if(self.end==True):
                    self.throw.clear()
                    self.Multiplier.clear()
                    self.finish=True
                    label4.configure(text="Game ended")
                    return
                else:
                    self.root.after(20,self.GetScore)
            
            else:
                if(self.finish==False):
                    self.s=self.s+("\nZiehe die Dartpfeile heraus\nKlicke dann auf NextPlayer")
                    label4.configure(text="{}".format(self.s))
                    self.root.after(20,self.NextPlayer)
                else:
                    self.throw.clear()
                    self.Multiplier.clear()
                    self.finish=True
                    label4.configure(text="Game ended")
                    return
        else:
            pass

    def AroundTheClockAdvanced(self):
        self.p=False
        self.save=0
        self.save4=0
        self.save2=0
        self.save3=0
        if(self.finish==False):
            if(self.save1!=1):
                self.save1=1
                self.throw.clear()
                self.Multiplier.clear()
                self.k=0
            
                self.root.after(20,self.AdvancedSchleife)
            else:
                pass
        else:
            self.throw.clear()
            self.Multiplier.clear()
            self.finish=True
            label4.configure(text="Game ended")
            return

    def ASchleife(self):
        self.save=0
        self.save2=0
        self.save3=0
        if(self.save1!=1):
            Score, Multiplier=self.PThrow
            if(Score==0):
                self.throw.append(0)
                self.Multiplier.append(0)
                self.s=self.s+(("\nPlayer: {}  Throw{}: Miss\nNextGoalSector: {}\n").format((self.actualPlayer+1),(self.k+1),self.Score[self.actualPlayer]))
                label4.configure(text="{}".format(self.s))
            elif(self.finish==True):
                    self.throw.clear()
                    self.Multiplier.clear()
                    self.finish=True
                    label4.configure(text="Game ended")
                    return
            else:
                self.throw.append(Score)
                self.Multiplier.append(Multiplier)
                        
            
                if(self.Score[self.actualPlayer]==26):
                    self.k=-1
                    self.s=self.s+("\nZiehe die Dartpfeile heraus\nKlicke dann auf NextPlayer")
                    label4.configure(text="{}".format(self.s))
                    self.root.after(20,self.NextPlayer)
                elif(self.throw[self.k]==self.Score[self.actualPlayer]):
                    if((self.Score[self.actualPlayer]+self.Multiplier[self.k])<25):
                        if((self.Score[self.actualPlayer]+self.Multiplier[self.k])<=20):
                            self.Score[self.actualPlayer]=self.Score[self.actualPlayer]+self.Multiplier[self.k]
                        else:
                            self.Score[self.actualPlayer]=25
                        self.s=self.s+(("\nPlayer: {}  Throw{}: {}  Multiplier: {}\nNextGoalSector: {}\n").format((self.actualPlayer+1),(self.k+1),Score,Multiplier,self.Score[self.actualPlayer]))
                        label4.configure(text="{}".format(self.s))
                    else:
                        self.Score[self.actualPlayer]=26
                        self.Playerfinished=self.Playerfinished+1
                        if(self.Playerfinished>=self.Spieler):
                            self.throw.clear()
                            self.Multiplier.clear()
                            self.finish=True
                            label4.configure(text="Game ended")
                            return
                        else:
                            self.s=self.s+("n\nPlayer: Player{}  Score: You finished {}st/nd/rd/th".format((self.actualPlayer+1),self.Playerfinished))
                            self.s=self.s+("\nZiehe die Dartpfeile heraus\nKlicke dann auf NextPlayer")
                            label4.configure(text="{}".format(self.s))
                            if(self.Playerfinished>=(self.Spieler-1)):
                                self.throw.clear()
                                self.Multiplier.clear()
                                self.finish=True
                                label4.configure(text="Game ended")
                                return
                            else:
                                self.k=-1
                                self.throw.clear()
                                self.Multiplier.clear()
                                self.s=self.s+("\nZiehe die Dartpfeile heraus\nKlicke dann auf NextPlayer")
                                label4.configure(text="{}".format(self.s))
                                self.root.after(20,self.NextPlayer)

                            
                else:
                    self.Score[self.actualPlayer]=self.Score[self.actualPlayer]
                    self.s=self.s+(("\nPlayer: {}  Throw{}: {}  Multiplier: {}\nYou got resettet   NextGoalSector: {}\n").format((self.actualPlayer+1),(self.k+1),Score,Multiplier,self.Score[self.actualPlayer]))
                    label4.configure(text="{}".format(self.s))
            if(self.k==2):
                self.k=-1
                self.throw.clear()
                self.Multiplier.clear()
                if(self.finish==False):
                    self.s=self.s+("\nZiehe die Dartpfeile heraus\nKlicke dann auf NextPlayer")
                    label4.configure(text="{}".format(self.s))
                    self.root.after(20,self.NextPlayer)
            elif(self.Score[self.actualPlayer]!=26):
                self.root.after(20,self.AdvancedSchleife)
            self.k=self.k+1
        else:
            pass
            
                

    def AdvancedSchleife(self):
        self.save=0
        self.save1=0
        self.save3=0
        if(self.save2!=1):
            self.save2=1
            if((self.k<3)and(self.finish==False)):
                if(self.end==True):
                    self.throw.clear()
                    self.Multiplier.clear()
                    self.finish=True
                    label4.configure(text="Game ended")
                    return
                else:
                    self.root.after(20,self.GetScore)
            else:
                if(self.finish==False):
                    self.root.after(20,self.AroundTheClockAdvanced)
                else:
                    self.throw.clear()
                    self.Multiplier.clear()
                    self.finish=True
                    label4.configure(text="Game ended")
                    return
        else:
            pass



   
       
def Herunterspielen1():
    
    
    
    fenster.deiconify()
    root.withdraw()
    
    Spiel.Herunterspielen(int(text1.get("1.0","1.2")),int(text2.get("1.0","1.3")),c1.get())
    
def ATK():
     
    
    
    fenster.deiconify()
    root.withdraw()
    
    
    Spiel.Start_AroundTheClock(int(text1.get("1.0","1.2")),c2.get())
    
def destroy():
        
    root.deiconify()
    fenster.withdraw()
    Spiel.GameEnd
    

root=ctk.CTk()
root.geometry("500x300")
root.title("Dartspiel - Setup")
Spiel=Game()

fenster=ctk.CTkToplevel(root)
fenster.geometry("1000x600")
fenster.title("Spielstand")
button1=ctk.CTkButton(fenster, text="EndGame",command=destroy, font=("Arial",36), height=100, width=200)
button1.place(x=700,y=450)
button2=ctk.CTkButton(fenster, text="NextPlayer",command=Spiel.NextP, font=("Arial",36), height=100, width=200)
button2.place(x=400,y=450)
button3=ctk.CTkButton(fenster, text="Miss",command=Spiel.miss, font=("Arial",36), height=100, width=200)
button3.place(x=100,y=450)
label3=ctk.CTkLabel(fenster,text="Player 0", anchor="w", font=("Arial",22))
label3.place(x=30,y=30)
label4=ctk.CTkLabel(fenster,text="",justify=ctk.LEFT, font=("Arial",22))
label4.place(x=30,y=60)
label5=ctk.CTkLabel(fenster,text="Score:\n\n", anchor="w", font=("Arial",22))
label5.place(x=600,y=30)
fenster.withdraw()

button4=ctk.CTkButton(root, text="Herunterspielen",command=Herunterspielen1, anchor="w", font=("Arial",24))
button4.place(x=30,y=150)
button5=ctk.CTkButton(root, text="AroundTheClock",command=ATK, anchor="w", font=("Arial",24))
button5.place(x=30,y=190)
text1=ctk.CTkTextbox(root,height=2,width=150, font=("Arial",22))
text1.place(x=300,y=95)
label1=ctk.CTkLabel(root,text="Startscore:", anchor="w", font=("Arial",22))
label1.place(x=30,y=50)
label2=ctk.CTkLabel(root,text="Spieleranzahl:",anchor="w", font=("Arial",22))
label2.place(x=30,y=100)
text2=ctk.CTkTextbox(root,height=2,width=150, font=("Arial",22))
text2.place(x=300,y=45)
c1=ctk.IntVar()
c2=ctk.IntVar()
cb1=ctk.CTkCheckBox(root,text="DoubleOut", variable=c1, onvalue=True, offvalue=False, font=("Arial",24))
cb1.place(x=300,y=150)
cb2=ctk.CTkCheckBox(root,text="Simple", variable=c2, onvalue=True, offvalue=False, font=("Arial",24))
cb2.place(x=300,y=190)
root.mainloop()

