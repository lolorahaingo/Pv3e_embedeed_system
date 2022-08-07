# @Date:   2021-03-02T15:32:13+01:00
# @Last modified time: 2021-03-22T12:57:59+01:00



from tkinter import *
import os
import math
from includes.chrono import *
import tkinter.font as font

class Test:
    def __init__(self, master):
        self.master = master

        #Variables du menu
        self.engine_rpm=2013 #RPM
        self.engine_torque=2.67 #Nm
        self.engine_temp=84.5 #°C
        self.p_fuel=3.45 #bars
        self.fuel_cons=2.25 #mL
        self.ice_clutch1=False #True si ICE Clutch ON
        self.motor_rpm=0
        self.motor_torque=0
        self.motor_temp=45.6
        self.distance=15.2 #km
        self.efficiency=712 #km/L
        self.ice_clutch2=True #False si ICE Clutch OFF
        self.fuel_mode=True #True si mode FUEL ON
        self.soc=57 #%
        self.lipo=65 #%
        self.connexion=True #True si état de connexion 3g OK
        self.gps=True #True si connexion GPS OK
        self.speed=25 #km/h
        self.hybride_mode=True #False si mode HY pas activé

        #CONDITIONNEMENT

        # Mode Hybride
        if self.hybride_mode==False :
            hy_color="white"
            hy_background="white"
            hy_police="black"
        else:
            hy_color="red"
            hy_background="red"
            hy_police="white"

        # Etat ICE Clutch engine
        if self.ice_clutch1==True :
            clutch1_background="red"
            clutch1_value="ON"
            clutch1_contour="red"
        else:
            clutch1_background="black"
            clutch1_contour="white"
            clutch1_value="OFF"

        # Etat ICE Clutch motor
        if self.ice_clutch2==True :
            clutch2_background="red"
            clutch2_value="ON"
            clutch2_contour="red"
        else:
            clutch2_background="black"
            clutch2_contour="white"
            clutch2_value="OFF"

        # Fuel mode
        if self.fuel_mode == True :
            fuel_mode_value="ON"
            fuel_mode_background="red"
            fuel_mode_contour="red"
        else:
            fuel_mode_value="OFF"
            fuel_mode_background="black"
            fuel_mode_contour="white"

        # Etat connexion 3g
        if self.connexion == True :
            etat_connexion_background="#03FF00"
            etat_connexion_label="black"
        else:
            etat_connexion_background="red"
            etat_connexion_label="white"

        # Etat connexion GPS
        if self.gps == True :
            etat_gps_background="#03FF00"
            etat_gps_label="black"
        else:
            etat_gps_background="red"
            etat_gps_label="white"

        #Fenêtre qui s'adapte à la taille de l'écran
        # width_screen = self.master.winfo_screenwidth()-math.ceil(self.master.winfo_screenwidth()/50) #math.ceil()pour récuupérer la partie entière. On prend une marge entre la résolution de l'écran et la fenêtre de travail.
        width_screen = self.master.winfo_screenwidth()-20 #-20 de highlightthockness=10
        # height_screen = self.master.winfo_screenheight()-math.ceil(self.master.winfo_screenheight()/50)
        height_screen = self.master.winfo_screenheight()-20 #-20 de highlightthockness=10
        space = math.ceil(width_screen/50) #variable qui va espacer les différents cadres
        self.master.geometry(f"{width_screen+space}x{height_screen+space}")
        self.master.title("Menu TEST")
        self.master.configure(bg="black", highlightbackground=hy_background, highlightcolor=hy_background, highlightthickness=10, padx=0, pady=0, borderwidth=0, relief="flat")
        # get current working directory
        cwd = os.getcwd()
        # Add full path of the .ico image
        # self.master.iconbitmap(cwd + "/images/estaca.ico")

        #On définit la taille des différentes font en fonction de la taille de l'écran
        font_titre=("Arial", int(space*0.8),"bold")
        font_titre_donnees=("Arial", int(space*1.5),"bold")
        font_donnees=("Arial", int(space*1.75),"bold")
        font_vitesse=("Arial", int(space*2.5),"bold")
        font_hy=("Arial", int(space*2),"bold")
        font_etat_clutch=("Arial", int(space*1.2),"bold")
        font_titre_signaux=("Arial", int(space*1.2),"bold")

        self.master.rowconfigure(0, minsize=height_screen/8)
        self.master.rowconfigure(1, minsize=height_screen/8)
        self.master.rowconfigure(2, minsize=height_screen/8)
        self.master.rowconfigure(3, minsize=height_screen/8)
        self.master.rowconfigure(4, minsize=height_screen/8)
        self.master.rowconfigure(5, minsize=height_screen/8)
        self.master.rowconfigure(6, minsize=5)
        self.master.rowconfigure(7, minsize=height_screen/8)
        self.master.rowconfigure(8, minsize=height_screen/8-5)

        self.master.columnconfigure(0, minsize=width_screen/8)
        self.master.columnconfigure(1, minsize=width_screen/8)
        self.master.columnconfigure(2, minsize=width_screen/8)
        self.master.columnconfigure(3, minsize=width_screen/8)
        self.master.columnconfigure(4, minsize=width_screen/8)
        self.master.columnconfigure(5, minsize=width_screen/8)
        self.master.columnconfigure(6, minsize=width_screen/8)
        self.master.columnconfigure(7, minsize=width_screen/8)

        self.hybride_mode_frame=Frame(self.master, width=width_screen/8, height=height_screen/8-5)
        self.hybride_mode_frame.grid(column=0,row=8)
        self.hybride_mode_frame.pack_propagate(0)
        self.hybride_mode_frame.configure(bg="black")

        self.hybride_mode_label= Label(self.hybride_mode_frame, text="HY")
        self.hybride_mode_label.pack(anchor="sw", side=BOTTOM)
        self.hybride_mode_label.configure(bg=hy_color, fg=hy_police, font=font_hy)

        #engine RPM

        self.engine_rpm_frame = Frame(self.master, width=width_screen/8-space, height=height_screen/8-space)
        self.engine_rpm_frame.grid(column=0, row=0)
        self.engine_rpm_frame.configure(bg="black")
        self.engine_rpm_frame.pack_propagate(0)

        self.engine_rpm_label=Label(self.engine_rpm_frame,text="Engine")
        self.engine_rpm_label.pack(side=RIGHT)
        self.engine_rpm_label.configure(bg=self.engine_rpm_frame["bg"], fg="white", font=font_titre)

        self.engine_rpm_frame = Frame(self.master, width=width_screen/8-space, height=height_screen/8-space)
        self.engine_rpm_frame.grid(column=1, row=0)
        self.engine_rpm_frame.configure(bg="black")
        self.engine_rpm_frame.pack_propagate(0)

        self.engine_rpm_label=Label(self.engine_rpm_frame,text="RPM")
        self.engine_rpm_label.pack(side=LEFT)
        self.engine_rpm_label.configure(bg=self.engine_rpm_frame["bg"], fg="white", font=font_titre)

        self.engine_rpm_value_frame=Frame(self.master,width=width_screen/8-space, height=height_screen/8-space)
        self.engine_rpm_value_frame.grid(column=2, row=0)
        self.engine_rpm_value_frame.configure(bg="black")
        self.engine_rpm_value_frame.pack_propagate(0)

        self.engine_rpm_value_label=Label(self.engine_rpm_value_frame, text=self.engine_rpm)
        self.engine_rpm_value_label.pack()
        self.engine_rpm_value_label.configure(bg=self.engine_rpm_value_frame["bg"], fg="yellow", font=font_donnees)
        self.rpm_frame=Frame(self.master, width=width_screen/8-space, height=height_screen/8-space)
        self.rpm_frame.grid(column=3, row=0)
        self.rpm_frame.configure(bg="black")
        self.rpm_frame.pack_propagate(0)
        self.rpm_label=Label(self.rpm_frame, text="RPM")
        self.rpm_label.pack(anchor="w", side=LEFT)
        self.rpm_label.configure(bg=self.engine_rpm_value_frame["bg"], fg="yellow", font=font_titre_donnees)

        #engine Torque

        self.engine_torque_frame = Frame(self.master, width=width_screen/8-space, height=height_screen/8-space)
        self.engine_torque_frame.grid(column=0, row=1)
        self.engine_torque_frame.configure(bg="black")
        self.engine_torque_frame.pack_propagate(0)

        self.engine_torque_label=Label(self.engine_torque_frame,text="Engine")
        self.engine_torque_label.pack(side=RIGHT)
        self.engine_torque_label.configure(bg=self.engine_torque_frame["bg"], fg="white", font=font_titre)

        self.engine_torque_frame = Frame(self.master, width=width_screen/8-space, height=height_screen/8-space)
        self.engine_torque_frame.grid(column=1, row=1)
        self.engine_torque_frame.configure(bg="black")
        self.engine_torque_frame.pack_propagate(0)

        self.engine_torque_label=Label(self.engine_torque_frame,text="Torque")
        self.engine_torque_label.pack(side=LEFT)
        self.engine_torque_label.configure(bg=self.engine_torque_frame["bg"], fg="white", font=font_titre)

        self.engine_torque_value_frame=Frame(self.master,width=width_screen/8-space, height=height_screen/8-space)
        self.engine_torque_value_frame.grid(column=2, row=1)
        self.engine_torque_value_frame.configure(bg="black")
        self.engine_torque_value_frame.pack_propagate(0)

        self.engine_torque_value_label=Label(self.engine_torque_value_frame, text=self.engine_torque)
        self.engine_torque_value_label.pack()
        self.engine_torque_value_label.configure(bg=self.engine_torque_value_frame["bg"], fg="yellow", font=font_donnees)
        self.torque_frame=Frame(self.master, width=width_screen/8-space, height=height_screen/8-space)
        self.torque_frame.grid(column=3, row=1)
        self.torque_frame.configure(bg="black")
        self.torque_frame.pack_propagate(0)
        self.torque_label=Label(self.torque_frame, text="Nm")
        self.torque_label.pack(anchor="w", side=LEFT)
        self.torque_label.configure(bg=self.engine_torque_value_frame["bg"], fg="yellow", font=font_titre_donnees)

        #engine Temp

        self.engine_temp_frame = Frame(self.master, width=width_screen/8-space, height=height_screen/8-space)
        self.engine_temp_frame.grid(column=0, row=2)
        self.engine_temp_frame.configure(bg="black")
        self.engine_temp_frame.pack_propagate(0)

        self.engine_temp_label=Label(self.engine_temp_frame,text="Engine")
        self.engine_temp_label.pack(side=RIGHT)
        self.engine_temp_label.configure(bg=self.engine_temp_frame["bg"], fg="white", font=font_titre)

        self.engine_temp_frame = Frame(self.master, width=width_screen/8-space, height=height_screen/8-space)
        self.engine_temp_frame.grid(column=1, row=2)
        self.engine_temp_frame.configure(bg="black")
        self.engine_temp_frame.pack_propagate(0)

        self.engine_temp_label=Label(self.engine_temp_frame,text="Temp.")
        self.engine_temp_label.pack(side=LEFT)
        self.engine_temp_label.configure(bg=self.engine_temp_frame["bg"], fg="white", font=font_titre)

        self.engine_temp_value_frame=Frame(self.master,width=width_screen/8-space, height=height_screen/8-space)
        self.engine_temp_value_frame.grid(column=2, row=2)
        self.engine_temp_value_frame.configure(bg="black")
        self.engine_temp_value_frame.pack_propagate(0)

        self.engine_temp_value_label=Label(self.engine_temp_value_frame, text=self.engine_temp)
        self.engine_temp_value_label.pack()
        self.engine_temp_value_label.configure(bg=self.engine_temp_value_frame["bg"], fg="yellow", font=font_donnees)
        self.temp_frame=Frame(self.master, width=width_screen/8-space, height=height_screen/8-space)
        self.temp_frame.grid(column=3, row=2)
        self.temp_frame.configure(bg="black")
        self.temp_frame.pack_propagate(0)
        self.temp_label=Label(self.temp_frame, text="°C")
        self.temp_label.pack(anchor="w", side=LEFT)
        self.temp_label.configure(bg=self.engine_temp_value_frame["bg"], fg="yellow", font=font_titre_donnees)

        #Pression fuel

        self.p_fuel_frame = Frame(self.master, width=width_screen/8-space, height=height_screen/8-space)
        self.p_fuel_frame.grid(column=0, row=3)
        self.p_fuel_frame.configure(bg="black")
        self.p_fuel_frame.pack_propagate(0)

        self.p_fuel_label=Label(self.p_fuel_frame,text="P Fuel")
        self.p_fuel_label.pack(side=RIGHT)
        self.p_fuel_label.configure(bg=self.p_fuel_frame["bg"], fg="white", font=font_titre)

        self.p_fuel_value_frame=Frame(self.master,width=width_screen/8-space, height=height_screen/8-space)
        self.p_fuel_value_frame.grid(column=2, row=3)
        self.p_fuel_value_frame.configure(bg="black")
        self.p_fuel_value_frame.pack_propagate(0)

        self.p_fuel_value_label=Label(self.p_fuel_value_frame, text=self.p_fuel)
        self.p_fuel_value_label.pack()
        self.p_fuel_value_label.configure(bg=self.p_fuel_value_frame["bg"], fg="yellow", font=font_donnees)
        self.p_fuel_unit_frame=Frame(self.master, width=width_screen/8-space, height=height_screen/8-space)
        self.p_fuel_unit_frame.grid(column=3, row=3)
        self.p_fuel_unit_frame.configure(bg="black")
        self.p_fuel_unit_frame.pack_propagate(0)
        self.p_fuel_unit_label=Label(self.p_fuel_unit_frame, text="bars")
        self.p_fuel_unit_label.pack(anchor="w", side=LEFT)
        self.p_fuel_unit_label.configure(bg=self.p_fuel_unit_frame["bg"], fg="yellow", font=font_titre_donnees)

        #Fuel cons

        self.fuel_cons_frame = Frame(self.master, width=width_screen/8-space, height=height_screen/8-space)
        self.fuel_cons_frame.grid(column=0, row=4)
        self.fuel_cons_frame.configure(bg="black")
        self.fuel_cons_frame.pack_propagate(0)

        self.fuel_cons_label=Label(self.fuel_cons_frame,text="Fuel")
        self.fuel_cons_label.pack(side=RIGHT)
        self.fuel_cons_label.configure(bg=self.fuel_cons_frame["bg"], fg="white", font=font_titre)

        self.fuel_cons_frame = Frame(self.master, width=width_screen/8-space, height=height_screen/8-space)
        self.fuel_cons_frame.grid(column=1, row=4)
        self.fuel_cons_frame.configure(bg="black")
        self.fuel_cons_frame.pack_propagate(0)

        self.fuel_cons_label=Label(self.fuel_cons_frame,text="Cons.")
        self.fuel_cons_label.pack(side=LEFT)
        self.fuel_cons_label.configure(bg=self.fuel_cons_frame["bg"], fg="white", font=font_titre)

        self.fuel_cons_value_frame=Frame(self.master,width=width_screen/8-space, height=height_screen/8-space)
        self.fuel_cons_value_frame.grid(column=2, row=4)
        self.fuel_cons_value_frame.configure(bg="black")
        self.fuel_cons_value_frame.pack_propagate(0)

        self.fuel_cons_value_label=Label(self.fuel_cons_value_frame, text=self.fuel_cons)
        self.fuel_cons_value_label.pack()
        self.fuel_cons_value_label.configure(bg=self.fuel_cons_value_frame["bg"], fg="yellow", font=font_donnees)
        self.fuel_frame=Frame(self.master, width=width_screen/8-space, height=height_screen/8-space)
        self.fuel_frame.grid(column=3, row=4)
        self.fuel_frame.configure(bg="black")
        self.fuel_frame.pack_propagate(0)
        self.fuel_label=Label(self.fuel_frame, text="mL")
        self.fuel_label.pack(anchor="w", side=LEFT)
        self.fuel_label.configure(bg=self.fuel_frame["bg"], fg="yellow", font=font_titre_donnees)

        #ICE Clutch n°1

        self.ice_clutch1_frame = Frame(self.master, width=width_screen/8-space, height=height_screen/8-space)
        self.ice_clutch1_frame.grid(column=0, row=5)
        self.ice_clutch1_frame.configure(bg="black")
        self.ice_clutch1_frame.pack_propagate(0)

        self.ice_clutch1_label=Label(self.ice_clutch1_frame,text="ICE")
        self.ice_clutch1_label.pack(side=RIGHT)
        self.ice_clutch1_label.configure(bg=self.ice_clutch1_frame["bg"], fg="white", font=font_titre)

        self.ice_clutch1_frame = Frame(self.master, width=width_screen/8-space, height=height_screen/8-space)
        self.ice_clutch1_frame.grid(column=1, row=5)
        self.ice_clutch1_frame.configure(bg="black")
        self.ice_clutch1_frame.pack_propagate(0)

        self.ice_clutch1_label=Label(self.ice_clutch1_frame,text="Clutch")
        self.ice_clutch1_label.pack(side=LEFT)
        self.ice_clutch1_label.configure(bg=self.ice_clutch1_frame["bg"], fg="white", font=font_titre)

        self.ice_clutch1_value_frame=Frame(self.master, width=width_screen/8-2*space, height=height_screen/8-space)
        self.ice_clutch1_value_frame.grid(column=2, row=5)
        self.ice_clutch1_value_frame.configure(bg=clutch1_background, highlightbackground=clutch1_contour, highlightthickness=2)
        self.ice_clutch1_value_frame.pack_propagate(0)

        self.ice_clutch1_value_label=Label(self.ice_clutch1_value_frame, text=clutch1_value, pady=100)
        self.ice_clutch1_value_label.pack()
        self.ice_clutch1_value_label.configure(bg=self.ice_clutch1_value_frame["bg"], fg="white", font=font_etat_clutch)

        #RPM Motor

        self.rpm_motor_frame = Frame(self.master, width=width_screen/8-space, height=height_screen/8-space)
        self.rpm_motor_frame.grid(column=4, row=0)
        self.rpm_motor_frame.configure(bg="black")
        self.rpm_motor_frame.pack_propagate(0)

        self.rpm_motor_label=Label(self.rpm_motor_frame,text="RPM")
        self.rpm_motor_label.pack(side=RIGHT)
        self.rpm_motor_label.configure(bg=self.rpm_motor_frame["bg"], fg="white", font=font_titre)

        self.rpm_motor_frame = Frame(self.master, width=width_screen/8-space, height=height_screen/8-space)
        self.rpm_motor_frame.grid(column=5, row=0)
        self.rpm_motor_frame.configure(bg="black")
        self.rpm_motor_frame.pack_propagate(0)

        self.rpm_motor_label=Label(self.rpm_motor_frame,text="Motor")
        self.rpm_motor_label.pack(side=LEFT)
        self.rpm_motor_label.configure(bg=self.rpm_motor_frame["bg"], fg="white", font=font_titre)

        self.rpm_motor_value_frame=Frame(self.master,width=width_screen/8-space, height=height_screen/8-space)
        self.rpm_motor_value_frame.grid(column=6, row=0)
        self.rpm_motor_value_frame.configure(bg="black")
        self.rpm_motor_value_frame.pack_propagate(0)

        self.rpm_motor_value_label=Label(self.rpm_motor_value_frame, text=self.motor_rpm)
        self.rpm_motor_value_label.pack()
        self.rpm_motor_value_label.configure(bg=self.rpm_motor_value_frame["bg"], fg="yellow", font=font_donnees)
        self.rpm_frame=Frame(self.master, width=width_screen/8-space, height=height_screen/8-space)
        self.rpm_frame.grid(column=7, row=0)
        self.rpm_frame.configure(bg="black")
        self.rpm_frame.pack_propagate(0)
        self.rpm_label=Label(self.rpm_frame, text="RPM")
        self.rpm_label.pack(anchor="w", side=LEFT)
        self.rpm_label.configure(bg=self.engine_rpm_value_frame["bg"], fg="yellow", font=font_titre_donnees)


        #Motor Torque

        self.torque_motor_frame = Frame(self.master, width=width_screen/8-space, height=height_screen/8-space)
        self.torque_motor_frame.grid(column=4, row=1)
        self.torque_motor_frame.configure(bg="black")
        self.torque_motor_frame.pack_propagate(0)

        self.torque_motor_label=Label(self.torque_motor_frame,text="Torque")
        self.torque_motor_label.pack(side=RIGHT)
        self.torque_motor_label.configure(bg=self.torque_motor_frame["bg"], fg="white", font=font_titre)

        self.torque_motor_frame = Frame(self.master, width=width_screen/8-space, height=height_screen/8-space)
        self.torque_motor_frame.grid(column=5, row=1)
        self.torque_motor_frame.configure(bg="black")
        self.torque_motor_frame.pack_propagate(0)

        self.torque_motor_label=Label(self.torque_motor_frame,text="motor")
        self.torque_motor_label.pack(side=LEFT)
        self.torque_motor_label.configure(bg=self.torque_motor_frame["bg"], fg="white", font=font_titre)

        self.torque_motor_value_frame=Frame(self.master,width=width_screen/8-space, height=height_screen/8-space)
        self.torque_motor_value_frame.grid(column=6, row=1)
        self.torque_motor_value_frame.configure(bg="black")
        self.torque_motor_value_frame.pack_propagate(0)

        self.torque_motor_value_label=Label(self.torque_motor_value_frame, text=self.motor_torque)
        self.torque_motor_value_label.pack()
        self.torque_motor_value_label.configure(bg=self.torque_motor_value_frame["bg"], fg="yellow", font=font_donnees)
        self.torque_frame=Frame(self.master, width=width_screen/8-space, height=height_screen/8-space)
        self.torque_frame.grid(column=7, row=1)
        self.torque_frame.configure(bg="black")
        self.torque_frame.pack_propagate(0)
        self.torque_label=Label(self.torque_frame, text="Nm")
        self.torque_label.pack(anchor="w", side=LEFT)
        self.torque_label.configure(bg=self.torque_motor_value_frame["bg"], fg="yellow", font=font_titre_donnees)

        #Motor Temp

        self.motor_temp_frame = Frame(self.master, width=width_screen/8-space, height=height_screen/8-space)
        self.motor_temp_frame.grid(column=4, row=2)
        self.motor_temp_frame.configure(bg="black")
        self.motor_temp_frame.pack_propagate(0)

        self.motor_temp_label=Label(self.motor_temp_frame,text="Motor")
        self.motor_temp_label.pack(side=RIGHT)
        self.motor_temp_label.configure(bg=self.motor_temp_frame["bg"], fg="white", font=font_titre)

        self.motor_temp_frame = Frame(self.master, width=width_screen/8-space, height=height_screen/8-space)
        self.motor_temp_frame.grid(column=5, row=2)
        self.motor_temp_frame.configure(bg="black")
        self.motor_temp_frame.pack_propagate(0)

        self.motor_temp_label=Label(self.motor_temp_frame,text="Temp.")
        self.motor_temp_label.pack(side=LEFT)
        self.motor_temp_label.configure(bg=self.motor_temp_frame["bg"], fg="white", font=font_titre)

        self.motor_temp_value_frame=Frame(self.master,width=width_screen/8-space, height=height_screen/8-space)
        self.motor_temp_value_frame.grid(column=6, row=2)
        self.motor_temp_value_frame.configure(bg="black")
        self.motor_temp_value_frame.pack_propagate(0)

        self.motor_temp_value_label=Label(self.motor_temp_value_frame, text=self.motor_temp)
        self.motor_temp_value_label.pack()
        self.motor_temp_value_label.configure(bg=self.motor_temp_value_frame["bg"], fg="yellow", font=font_donnees)
        self.temp_frame=Frame(self.master, width=width_screen/8-space, height=height_screen/8-space)
        self.temp_frame.grid(column=7, row=2)
        self.temp_frame.configure(bg="black")
        self.temp_frame.pack_propagate(0)
        self.temp_label=Label(self.temp_frame, text="°C")
        self.temp_label.pack(anchor="w", side=LEFT)
        self.temp_label.configure(bg=self.motor_temp_value_frame["bg"], fg="yellow", font=font_titre_donnees)

        #Distance

        self.distance_frame = Frame(self.master, width=width_screen/8-space, height=height_screen/8-space)
        self.distance_frame.grid(column=4, row=3)
        self.distance_frame.configure(bg="black")
        self.distance_frame.pack_propagate(0)

        self.distance_label=Label(self.distance_frame,text="Distance")
        self.distance_label.pack(side=RIGHT)
        self.distance_label.configure(bg=self.distance_frame["bg"], fg="white", font=font_titre)

        self.distance_value_frame=Frame(self.master,width=width_screen/8-space, height=height_screen/8-space)
        self.distance_value_frame.grid(column=6, row=3)
        self.distance_value_frame.configure(bg="black")
        self.distance_value_frame.pack_propagate(0)

        self.distance_value_label=Label(self.distance_value_frame, text=self.distance)
        self.distance_value_label.pack()
        self.distance_value_label.configure(bg=self.distance_value_frame["bg"], fg="yellow", font=font_donnees)
        self.distance_unit_frame=Frame(self.master, width=width_screen/8-space, height=height_screen/8-space)
        self.distance_unit_frame.grid(column=7, row=3)
        self.distance_unit_frame.configure(bg="black")
        self.distance_unit_frame.pack_propagate(0)
        self.distance_unit_label=Label(self.distance_unit_frame, text="km")
        self.distance_unit_label.pack(anchor="w", side=LEFT)
        self.distance_unit_label.configure(bg=self.distance_unit_frame["bg"], fg="yellow", font=font_titre_donnees)

        #Efficiency

        self.efficiency_frame = Frame(self.master, width=width_screen/8-space, height=height_screen/8-space)
        self.efficiency_frame.grid(column=4, row=4)
        self.efficiency_frame.configure(bg="black")
        self.efficiency_frame.pack_propagate(0)

        self.efficiency_label=Label(self.efficiency_frame,text="Efficiency")
        self.efficiency_label.pack(side=RIGHT)
        self.efficiency_label.configure(bg=self.efficiency_frame["bg"], fg="white", font=font_titre)

        self.efficiency_value_frame=Frame(self.master,width=width_screen/8-space, height=height_screen/8-space)
        self.efficiency_value_frame.grid(column=6, row=4)
        self.efficiency_value_frame.configure(bg="black")
        self.efficiency_value_frame.pack_propagate(0)

        self.efficiency_value_label=Label(self.efficiency_value_frame, text=self.efficiency)
        self.efficiency_value_label.pack()
        self.efficiency_value_label.configure(bg=self.efficiency_value_frame["bg"], fg="yellow", font=font_donnees)
        self.efficiency_unit_frame=Frame(self.master, width=width_screen/8-space, height=height_screen/8-space)
        self.efficiency_unit_frame.grid(column=7, row=4)
        self.efficiency_unit_frame.configure(bg="black")
        self.efficiency_unit_frame.pack_propagate(0)
        self.efficiency_unit_label=Label(self.efficiency_unit_frame, text="km/L")
        self.efficiency_unit_label.pack(anchor="w", side=LEFT)
        self.efficiency_unit_label.configure(bg=self.efficiency_unit_frame["bg"], fg="yellow", font=font_titre_donnees)

        #ICE Clutch n°2

        self.ice_clutch2_frame = Frame(self.master, width=width_screen/8-space, height=height_screen/8-space)
        self.ice_clutch2_frame.grid(column=4, row=5)
        self.ice_clutch2_frame.configure(bg="black")
        self.ice_clutch2_frame.pack_propagate(0)

        self.ice_clutch2_label=Label(self.ice_clutch2_frame,text="ICE")
        self.ice_clutch2_label.pack(side=RIGHT)
        self.ice_clutch2_label.configure(bg=self.ice_clutch2_frame["bg"], fg="white", font=font_titre)

        self.ice_clutch2_frame = Frame(self.master, width=width_screen/8-space, height=height_screen/8-space)
        self.ice_clutch2_frame.grid(column=5, row=5)
        self.ice_clutch2_frame.configure(bg="black")
        self.ice_clutch2_frame.pack_propagate(0)

        self.ice_clutch2_label=Label(self.ice_clutch2_frame,text="Clutch")
        self.ice_clutch2_label.pack(side=LEFT)
        self.ice_clutch2_label.configure(bg=self.ice_clutch2_frame["bg"], fg="white", font=font_titre)

        self.ice_clutch2_value_frame=Frame(self.master, width=width_screen/8-2*space, height=height_screen/8-space)
        self.ice_clutch2_value_frame.grid(column=6, row=5)
        self.ice_clutch2_value_frame.configure(bg=clutch2_background,highlightbackground=clutch2_contour, highlightthickness=2)
        self.ice_clutch2_value_frame.pack_propagate(0)

        self.ice_clutch2_value_label=Label(self.ice_clutch2_value_frame, text=clutch2_value, pady=100)
        self.ice_clutch2_value_label.pack()
        self.ice_clutch2_value_label.configure(bg=self.ice_clutch2_value_frame["bg"], fg="white", font=font_etat_clutch)

        #Spacer ligne blanche

        self.spacer_frame = Frame(self.master, width=width_screen, height=5)
        self.spacer_frame.grid(column=0, row=6, columnspan=8)
        self.spacer_frame.configure(bg=hy_color)

        #Fuel mode

        self.fuel_mode_frame = Frame(self.master, width=width_screen/8-space, height=height_screen/5-space)
        self.fuel_mode_frame.grid(column=1, row=7, rowspan=8)
        self.fuel_mode_frame.configure(bg=fuel_mode_background,highlightbackground=fuel_mode_contour, highlightthickness=2)
        self.fuel_mode_frame.pack_propagate(0)

        self.fuel_label=Label(self.fuel_mode_frame, text="FUEL")
        self.fuel_label.pack()
        self.fuel_label.configure(bg=self.fuel_mode_frame["bg"], fg="white", font=font_titre_signaux)

        self.fuel_mode_label=Label(self.fuel_mode_frame, text=fuel_mode_value)
        self.fuel_mode_label.pack(expand=True)
        self.fuel_mode_label.configure(bg=self.fuel_mode_frame["bg"], fg="yellow", font=font_donnees)

        # SOC

        self.soc_frame = Frame(self.master, width=width_screen/8-space, height=height_screen/5-space)
        self.soc_frame.grid(column=2, row=7, rowspan=8)
        self.soc_frame.configure(bg="black", highlightbackground="white", highlightthickness=2)
        self.soc_frame.pack_propagate(0)

        self.soc_label=Label(self.soc_frame, text="SOC")
        self.soc_label.pack()
        self.soc_label.configure(bg=self.soc_frame["bg"],fg="white", font=font_titre_signaux)

        self.soc_value_label=Label(self.soc_frame, text="%s %s" % (self.soc,"%"))
        self.soc_value_label.pack(expand=True)
        self.soc_value_label.configure(bg=self.soc_frame["bg"], fg="yellow", font=font_titre_donnees)

        #LIPO

        self.lipo_frame = Frame(self.master, width=width_screen/8-space, height=height_screen/5-space)
        self.lipo_frame.grid(column=3, row=7, rowspan=8)
        self.lipo_frame.configure(bg="black", highlightbackground="white", highlightthickness=2)
        self.lipo_frame.pack_propagate(0)

        self.lipo_label=Label(self.lipo_frame, text="LIPO")
        self.lipo_label.pack()
        self.lipo_label.configure(bg=self.lipo_frame["bg"],fg="white", font=font_titre_signaux)

        self.lipo_value_label=Label(self.lipo_frame, text="%s %s" % (self.lipo,"%"))
        self.lipo_value_label.pack(expand=True)
        self.lipo_value_label.configure(bg=self.lipo_frame["bg"], fg="yellow", font=font_titre_donnees)

        #3G

        self.connexion_frame = Frame(self.master, width=width_screen/8-space, height=height_screen/8-space)
        self.connexion_frame.grid(column=5, row=7)
        self.connexion_frame.configure(bg=etat_connexion_background)
        self.connexion_frame.pack_propagate(0)

        self.connexion_label=Label(self.connexion_frame, text="3G")
        self.connexion_label.pack(pady=0.5*space)
        self.connexion_label.configure(bg=self.connexion_frame["bg"],fg=etat_connexion_label, font=font_titre_donnees)

        #GPS

        self.gps_frame = Frame(self.master, width=width_screen/8-space, height=height_screen/8-space)
        self.gps_frame.grid(column=5, row=8)
        self.gps_frame.configure(bg=etat_gps_background)
        self.gps_frame.pack_propagate(0)

        self.gps_label=Label(self.gps_frame, text="GPS")
        self.gps_label.pack(pady=0.5*space)
        self.gps_label.configure(bg=self.gps_frame["bg"],fg=etat_gps_label, font=font_titre_donnees)

        #Speed

        self.speed_frame=Frame(self.master, width=width_screen/8-space, height=height_screen/8-space)
        self.speed_frame.grid(column=6, row=7)
        self.speed_frame.configure(bg="black")
        self.speed_frame.pack_propagate(0)

        self.speed_label=Label(self.speed_frame, text="SPEED")
        self.speed_label.pack(anchor=NW, side=LEFT)
        self.speed_label.configure(bg=self.speed_frame["bg"],fg="white",font=font_titre)

        self.speed_value_frame=Frame(self.master, width=width_screen/8-space, height=height_screen/8-space)
        self.speed_value_frame.grid(column=6, row=8)
        self.speed_value_frame.configure(bg="black")
        self.speed_value_frame.pack_propagate(0)

        self.speed_value_label=Label(self.speed_value_frame, text=self.speed)
        self.speed_value_label.pack(expand=True, anchor=E)
        self.speed_value_label.configure(bg=self.speed_value_frame["bg"],fg="yellow", font=font_vitesse)

        self.speed_unit_frame=Frame(self.master, width=width_screen/8-space, height=height_screen/8-space)
        self.speed_unit_frame.grid(column=7, row=8)
        self.speed_unit_frame.configure(bg="black")
        self.speed_unit_frame.pack_propagate(0)

        self.speed_unit_label=Label(self.speed_unit_frame, text="km/h")
        self.speed_unit_label.pack(expand=True, anchor=W)
        self.speed_unit_label.configure(bg=self.speed_unit_frame["bg"],fg="yellow", font=font_titre_donnees)
