# -*- coding: utf-8 -*-
"""
Created on Wed May 19 10:12:32 2021

@author: abertheleme

Code sale et à l'arrache
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import numpy as np
import pandas as pd
import gc
#import numpy.random.common
#import numpy.random.bounded_integers
#import numpy.random.entropy

## Creation du dossier de résultats
#
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
        

output_dir = "../Desktop/EHPCourbes/Courbes épreuve"
mkdir_p(output_dir)

#

##### Début du traçage de courbes #####

gc.collect() #vide la mémoire

EHPdata = pd.read_csv('ExportAcquisitions_1_1.csv' ,sep=';', header=15)


#print(EHPdata)

Date=pd.to_datetime(EHPdata.Horodatage, infer_datetime_format=True)



#print(Date)

##Evolution de la pression RCP pendant l'épreuve
##
#
fig,ax1 = plt.subplots()
plt.plot(Date,EHPdata.EHP001MP, label='EHP001MP')
plt.plot(Date,EHPdata.EHP002MP, label='EHP002MP')
plt.title("Evolution de la pression RCP pendant l'épreuve")
plt.xlabel("Date")
plt.ylabel("Pression (bar)")
plt.xticks(rotation=30)
ax1.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y\n%H:%M")) #Passage en format européen
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
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
DateEpreuveMule=pd.to_datetime(maskEHP003MP.Horodatage, infer_datetime_format=True)
#debug
#print(maskEHP003MP.EHP003MP)


plt.plot(DateEpreuveMule,maskEHP003MP.EHP003MP, label='EHP003MP',linewidth=0.5)
plt.hlines(236,np.min(DateEpreuveMule), np.max(DateEpreuveMule),linewidth=0.5, colors='purple', label='Pression limite EHP003MP 236bars')
plt.hlines(232,np.min(DateEpreuveMule), np.max(DateEpreuveMule),linewidth=0.5, colors='red', label='Seuil arrêt de la pompe \nRCV191PO 232bars')
plt.hlines(228,np.min(DateEpreuveMule), np.max(DateEpreuveMule),linewidth=0.5, colors='orange', label='Seuil alarme haute pression de refoulement \nRCV191PO 228bars')
plt.title("Evolution de la pression de refoulement de la pompe RCV191PO")
plt.xlabel("Date")
plt.ylabel("Pression (bar)")
plt.xticks(rotation=30)#rotation des dates sur l'axe x pour meilleure lisibilité
ax3.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y\n%H:%M")) #Passage en format européen
plt.legend(loc='lower center', fontsize=6)
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
DateTmoysup50=pd.to_datetime(maskTMOYfiltsup.Horodatage, infer_datetime_format=True)



#filtrage pour avoir T<50
TMOYfiltinf=EHPdata["TMOY"]<50
positions = np.flatnonzero(TMOYfiltinf)
maskTMOYfiltinf=EHPdata.iloc[positions]
DateTmoyinf50=pd.to_datetime(maskTMOYfiltinf.Horodatage, infer_datetime_format=True)


#filtrage pour avoir T=50
TMOYfiltegal=EHPdata["TMOY"]==50
positions = np.flatnonzero(TMOYfiltegal)
maskTMOYfiltegal=EHPdata.iloc[positions]
DateTmoyegal50=pd.to_datetime(maskTMOYfiltegal.Horodatage, infer_datetime_format=True)

plt.hlines(28,np.min(DateTmoysup50), np.max(DateTmoysup50), colors='purple', label='+/-28°C/h', linewidth=1)
plt.hlines(-28,np.min(DateTmoysup50), np.max(DateTmoysup50), colors='purple', linewidth=1)
plt.vlines(DateTmoyegal50,-28,-14, colors='purple', linewidth=0.5)
plt.vlines(DateTmoyegal50,28,14, colors='purple', linewidth=0.5)
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
plt.tight_layout() #sert à ce que la figure ne dépasse pas des bords du PDF
plt.savefig("{}/Suivi Tgrad.pdf".format(output_dir))

#plt.show() 

##Suivi des températures fluide pendant l'EHP
##
#
fig,ax10 = plt.subplots()
plt.plot(Date,EHPdata.RCP009MT, label='RCP009MT', linewidth=0.5)
plt.plot(Date,EHPdata.RCP010MT, label='RCP014MT', linewidth=0.5) #Uniquement DPY
plt.plot(Date,EHPdata.RCP028MT, label='RCP100MT', linewidth=0.5) #Uniquement DPY
plt.plot(Date,EHPdata.RCP029MT, label='RCP104MT', linewidth=0.5) #Uniquement DPY
plt.plot(Date,EHPdata.RCP043MT, label='RCP200MT', linewidth=0.5) #Uniquement DPY
plt.plot(Date,EHPdata.RCP044MT, label='RCP204MT', linewidth=0.5) #Uniquement DPY
plt.plot(Date,EHPdata.RCP055MT, label='RCP300MT', linewidth=0.5) #Uniquement DPY
plt.plot(Date,EHPdata.RCP056MT, label='RCP304MT', linewidth=0.5) #Uniquement DPY
plt.plot(Date,EHPdata.RCP400MT, label='RCP400MT', linewidth=0.5)
plt.plot(Date,EHPdata.RCP404MT, label='RCP404MT', linewidth=0.5)
plt.title("Suivi des températures fluide pendant l'EHP")
plt.xlabel("Date")
plt.ylabel("Température (°C/h)")
plt.xticks(rotation=30) #rotation des dates sur l'axe x pour meilleure lisibilité
ax10.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y\n%H:%M")) #Passage en format européen
plt.legend(loc='lower center', ncol=2)
plt.tight_layout() #sert à ce que la figure ne dépasse pas des bords du PDF
plt.savefig("{}/Suivi des températures fluide pendant l'EHP.pdf".format(output_dir))
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
DateEpreuveMule=pd.to_datetime(maskEHP001MP.Horodatage, infer_datetime_format=True)
EHP002MPfilt=EHPdata["EHP002MP"]>172
positions = np.flatnonzero(EHP002MPfilt)
maskEHP002MP=EHPdata.iloc[positions]
DateEpreuveMule2=pd.to_datetime(maskEHP002MP.Horodatage, infer_datetime_format=True)


plt.plot(DateEpreuveMule,maskEHP001MP.EHP001MP, label='EHP001MP', linewidth=0.5)
plt.plot(DateEpreuveMule2,maskEHP002MP.EHP002MP, label='EHP002MP', linewidth=0.5)
plt.hlines(207.8,np.min(DateEpreuveMule), np.max(DateEpreuveMule), colors='purple', label='207.8 bar', linewidth=0.5)
plt.hlines(206.9,np.min(DateEpreuveMule), np.max(DateEpreuveMule), colors='purple', label='206,9 bar', linewidth=0.5)

plt.title("Evolution de la pression pendant le palier d'épreuve")
plt.xlabel("Date")
plt.ylabel("Pression (bar)")
plt.xticks(rotation=30)#rotation des dates sur l'axe x pour meilleure lisibilité
ax12.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y\n%H:%M")) #Passage en format européen
plt.legend(loc='upper left')
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
DateEpreuveMule=pd.to_datetime(maskEHP001MP.Horodatage, infer_datetime_format=True)
EHP002MPfilt=EHPdata["EHP002MP"]>205
positions = np.flatnonzero(EHP002MPfilt)
maskEHP002MP=EHPdata.iloc[positions]
DateEpreuveMule2=pd.to_datetime(maskEHP002MP.Horodatage, infer_datetime_format=True)


plt.plot(DateEpreuveMule,maskEHP001MP.EHP001MP, label='EHP001MP')
plt.plot(DateEpreuveMule2,maskEHP002MP.EHP002MP, label='EHP002MP')
plt.hlines(206,np.min(DateEpreuveMule), np.max(DateEpreuveMule), colors='purple', label='206 bar', linewidth=0.5)
plt.hlines(206.9,np.min(DateEpreuveMule), np.max(DateEpreuveMule), colors='purple', label='206,9 bar', linewidth=0.5)
plt.title("Evolution de la pression pendant le palier d'épreuve")
plt.xlabel("Date")
plt.ylabel("Pression (bar)")
plt.xticks(rotation=30)#rotation des dates sur l'axe x pour meilleure lisibilité
ax13.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%y\n%H:%M")) #Passage en format européen
plt.legend(loc='lower center')
plt.tight_layout() #sert à ce que la figure ne dépasse pas des bords du PDF
plt.savefig("{}/Evolution de la pression pendant le palier 206bar.pdf".format(output_dir))
plt.show()

##
gc.collect() #vide la mémoire