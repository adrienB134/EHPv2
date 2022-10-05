# -*- coding: utf-8 -*-
"""
Created on Mon Jun  7 16:18:02 2021

@author: Adrien Berthélémé

code écrit d'abord comme un script pour sortir les courbes d'une EHP qui a 
évolué pour devenir un programme avec interface graphique pour toutes les EHP
si c'était a refaire je ferais ça plus proprement en écrivant une fonction 
(ou une classe peut être) pour chaque courbe dans laquelle on viendrait passer
en arguments les spec du palier et la frame pandas. Le code serait plus propre comme ça.  '
"""

from tkinter import * 
from tkinter.filedialog import askopenfilename 
from tkinter.filedialog import askdirectory
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import xlwt

import numpy as np
import pandas as pd
import gc
#import numpy.random.common #Sert pour faire un executable inutile sinon
#import numpy.random.bounded_integers #Sert pour faire un executable inutile sinon
#import numpy.random.entropy #Sert pour faire un executable inutile sinon



def courbesDPY():
    def mkdir_p(mypath):
        '''Creates a directory. equivalent to using mkdir -p on the command line'''
        from errno import EEXIST
        from os import makedirs,path

        try:
            makedirs(mypath)
        except OSError as exc: # Python >2.5
                if exc.errno == EEXIST and path.isdir(mypath):
                    pass
                else: raise
     
    if filepath=="":
        fenetre4=Tk()
        w=Label(fenetre4, text="Veuillez selectionner un fichier de données")
        w.pack()
        Bouton=Button(fenetre4, text="Fermer", command=fenetre4.destroy)
        Bouton.pack() 
        return() 
    if savepath=="":
        fenetre3=Tk()
        w=Label(fenetre3, text="Veuillez selectionner un dossier de sauvegarde")
        w.pack()
        Bouton=Button(fenetre3, text="Fermer", command=fenetre3.destroy)
        Bouton.pack() 
        return()    

    output_dir = savepath+"/Courbes épreuve"
    mkdir_p(output_dir)

    #
    
    ##### Début du traçage de courbes #####
    
    gc.collect() #vide la mémoire
    
    EHPdata = pd.read_csv(filepath ,sep=';', header=15)
    
    
    #print(EHPdata)
    
    Date=pd.to_datetime(EHPdata.Horodatage, infer_datetime_format=True, dayfirst=True)
    
    
    
    #print(Date)
    
    ##Evolution de la pression RCP pendant l'épreuve
    ##
    #
    fig,ax1 = plt.subplots()
    plt.plot(Date,EHPdata.EHP001MP, label='EHP001MP', linewidth=0.5)
    plt.plot(Date,EHPdata.EHP002MP, label='EHP002MP', linewidth=0.5)
    plt.title("Evolution de la pression RCP pendant l'épreuve")
    plt.xlabel("Date")
    plt.ylabel("Pression (bar)")
    plt.xticks(rotation=30)
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y\n%H:%M"))#Passage en format européen
    #ax1.xaxis.set_minor_formatter(mdates.DateFormatter("%d-%m-%y\n%H:%M"))
    plt.legend(loc='upper left')
    plt.grid(color = 'grey', linestyle = '--', linewidth = 0.25)
    #plt.legend()
    plt.tight_layout() #sert à ce que la figure ne dépasse pas des bords du PDF
    plt.savefig("{}/Evolution de la pression RCP pendant l'épreuve.pdf".format(output_dir))
    #plt.show()
    
    ###Evolution de la pression de refoulement de la pompe RCV191PO
    ##
    ##
    fig,ax2 = plt.subplots()
    plt.plot(Date,EHPdata.EHP003MP, label='EHP003MP', linewidth=0.5)
    plt.hlines(236,np.min(Date), np.max(Date),linewidth=0.5, colors='purple', label='Pression limite EHP003MP 236bars')
    plt.hlines(232,np.min(Date), np.max(Date),linewidth=0.5, colors='red', label='Seuil arrêt de la pompe \nRCV191PO 232bars')
    plt.hlines(228,np.min(Date), np.max(Date),linewidth=0.5, colors='orange', label='Seuil alarme haute pression de refoulement \nRCV191PO 228bars')
    plt.title("Evolution de la pression de refoulement de la pompe RCV191PO")
    plt.xlabel("Date")
    plt.ylabel("Pression (bar)")
    plt.xticks(rotation=30)
    ax2.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y\n%H:%M")) #Passage en format européen
    plt.legend(loc='center left', fontsize=6)
    plt.grid(color = 'grey', linestyle = '--', linewidth = 0.25)
    plt.tight_layout() #sert à ce que la figure ne dépasse pas des bords du PDF
    plt.savefig("{}/Pression de refoulement RCV191PO.pdf".format(output_dir))
    #plt.show()
    
    ###Evolution de la pression de refoulement de la pompe RCV191PO
    ##
    ##
    fig,ax3 = plt.subplots()
    #filtrage pour avoir que l'épreuve
    EHP003MPfilt=EHPdata["EHP003MP"]>4
    positions = np.flatnonzero(EHP003MPfilt)
    maskEHP003MP=EHPdata.iloc[positions]
    DateEpreuveMule=pd.to_datetime(maskEHP003MP.Horodatage, infer_datetime_format=True, dayfirst=True)
    #debug
    #print(maskEHP003MP.EHP003MP)
    
    
    plt.plot(DateEpreuveMule,maskEHP003MP.EHP003MP, label='EHP003MP',linewidth=0.5)
    if not DateEpreuveMule.empty:
        plt.hlines(236,np.min(DateEpreuveMule), np.max(DateEpreuveMule),linewidth=0.5, colors='purple', label='Pression limite EHP003MP 236bars')
        plt.hlines(232,np.min(DateEpreuveMule), np.max(DateEpreuveMule),linewidth=0.5, colors='red', label='Seuil arrêt de la pompe \nRCV191PO 232bars')
        plt.hlines(228,np.min(DateEpreuveMule), np.max(DateEpreuveMule),linewidth=0.5, colors='orange', label='Seuil alarme haute pression de refoulement \nRCV191PO 228bars')
    plt.title("Evolution de la pression de refoulement de la pompe RCV191PO")
    plt.xlabel("Date")
    plt.ylabel("Pression (bar)")
    plt.xticks(rotation=30)#rotation des dates sur l'axe x pour meilleure lisibilité
    ax3.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y\n%H:%M")) #Passage en format européen
    plt.legend(loc='lower center', fontsize=6)
    plt.grid(color = 'grey', linestyle = '--', linewidth = 0.25)
    plt.tight_layout() #sert à ce que la figure ne dépasse pas des bords du PDF
    plt.savefig("{}/Evolution de la pression de refoulement RCV191PO - détail.pdf".format(output_dir))
    #plt.show()
    
    ##Température des gros composants du CPP - Fond de cuve
    ##
    #
    fig,ax4 = plt.subplots()
    plt.plot(Date,EHPdata.EHP001MT, label='EHP001MT', linewidth=0.5)
    plt.plot(Date,EHPdata.EHP002MT, label='EHP002MT',linewidth=0.5)
    plt.plot(Date,EHPdata.EHP003MT, label='EHP003MT', linewidth=0.5)
    plt.title("Température des gros composants du CPP - Fond de cuve")
    plt.xlabel("Date")
    plt.ylabel("Température (°C)")
    plt.xticks(rotation=30)#rotation des dates sur l'axe x pour meilleure lisibilité
    ax4.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y\n%H:%M")) #Passage en format européen
    plt.legend(loc='lower center')
    plt.grid(color = 'grey', linestyle = '--', linewidth = 0.25)
    plt.tight_layout() #sert à ce que la figure ne dépasse pas des bords du PDF
    plt.savefig("{}/Température des gros composants.pdf".format(output_dir))
    #plt.show()
    
    ##Température des gros composants - couvercle&pressu
    ##
    #
    fig,ax5 = plt.subplots()
    plt.plot(Date,EHPdata.EHP004MT, label='EHP004MT - Bride de cuve', linewidth=0.5)
    plt.plot(Date,EHPdata.EHP005MT, label='EHP005MT - Bride de couvercle',linewidth=0.5)
    plt.plot(Date,EHPdata.EHP006MT, label='EHP006MT - JEP Pressu', linewidth=0.5)
    plt.title("Température des gros composants du CPP")
    plt.xlabel("Date")
    plt.ylabel("Température (°C)")
    plt.xticks(rotation=30) #rotation des dates sur l'axe x pour meilleure lisibilité
    ax5.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y\n%H:%M")) #Passage en format européen
    plt.legend(loc='lower center')
    plt.grid(color = 'grey', linestyle = '--', linewidth = 0.25)
    plt.tight_layout() #sert à ce que la figure ne dépasse pas des bords du PDF
    plt.savefig("{}/Température des gros composants - couvercle&pressu.pdf".format(output_dir))
    #plt.show()
    
    ##Température des gros composants - GVs
    ##
    #
    fig,ax6 = plt.subplots()
    plt.plot(Date,EHPdata.EHP007MT, label='EHP007MT - GV1', linewidth=0.5)
    plt.plot(Date,EHPdata.EHP008MT, label='EHP008MT - GV2',linewidth=0.5)
    plt.plot(Date,EHPdata.EHP009MT, label='EHP009MT - GV3', linewidth=0.5)
    plt.plot(Date,EHPdata.EHP010MT, label='EHP010MT - GV4', linewidth=0.5)
    plt.title("Température des gros composants du CPP")
    plt.xlabel("Date")
    plt.ylabel("Température (°C)")
    plt.xticks(rotation=30) #rotation des dates sur l'axe x pour meilleure lisibilité
    ax6.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y\n%H:%M")) #Passage en format européen
    plt.legend(loc='lower center')
    plt.grid(color = 'grey', linestyle = '--', linewidth = 0.25)
    plt.tight_layout() #sert à ce que la figure ne dépasse pas des bords du PDF
    plt.savefig("{}/Température des gros composants - GVs.pdf".format(output_dir))
    #plt.show()
    
    
    ##Gradients de pression
    ##
    #
    fig,ax7 = plt.subplots()
    plt.plot(Date,EHPdata.EHP001MPGrad, label='EHP001MPGrad', linewidth=0.5)
    plt.plot(Date,EHPdata.EHP002MPGrad, label='EHP002MPGrad',linewidth=0.5)
    plt.hlines(4,np.min(Date), np.max(Date), colors='purple', label='Valeur Max Gradient (+4 bar/min)', linewidth=0.5)
    plt.hlines(-4,np.min(Date), np.max(Date), colors='purple', label='Valeur Min Gradient (-4 bar/min)', linewidth=0.5)
    plt.title("Gradients de Pression de l'EHP")
    plt.xlabel("Date")
    plt.ylabel("Gradient de pression en bar/min")
    ax7.set_ylim(-15,15) #limitation de y à -15/+15
    plt.xticks(rotation=30) #rotation des dates sur l'axe x pour meilleure lisibilité
    ax7.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y\n%H:%M")) #Passage en format européen
    plt.legend(loc='lower left', fontsize=6)
    plt.grid(color = 'grey', linestyle = '--', linewidth = 0.25)
    plt.tight_layout() #sert à ce que la figure ne dépasse pas des bords du PDF
    plt.savefig("{}/Gradients de pression.pdf".format(output_dir))
    #plt.show() 
    
    ##Suivi Tmoy
    ##
    #
    fig,ax8 = plt.subplots()
    plt.plot(Date,EHPdata.TMOY, label='Tmoy', linewidth=0.5)
    plt.title("Suivi de la Tmoy de l'EHP")
    plt.xlabel("Date")
    plt.ylabel("Température (°C)")
    plt.xticks(rotation=30) #rotation des dates sur l'axe x pour meilleure lisibilité
    ax8.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y\n%H:%M")) #Passage en format européen
    plt.legend(loc='lower center')
    plt.grid(color = 'grey', linestyle = '--', linewidth = 0.25)
    plt.tight_layout() #sert à ce que la figure ne dépasse pas des bords du PDF
    plt.savefig("{}/Suivi Tmoy.pdf".format(output_dir))
    #plt.show() 
    
    ##Suivi gradient Tmoy
    ##
    #
    fig,ax9 = plt.subplots()
    plt.plot(Date,EHPdata.TGRAD, label='Tgrad', linewidth=0.5)
    
    #limites de gradient
    #filtrage pour avoir T>50
    TMOYfiltsup=EHPdata["TMOY"]>50
    positions = np.flatnonzero(TMOYfiltsup)
    maskTMOYfiltsup=EHPdata.iloc[positions]
    DateTmoysup50=pd.to_datetime(maskTMOYfiltsup.Horodatage, infer_datetime_format=True, dayfirst=True)
    
    
    
    #filtrage pour avoir T<50
    TMOYfiltinf=EHPdata["TMOY"]<50
    positions = np.flatnonzero(TMOYfiltinf)
    maskTMOYfiltinf=EHPdata.iloc[positions]
    DateTmoyinf50=pd.to_datetime(maskTMOYfiltinf.Horodatage, infer_datetime_format=True, dayfirst=True)
    
    
    #filtrage pour avoir T=50
    TMOYfiltegal=EHPdata["TMOY"]==50
    positions = np.flatnonzero(TMOYfiltegal)
    maskTMOYfiltegal=EHPdata.iloc[positions]
    DateTmoyegal50=pd.to_datetime(maskTMOYfiltegal.Horodatage, infer_datetime_format=True, dayfirst=True)
    
    if not DateTmoysup50.empty:
        plt.hlines(28,np.min(DateTmoysup50), np.max(DateTmoysup50), colors='purple', label='+/-28°C/h', linewidth=1)
        plt.hlines(-28,np.min(DateTmoysup50), np.max(DateTmoysup50), colors='purple', linewidth=1)
    plt.vlines(DateTmoyegal50,-28,-14, colors='purple', linewidth=0.5)
    plt.vlines(DateTmoyegal50,28,14, colors='purple', linewidth=0.5)
    if not DateTmoysup50.empty:
        if not DateTmoyegal50.empty:
            plt.hlines(14,np.min(DateTmoyinf50), np.min(DateTmoyegal50), colors='orange', label='+/-14°C/h', linewidth=0.5)
            plt.hlines(-14,np.min(DateTmoyinf50), np.min(DateTmoyegal50), colors='orange', linewidth=0.5)
            plt.hlines(14, np.max(DateTmoyegal50), np.max(DateTmoyinf50), colors='orange', linewidth=0.5)
            plt.hlines(-14, np.max(DateTmoyegal50),np.max(DateTmoyinf50), colors='orange', linewidth=0.5)
    
    #Fin limites de gradient
    
    plt.title("Suivi du gradient de Tmoy de l'EHP")
    plt.xlabel("Date")
    plt.ylabel("Température (°C)")
    plt.xticks(rotation=30) #rotation des dates sur l'axe x pour meilleure lisibilité
    ax9.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y\n%H:%M")) #Passage en format européen
    plt.legend(loc='upper left')
    plt.grid(color = 'grey', linestyle = '--', linewidth = 0.25)
    plt.tight_layout() #sert à ce que la figure ne dépasse pas des bords du PDF
    plt.savefig("{}/Suivi Tgrad.pdf".format(output_dir))
    
    #plt.show() 
    
    ##Suivi des températures fluide pendant l'EHP
    ##
    #
 
    fig,ax10 = plt.subplots()
    plt.plot(Date,EHPdata.RCP009MT, label='RCP009MT', linewidth=0.5)
    plt.plot(Date,EHPdata.RCP010MT, label='RCP014MT', linewidth=0.5) 
    plt.plot(Date,EHPdata.RCP028MT, label='RCP0100MT', linewidth=0.5) 
    
    plt.title("Suivi des températures fluide pendant l'EHP")
    plt.xlabel("Date")
    plt.ylabel("Température (°C/h)")
    plt.xticks(rotation=30) #rotation des dates sur l'axe x pour meilleure lisibilité
    ax10.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y\n%H:%M")) #Passage en format européen
    plt.legend(loc='lower center')
    plt.grid(color = 'grey', linestyle = '--', linewidth = 0.25)
    plt.tight_layout() #sert à ce que la figure ne dépasse pas des bords du PDF
    plt.savefig("{}/Suivi des températures fluide pendant l'EHP - 1.pdf".format(output_dir))
    #plt.show() 
    
    fig,ax101 = plt.subplots()
    plt.plot(Date,EHPdata.RCP029MT, label='RCP104MT', linewidth=0.5) 
    plt.plot(Date,EHPdata.RCP043MT, label='RCP200MT', linewidth=0.5) 
    plt.plot(Date,EHPdata.RCP044MT, label='RCP204MT', linewidth=0.5) 
   
    plt.title("Suivi des températures fluide pendant l'EHP")
    plt.xlabel("Date")
    plt.ylabel("Température (°C/h)")
    plt.xticks(rotation=30) #rotation des dates sur l'axe x pour meilleure lisibilité
    ax101.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y\n%H:%M")) #Passage en format européen
    plt.legend(loc='lower center')
    plt.grid(color = 'grey', linestyle = '--', linewidth = 0.25)
    plt.tight_layout() #sert à ce que la figure ne dépasse pas des bords du PDF
    plt.savefig("{}/Suivi des températures fluide pendant l'EHP - 2.pdf".format(output_dir))
    #plt.show()
    
    fig,ax102 = plt.subplots()

    plt.plot(Date,EHPdata.RCP055MT, label='RCP300MT', linewidth=0.5) 
    plt.plot(Date,EHPdata.RCP056MT, label='RCP304MT', linewidth=0.5) 
    plt.plot(Date,EHPdata.RCP055MT, label='RCP400MT', linewidth=0.5) 
    plt.plot(Date,EHPdata.RCP056MT, label='RCP404MT', linewidth=0.5)
    plt.title("Suivi des températures fluide pendant l'EHP")
    plt.xlabel("Date")
    plt.ylabel("Température (°C/h)")
    plt.xticks(rotation=30) #rotation des dates sur l'axe x pour meilleure lisibilité
    ax102.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y\n%H:%M")) #Passage en format européen
    plt.legend(loc='lower center')
    plt.grid(color = 'grey', linestyle = '--', linewidth = 0.25)
    plt.tight_layout() #sert à ce que la figure ne dépasse pas des bords du PDF
    plt.savefig("{}/Suivi des températures fluide pendant l'EHP - 3.pdf".format(output_dir))
    #plt.show() 
    
    ##Gradient des températures métal pendant l'EHP - 1
    ##
    #
    fig,ax11 = plt.subplots()
    plt.plot(Date,EHPdata.EHP001MTGrad, label='EHP001MTGrad', linewidth=0.5)
    plt.plot(Date,EHPdata.EHP002MTGrad, label='EHP002MTGrad', linewidth=0.5)
    plt.plot(Date,EHPdata.EHP003MTGrad, label='EHP003MTGrad', linewidth=0.5)
    
    
    plt.title("Gradient des températures métal pendant l'EHP - Fond de cuve")
    plt.xlabel("Date")
    plt.ylabel("Gradient de température (°C/h)")
    plt.xticks(rotation=30) #rotation des dates sur l'axe x pour meilleure lisibilité
    ax11.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y\n%H:%M")) #Passage en format européen
    ax11.set_ylim(-30,30) #limitation de y à -30/+30
    plt.legend(loc='lower right', fontsize = 6, ncol=2)
    plt.grid(color = 'grey', linestyle = '--', linewidth = 0.25)
    plt.tight_layout() #sert à ce que la figure ne dépasse pas des bords du PDF
    plt.savefig("{}/Gradient des températures métal pendant l'EHP - Fond de cuve.pdf".format(output_dir))
    #plt.show() 
    
    ##Gradient des températures métal pendant l'EHP - Couvercle et pressu
    ##
    #
    fig,ax14 = plt.subplots()
    
    plt.plot(Date,EHPdata.EHP004MTGrad, label='EHP004MTGrad - Bride de cuve', linewidth=0.5)
    plt.plot(Date,EHPdata.EHP005MTGrad, label='EHP005MTGrad - Bride de couvercle', linewidth=0.5)
    plt.plot(Date,EHPdata.EHP006MTGrad, label='EHP006MTGrad - JEP Pressu', linewidth=0.5)
    
    plt.title("Gradient des températures métal pendant l'EHP - Couvercle et Pressu")
    plt.xlabel("Date")
    plt.ylabel("Gradient de température (°C/h)")
    plt.xticks(rotation=30) #rotation des dates sur l'axe x pour meilleure lisibilité
    ax14.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y\n%H:%M")) #Passage en format européen
    ax14.set_ylim(-30,30) #limitation de y à -30/+30
    plt.legend(loc='lower right', fontsize = 6, ncol=2)
    plt.grid(color = 'grey', linestyle = '--', linewidth = 0.25)
    plt.tight_layout() #sert à ce que la figure ne dépasse pas des bords du PDF
    plt.savefig("{}/Gradient des températures métal pendant l'EHP - Couvercle et pressu.pdf".format(output_dir))
    #plt.show() 
    
    ##Gradient des températures métal pendant l'EHP - GV
    ##
    #
    fig,ax15 = plt.subplots()
    
    plt.plot(Date,EHPdata.EHP007MTGrad, label='EHP007MTGrad - GV1', linewidth=0.5)
    plt.plot(Date,EHPdata.EHP008MTGrad, label='EHP008MTGrad - GV2', linewidth=0.5)
    plt.plot(Date,EHPdata.EHP009MTGrad, label='EHP009MTGrad - GV3', linewidth=0.5)
    plt.plot(Date,EHPdata.EHP010MTGrad, label='EHP010MTGrad - GV4', linewidth=0.5)
    plt.title("Gradient des températures métal pendant l'EHP - GV")
    plt.xlabel("Date")
    plt.ylabel("Gradient de température (°C/h)")
    plt.xticks(rotation=30) #rotation des dates sur l'axe x pour meilleure lisibilité
    ax15.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y\n%H:%M")) #Passage en format européen
    ax15.set_ylim(-30,30) #limitation de y à -30/+30
    plt.legend(loc='lower right', fontsize = 6, ncol=2)
    plt.grid(color = 'grey', linestyle = '--', linewidth = 0.25)
    plt.tight_layout() #sert à ce que la figure ne dépasse pas des bords du PDF
    plt.savefig("{}/Gradient des températures métal pendant l'EHP - GV.pdf".format(output_dir))
    #plt.show() 
    
    ###Evolution de la pression pendant l'épreuve
    ##
    ##
    fig,ax12 = plt.subplots()
    #filtrage pour avoir que le palier
    EHP001MPfilt=EHPdata["EHP001MP"]>172
    positions = np.flatnonzero(EHP001MPfilt)
    maskEHP001MP=EHPdata.iloc[positions]
    DateEpreuveMule=pd.to_datetime(maskEHP001MP.Horodatage, infer_datetime_format=True, dayfirst=True)
    EHP002MPfilt=EHPdata["EHP002MP"]>172
    positions = np.flatnonzero(EHP002MPfilt)
    maskEHP002MP=EHPdata.iloc[positions]
    DateEpreuveMule2=pd.to_datetime(maskEHP002MP.Horodatage, infer_datetime_format=True, dayfirst=True)
    
    
    plt.plot(DateEpreuveMule,maskEHP001MP.EHP001MP, label='EHP001MP', linewidth=0.5)
    plt.plot(DateEpreuveMule2,maskEHP002MP.EHP002MP, label='EHP002MP', linewidth=0.5)
    if not DateEpreuveMule.empty:
        plt.hlines(207.8,np.min(DateEpreuveMule), np.max(DateEpreuveMule), colors='purple', label='207.8 bar', linewidth=0.5)
        plt.hlines(206.9,np.min(DateEpreuveMule), np.max(DateEpreuveMule), colors='purple', label='206,9 bar', linewidth=0.5)
    
    plt.title("Evolution de la pression pendant le palier d'épreuve")
    plt.xlabel("Date")
    plt.ylabel("Pression (bar)")
    plt.xticks(rotation=30)#rotation des dates sur l'axe x pour meilleure lisibilité
    ax12.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y\n%H:%M")) #Passage en format européen
    plt.legend(loc='upper left')
    plt.grid(color = 'grey', linestyle = '--', linewidth = 0.25)
    plt.tight_layout() #sert à ce que la figure ne dépasse pas des bords du PDF
    plt.savefig("{}/Evolution de la pression pendant l'épreuve.pdf".format(output_dir))
    #plt.show()
    
    ###Evolution de la pression pendant le palier 206bar
    ##
    ##
    fig,ax13 = plt.subplots()
    #filtrage pour avoir que le palier
    EHP001MPfilt=EHPdata["EHP001MP"]>205
    positions = np.flatnonzero(EHP001MPfilt)
    maskEHP001MP=EHPdata.iloc[positions]
    DateEpreuveMule=pd.to_datetime(maskEHP001MP.Horodatage, infer_datetime_format=True, dayfirst=True)
    EHP002MPfilt=EHPdata["EHP002MP"]>205
    positions = np.flatnonzero(EHP002MPfilt)
    maskEHP002MP=EHPdata.iloc[positions]
    DateEpreuveMule2=pd.to_datetime(maskEHP002MP.Horodatage, infer_datetime_format=True, dayfirst=True)
    
    
    plt.plot(DateEpreuveMule,maskEHP001MP.EHP001MP, label='EHP001MP', linewidth=0.5)
    plt.plot(DateEpreuveMule2,maskEHP002MP.EHP002MP, label='EHP002MP', linewidth=0.5)
    if not DateEpreuveMule.empty:
        plt.hlines(206,np.min(DateEpreuveMule), np.max(DateEpreuveMule), colors='purple', label='206 bar', linewidth=0.5)
        plt.hlines(206.9,np.min(DateEpreuveMule), np.max(DateEpreuveMule), colors='purple', label='206,9 bar', linewidth=0.5)
    plt.title("Evolution de la pression pendant le palier d'épreuve")
    plt.xlabel("Date")
    plt.ylabel("Pression (bar)")
    plt.xticks(rotation=30)#rotation des dates sur l'axe x pour meilleure lisibilité
    ax13.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y\n%H:%M")) #Passage en format européen
    plt.legend(loc='lower center')
    plt.grid(color = 'grey', linestyle = '--', linewidth = 0.25)
    plt.tight_layout() #sert à ce que la figure ne dépasse pas des bords du PDF
    plt.savefig("{}/Evolution de la pression pendant le palier 206bar.pdf".format(output_dir))
    if value2.get()==1:
        plt.show()
    
    ##
    gc.collect() #vide la mémoire

def courbesPQY():
    def mkdir_p(mypath):
        '''Creates a directory. equivalent to using mkdir -p on the command line'''
        from errno import EEXIST
        from os import makedirs,path

        try:
            makedirs(mypath)
        except OSError as exc: # Python >2.5
                if exc.errno == EEXIST and path.isdir(mypath):
                    pass
                else: raise
                
    if filepath=="":
        fenetre4=Tk()
        w=Label(fenetre4, text="Veuillez selectionner un fichier de données")
        w.pack()
        Bouton=Button(fenetre4, text="Fermer", command=fenetre4.destroy)
        Bouton.pack() 
        return() 
    if savepath=="":
        fenetre3=Tk()
        w=Label(fenetre3, text="Veuillez selectionner un dossier de sauvegarde")
        w.pack()
        Bouton=Button(fenetre3, text="Fermer", command=fenetre3.destroy)
        Bouton.pack() 
        return()    

    output_dir = savepath+"/Courbes épreuve"
    mkdir_p(output_dir)

    #
    
    ##### Début du traçage de courbes #####
    
    gc.collect() #vide la mémoire
    
    EHPdata = pd.read_csv(filepath ,sep=';', header=15)
    
    
    #print(EHPdata)
    
    Date=pd.to_datetime(EHPdata.Horodatage, infer_datetime_format=True, dayfirst=True)
    
    
    
    #print(Date)
    
    ##Evolution de la pression RCP pendant l'épreuve
    ##
    #
    fig,ax1 = plt.subplots()
    plt.plot(Date,EHPdata.EHP001MP, label='EHP001MP', linewidth=0.5)
    plt.plot(Date,EHPdata.EHP002MP, label='EHP002MP', linewidth=0.5)
    plt.title("Evolution de la pression RCP pendant l'épreuve")
    plt.xlabel("Date")
    plt.ylabel("Pression (bar)")
    plt.xticks(rotation=30)
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y\n%H:%M")) #Passage en format européen
    plt.legend(loc='upper left')
    plt.grid(color = 'grey', linestyle = '--', linewidth = 0.25)
    plt.tight_layout() #sert à ce que la figure ne dépasse pas des bords du PDF
    plt.savefig("{}/Evolution de la pression RCP pendant l'épreuve.pdf".format(output_dir))
    #plt.show()
    
    ###Evolution de la pression de refoulement de la pompe RCV191PO
    ##
    ##
    fig,ax2 = plt.subplots()
    plt.plot(Date,EHPdata.EHP003MP, label='EHP003MP', linewidth=0.5)
    plt.hlines(244,np.min(Date), np.max(Date),linewidth=0.5, colors='purple', label='Pression limite EHP003MP 244bars')
    plt.hlines(239,np.min(Date), np.max(Date),linewidth=0.5, colors='red', label='Seuil arrêt de la pompe \nRCV191PO 239bars')
    plt.hlines(234,np.min(Date), np.max(Date),linewidth=0.5, colors='orange', label='Seuil alarme haute pression de refoulement \nRCV191PO 234bars')
    plt.title("Evolution de la pression de refoulement de la pompe RCV191PO")
    plt.xlabel("Date")
    plt.ylabel("Pression (bar)")
    plt.xticks(rotation=30)
    ax2.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y\n%H:%M")) #Passage en format européen
    plt.legend(loc='center left', fontsize=6)
    plt.grid(color = 'grey', linestyle = '--', linewidth = 0.25)
    plt.tight_layout() #sert à ce que la figure ne dépasse pas des bords du PDF
    plt.savefig("{}/Pression de refoulement RCV191PO.pdf".format(output_dir))
    #plt.show()
    
    ###Evolution de la pression de refoulement de la pompe RCV191PO
    ##
    ##
    fig,ax3 = plt.subplots()
    #filtrage pour avoir que l'épreuve
    EHP003MPfilt=EHPdata["EHP003MP"]>4
    positions = np.flatnonzero(EHP003MPfilt)
    maskEHP003MP=EHPdata.iloc[positions]
    DateEpreuveMule=pd.to_datetime(maskEHP003MP.Horodatage, infer_datetime_format=True, dayfirst=True)
    #debug
    #print(maskEHP003MP.EHP003MP)
    
    
    plt.plot(DateEpreuveMule,maskEHP003MP.EHP003MP, label='EHP003MP',linewidth=0.5)
    if not DateEpreuveMule.empty:
        plt.hlines(244,np.min(DateEpreuveMule), np.max(DateEpreuveMule),linewidth=0.5, colors='purple', label='Pression limite EHP003MP 244bars')
        plt.hlines(239,np.min(DateEpreuveMule), np.max(DateEpreuveMule),linewidth=0.5, colors='red', label='Seuil arrêt de la pompe \nRCV191PO 239bars')
        plt.hlines(234,np.min(DateEpreuveMule), np.max(DateEpreuveMule),linewidth=0.5, colors='orange', label='Seuil alarme haute pression de refoulement \nRCV191PO 234bars')
    plt.title("Evolution de la pression de refoulement de la pompe RCV191PO")
    plt.xlabel("Date")
    plt.ylabel("Pression (bar)")
    plt.xticks(rotation=30)#rotation des dates sur l'axe x pour meilleure lisibilité
    ax3.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y\n%H:%M")) #Passage en format européen
    plt.legend(loc='lower center', fontsize=6)
    plt.grid(color = 'grey', linestyle = '--', linewidth = 0.25)
    plt.tight_layout() #sert à ce que la figure ne dépasse pas des bords du PDF
    plt.savefig("{}/Evolution de la pression de refoulement RCV191PO - détail.pdf".format(output_dir))
    #plt.show()
    
    ##Température des gros composants du CPP - Fond de cuve
    ##
    #
    fig,ax4 = plt.subplots()
    plt.plot(Date,EHPdata.EHP001MT, label='EHP001MT', linewidth=0.5)
    plt.plot(Date,EHPdata.EHP002MT, label='EHP002MT',linewidth=0.5)
    plt.plot(Date,EHPdata.EHP003MT, label='EHP003MT', linewidth=0.5)
    plt.title("Température des gros composants du CPP - Fond de cuve")
    plt.xlabel("Date")
    plt.ylabel("Température (°C)")
    plt.xticks(rotation=30)#rotation des dates sur l'axe x pour meilleure lisibilité
    ax4.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y\n%H:%M")) #Passage en format européen
    plt.legend(loc='lower center')
    plt.grid(color = 'grey', linestyle = '--', linewidth = 0.25)
    plt.tight_layout() #sert à ce que la figure ne dépasse pas des bords du PDF
    plt.savefig("{}/Température des gros composants.pdf".format(output_dir))
    #plt.show()
    
    ##Température des gros composants - couvercle&pressu
    ##
    #
    fig,ax5 = plt.subplots()
    plt.plot(Date,EHPdata.EHP004MT, label='EHP004MT - Bride de cuve', linewidth=0.5)
    plt.plot(Date,EHPdata.EHP005MT, label='EHP005MT - Bride de couvercle',linewidth=0.5)
    plt.plot(Date,EHPdata.EHP006MT, label='EHP006MT - JEP Pressu', linewidth=0.5)
    plt.title("Température des gros composants du CPP")
    plt.xlabel("Date")
    plt.ylabel("Température (°C)")
    plt.xticks(rotation=30) #rotation des dates sur l'axe x pour meilleure lisibilité
    ax5.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y\n%H:%M")) #Passage en format européen
    plt.legend(loc='lower center')
    plt.grid(color = 'grey', linestyle = '--', linewidth = 0.25)
    plt.tight_layout() #sert à ce que la figure ne dépasse pas des bords du PDF
    plt.savefig("{}/Température des gros composants - couvercle&pressu.pdf".format(output_dir))
    #plt.show()
    
    ##Température des gros composants - GVs
    ##
    #
    fig,ax6 = plt.subplots()
    plt.plot(Date,EHPdata.EHP007MT, label='EHP007MT - GV1', linewidth=0.5)
    plt.plot(Date,EHPdata.EHP008MT, label='EHP008MT - GV2',linewidth=0.5)
    plt.plot(Date,EHPdata.EHP009MT, label='EHP009MT - GV3', linewidth=0.5)
    plt.plot(Date,EHPdata.EHP010MT, label='EHP010MT - GV4', linewidth=0.5)
    plt.title("Température des gros composants du CPP")
    plt.xlabel("Date")
    plt.ylabel("Température (°C)")
    plt.xticks(rotation=30) #rotation des dates sur l'axe x pour meilleure lisibilité
    ax6.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y\n%H:%M")) #Passage en format européen
    plt.legend(loc='lower center')
    plt.grid(color = 'grey', linestyle = '--', linewidth = 0.25)
    plt.tight_layout() #sert à ce que la figure ne dépasse pas des bords du PDF
    plt.savefig("{}/Température des gros composants - GVs.pdf".format(output_dir))
    #plt.show()
    
    
    ##Gradients de pression
    ##
    #
    fig,ax7 = plt.subplots()
    plt.plot(Date,EHPdata.EHP001MPGrad, label='EHP001MPGrad', linewidth=0.5)
    plt.plot(Date,EHPdata.EHP002MPGrad, label='EHP002MPGrad',linewidth=0.5)
    plt.hlines(4,np.min(Date), np.max(Date), colors='purple', label='Valeur Max Gradient (+4 bar/min)', linewidth=0.5)
    plt.hlines(-4,np.min(Date), np.max(Date), colors='purple', label='Valeur Min Gradient (-4 bar/min)', linewidth=0.5)
    plt.title("Gradients de Pression de l'EHP")
    plt.xlabel("Date")
    plt.ylabel("Gradient de pression en bar/min")
    ax7.set_ylim(-15,15) #limitation de y à -15/+15
    plt.xticks(rotation=30) #rotation des dates sur l'axe x pour meilleure lisibilité
    ax7.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y\n%H:%M")) #Passage en format européen
    plt.legend(loc='lower left', fontsize=6)
    plt.grid(color = 'grey', linestyle = '--', linewidth = 0.25)
    plt.tight_layout() #sert à ce que la figure ne dépasse pas des bords du PDF
    plt.savefig("{}/Gradients de pression.pdf".format(output_dir))
    #plt.show() 
    
    ##Suivi Tmoy
    ##
    #
    fig,ax8 = plt.subplots()
    plt.plot(Date,EHPdata.TMOY, label='Tmoy', linewidth=0.5)
    plt.title("Suivi de la Tmoy de l'EHP")
    plt.xlabel("Date")
    plt.ylabel("Température (°C)")
    plt.xticks(rotation=30) #rotation des dates sur l'axe x pour meilleure lisibilité
    ax8.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y\n%H:%M")) #Passage en format européen
    plt.legend(loc='lower center')
    plt.grid(color = 'grey', linestyle = '--', linewidth = 0.25)
    plt.tight_layout() #sert à ce que la figure ne dépasse pas des bords du PDF
    plt.savefig("{}/Suivi Tmoy.pdf".format(output_dir))
    #plt.show() 
    
    ##Suivi gradient Tmoy
    ##
    #
    fig,ax9 = plt.subplots()
    plt.plot(Date,EHPdata.TGRAD, label='Tgrad', linewidth=0.5)
    
    #limites de gradient
    #filtrage pour avoir T>50
    TMOYfiltsup=EHPdata["TMOY"]>50
    positions = np.flatnonzero(TMOYfiltsup)
    maskTMOYfiltsup=EHPdata.iloc[positions]
    DateTmoysup50=pd.to_datetime(maskTMOYfiltsup.Horodatage, infer_datetime_format=True, dayfirst=True)
    
    
    
    #filtrage pour avoir T<50
    TMOYfiltinf=EHPdata["TMOY"]<50
    positions = np.flatnonzero(TMOYfiltinf)
    maskTMOYfiltinf=EHPdata.iloc[positions]
    DateTmoyinf50=pd.to_datetime(maskTMOYfiltinf.Horodatage, infer_datetime_format=True, dayfirst=True)
    
    
    #filtrage pour avoir T=50
    TMOYfiltegal=EHPdata["TMOY"]==50
    positions = np.flatnonzero(TMOYfiltegal)
    maskTMOYfiltegal=EHPdata.iloc[positions]
    DateTmoyegal50=pd.to_datetime(maskTMOYfiltegal.Horodatage, infer_datetime_format=True , dayfirst=True)
    
    if not DateTmoysup50.empty:
        plt.hlines(28,np.min(DateTmoysup50), np.max(DateTmoysup50), colors='purple', label='+/-28°C/h', linewidth=1)
        plt.hlines(-28,np.min(DateTmoysup50), np.max(DateTmoysup50), colors='purple', linewidth=1)
    plt.vlines(DateTmoyegal50,-28,-14, colors='purple', linewidth=0.5)
    plt.vlines(DateTmoyegal50,28,14, colors='purple', linewidth=0.5)
    if not DateTmoyinf50.empty:
        if not DateTmoyegal50.empty:
            plt.hlines(14,np.min(DateTmoyinf50), np.min(DateTmoyegal50), colors='orange', label='+/-14°C/h', linewidth=0.5)
            plt.hlines(-14,np.min(DateTmoyinf50), np.min(DateTmoyegal50), colors='orange', linewidth=0.5)
            plt.hlines(14, np.max(DateTmoyegal50), np.max(DateTmoyinf50), colors='orange', linewidth=0.5)
            plt.hlines(-14, np.max(DateTmoyegal50),np.max(DateTmoyinf50), colors='orange', linewidth=0.5)
    
    #Fin limites de gradient
    
    plt.title("Suivi du gradient de Tmoy de l'EHP")
    plt.xlabel("Date")
    plt.ylabel("Température (°C)")
    plt.xticks(rotation=30) #rotation des dates sur l'axe x pour meilleure lisibilité
    ax9.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y\n%H:%M")) #Passage en format européen
    plt.legend(loc='upper left')
    plt.grid(color = 'grey', linestyle = '--', linewidth = 0.25)
    plt.tight_layout() #sert à ce que la figure ne dépasse pas des bords du PDF
    plt.savefig("{}/Suivi Tgrad.pdf".format(output_dir))
    
    #plt.show() 
    
    ##Suivi des températures fluide pendant l'EHP
    ##
    #
 
    fig,ax10 = plt.subplots()
    plt.plot(Date,EHPdata.RCP009MT, label='RCP009MT', linewidth=0.5)
    plt.plot(Date,EHPdata.RCP010MT, label='RCP014MT', linewidth=0.5) 
    plt.plot(Date,EHPdata.RCP028MT, label='RCP0100MT', linewidth=0.5) 
    
    plt.title("Suivi des températures fluide pendant l'EHP")
    plt.xlabel("Date")
    plt.ylabel("Température (°C/h)")
    plt.xticks(rotation=30) #rotation des dates sur l'axe x pour meilleure lisibilité
    ax10.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y\n%H:%M")) #Passage en format européen
    plt.legend(loc='lower center')
    plt.grid(color = 'grey', linestyle = '--', linewidth = 0.25)
    plt.tight_layout() #sert à ce que la figure ne dépasse pas des bords du PDF
    plt.savefig("{}/Suivi des températures fluide pendant l'EHP - 1.pdf".format(output_dir))
    #plt.show() 
    
    fig,ax101 = plt.subplots()
    plt.plot(Date,EHPdata.RCP029MT, label='RCP104MT', linewidth=0.5) 
    plt.plot(Date,EHPdata.RCP043MT, label='RCP200MT', linewidth=0.5) 
    plt.plot(Date,EHPdata.RCP044MT, label='RCP204MT', linewidth=0.5) 
   
    plt.title("Suivi des températures fluide pendant l'EHP")
    plt.xlabel("Date")
    plt.ylabel("Température (°C/h)")
    plt.xticks(rotation=30) #rotation des dates sur l'axe x pour meilleure lisibilité
    ax101.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y\n%H:%M")) #Passage en format européen
    plt.legend(loc='lower center')
    plt.grid(color = 'grey', linestyle = '--', linewidth = 0.25)
    plt.tight_layout() #sert à ce que la figure ne dépasse pas des bords du PDF
    plt.savefig("{}/Suivi des températures fluide pendant l'EHP - 2.pdf".format(output_dir))
    #plt.show()
    
    fig,ax102 = plt.subplots()

    plt.plot(Date,EHPdata.RCP055MT, label='RCP300MT', linewidth=0.5) 
    plt.plot(Date,EHPdata.RCP056MT, label='RCP304MT', linewidth=0.5) 
    plt.plot(Date,EHPdata.RCP055MT, label='RCP400MT', linewidth=0.5) 
    plt.plot(Date,EHPdata.RCP056MT, label='RCP404MT', linewidth=0.5)
    plt.title("Suivi des températures fluide pendant l'EHP")
    plt.xlabel("Date")
    plt.ylabel("Température (°C/h)")
    plt.xticks(rotation=30) #rotation des dates sur l'axe x pour meilleure lisibilité
    ax102.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y\n%H:%M")) #Passage en format européen
    plt.legend(loc='lower center')
    plt.grid(color = 'grey', linestyle = '--', linewidth = 0.25)
    plt.tight_layout() #sert à ce que la figure ne dépasse pas des bords du PDF
    plt.savefig("{}/Suivi des températures fluide pendant l'EHP - 3.pdf".format(output_dir))
    #plt.show()
    
    ##Gradient des températures métal pendant l'EHP - 1
    ##
    #
    fig,ax11 = plt.subplots()
    plt.plot(Date,EHPdata.EHP001MTGrad, label='EHP001MTGrad', linewidth=0.5)
    plt.plot(Date,EHPdata.EHP002MTGrad, label='EHP002MTGrad', linewidth=0.5)
    plt.plot(Date,EHPdata.EHP003MTGrad, label='EHP003MTGrad', linewidth=0.5)
    
    
    plt.title("Gradient des températures métal pendant l'EHP - Fond de cuve")
    plt.xlabel("Date")
    plt.ylabel("Gradient de température (°C/h)")
    plt.xticks(rotation=30) #rotation des dates sur l'axe x pour meilleure lisibilité
    ax11.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y\n%H:%M")) #Passage en format européen
    ax11.set_ylim(-30,30) #limitation de y à -30/+30
    plt.legend(loc='lower right', fontsize = 6, ncol=2)
    plt.grid(color = 'grey', linestyle = '--', linewidth = 0.25)
    plt.tight_layout() #sert à ce que la figure ne dépasse pas des bords du PDF
    plt.savefig("{}/Gradient des températures métal pendant l'EHP - Fond de cuve.pdf".format(output_dir))
    #plt.show() 
    
    ##Gradient des températures métal pendant l'EHP - Couvercle et pressu
    ##
    #
    fig,ax14 = plt.subplots()
    
    plt.plot(Date,EHPdata.EHP004MTGrad, label='EHP004MTGrad - Bride de cuve', linewidth=0.5)
    plt.plot(Date,EHPdata.EHP005MTGrad, label='EHP005MTGrad - Bride de couvercle', linewidth=0.5)
    plt.plot(Date,EHPdata.EHP006MTGrad, label='EHP006MTGrad - JEP Pressu', linewidth=0.5)
    
    plt.title("Gradient des températures métal pendant l'EHP - Couvercle et Pressu")
    plt.xlabel("Date")
    plt.ylabel("Gradient de température (°C/h)")
    plt.xticks(rotation=30) #rotation des dates sur l'axe x pour meilleure lisibilité
    ax14.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y\n%H:%M")) #Passage en format européen
    ax14.set_ylim(-30,30) #limitation de y à -30/+30
    plt.legend(loc='lower right', fontsize = 6, ncol=2)
    plt.grid(color = 'grey', linestyle = '--', linewidth = 0.25)
    plt.tight_layout() #sert à ce que la figure ne dépasse pas des bords du PDF
    plt.savefig("{}/Gradient des températures métal pendant l'EHP - Couvercle et pressu.pdf".format(output_dir))
    #plt.show() 
    
    ##Gradient des températures métal pendant l'EHP - GV
    ##
    #
    fig,ax15 = plt.subplots()
    
    plt.plot(Date,EHPdata.EHP007MTGrad, label='EHP007MTGrad - GV1', linewidth=0.5)
    plt.plot(Date,EHPdata.EHP008MTGrad, label='EHP008MTGrad - GV2', linewidth=0.5)
    plt.plot(Date,EHPdata.EHP009MTGrad, label='EHP009MTGrad - GV3', linewidth=0.5)
    plt.plot(Date,EHPdata.EHP010MTGrad, label='EHP010MTGrad - GV4', linewidth=0.5)
    plt.title("Gradient des températures métal pendant l'EHP - GV")
    plt.xlabel("Date")
    plt.ylabel("Gradient de température (°C/h)")
    plt.xticks(rotation=30) #rotation des dates sur l'axe x pour meilleure lisibilité
    ax15.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y\n%H:%M")) #Passage en format européen
    ax15.set_ylim(-30,30) #limitation de y à -30/+30
    plt.legend(loc='lower right', fontsize = 6, ncol=2)
    plt.grid(color = 'grey', linestyle = '--', linewidth = 0.25)
    plt.tight_layout() #sert à ce que la figure ne dépasse pas des bords du PDF
    plt.savefig("{}/Gradient des températures métal pendant l'EHP - GV.pdf".format(output_dir))
    #plt.show() 
    
    ###Evolution de la pression pendant l'épreuve
    ##
    ##
    fig,ax12 = plt.subplots()
    #filtrage pour avoir que le palier
    EHP001MPfilt=EHPdata["EHP001MP"]>172
    positions = np.flatnonzero(EHP001MPfilt)
    maskEHP001MP=EHPdata.iloc[positions]
    DateEpreuveMule=pd.to_datetime(maskEHP001MP.Horodatage, infer_datetime_format=True, dayfirst=True)
    EHP002MPfilt=EHPdata["EHP002MP"]>172
    positions = np.flatnonzero(EHP002MPfilt)
    maskEHP002MP=EHPdata.iloc[positions]
    DateEpreuveMule2=pd.to_datetime(maskEHP002MP.Horodatage, infer_datetime_format=True, dayfirst=True)
    
    
    plt.plot(DateEpreuveMule,maskEHP001MP.EHP001MP, label='EHP001MP', linewidth=0.5)
    plt.plot(DateEpreuveMule2,maskEHP002MP.EHP002MP, label='EHP002MP', linewidth=0.5)
    if not DateEpreuveMule.empty:   
        plt.hlines(207.8,np.min(DateEpreuveMule), np.max(DateEpreuveMule), colors='purple', label='207.8 bar', linewidth=0.5)
        plt.hlines(206.9,np.min(DateEpreuveMule), np.max(DateEpreuveMule), colors='purple', label='206,9 bar', linewidth=0.5)
    
    plt.title("Evolution de la pression pendant le palier d'épreuve")
    plt.xlabel("Date")
    plt.ylabel("Pression (bar)")
    plt.xticks(rotation=30)#rotation des dates sur l'axe x pour meilleure lisibilité
    ax12.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y\n%H:%M")) #Passage en format européen
    plt.legend(loc='upper left')
    plt.grid(color = 'grey', linestyle = '--', linewidth = 0.25)
    plt.tight_layout() #sert à ce que la figure ne dépasse pas des bords du PDF
    plt.savefig("{}/Evolution de la pression pendant l'épreuve.pdf".format(output_dir))
    #plt.show()
    
    ###Evolution de la pression pendant le palier 206bar
    ##
    ##
    fig,ax13 = plt.subplots()
    #filtrage pour avoir que le palier
    EHP001MPfilt=EHPdata["EHP001MP"]>205
    positions = np.flatnonzero(EHP001MPfilt)
    maskEHP001MP=EHPdata.iloc[positions]
    DateEpreuveMule=pd.to_datetime(maskEHP001MP.Horodatage, infer_datetime_format=True, dayfirst=True)
    EHP002MPfilt=EHPdata["EHP002MP"]>205
    positions = np.flatnonzero(EHP002MPfilt)
    maskEHP002MP=EHPdata.iloc[positions]
    DateEpreuveMule2=pd.to_datetime(maskEHP002MP.Horodatage, infer_datetime_format=True, dayfirst=True)
    
    
    plt.plot(DateEpreuveMule,maskEHP001MP.EHP001MP, label='EHP001MP', linewidth=0.5)
    plt.plot(DateEpreuveMule2,maskEHP002MP.EHP002MP, label='EHP002MP', linewidth=0.5)
    if not DateEpreuveMule.empty:    
        plt.hlines(206,np.min(DateEpreuveMule), np.max(DateEpreuveMule), colors='purple', label='206 bar', linewidth=0.5)
        plt.hlines(206.9,np.min(DateEpreuveMule), np.max(DateEpreuveMule), colors='purple', label='206,9 bar', linewidth=0.5)
    plt.title("Evolution de la pression pendant le palier d'épreuve")
    plt.xlabel("Date")
    plt.ylabel("Pression (bar)")
    plt.xticks(rotation=30)#rotation des dates sur l'axe x pour meilleure lisibilité
    ax13.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y\n%H:%M")) #Passage en format européen
    plt.legend(loc='lower center')
    plt.grid(color = 'grey', linestyle = '--', linewidth = 0.25)
    plt.tight_layout() #sert à ce que la figure ne dépasse pas des bords du PDF
    plt.savefig("{}/Evolution de la pression pendant le palier 206bar.pdf".format(output_dir))
    if value2.get()==1:
        plt.show()
    
    ##
    gc.collect() #vide la mémoire    
    
    
def courbes900():
    def mkdir_p(mypath):
        '''Creates a directory. equivalent to using mkdir -p on the command line'''
        from errno import EEXIST
        from os import makedirs,path

        try:
            makedirs(mypath)
        except OSError as exc: # Python >2.5
                if exc.errno == EEXIST and path.isdir(mypath):
                    pass
                else: raise
    
    if filepath=="":
        fenetre4=Tk()
        w=Label(fenetre4, text="Veuillez selectionner un fichier de données")
        w.pack()
        Bouton=Button(fenetre4, text="Fermer", command=fenetre4.destroy)
        Bouton.pack() 
        return() 
    if savepath=="":
        fenetre3=Tk()
        w=Label(fenetre3, text="Veuillez selectionner un dossier de sauvegarde")
        w.pack()
        Bouton=Button(fenetre3, text="Fermer", command=fenetre3.destroy)
        Bouton.pack() 
        return()    

    output_dir = savepath+"/Courbes épreuve"
    mkdir_p(output_dir)

    #
    
    ##### Début du traçage de courbes #####
    
    gc.collect() #vide la mémoire
    
    EHPdata = pd.read_csv(filepath ,sep=';', header=15)
    
    
    #print(EHPdata)
    
    Date=pd.to_datetime(EHPdata.Horodatage, infer_datetime_format=True, dayfirst=True)
    
    
    
    #print(Date)
    
    ##Evolution de la pression RCP pendant l'épreuve
    ##
    #
    fig,ax1 = plt.subplots()
    plt.plot(Date,EHPdata.EHP001MP, label='EHP001MP', linewidth=0.5)
    plt.plot(Date,EHPdata.EHP002MP, label='EHP002MP', linewidth=0.5)
    plt.title("Evolution de la pression RCP pendant l'épreuve")
    plt.xlabel("Date")
    plt.ylabel("Pression (bar)")
    plt.xticks(rotation=30)
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y\n%H:%M")) #Passage en format européen
    plt.minorticks_on
    plt.legend(loc='upper left')
    plt.grid(color = 'grey', linestyle = '--', linewidth = 0.25)
    plt.tight_layout() #sert à ce que la figure ne dépasse pas des bords du PDF
    plt.savefig("{}/Evolution de la pression RCP pendant l'épreuve.pdf".format(output_dir))
    #plt.show()
    
    ###Evolution de la pression de refoulement de la pompe RCV191PO
    ##
    ##
    fig,ax2 = plt.subplots()
    plt.plot(Date,EHPdata.EHP003MP, label='EHP003MP', linewidth=0.5)
    plt.hlines(241,np.min(Date), np.max(Date),linewidth=0.5, colors='purple', label='Pression limite EHP003MP 241bars')
    plt.hlines(235.5,np.min(Date), np.max(Date),linewidth=0.5, colors='red', label='Seuil arrêt de la pompe \nRIS011PO 235,5bars')
    plt.hlines(230,np.min(Date), np.max(Date),linewidth=0.5, colors='orange', label='Seuil alarme haute pression de refoulement \nRIS011PO 230bars')
    plt.title("Evolution de la pression de refoulement de la pompe RIS011PO")
    plt.xlabel("Date")
    plt.ylabel("Pression (bar)")
    plt.xticks(rotation=30)
    ax2.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y\n%H:%M")) #Passage en format européen
    plt.legend(loc='center left', fontsize=6)
    plt.grid(color = 'grey', linestyle = '--', linewidth = 0.25)
    plt.tight_layout() #sert à ce que la figure ne dépasse pas des bords du PDF
    plt.savefig("{}/Pression de refoulement RIS011PO.pdf".format(output_dir))
    #plt.show()
    
    ###Evolution de la pression de refoulement de la pompe RCV191PO
    ##
    ##
    fig,ax3 = plt.subplots()
    #filtrage pour avoir que l'épreuve
    EHP003MPfilt=EHPdata["EHP003MP"]>4
    positions = np.flatnonzero(EHP003MPfilt)
    maskEHP003MP=EHPdata.iloc[positions]
    DateEpreuveMule=pd.to_datetime(maskEHP003MP.Horodatage, infer_datetime_format=True, dayfirst=True)
    #debug
    #print(maskEHP003MP.EHP003MP)
    
    
    plt.plot(DateEpreuveMule,maskEHP003MP.EHP003MP, label='EHP003MP',linewidth=0.5)
    if not DateEpreuveMule.empty:
        plt.hlines(241,np.min(DateEpreuveMule), np.max(DateEpreuveMule),linewidth=0.5, colors='purple', label='Pression limite EHP003MP 241bars')
        plt.hlines(235.5,np.min(DateEpreuveMule), np.max(DateEpreuveMule),linewidth=0.5, colors='red', label='Seuil arrêt de la pompe \nRIS011PO 235,5bars')
        plt.hlines(230,np.min(DateEpreuveMule), np.max(DateEpreuveMule),linewidth=0.5, colors='orange', label='Seuil alarme haute pression de refoulement \nRIS011PO 230bars')
    plt.title("Evolution de la pression de refoulement de la pompe RIS011PO")
    plt.xlabel("Date")
    plt.ylabel("Pression (bar)")
    plt.xticks(rotation=30)#rotation des dates sur l'axe x pour meilleure lisibilité
    ax3.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y\n%H:%M")) #Passage en format européen
    plt.legend(loc='lower center', fontsize=6)
    plt.grid(color = 'grey', linestyle = '--', linewidth = 0.25)
    plt.tight_layout() #sert à ce que la figure ne dépasse pas des bords du PDF
    plt.savefig("{}/Evolution de la pression de refoulement RIS011PO - détail.pdf".format(output_dir))
    #plt.show()
    
    ##Température des gros composants du CPP - Fond de cuve
    ##
    #
    fig,ax4 = plt.subplots()
    plt.plot(Date,EHPdata.EHP001MT, label='EHP001MT', linewidth=0.5)
    plt.plot(Date,EHPdata.EHP002MT, label='EHP002MT',linewidth=0.5)
    plt.plot(Date,EHPdata.EHP003MT, label='EHP003MT', linewidth=0.5)
    plt.title("Température des gros composants du CPP - Fond de cuve")
    plt.xlabel("Date")
    plt.ylabel("Température (°C)")
    plt.xticks(rotation=30)#rotation des dates sur l'axe x pour meilleure lisibilité
    ax4.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y\n%H:%M")) #Passage en format européen
    plt.legend(loc='lower center')
    plt.grid(color = 'grey', linestyle = '--', linewidth = 0.25)
    plt.tight_layout() #sert à ce que la figure ne dépasse pas des bords du PDF
    plt.savefig("{}/Température des gros composants.pdf".format(output_dir))
    #plt.show()
    
    ##Température des gros composants - couvercle&pressu
    ##
    #
    fig,ax5 = plt.subplots()
    plt.plot(Date,EHPdata.EHP004MT, label='EHP004MT - Bride de cuve', linewidth=0.5)
    plt.plot(Date,EHPdata.EHP005MT, label='EHP005MT - Bride de couvercle',linewidth=0.5)
    plt.plot(Date,EHPdata.EHP006MT, label='EHP006MT - JEP Pressu', linewidth=0.5)
    plt.title("Température des gros composants du CPP")
    plt.xlabel("Date")
    plt.ylabel("Température (°C)")
    plt.xticks(rotation=30) #rotation des dates sur l'axe x pour meilleure lisibilité
    ax5.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y\n%H:%M")) #Passage en format européen
    plt.legend(loc='lower center')
    plt.grid(color = 'grey', linestyle = '--', linewidth = 0.25)
    plt.tight_layout() #sert à ce que la figure ne dépasse pas des bords du PDF
    plt.savefig("{}/Température des gros composants - couvercle&pressu.pdf".format(output_dir))
    #plt.show()
    
    ##Température des gros composants - GVs
    ##
    #
    fig,ax6 = plt.subplots()
    plt.plot(Date,EHPdata.EHP007MT, label='EHP007MT - GV1', linewidth=0.5)
    plt.plot(Date,EHPdata.EHP008MT, label='EHP008MT - GV2',linewidth=0.5)
    plt.plot(Date,EHPdata.EHP009MT, label='EHP009MT - GV3', linewidth=0.5)
    plt.title("Température des gros composants du CPP")
    plt.xlabel("Date")
    plt.ylabel("Température (°C)")
    plt.xticks(rotation=30) #rotation des dates sur l'axe x pour meilleure lisibilité
    ax6.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y\n%H:%M")) #Passage en format européen
    plt.legend(loc='lower center')
    plt.grid(color = 'grey', linestyle = '--', linewidth = 0.25)
    plt.tight_layout() #sert à ce que la figure ne dépasse pas des bords du PDF
    plt.savefig("{}/Température des gros composants - GVs.pdf".format(output_dir))
    #plt.show()
    
    
    ##Gradients de pression
    ##
    #
    fig,ax7 = plt.subplots()
    plt.plot(Date,EHPdata.EHP001MPGrad, label='EHP001MPGrad', linewidth=0.5)
    plt.plot(Date,EHPdata.EHP002MPGrad, label='EHP002MPGrad',linewidth=0.5)
    plt.hlines(4,np.min(Date), np.max(Date), colors='purple', label='Valeur Max Gradient (+4 bar/min)', linewidth=0.5)
    plt.hlines(-4,np.min(Date), np.max(Date), colors='purple', label='Valeur Min Gradient (-4 bar/min)', linewidth=0.5)
    plt.title("Gradients de Pression de l'EHP")
    plt.xlabel("Date")
    plt.ylabel("Gradient de pression en bar/min")
    ax7.set_ylim(-15,15) #limitation de y à -15/+15
    plt.xticks(rotation=30) #rotation des dates sur l'axe x pour meilleure lisibilité
    ax7.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y\n%H:%M")) #Passage en format européen
    plt.legend(loc='lower left', fontsize=6)
    plt.grid(color = 'grey', linestyle = '--', linewidth = 0.25)
    plt.tight_layout() #sert à ce que la figure ne dépasse pas des bords du PDF
    plt.savefig("{}/Gradients de pression.pdf".format(output_dir))
    #plt.show() 
    
    ##Suivi Tmoy
    ##
    #
    fig,ax8 = plt.subplots()
    plt.plot(Date,EHPdata.TMOY, label='Tmoy', linewidth=0.5)
    plt.title("Suivi de la Tmoy de l'EHP")
    plt.xlabel("Date")
    plt.ylabel("Température (°C)")
    plt.xticks(rotation=30) #rotation des dates sur l'axe x pour meilleure lisibilité
    ax8.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y\n%H:%M")) #Passage en format européen
    plt.legend(loc='lower center')
    plt.grid(color = 'grey', linestyle = '--', linewidth = 0.25)
    plt.tight_layout() #sert à ce que la figure ne dépasse pas des bords du PDF
    plt.savefig("{}/Suivi Tmoy.pdf".format(output_dir))
    #plt.show() 
    
    ##Suivi gradient Tmoy
    ##
    #
    fig,ax9 = plt.subplots()
    plt.plot(Date,EHPdata.TGRAD, label='Tgrad', linewidth=0.5)
    
    #limites de gradient
    #filtrage pour avoir T>50
    TMOYfiltsup=EHPdata["TMOY"]>50
    positions = np.flatnonzero(TMOYfiltsup)
    maskTMOYfiltsup=EHPdata.iloc[positions]
    DateTmoysup50=pd.to_datetime(maskTMOYfiltsup.Horodatage, infer_datetime_format=True, dayfirst=True)
    
    
    
    #filtrage pour avoir T<50
    TMOYfiltinf=EHPdata["TMOY"]<50
    positions = np.flatnonzero(TMOYfiltinf)
    maskTMOYfiltinf=EHPdata.iloc[positions]
    DateTmoyinf50=pd.to_datetime(maskTMOYfiltinf.Horodatage, infer_datetime_format=True, dayfirst=True)
    
    
    #filtrage pour avoir T=50
    TMOYfiltegal=EHPdata["TMOY"]==50
    positions = np.flatnonzero(TMOYfiltegal)
    maskTMOYfiltegal=EHPdata.iloc[positions]
    DateTmoyegal50=pd.to_datetime(maskTMOYfiltegal.Horodatage, infer_datetime_format=True, dayfirst=True)
    if not DateTmoysup50.empty:
        plt.hlines(28,np.min(DateTmoysup50), np.max(DateTmoysup50), colors='purple', label='+/-28°C/h', linewidth=1)
        plt.hlines(-28,np.min(DateTmoysup50), np.max(DateTmoysup50), colors='purple', linewidth=1)
    plt.vlines(DateTmoyegal50,-28,-14, colors='purple', linewidth=0.5)
    plt.vlines(DateTmoyegal50,28,14, colors='purple', linewidth=0.5)

    if not DateTmoyinf50.empty:
        if not DateTmoyegal50.empty:
            plt.hlines(14,np.min(DateTmoyinf50), np.min(DateTmoyegal50), colors='orange', label='+/-14°C/h', linewidth=0.5)
            plt.hlines(-14,np.min(DateTmoyinf50), np.min(DateTmoyegal50), colors='orange', linewidth=0.5)
            plt.hlines(14, np.max(DateTmoyegal50), np.max(DateTmoyinf50), colors='orange', linewidth=0.5)
            plt.hlines(-14, np.max(DateTmoyegal50),np.max(DateTmoyinf50), colors='orange', linewidth=0.5)
    
    #Fin limites de gradient
    
    plt.title("Suivi du gradient de Tmoy de l'EHP")
    plt.xlabel("Date")
    plt.ylabel("Température (°C)")
    plt.xticks(rotation=30) #rotation des dates sur l'axe x pour meilleure lisibilité
    ax9.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y\n%H:%M")) #Passage en format européen
    plt.legend(loc='upper left')
    plt.grid(color = 'grey', linestyle = '--', linewidth = 0.25)
    plt.tight_layout() #sert à ce que la figure ne dépasse pas des bords du PDF
    plt.savefig("{}/Suivi Tgrad.pdf".format(output_dir))
    
    #plt.show() 
    
    ##Suivi des températures fluide pendant l'EHP
    ##
    #
    fig,ax10 = plt.subplots()
    plt.plot(Date,EHPdata.RCP009MT, label='RCP009MT', linewidth=0.5)
    plt.plot(Date,EHPdata.RCP010MT, label='RCP010MT', linewidth=0.5) 
    plt.plot(Date,EHPdata.RCP028MT, label='RCP028MT', linewidth=0.5) 
    
    plt.title("Suivi des températures fluide pendant l'EHP")
    plt.xlabel("Date")
    plt.ylabel("Température (°C/h)")
    plt.xticks(rotation=30) #rotation des dates sur l'axe x pour meilleure lisibilité
    ax10.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y\n%H:%M")) #Passage en format européen
    plt.legend(loc='lower center')
    plt.grid(color = 'grey', linestyle = '--', linewidth = 0.25)
    plt.tight_layout() #sert à ce que la figure ne dépasse pas des bords du PDF
    plt.savefig("{}/Suivi des températures fluide pendant l'EHP - 1.pdf".format(output_dir))
    #plt.show() 
    
    fig,ax101 = plt.subplots()
    plt.plot(Date,EHPdata.RCP029MT, label='RCP029MT', linewidth=0.5) 
    plt.plot(Date,EHPdata.RCP043MT, label='RCP043MT', linewidth=0.5) 
    plt.plot(Date,EHPdata.RCP044MT, label='RCP044MT', linewidth=0.5) 
   
    plt.title("Suivi des températures fluide pendant l'EHP")
    plt.xlabel("Date")
    plt.ylabel("Température (°C/h)")
    plt.xticks(rotation=30) #rotation des dates sur l'axe x pour meilleure lisibilité
    ax101.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y\n%H:%M")) #Passage en format européen
    plt.legend(loc='lower center')
    plt.grid(color = 'grey', linestyle = '--', linewidth = 0.25)
    plt.tight_layout() #sert à ce que la figure ne dépasse pas des bords du PDF
    plt.savefig("{}/Suivi des températures fluide pendant l'EHP - 2.pdf".format(output_dir))
    #plt.show()
    
    fig,ax102 = plt.subplots()

    plt.plot(Date,EHPdata.RCP055MT, label='RCP055MT', linewidth=0.5) 
    plt.plot(Date,EHPdata.RCP056MT, label='RCP056MT', linewidth=0.5) 
    plt.title("Suivi des températures fluide pendant l'EHP")
    plt.xlabel("Date")
    plt.ylabel("Température (°C/h)")
    plt.xticks(rotation=30) #rotation des dates sur l'axe x pour meilleure lisibilité
    ax102.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y\n%H:%M")) #Passage en format européen
    plt.legend(loc='lower center')
    plt.grid(color = 'grey', linestyle = '--', linewidth = 0.25)
    plt.tight_layout() #sert à ce que la figure ne dépasse pas des bords du PDF
    plt.savefig("{}/Suivi des températures fluide pendant l'EHP - 3.pdf".format(output_dir))
    #plt.show()
    
    ##Gradient des températures métal pendant l'EHP - 1
    ##
    #
    fig,ax11 = plt.subplots()
    plt.plot(Date,EHPdata.EHP001MTGrad, label='EHP001MTGrad', linewidth=0.5)
    plt.plot(Date,EHPdata.EHP002MTGrad, label='EHP002MTGrad', linewidth=0.5)
    plt.plot(Date,EHPdata.EHP003MTGrad, label='EHP003MTGrad', linewidth=0.5)
    
    
    plt.title("Gradient des températures métal pendant l'EHP - Fond de cuve")
    plt.xlabel("Date")
    plt.ylabel("Gradient de température (°C/h)")
    plt.xticks(rotation=30) #rotation des dates sur l'axe x pour meilleure lisibilité
    ax11.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y\n%H:%M")) #Passage en format européen
    ax11.set_ylim(-30,30) #limitation de y à -30/+30
    plt.legend(loc='lower right', fontsize = 6, ncol=2)
    plt.grid(color = 'grey', linestyle = '--', linewidth = 0.25)
    plt.tight_layout() #sert à ce que la figure ne dépasse pas des bords du PDF
    plt.savefig("{}/Gradient des températures métal pendant l'EHP - Fond de cuve.pdf".format(output_dir))
    #plt.show() 
    
    ##Gradient des températures métal pendant l'EHP - Couvercle et pressu
    ##
    #
    fig,ax14 = plt.subplots()
    
    plt.plot(Date,EHPdata.EHP004MTGrad, label='EHP004MTGrad - Bride de cuve', linewidth=0.5)
    plt.plot(Date,EHPdata.EHP005MTGrad, label='EHP005MTGrad - Bride de couvercle', linewidth=0.5)
    plt.plot(Date,EHPdata.EHP006MTGrad, label='EHP006MTGrad - JEP Pressu', linewidth=0.5)
    
    plt.title("Gradient des températures métal pendant l'EHP - Couvercle et Pressu")
    plt.xlabel("Date")
    plt.ylabel("Gradient de température (°C/h)")
    plt.xticks(rotation=30) #rotation des dates sur l'axe x pour meilleure lisibilité
    ax14.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y\n%H:%M")) #Passage en format européen
    ax14.set_ylim(-30,30) #limitation de y à -30/+30
    plt.legend(loc='lower right', fontsize = 6, ncol=2)
    plt.grid(color = 'grey', linestyle = '--', linewidth = 0.25)
    plt.tight_layout() #sert à ce que la figure ne dépasse pas des bords du PDF
    plt.savefig("{}/Gradient des températures métal pendant l'EHP - Couvercle et pressu.pdf".format(output_dir))
    #plt.show() 
    
    ##Gradient des températures métal pendant l'EHP - GV
    ##
    #
    fig,ax15 = plt.subplots()
    
    plt.plot(Date,EHPdata.EHP007MTGrad, label='EHP007MTGrad - GV1', linewidth=0.5)
    plt.plot(Date,EHPdata.EHP008MTGrad, label='EHP008MTGrad - GV2', linewidth=0.5)
    plt.plot(Date,EHPdata.EHP009MTGrad, label='EHP009MTGrad - GV3', linewidth=0.5)
    plt.title("Gradient des températures métal pendant l'EHP - GV")
    plt.xlabel("Date")
    plt.ylabel("Gradient de température (°C/h)")
    plt.xticks(rotation=30) #rotation des dates sur l'axe x pour meilleure lisibilité
    ax15.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y\n%H:%M")) #Passage en format européen
    ax15.set_ylim(-30,30) #limitation de y à -30/+30
    plt.legend(loc='lower right', fontsize = 6, ncol=2)
    plt.grid(color = 'grey', linestyle = '--', linewidth = 0.25)
    plt.tight_layout() #sert à ce que la figure ne dépasse pas des bords du PDF
    plt.savefig("{}/Gradient des températures métal pendant l'EHP - GV.pdf".format(output_dir))
    #plt.show() 
    
    ###Evolution de la pression pendant l'épreuve
    ##
    ##
    fig,ax12 = plt.subplots()
    #filtrage pour avoir que le palier
    EHP001MPfilt=EHPdata["EHP001MP"]>172
    positions = np.flatnonzero(EHP001MPfilt)
    maskEHP001MP=EHPdata.iloc[positions]
    DateEpreuveMule=pd.to_datetime(maskEHP001MP.Horodatage, infer_datetime_format=True, dayfirst=True)
    EHP002MPfilt=EHPdata["EHP002MP"]>172
    positions = np.flatnonzero(EHP002MPfilt)
    maskEHP002MP=EHPdata.iloc[positions]
    DateEpreuveMule2=pd.to_datetime(maskEHP002MP.Horodatage, infer_datetime_format=True, dayfirst=True)
    
    
    plt.plot(DateEpreuveMule,maskEHP001MP.EHP001MP, label='EHP001MP', linewidth=0.5)
    plt.plot(DateEpreuveMule2,maskEHP002MP.EHP002MP, label='EHP002MP', linewidth=0.5)
    if not DateEpreuveMule.empty:
        plt.hlines(207.8,np.min(DateEpreuveMule), np.max(DateEpreuveMule), colors='purple', label='207.8 bar', linewidth=0.5)
        plt.hlines(206.9,np.min(DateEpreuveMule), np.max(DateEpreuveMule), colors='purple', label='206,9 bar', linewidth=0.5)
    
    plt.title("Evolution de la pression pendant le palier d'épreuve")
    plt.xlabel("Date")
    plt.ylabel("Pression (bar)")
    plt.xticks(rotation=30)#rotation des dates sur l'axe x pour meilleure lisibilité
    ax12.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y\n%H:%M")) #Passage en format européen
    plt.legend(loc='upper left')
    plt.grid(color = 'grey', linestyle = '--', linewidth = 0.25)
    plt.tight_layout() #sert à ce que la figure ne dépasse pas des bords du PDF
    plt.savefig("{}/Evolution de la pression pendant l'épreuve.pdf".format(output_dir))
    #plt.show()
    
    ###Evolution de la pression pendant le palier 206bar
    ##
    ##
    fig,ax13 = plt.subplots()
    #filtrage pour avoir que le palier
    EHP001MPfilt=EHPdata["EHP001MP"]>205
    positions = np.flatnonzero(EHP001MPfilt)
    maskEHP001MP=EHPdata.iloc[positions]
    DateEpreuveMule=pd.to_datetime(maskEHP001MP.Horodatage, infer_datetime_format=True, dayfirst=True)
    EHP002MPfilt=EHPdata["EHP002MP"]>205
    positions = np.flatnonzero(EHP002MPfilt)
    maskEHP002MP=EHPdata.iloc[positions]
    DateEpreuveMule2=pd.to_datetime(maskEHP002MP.Horodatage, infer_datetime_format=True, dayfirst=True)
    
    
    plt.plot(DateEpreuveMule,maskEHP001MP.EHP001MP, label='EHP001MP', linewidth=0.5)
    plt.plot(DateEpreuveMule2,maskEHP002MP.EHP002MP, label='EHP002MP', linewidth=0.5)
    if not DateEpreuveMule.empty:
        plt.hlines(206,np.min(DateEpreuveMule), np.max(DateEpreuveMule), colors='purple', label='206 bar', linewidth=0.5)
        plt.hlines(206.9,np.min(DateEpreuveMule), np.max(DateEpreuveMule), colors='purple', label='206,9 bar', linewidth=0.5)
    plt.title("Evolution de la pression pendant le palier d'épreuve")
    plt.xlabel("Date")
    plt.ylabel("Pression (bar)")
    plt.xticks(rotation=30)#rotation des dates sur l'axe x pour meilleure lisibilité
    ax13.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y\n%H:%M")) #Passage en format européen
    plt.legend(loc='lower center')
    plt.grid(color = 'grey', linestyle = '--', linewidth = 0.25)
    plt.tight_layout() #sert à ce que la figure ne dépasse pas des bords du PDF
    plt.savefig("{}/Evolution de la pression pendant le palier 206bar.pdf".format(output_dir))
    if value2.get()==1:
        plt.show()
    
    ##
    gc.collect() #vide la mémoire
    
def courbes900Seg():
    def mkdir_p(mypath):
        '''Creates a directory. equivalent to using mkdir -p on the command line'''
        from errno import EEXIST
        from os import makedirs,path

        try:
            makedirs(mypath)
        except OSError as exc: # Python >2.5
                if exc.errno == EEXIST and path.isdir(mypath):
                    pass
                else: raise
    
    if filepath=="":
        fenetre4=Tk()
        w=Label(fenetre4, text="Veuillez selectionner un fichier de données")
        w.pack()
        Bouton=Button(fenetre4, text="Fermer", command=fenetre4.destroy)
        Bouton.pack() 
        return() 
    if savepath=="":
        fenetre3=Tk()
        w=Label(fenetre3, text="Veuillez selectionner un dossier de sauvegarde")
        w.pack()
        Bouton=Button(fenetre3, text="Fermer", command=fenetre3.destroy)
        Bouton.pack() 
        return()
    output_dir = savepath+"/Courbes épreuve"
    mkdir_p(output_dir)

    #
    
    ##### Début du traçage de courbes #####
    
    gc.collect() #vide la mémoire
    
    EHPdata = pd.read_csv(filepath ,sep=';', header=15)
    
    
    #print(EHPdata)
    
    Date=pd.to_datetime(EHPdata.Horodatage, infer_datetime_format=True, dayfirst=True)
    
    
    
    #print(Date)
    
    ##Evolution de la pression RCP pendant l'épreuve
    ##
    #
    fig,ax1 = plt.subplots()
    plt.plot(Date,EHPdata.EHP001MP, label='EHP001MP', linewidth=0.5)
    plt.plot(Date,EHPdata.EHP002MP, label='EHP002MP', linewidth=0.5)
    plt.title("Evolution de la pression RCP pendant l'épreuve")
    plt.xlabel("Date")
    plt.ylabel("Pression (bar)")
    plt.xticks(rotation=30)
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y\n%H:%M")) #Passage en format européen
    plt.legend(loc='upper left')
    plt.grid(color = 'grey', linestyle = '--', linewidth = 0.25)
    plt.tight_layout() #sert à ce que la figure ne dépasse pas des bords du PDF
    plt.savefig("{}/Evolution de la pression RCP pendant l'épreuve.pdf".format(output_dir))
    #plt.show()
    
    ###Evolution de la pression de refoulement de la pompe RCV191PO
    ##
    ##
    fig,ax2 = plt.subplots()
    plt.plot(Date,EHPdata.EHP003MP, label='EHP003MP', linewidth=0.5)
    plt.hlines(241,np.min(Date), np.max(Date),linewidth=0.5, colors='purple', label='Pression limite EHP003MP 241bars')
    plt.hlines(235.5,np.min(Date), np.max(Date),linewidth=0.5, colors='red', label='Seuil arrêt de la pompe \nRIS011PO 235,5bars')
    plt.hlines(230,np.min(Date), np.max(Date),linewidth=0.5, colors='orange', label='Seuil alarme haute pression de refoulement \nRIS011PO 230bars')
    plt.title("Evolution de la pression de refoulement de la pompe RIS011PO")
    plt.xlabel("Date")
    plt.ylabel("Pression (bar)")
    plt.xticks(rotation=30)
    ax2.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y\n%H:%M")) #Passage en format européen
    plt.legend(loc='center left', fontsize=6)
    plt.grid(color = 'grey', linestyle = '--', linewidth = 0.25)
    plt.tight_layout() #sert à ce que la figure ne dépasse pas des bords du PDF
    plt.savefig("{}/Pression de refoulement RIS011PO.pdf".format(output_dir))
    #plt.show()
    
    ###Evolution de la pression de refoulement de la pompe RCV191PO
    ##
    ##
    fig,ax3 = plt.subplots()
    #filtrage pour avoir que l'épreuve
    EHP003MPfilt=EHPdata["EHP003MP"]>4
    positions = np.flatnonzero(EHP003MPfilt)
    maskEHP003MP=EHPdata.iloc[positions]
    DateEpreuveMule=pd.to_datetime(maskEHP003MP.Horodatage, infer_datetime_format=True, dayfirst=True)
    #debug
    #print(maskEHP003MP.EHP003MP)
    
    
    plt.plot(DateEpreuveMule,maskEHP003MP.EHP003MP, label='EHP003MP',linewidth=0.5)
    if not DateEpreuveMule.empty:
        plt.hlines(241,np.min(DateEpreuveMule), np.max(DateEpreuveMule),linewidth=0.5, colors='purple', label='Pression limite EHP003MP 241bars')
        plt.hlines(235.5,np.min(DateEpreuveMule), np.max(DateEpreuveMule),linewidth=0.5, colors='red', label='Seuil arrêt de la pompe \nRIS011PO 235,5bars')
        plt.hlines(230,np.min(DateEpreuveMule), np.max(DateEpreuveMule),linewidth=0.5, colors='orange', label='Seuil alarme haute pression de refoulement \nRIS011PO 230bars')
    plt.title("Evolution de la pression de refoulement de la pompe RIS011PO")
    plt.xlabel("Date")
    plt.ylabel("Pression (bar)")
    plt.xticks(rotation=30)#rotation des dates sur l'axe x pour meilleure lisibilité
    ax3.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y\n%H:%M")) #Passage en format européen
    plt.legend(loc='lower center', fontsize=6)
    plt.grid(color = 'grey', linestyle = '--', linewidth = 0.25)
    plt.tight_layout() #sert à ce que la figure ne dépasse pas des bords du PDF
    plt.savefig("{}/Evolution de la pression de refoulement RIS011PO - détail.pdf".format(output_dir))
    #plt.show()
    
    ##Température des gros composants du CPP - Fond de cuve
    ##
    #
    fig,ax4 = plt.subplots()
    plt.plot(Date,EHPdata.EHP001MT, label='EHP001MT', linewidth=0.5)
    plt.plot(Date,EHPdata.EHP002MT, label='EHP002MT',linewidth=0.5)
    plt.plot(Date,EHPdata.EHP003MT, label='EHP003MT', linewidth=0.5)
    plt.title("Température des gros composants du CPP - Fond de cuve")
    plt.xlabel("Date")
    plt.ylabel("Température (°C)")
    plt.xticks(rotation=30)#rotation des dates sur l'axe x pour meilleure lisibilité
    ax4.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y\n%H:%M")) #Passage en format européen
    plt.legend(loc='lower center')
    plt.grid(color = 'grey', linestyle = '--', linewidth = 0.25)
    plt.tight_layout() #sert à ce que la figure ne dépasse pas des bords du PDF
    plt.savefig("{}/Température des gros composants.pdf".format(output_dir))
    #plt.show()
    
    ##Température des gros composants - couvercle&pressu
    ##
    #
    fig,ax5 = plt.subplots()
    plt.plot(Date,EHPdata.EHP004MT, label='EHP004MT - Bride de cuve', linewidth=0.5)
    plt.plot(Date,EHPdata.EHP005MT, label='EHP005MT - Bride de couvercle',linewidth=0.5)
    plt.plot(Date,EHPdata.EHP006MT, label='EHP006MT - JEP Pressu', linewidth=0.5)
    plt.title("Température des gros composants du CPP")
    plt.xlabel("Date")
    plt.ylabel("Température (°C)")
    plt.xticks(rotation=30) #rotation des dates sur l'axe x pour meilleure lisibilité
    ax5.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y\n%H:%M")) #Passage en format européen
    plt.legend(loc='lower center')
    plt.grid(color = 'grey', linestyle = '--', linewidth = 0.25)
    plt.tight_layout() #sert à ce que la figure ne dépasse pas des bords du PDF
    plt.savefig("{}/Température des gros composants - couvercle&pressu.pdf".format(output_dir))
    #plt.show()
    
    ##Température des gros composants - GVs
    ##
    #
    fig,ax6 = plt.subplots()
    plt.plot(Date,EHPdata.EHP007MT, label='EHP007MT - GV1', linewidth=0.5)
    plt.plot(Date,EHPdata.EHP008MT, label='EHP008MT - GV2',linewidth=0.5)
    plt.plot(Date,EHPdata.EHP009MT, label='EHP009MT - GV3', linewidth=0.5)
    plt.title("Température des gros composants du CPP")
    plt.xlabel("Date")
    plt.ylabel("Température (°C)")
    plt.xticks(rotation=30) #rotation des dates sur l'axe x pour meilleure lisibilité
    ax6.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y\n%H:%M")) #Passage en format européen
    plt.legend(loc='lower center')
    plt.grid(color = 'grey', linestyle = '--', linewidth = 0.25)
    plt.tight_layout() #sert à ce que la figure ne dépasse pas des bords du PDF
    plt.savefig("{}/Température des gros composants - GVs.pdf".format(output_dir))
    #plt.show()
    
    
    ##Gradients de pression
    ##
    #
    fig,ax7 = plt.subplots()
    plt.plot(Date,EHPdata.EHP001MPGrad, label='EHP001MPGrad', linewidth=0.5)
    plt.plot(Date,EHPdata.EHP002MPGrad, label='EHP002MPGrad',linewidth=0.5)
    plt.hlines(4,np.min(Date), np.max(Date), colors='purple', label='Valeur Max Gradient (+4 bar/min)', linewidth=0.5)
    plt.hlines(-4,np.min(Date), np.max(Date), colors='purple', label='Valeur Min Gradient (-4 bar/min)', linewidth=0.5)
    plt.title("Gradients de Pression de l'EHP")
    plt.xlabel("Date")
    plt.ylabel("Gradient de pression en bar/min")
    ax7.set_ylim(-15,15) #limitation de y à -15/+15
    plt.xticks(rotation=30) #rotation des dates sur l'axe x pour meilleure lisibilité
    ax7.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y\n%H:%M")) #Passage en format européen
    plt.legend(loc='lower left', fontsize=6)
    plt.grid(color = 'grey', linestyle = '--', linewidth = 0.25)
    plt.tight_layout() #sert à ce que la figure ne dépasse pas des bords du PDF
    plt.savefig("{}/Gradients de pression.pdf".format(output_dir))
    #plt.show() 
    
    ##Suivi Tmoy
    ##
    #
    fig,ax8 = plt.subplots()
    plt.plot(Date,EHPdata.TMOY, label='Tmoy', linewidth=0.5)
    plt.title("Suivi de la Tmoy de l'EHP")
    plt.xlabel("Date")
    plt.ylabel("Température (°C)")
    plt.xticks(rotation=30) #rotation des dates sur l'axe x pour meilleure lisibilité
    ax8.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y\n%H:%M")) #Passage en format européen
    plt.legend(loc='lower center')
    plt.grid(color = 'grey', linestyle = '--', linewidth = 0.25)
    plt.tight_layout() #sert à ce que la figure ne dépasse pas des bords du PDF
    plt.savefig("{}/Suivi Tmoy.pdf".format(output_dir))
    #plt.show() 
    
    ##Suivi gradient Tmoy
    ##
    #
    fig,ax9 = plt.subplots()
    plt.plot(Date,EHPdata.TGRAD, label='Tgrad', linewidth=0.5)
    
    #limites de gradient
    #filtrage pour avoir T>50
    TMOYfiltsup=EHPdata["TMOY"]>60
    positions = np.flatnonzero(TMOYfiltsup)
    maskTMOYfiltsup=EHPdata.iloc[positions]
    DateTmoysup50=pd.to_datetime(maskTMOYfiltsup.Horodatage, infer_datetime_format=True, dayfirst=True)
    
    
    
    #filtrage pour avoir T<50
    TMOYfiltinf=EHPdata["TMOY"]<60
    positions = np.flatnonzero(TMOYfiltinf)
    maskTMOYfiltinf=EHPdata.iloc[positions]
    DateTmoyinf50=pd.to_datetime(maskTMOYfiltinf.Horodatage, infer_datetime_format=True, dayfirst=True)
    
    
    #filtrage pour avoir T=50
    TMOYfiltegal=EHPdata["TMOY"]==60
    positions = np.flatnonzero(TMOYfiltegal)
    maskTMOYfiltegal=EHPdata.iloc[positions]
    DateTmoyegal50=pd.to_datetime(maskTMOYfiltegal.Horodatage, infer_datetime_format=True, dayfirst=True)
    if not DateTmoysup50.empty:
        plt.hlines(28,np.min(DateTmoysup50), np.max(DateTmoysup50), colors='purple', label='+/-28°C/h', linewidth=1)
        plt.hlines(-28,np.min(DateTmoysup50), np.max(DateTmoysup50), colors='purple', linewidth=1)
    plt.vlines(DateTmoyegal50,-28,-14, colors='purple', linewidth=0.5)
    plt.vlines(DateTmoyegal50,28,14, colors='purple', linewidth=0.5)
    if not DateTmoyinf50.empty:
        if not DateTmoyegal50.empty:
            plt.hlines(14,np.min(DateTmoyinf50), np.min(DateTmoyegal50), colors='orange', label='+/-14°C/h', linewidth=0.5)
            plt.hlines(-14,np.min(DateTmoyinf50), np.min(DateTmoyegal50), colors='orange', linewidth=0.5)
            plt.hlines(14, np.max(DateTmoyegal50), np.max(DateTmoyinf50), colors='orange', linewidth=0.5)
            plt.hlines(-14, np.max(DateTmoyegal50),np.max(DateTmoyinf50), colors='orange', linewidth=0.5)
    
    #Fin limites de gradient
    
    plt.title("Suivi du gradient de Tmoy de l'EHP")
    plt.xlabel("Date")
    plt.ylabel("Température (°C)")
    plt.xticks(rotation=30) #rotation des dates sur l'axe x pour meilleure lisibilité
    ax9.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y\n%H:%M")) #Passage en format européen
    plt.legend(loc='upper left')
    plt.grid(color = 'grey', linestyle = '--', linewidth = 0.25)
    plt.tight_layout() #sert à ce que la figure ne dépasse pas des bords du PDF
    plt.savefig("{}/Suivi Tgrad.pdf".format(output_dir))
    
    #plt.show() 
    
    ##Suivi des températures fluide pendant l'EHP
    ##
    #
    fig,ax10 = plt.subplots()
    plt.plot(Date,EHPdata.RCP009MT, label='RCP009MT', linewidth=0.5)
    plt.plot(Date,EHPdata.RCP010MT, label='RCP010MT', linewidth=0.5) 
    plt.plot(Date,EHPdata.RCP028MT, label='RCP028MT', linewidth=0.5) 
    
    plt.title("Suivi des températures fluide pendant l'EHP")
    plt.xlabel("Date")
    plt.ylabel("Température (°C/h)")
    plt.xticks(rotation=30) #rotation des dates sur l'axe x pour meilleure lisibilité
    ax10.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y\n%H:%M")) #Passage en format européen
    plt.legend(loc='lower center')
    plt.grid(color = 'grey', linestyle = '--', linewidth = 0.25)
    plt.tight_layout() #sert à ce que la figure ne dépasse pas des bords du PDF
    plt.savefig("{}/Suivi des températures fluide pendant l'EHP - 1.pdf".format(output_dir))
    #plt.show() 
    
    fig,ax101 = plt.subplots()
    plt.plot(Date,EHPdata.RCP029MT, label='RCP029MT', linewidth=0.5) 
    plt.plot(Date,EHPdata.RCP043MT, label='RCP043MT', linewidth=0.5) 
    plt.plot(Date,EHPdata.RCP044MT, label='RCP044MT', linewidth=0.5) 
   
    plt.title("Suivi des températures fluide pendant l'EHP")
    plt.xlabel("Date")
    plt.ylabel("Température (°C/h)")
    plt.xticks(rotation=30) #rotation des dates sur l'axe x pour meilleure lisibilité
    ax101.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y\n%H:%M")) #Passage en format européen
    plt.legend(loc='lower center')
    plt.grid(color = 'grey', linestyle = '--', linewidth = 0.25)
    plt.tight_layout() #sert à ce que la figure ne dépasse pas des bords du PDF
    plt.savefig("{}/Suivi des températures fluide pendant l'EHP - 2.pdf".format(output_dir))
    #plt.show()
    
    fig,ax102 = plt.subplots()

    plt.plot(Date,EHPdata.RCP055MT, label='RCP055MT', linewidth=0.5) 
    plt.plot(Date,EHPdata.RCP056MT, label='RCP056MT', linewidth=0.5) 
    plt.title("Suivi des températures fluide pendant l'EHP")
    plt.xlabel("Date")
    plt.ylabel("Température (°C/h)")
    plt.xticks(rotation=30) #rotation des dates sur l'axe x pour meilleure lisibilité
    ax102.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y\n%H:%M")) #Passage en format européen
    plt.legend(loc='lower center' )
    plt.grid(color = 'grey', linestyle = '--', linewidth = 0.25)
    plt.tight_layout() #sert à ce que la figure ne dépasse pas des bords du PDF
    plt.savefig("{}/Suivi des températures fluide pendant l'EHP - 3.pdf".format(output_dir))
    #plt.show()
    
    ##Gradient des températures métal pendant l'EHP - 1
    ##
    #
    fig,ax11 = plt.subplots()
    plt.plot(Date,EHPdata.EHP001MTGrad, label='EHP001MTGrad', linewidth=0.5)
    plt.plot(Date,EHPdata.EHP002MTGrad, label='EHP002MTGrad', linewidth=0.5)
    plt.plot(Date,EHPdata.EHP003MTGrad, label='EHP003MTGrad', linewidth=0.5)
    
    
    plt.title("Gradient des températures métal pendant l'EHP - Fond de cuve")
    plt.xlabel("Date")
    plt.ylabel("Gradient de température (°C/h)")
    plt.xticks(rotation=30) #rotation des dates sur l'axe x pour meilleure lisibilité
    ax11.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y\n%H:%M")) #Passage en format européen
    ax11.set_ylim(-30,30) #limitation de y à -30/+30
    plt.legend(loc='lower right', fontsize = 6, ncol=2)
    plt.grid(color = 'grey', linestyle = '--', linewidth = 0.25)
    plt.tight_layout() #sert à ce que la figure ne dépasse pas des bords du PDF
    plt.savefig("{}/Gradient des températures métal pendant l'EHP - Fond de cuve.pdf".format(output_dir))
    #plt.show() 
    
    ##Gradient des températures métal pendant l'EHP - Couvercle et pressu
    ##
    #
    fig,ax14 = plt.subplots()
    
    plt.plot(Date,EHPdata.EHP004MTGrad, label='EHP004MTGrad - Bride de cuve', linewidth=0.5)
    plt.plot(Date,EHPdata.EHP005MTGrad, label='EHP005MTGrad - Bride de couvercle', linewidth=0.5)
    plt.plot(Date,EHPdata.EHP006MTGrad, label='EHP006MTGrad - JEP Pressu', linewidth=0.5)
    
    plt.title("Gradient des températures métal pendant l'EHP - Couvercle et Pressu")
    plt.xlabel("Date")
    plt.ylabel("Gradient de température (°C/h)")
    plt.xticks(rotation=30) #rotation des dates sur l'axe x pour meilleure lisibilité
    ax14.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y\n%H:%M")) #Passage en format européen
    ax14.set_ylim(-30,30) #limitation de y à -30/+30
    plt.legend(loc='lower right', fontsize = 6, ncol=2)
    plt.grid(color = 'grey', linestyle = '--', linewidth = 0.25)
    plt.tight_layout() #sert à ce que la figure ne dépasse pas des bords du PDF
    plt.savefig("{}/Gradient des températures métal pendant l'EHP - Couvercle et pressu.pdf".format(output_dir))
    #plt.show() 
    
    ##Gradient des températures métal pendant l'EHP - GV
    ##
    #
    fig,ax15 = plt.subplots()
    
    plt.plot(Date,EHPdata.EHP007MTGrad, label='EHP007MTGrad - GV1', linewidth=0.5)
    plt.plot(Date,EHPdata.EHP008MTGrad, label='EHP008MTGrad - GV2', linewidth=0.5)
    plt.plot(Date,EHPdata.EHP009MTGrad, label='EHP009MTGrad - GV3', linewidth=0.5)
    plt.title("Gradient des températures métal pendant l'EHP - GV")
    plt.xlabel("Date")
    plt.ylabel("Gradient de température (°C/h)")
    plt.xticks(rotation=30) #rotation des dates sur l'axe x pour meilleure lisibilité
    ax15.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y\n%H:%M")) #Passage en format européen
    ax15.set_ylim(-30,30) #limitation de y à -30/+30
    plt.legend(loc='lower right', fontsize = 6, ncol=2)
    plt.grid(color = 'grey', linestyle = '--', linewidth = 0.25)
    plt.tight_layout() #sert à ce que la figure ne dépasse pas des bords du PDF
    plt.savefig("{}/Gradient des températures métal pendant l'EHP - GV.pdf".format(output_dir))
    #plt.show() 
    
    ###Evolution de la pression pendant l'épreuve
    ##
    ##
    fig,ax12 = plt.subplots()
    #filtrage pour avoir que le palier
    EHP001MPfilt=EHPdata["EHP001MP"]>172
    positions = np.flatnonzero(EHP001MPfilt)
    maskEHP001MP=EHPdata.iloc[positions]
    DateEpreuveMule=pd.to_datetime(maskEHP001MP.Horodatage, infer_datetime_format=True, dayfirst=True)
    EHP002MPfilt=EHPdata["EHP002MP"]>172
    positions = np.flatnonzero(EHP002MPfilt)
    maskEHP002MP=EHPdata.iloc[positions]
    DateEpreuveMule2=pd.to_datetime(maskEHP002MP.Horodatage, infer_datetime_format=True, dayfirst=True)
    
    
    plt.plot(DateEpreuveMule,maskEHP001MP.EHP001MP, label='EHP001MP', linewidth=0.5)
    plt.plot(DateEpreuveMule2,maskEHP002MP.EHP002MP, label='EHP002MP', linewidth=0.5)
    if not DateEpreuveMule.empty:
        plt.hlines(207.8,np.min(DateEpreuveMule), np.max(DateEpreuveMule), colors='purple', label='207.8 bar', linewidth=0.5)
        plt.hlines(206.9,np.min(DateEpreuveMule), np.max(DateEpreuveMule), colors='purple', label='206,9 bar', linewidth=0.5)
    
    plt.title("Evolution de la pression pendant le palier d'épreuve")
    plt.xlabel("Date")
    plt.ylabel("Pression (bar)")
    plt.xticks(rotation=30)#rotation des dates sur l'axe x pour meilleure lisibilité
    ax12.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y\n%H:%M")) #Passage en format européen
    plt.legend(loc='upper left')
    plt.grid(color = 'grey', linestyle = '--', linewidth = 0.25)
    plt.tight_layout() #sert à ce que la figure ne dépasse pas des bords du PDF
    plt.savefig("{}/Evolution de la pression pendant l'épreuve.pdf".format(output_dir))
    #plt.show()
    
    ###Evolution de la pression pendant le palier 206bar
    ##
    ##
    fig,ax13 = plt.subplots()
    #filtrage pour avoir que le palier
    EHP001MPfilt=EHPdata["EHP001MP"]>205
    positions = np.flatnonzero(EHP001MPfilt)
    maskEHP001MP=EHPdata.iloc[positions]
    DateEpreuveMule=pd.to_datetime(maskEHP001MP.Horodatage, infer_datetime_format=True, dayfirst=True)
    EHP002MPfilt=EHPdata["EHP002MP"]>205
    positions = np.flatnonzero(EHP002MPfilt)
    maskEHP002MP=EHPdata.iloc[positions]
    DateEpreuveMule2=pd.to_datetime(maskEHP002MP.Horodatage, infer_datetime_format=True, dayfirst=True)
    
    
    plt.plot(DateEpreuveMule,maskEHP001MP.EHP001MP, label='EHP001MP', linewidth=0.5)
    plt.plot(DateEpreuveMule2,maskEHP002MP.EHP002MP, label='EHP002MP', linewidth=0.5)
    if not DateEpreuveMule.empty:
        plt.hlines(206,np.min(DateEpreuveMule), np.max(DateEpreuveMule), colors='purple', label='206 bar', linewidth=0.5)
        plt.hlines(206.9,np.min(DateEpreuveMule), np.max(DateEpreuveMule), colors='purple', label='206,9 bar', linewidth=0.5)
    plt.title("Evolution de la pression pendant le palier d'épreuve")
    plt.xlabel("Date")
    plt.ylabel("Pression (bar)")
    plt.xticks(rotation=30)#rotation des dates sur l'axe x pour meilleure lisibilité
    ax13.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y\n%H:%M")) #Passage en format européen
    plt.legend(loc='lower center')
    plt.grid(color = 'grey', linestyle = '--', linewidth = 0.25)
    plt.tight_layout() #sert à ce que la figure ne dépasse pas des bords du PDF
    plt.savefig("{}/Evolution de la pression pendant le palier 206bar.pdf".format(output_dir))
    if value2.get()==1:
        plt.show()
    
    ##
    gc.collect() #vide la mémoire

def extractionHC():
    gc.collect() #vide la mémoire
    def mkdir_p(mypath):
        '''Creates a directory. equivalent to using mkdir -p on the command line'''
        from errno import EEXIST
        from os import makedirs,path

        try:
            makedirs(mypath)
        except OSError as exc: # Python >2.5
                if exc.errno == EEXIST and path.isdir(mypath):
                    pass
                else: raise
    
    if filepath=="":
        fenetre4=Tk()
        w=Label(fenetre4, text="Veuillez selectionner un fichier de données")
        w.pack()
        Bouton=Button(fenetre4, text="Fermer", command=fenetre4.destroy)
        Bouton.pack() 
        return() 
    if savepath=="":
        fenetre3=Tk()
        w=Label(fenetre3, text="Veuillez selectionner un dossier de sauvegarde")
        w.pack()
        Bouton=Button(fenetre3, text="Fermer", command=fenetre3.destroy)
        Bouton.pack() 
        return()
    output_dir = savepath+"/Gradients Hors critères"
    mkdir_p(output_dir)
   
    
    EHPdata = pd.read_csv(filepath ,sep=';', header=15)



    Date=pd.to_datetime(EHPdata.Horodatage, infer_datetime_format=True, dayfirst=True)

    EHP001MPfilt=EHPdata["EHP001MPGrad"]>4
    positions = np.flatnonzero(EHP001MPfilt)
    maskEHP001MP=EHPdata.iloc[positions]
    DateEpreuveMule=pd.to_datetime(maskEHP001MP.Horodatage, infer_datetime_format=True, dayfirst=True)
    
    maskEHP001MP.to_excel(output_dir+r'\EHP1MPGrad_sup4.xlsx')
    
    EHP001MPfilt=EHPdata["EHP001MPGrad"]<-4
    positions = np.flatnonzero(EHP001MPfilt)
    maskEHP001MP=EHPdata.iloc[positions]
    
    maskEHP001MP.to_excel(output_dir+r'\EHP1MPGrad_inf-4.xlsx')
    
    EHP001MPfilt=EHPdata["TGRAD"]>28
    positions = np.flatnonzero(EHP001MPfilt)
    maskEHP001MP=EHPdata.iloc[positions]
    
    ##print(maskEHP003MP)
    maskEHP001MP.to_excel(output_dir+r'\TGrad_sup28.xlsx')
    
    EHP001MPfilt=EHPdata["TGRAD"]<-28
    positions = np.flatnonzero(EHP001MPfilt)
    maskEHP001MP=EHPdata.iloc[positions]
    
    maskEHP001MP.to_excel(output_dir+r'\TGrad_inf-28.xlsx')
    
    if value.get()==2: ##900seg
        print("OK segregation")
        TMOYfiltinf=EHPdata["TMOY"]<60
        positions = np.flatnonzero(TMOYfiltinf)
        maskTMOYfiltinf = EHPdata.iloc[positions]
        TGRADfilt=maskTMOYfiltinf["TGRAD"]>14
        positions = np.flatnonzero(TGRADfilt)
        maskTGRADfilt=EHPdata.iloc[positions]
    
        maskTGRADfilt.to_excel(output_dir+r'\TGrad_sup14.xlsx')
    
        TMOYfiltinf=EHPdata["TMOY"]<60
        positions = np.flatnonzero(TMOYfiltinf)
        maskTMOYfiltinf = EHPdata.iloc[positions]
        TGRADfilt=maskTMOYfiltinf["TGRAD"]<-14
        positions = np.flatnonzero(TGRADfilt)
        maskTGRADfilt=EHPdata.iloc[positions]
    
        maskTGRADfilt.to_excel(output_dir+r'\TGrad_inf-14.xlsx')
    else:
        print("NOK SEG")
        TMOYfiltinf=EHPdata["TMOY"]<50
        positions = np.flatnonzero(TMOYfiltinf)
        maskTMOYfiltinf = EHPdata.iloc[positions]
        TGRADfilt=maskTMOYfiltinf["TGRAD"]>14
        positions = np.flatnonzero(TGRADfilt)
        maskTGRADfilt=EHPdata.iloc[positions]
    
        maskTGRADfilt.to_excel(output_dir+r'\TGrad_sup14.xlsx')
    
        TMOYfiltinf=EHPdata["TMOY"]<50
        positions = np.flatnonzero(TMOYfiltinf)
        maskTMOYfiltinf = EHPdata.iloc[positions]
        TGRADfilt=maskTMOYfiltinf["TGRAD"]<-14
        positions = np.flatnonzero(TGRADfilt)
        maskTGRADfilt=EHPdata.iloc[positions]
    
        maskTGRADfilt.to_excel(output_dir+r'\TGrad_inf-14.xlsx')
        
    gc.collect() #vide la mémoire


def open_file():
    """Ouvrir le fichier de données du banc"""
    global filepath
    filepath = askopenfilename(
        filetypes=[ ("All Files", "*.*")]
    )
    if not filepath:
        return
    
def save_file():
    """Choisir un dossier pour les courbes"""
    global savepath
    savepath = askdirectory()
    if not savepath:
        return  
    
    
def diag_PT():
    def mkdir_p(mypath):
        '''Creates a directory. equivalent to using mkdir -p on the command line'''
        from errno import EEXIST
        from os import makedirs,path

        try:
            makedirs(mypath)
        except OSError as exc: # Python >2.5
                if exc.errno == EEXIST and path.isdir(mypath):
                    pass
                else: raise
    
    if filepath=="":
        fenetre4=Tk()
        w=Label(fenetre4, text="Veuillez selectionner un fichier de données")
        w.pack()
        Bouton=Button(fenetre4, text="Fermer", command=fenetre4.destroy)
        Bouton.pack() 
        return() 
    if savepath=="":
        fenetre3=Tk()
        w=Label(fenetre3, text="Veuillez selectionner un dossier de sauvegarde")
        w.pack()
        Bouton=Button(fenetre3, text="Fermer", command=fenetre3.destroy)
        Bouton.pack() 
        return()
    output_dir = savepath+"/Courbes épreuve"
    mkdir_p(output_dir)

    #
    
    ##### Début du traçage de courbes #####
    
    gc.collect() #vide la mémoire
    
    EHPdata = pd.read_csv(filepath ,sep=';', header=15)
       
    
    EHP00XMTmin=min(EHPdata["EHP001MT"].sum(),EHPdata["EHP002MT"].sum(),EHPdata["EHP003MT"].sum())
    
    if EHP00XMTmin==EHPdata["EHP001MT"].sum():
        DiagPTxaxis=EHPdata.EHP001MT
    elif EHP00XMTmin==EHPdata["EHP002MT"].sum():
        DiagPTxaxis=EHPdata.EHP002MT
    elif EHP00XMTmin==EHPdata["EHP003MT"].sum():
        DiagPTxaxis=EHPdata.EHP003MT
    else:
        return
    ##Diagramme PT
    ##
    #
    fig,ax1 = plt.subplots()
    plt.plot(DiagPTxaxis,EHPdata.EHP001MP, linewidth=0.5)
    plt.title("Diagramme P,T")
    plt.xlabel("Température (°C)")
    plt.ylabel("Pression (bar)")
    plt.grid(color = 'grey', linestyle = '--', linewidth = 0.25)
    plt.tight_layout() #sert à ce que la figure ne dépasse pas des bords du PDF
    plt.savefig("{}/DiagrammePT.pdf".format(output_dir))
    if value3.get()==1:
        plt.show()    


##############  MAIN ##############
    
fenetre = Tk()

fenetre.geometry("150x630+10+10")
#variables globales
filepath=str("")
savepath=str("")

##fonctions de l'interface
def Palier():
    palier=value.get()
    if palier==1:
        courbes900()
    elif palier==2:
        courbes900Seg()
    elif palier==3:
        courbesPQY()
    elif palier==4:
        courbesDPY()
    else :
        callback()
        
def callback():
    fenetre2=Tk()
    w=Label(fenetre2, text="Veuillez selectionner un palier")
    w.pack()
    Bouton=Button(fenetre2, text="Fermer", command=fenetre2.destroy)
    Bouton.pack()
    
##Interface
l1 = LabelFrame(fenetre, text="1. Charger le fichier", padx=20, pady=20)
l1.pack(fill="both", expand="yes")

l = LabelFrame(fenetre, text="2. Palier", padx=20, pady=20)
l.pack(fill="both", expand="yes")

l3 = LabelFrame(fenetre, text="3. Dossier de sauvegarde", padx=20, pady=20)
l3.pack(fill="both", expand="yes")

l4 = LabelFrame(fenetre, text="4. Courbes", padx=20, pady=20)
l4.pack(fill="both", expand="yes")

l5 = LabelFrame(fenetre, text="5. Hors critères gradients", padx=20, pady=20)
l5.pack(fill="both", expand="yes")

l6 = LabelFrame(fenetre, text="6. Diagramme P,T", padx=20, pady=20)
l6.pack(fill="both", expand="yes")
# radiobutton


        
value = IntVar()
Rbouton1 = Radiobutton(l, text="900", variable=value, value=1)
Rbouton2 = Radiobutton(l, text="900 Ségrégué", variable=value, value=2)
Rbouton3 = Radiobutton(l, text="P4", variable=value, value=3)
Rbouton4 = Radiobutton(l, text="P'4", variable=value, value=4)
Rbouton1.pack(anchor = 'w')
Rbouton2.pack(anchor = 'w')
Rbouton3.pack(anchor = 'w')
Rbouton4.pack(anchor = 'w')

value2 = IntVar()
c1 = Checkbutton(l4, text='Afficher courbes',variable=value2, onvalue=1, offvalue=0)
c1.pack()

value3 = IntVar()
c2 = Checkbutton(l6, text='Afficher courbes',variable=value3, onvalue=1, offvalue=0)
c2.pack()

bouton=Button(l1, text="Ouvrir", command=open_file)
bouton2=Button(l4, text="Tracer", command=Palier)
bouton3=Button(l3, text="Sauvegarder", command=save_file)
bouton4=Button(l5, text="Extraire sous excel", command=extractionHC)
bouton5=Button(l6, text="Tracer", command=diag_PT)
bouton.pack()
bouton2.pack()
bouton3.pack()
bouton4.pack()
bouton5.pack()

fenetre.mainloop()

