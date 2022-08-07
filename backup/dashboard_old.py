# @Date:   2020-10-15T19:31:27+02:00
# @Last modified time: 2020-12-26T18:42:03+01:00

from tkinter import *
import os
from includes.gaugelib import *
from includes.chrono import *


class Dashboard:
    def __init__(self, master):
        self.master = master

        # set windows dimensions adapted to the screen
        width_screen = self.master.winfo_screenwidth()
        height_screen = self.master.winfo_screenheight()
        self.master.geometry(f"{width_screen - 150}x{height_screen - 150}")
        self.master.title("Interface Pilote")
        # get current working directory
        cwd = os.getcwd()
        # Add full path of the .ico image
        self.master.iconbitmap(cwd + "/images/estaca.ico")

        # DONNEES MOTEUR
        # - Signal fuel ON (contact voiture)
        # - Température moteur
        # - Temps ouverture injecteur
        # - Pression du carburant
        # - Rotation par minute

        self.motor_frame = LabelFrame(self.master, text="DONNÉES MOTEUR", padx=5, pady=5)
        self.motor_frame.pack(side=LEFT, anchor=NW)

        fuel_on = Label(self.motor_frame, text="Signal fuel ON")
        fuel_on.grid(column=0, row=0)
        motor_temp = Label(self.motor_frame, text="Température moteur")
        motor_temp.grid(column=0, row=3)
        injection_op_time = Label(self.motor_frame, text="Temps ouverture injecteur")
        injection_op_time.grid(column=0, row=4)
        fuel_pressure = Label(self.motor_frame, text="Pression carburant")
        fuel_pressure.grid(column=0, row=2)
        rpm = Label(self.motor_frame, text="Rotation par minute")
        rpm.grid(column=0, row=1)

        # TEMPS
        # - temps par tour
        # - chronometre depuis le debut du tour

        self.time_frame = LabelFrame(self.master, text="TEMPS", padx=5, pady=5)
        self.time_frame.pack(side=TOP, anchor=E)

        time_round = Label(self.time_frame, text="Temps par tour")
        time_round.grid(column=0, row=0)
        chrono_round = Label(self.time_frame, text="Chrono depuis le début du tour")
        chrono_round.grid(column=1, row=0)

        # VITESSES
        # - Vitesse instantanée
        # - Vitesse moyenne tour actuel
        # - Vitesse moyenne tour précédent

        self.speed_frame = LabelFrame(self.master, text="VITESSES", padx=5, pady=5)
        self.speed_frame.place(relx=.5, rely=.5, anchor=CENTER)

        speed_round = Label(self.speed_frame, text="Vitesse moyenne tour actuel")
        speed_round.grid(column=0, row=0)
        speed = Label(self.speed_frame, text="Vitesse instantanée")
        speed.grid(column=0, row=1)
        speed_last_round = Label(self.speed_frame, text="Vitesse moyenne tour précédent")
        speed_last_round.grid(column=0, row=2)

        # AUTRES
        # - Tension de la batterie
        # - Données de la sonde lambda

        self.others_frame = LabelFrame(self.master, text="AUTRES", padx=5, pady=5)
        self.others_frame.pack(side=RIGHT, anchor=S)

        battery_tension = Label(self.others_frame, text="Tension de la batterie")
        battery_tension.grid(column=0, row=0)
        lambda_sens = Label(self.others_frame, text="Données de la sonde lambda")
        lambda_sens.grid(column=1, row=0)



    def draw_gauge(self):
        speed = DrawGauge2(
            self.speed_frame,
            max_value=50,
            min_value=0,
            size=200,
            bg_col='black',
            unit="Vitesse km/h", bg_sel=2)
        speed.grid(column=0, row=2)
        speed.set_value(30)

        rpm = DrawGauge2(
            self.motor_frame,
            max_value=5000.0,
            min_value=0,
            size=200,
            bg_col='black',
            unit="tour/min", bg_sel=2)
        rpm.grid(column=0, row=2)

    def draw_chrono(self):
        chrono = Chrono(self.time_frame)
        chrono.grid(column=2, row=0)
