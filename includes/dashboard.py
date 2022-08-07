# @Date:   2021-03-22T12:52:26+01:00
# @Last modified time: 2021-04-11T19:43:17+02:00

from tkinter import *
import os
import math
from includes.chrono import *
import tkinter.font as font
import csv

class Dashboard:
    def __init__(self, master):
        self.master = master
        # self.FrameDestroy()
        self.update_Datas()
        #FENETRE PRINCIPALE
        self.width_screen = self.master.winfo_screenwidth()-20 #-20 de highlightthickness=10
        self.height_screen = self.master.winfo_screenheight()-20 #-20 de highlightthickness=10
        self.space = math.ceil(self.width_screen/50) #variable qui va espacer les différents cadres
        self.master.geometry(f"{self.width_screen}x{self.height_screen}")
        self.master.configure(bg="black", highlightbackground=self.hy_background, highlightcolor=self.hy_background, highlightthickness=10, padx=0, pady=0, borderwidth=0, relief="flat")


        #POLICES
        self.font_titre=("Arial", int(self.space*0.8),"bold")
        self.font_titre_donnees=("Arial", int(self.space*1.5),"bold")
        self.font_donnees=("Arial", int(self.space*1.5),"bold")
        self.font_donnees_track=("Arial", int(self.space*1.8),"bold")
        self.font_time=("Arial", int(self.space*3),"bold")
        self.font_vitesse_track=("Arial", int(self.space*3),"bold")
        self.font_turn=("Arial", int(self.space*2.5),"bold")
        self.font_donnees_signaux=("Arial", int(self.space*1.4),"bold")
        self.font_vitesse=("Arial", int(self.space*2.3),"bold")
        self.font_hy=("Arial", int(self.space*2),"bold")
        self.font_etat_clutch=("Arial", int(self.space*1.2),"bold")
        self.font_titre_ice=("Arial", int(self.space*1),"bold")
        self.font_titre_signaux=("Arial", int(self.space*1.2),"bold")
        self.master.attributes('-fullscreen',True) #affichage plein écran
        self.master.bind("<Escape>", lambda e: self.master.destroy()) #<ESC> pour pouvoir fermer le programe

    def waitForLeft(self, var, ft):
        self.master.bind("<Left>", lambda var : ft(self.master)) #<Left> pour afficher le menu track

    def update_Datas(self):
        with open("log_test.csv") as log:
            file = csv.reader(log, delimiter=',')
            for row in file:
                #VARIABLES DU DASHBOARD
                self.engine_rpm=int(row[0])
                self.engine_torque=float(row[1]) #Nm
                self.engine_temp=float(row[2]) #°C
                self.p_fuel=float(row[3]) #bars
                self.fuel_cons=float(row[4]) #mL
                self.ice_clutch1=row[5] #True si ICE Clutch ON
                self.motor_rpm=int(row[6])
                self.motor_torque=float(row[7])
                self.motor_temp=float(row[8])
                self.distance=float(row[9]) #km
                self.efficiency=float(row[10]) #km/L
                self.ice_clutch2=row[11] #False si ICE Clutch OFF
                self.fuel_mode=row[12] #True si mode FUEL ON
                self.soc=float(row[13]) #%
                self.lipo=float(row[14]) #%
                self.connexion=row[15] #True si état de connexion 3g OK
                self.gps=row[16] #True si connexion GPS OK
                self.speed=int(row[17]) #km/h
                self.hybride_mode=row[18] #False si mode HY pas activé
                self.time = float(row[19])  # en millisecondes
                self.break_value = row[20]
                self.turn_regen = int(row[21])
                self.value_regen = float(row[22])  # en pourcent
                self.target_speed = float(row[23]) # en km
                self.turn_ice = int(row[24])
                self.race_delta = float(row[25])
                self.live_delta = float(row[26])
                self.n_1_delta = float(row[27])
                self.target_soc = float(row[28])


        #CONDITIONNEMENT
        # Mode Hybride
        if self.hybride_mode == "False" :
            self.hy_background="white"
            self.hy_police="black"
        else:
            self.hy_background="red"
            self.hy_police="white"
        # Etat ICE Clutch engine
        if self.ice_clutch1 == "True" :
            self.clutch1_background="red"
            self.clutch1_value="ON"
            self.clutch1_contour="red"
        else:
            self.clutch1_background="black"
            self.clutch1_contour="white"
            self.clutch1_value="OFF"
        # Etat ICE Clutch motor
        if self.ice_clutch2 == "True" :
            self.clutch2_background="red"
            self.clutch2_value="ON"
            self.clutch2_contour="red"
        else:
            self.clutch2_background="black"
            self.clutch2_contour="white"
            self.clutch2_value="OFF"
        # Fuel mode
        if self.fuel_mode == "True" :
            self.fuel_mode_value="ON"
            self.fuel_mode_background="red"
            self.fuel_mode_contour="red"
        else:
            self.fuel_mode_value="OFF"
            self.fuel_mode_background="black"
            self.fuel_mode_contour="white"
        # Etat connexion 3g
        if self.connexion == "True" :
            self.etat_connexion_background="#03FF00"
            self.etat_connexion_label="black"
        else:
            self.etat_connexion_background="red"
            self.etat_connexion_label="white"
        # Etat connexion GPS
        if self.gps == "True" :
            self.etat_gps_background="#03FF00"
            self.etat_gps_label="black"
        else:
            self.etat_gps_background="red"
            self.etat_gps_label="white"
        # Etat Breaks
        if self.break_value == "False" :
            self.breaks_background="black"
        else:
            self.breaks_background= "red"
        self.master.after(50, self.update_Datas)


    def FrameDestroy(self):
        for widget in self.master.winfo_children():
            widget.destroy()
