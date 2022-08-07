# @Date:   2021-04-11T17:21:44+02:00
# @Last modified time: 2021-04-11T19:42:20+02:00

from tkinter import *
import os
import math
from includes.chrono import *
from includes.dashboard import *


class Track(Dashboard):
    def __init__(self, master):
        super().__init__(master)
        # self.FrameDestroy()
        self.master.columnconfigure(0, minsize=self.width_screen/6)
        self.master.columnconfigure(1, minsize=self.width_screen/6)
        self.master.columnconfigure(2, minsize=self.width_screen/6)
        self.master.columnconfigure(3, minsize=self.width_screen/6)
        self.master.columnconfigure(4, minsize=self.width_screen/6)
        self.master.columnconfigure(5, minsize=self.width_screen/6)

        self.master.rowconfigure(0, minsize=self.height_screen/4)
        self.master.rowconfigure(1, minsize=self.height_screen/4)
        self.master.rowconfigure(2, minsize=self.height_screen/4)
        self.master.rowconfigure(3, minsize=self.space)
        self.master.rowconfigure(4, minsize=self.height_screen/4-self.space)
        self.update_Frame()
        self.master.mainloop()
        # self.master.bind("<Left>", lambda e: Test(window)) #<Left> pour afficher le menu track


    

    def update_Frame(self):
        self.lap_frame = Frame(self.master, width=self.width_screen/6-self.space, height=self.height_screen/4-self.space)
        self.lap_frame.grid(column=0, row=0)
        self.lap_frame.configure(bg="black", highlightbackground="white", highlightthickness=2)
        self.lap_frame.pack_propagate(0)

        self.lap_label = Label(self.lap_frame, text="LAP")
        self.lap_label.pack()
        self.lap_label.configure(bg=self.lap_frame["bg"], fg="white", font=self.font_titre)

        self.num_lap_label = Label(self.lap_frame, text="8/11")
        self.num_lap_label.pack(expand=True)
        self.num_lap_label.configure(bg=self.lap_frame["bg"], fg="yellow", font=self.font_donnees_track)

        self.SOC_frame = LabelFrame(self.master, width=self.width_screen/6-self.space, height=self.height_screen/4-self.space)
        self.SOC_frame.grid(column=5, row=0)
        self.SOC_frame.configure(bg="black", highlightbackground="white", highlightthickness=2)
        self.SOC_frame.pack_propagate(0)

        self.SOC_label = Label(self.SOC_frame, text="SOC")
        self.SOC_label.pack()
        self.SOC_label.configure(bg=self.SOC_frame["bg"], fg="white", font=self.font_titre)

        self.state_label = Label(self.SOC_frame, text=str(self.soc)+'%')
        self.state_label.pack(expand=True)
        self.state_label.configure(bg=self.SOC_frame["bg"], fg="yellow", font=self.font_donnees_track)

        self.TSOC_frame = Frame(self.master)
        self.TSOC_frame.grid(column=1, row=0, columnspan=4)
        self.TSOC_frame.configure(bg="black")

        self.TSOC_jauge_frame = Frame(self.TSOC_frame, width=4*self.width_screen/6-self.space,
                                      height=self.height_screen/10-self.space)
        self.TSOC_jauge_frame.grid(column=0, row=0)
        self.TSOC_jauge_frame.configure(bg="black", highlightbackground="white", highlightthickness=4)

        if self.soc < self.target_soc:

            self.TSOC_full_jauge_frame = Frame(self.TSOC_jauge_frame,
                                               width=self.soc/100*self.TSOC_jauge_frame["width"],
                                               height=self.height_screen/10-self.space)
            self.TSOC_full_jauge_frame.grid(column=0, row=0)
            self.TSOC_full_jauge_frame.configure(bg="green")

            self.TSOC_empty1_jauge_frame = Frame(self.TSOC_jauge_frame, width=(self.target_soc-self.soc)/100*self.TSOC_jauge_frame["width"],
                                                height=self.height_screen/10-self.space)
            self.TSOC_empty1_jauge_frame.grid(column=1, row=0)
            self.TSOC_empty1_jauge_frame.configure(bg="black")

            self.TSOC_empty2_jauge_frame = Frame(self.TSOC_jauge_frame, width=(100-self.target_soc+1)/100*self.TSOC_jauge_frame[
                                                     "width"],
                                                 height=self.height_screen/10-self.space)
            self.TSOC_empty2_jauge_frame.grid(column=3, row=0)
            self.TSOC_empty2_jauge_frame.configure(bg="black")

            self.TSOC_cursor_jauge_frame = Frame(self.TSOC_jauge_frame,
                                                width=0.01* self.TSOC_jauge_frame["width"],
                                                height=self.height_screen/10-self.space)
            self.TSOC_cursor_jauge_frame.grid(column=2, row=0)
            self.TSOC_cursor_jauge_frame.configure(bg="white")

        elif self.soc > self.target_soc:
            self.TSOC_full1_jauge_frame = Frame(self.TSOC_jauge_frame,
                                               width=self.target_soc/100*self.TSOC_jauge_frame["width"],
                                               height=self.height_screen/10-self.space)
            self.TSOC_full1_jauge_frame.grid(column=0, row=0)
            self.TSOC_full1_jauge_frame.configure(bg="green")

            self.TSOC_full2_jauge_frame = Frame(self.TSOC_jauge_frame,
                                                width=(self.soc-self.target_soc +1)/100*self.TSOC_jauge_frame["width"],
                                                height=self.height_screen/10-self.space)
            self.TSOC_full2_jauge_frame.grid(column=2, row=0)
            self.TSOC_full2_jauge_frame.configure(bg="green")

            self.TSOC_empty_jauge_frame = Frame(self.TSOC_jauge_frame,
                                                 width=(100-self.soc)/100*self.TSOC_jauge_frame[
                                                     "width"],
                                                 height=self.height_screen/10-self.space)
            self.TSOC_empty_jauge_frame.grid(column=3, row=0)
            self.TSOC_empty_jauge_frame.configure(bg="black")


            self.TSOC_cursor_jauge_frame = Frame(self.TSOC_jauge_frame,
                                                 width=0.01*self.TSOC_jauge_frame["width"],
                                                 height=self.height_screen/10-self.space)
            self.TSOC_cursor_jauge_frame.grid(column=1, row=0)
            self.TSOC_cursor_jauge_frame.configure(bg="white")

        elif self.soc == self.target_soc:
            self.TSOC_full_jauge_frame = Frame(self.TSOC_jauge_frame,
                                               width=self.soc/100*self.TSOC_jauge_frame["width"],
                                               height=self.height_screen/10-self.space)
            self.TSOC_full_jauge_frame.grid(column=0, row=0)
            self.TSOC_full_jauge_frame.configure(bg="green")

            self.TSOC_empty_jauge_frame = Frame(self.TSOC_jauge_frame,
                                                 width=(100-self.soc)/100*self.TSOC_jauge_frame[
                                                     "width"],
                                                 height=self.height_screen/10-self.space)
            self.TSOC_empty_jauge_frame.grid(column=1, row=0)
            self.TSOC_empty_jauge_frame.configure(bg="black")



        self.TSOC_num_frame = Frame(self.TSOC_frame)
        self.TSOC_num_frame.grid(column=0, row=1, sticky='w')
        self.TSOC_num_frame.configure(bg="black")

        self.TSOC_title_label = Label(self.TSOC_num_frame, text='TARGET SOC ')
        self.TSOC_title_label.configure(font=self.font_titre, bg='black', fg='white')
        self.TSOC_title_label.grid(column=0, row=0, sticky='s')

        self.TSOC_num_label = Label(self.TSOC_num_frame, text=str(self.target_soc)+'%')
        self.TSOC_num_label.configure(font=self.font_donnees_track, bg='black', fg='yellow')
        self.TSOC_num_label.grid(column=1, row=0)




        self.others_frame = LabelFrame(self.master, text="EMPTY", bd=3, width=self.width_screen/6-self.space,
                                       height=self.height_screen/4-self.space)
        self.others_frame.grid(column=0, row=1)
        self.others_frame.configure(bg="black", fg="white")

        self.deltas_frame = Frame(self.master, width=4*self.width_screen/6-self.space*2, height=self.height_screen/4-self.space)
        self.deltas_frame.grid(column=1, row=1, columnspan=4)
        self.deltas_frame.configure(bg="black", highlightbackground="white", highlightthickness=2)
        self.deltas_frame.grid_propagate(0)

        self.liveD_frame = Frame(self.deltas_frame, width=self.width_screen*2/9-2-2*self.space/3,
                                 height=self.height_screen/4-self.space-4, bg='white')
        self.liveD_frame.grid(column=1, row=0)
        self.liveD_frame.pack_propagate(0)

        self.liveD_label = Label(self.liveD_frame, text='LIVE DELTA')
        self.liveD_label.configure(font=self.font_titre, bg='white', fg='black')
        self.liveD_label.pack()

        self.num_liveD_label = Label(self.liveD_frame, text=str(self.live_delta)+'s')
        self.num_liveD_label.configure(font=self.font_donnees, bg='white', fg='red')
        self.num_liveD_label.pack(expand=True)

        self.raceD_frame = Frame(self.deltas_frame, width=self.width_screen*2/9-2-2*self.space/3,
                                 height=self.height_screen/4-self.space-4, bg='black')
        self.raceD_frame.grid(column=0, row=0)
        self.raceD_frame.pack_propagate(0)

        self.raceD_label = Label(self.raceD_frame, text='RACE DELTA')
        self.raceD_label.configure(font=self.font_titre, bg=self.deltas_frame["bg"], fg='white')
        self.raceD_label.pack()

        self.num_raceD_label = Label(self.raceD_frame, text=str(self.race_delta)+'s')
        self.num_raceD_label.configure(font=self.font_donnees, bg=self.deltas_frame["bg"], fg='green')
        self.num_raceD_label.pack(expand=True)

        self.nD_frame = Frame(self.deltas_frame, width=self.width_screen*2/9-2-2*self.space/3,
                              height=self.height_screen/4-self.space-4, bg='black')
        self.nD_frame.grid(column=2, row=0)
        self.nD_frame.pack_propagate(0)

        self.nD_label = Label(self.nD_frame, text='N-1 DELTA')
        self.nD_label.configure(font=self.font_titre, bg=self.deltas_frame["bg"], fg='white')
        self.nD_label.pack()

        self.nD_label = Label(self.nD_frame, text=str(self.n_1_delta)+'s')
        self.nD_label.configure(font=self.font_donnees, bg=self.deltas_frame["bg"], fg='green')
        self.nD_label.pack(expand=True)

        self.fuel_frame = Frame(self.master, width=self.width_screen/6-self.space, height=self.height_screen/4-self.space)
        self.fuel_frame.grid(column=5, row=1)
        self.fuel_frame.configure(bg="black", highlightbackground="white", highlightthickness=2)
        self.fuel_frame.pack_propagate(0)

        self.fuel_label = Label(self.fuel_frame, text="FUEL")
        self.fuel_label.pack()
        self.fuel_label.configure(bg=self.fuel_frame["bg"], fg="white", font=self.font_titre)

        self.state_label = Label(self.fuel_frame, text="ON")
        self.state_label.pack(expand=True)
        self.state_label.configure(bg=self.fuel_frame["bg"], fg="yellow", font=self.font_donnees_track)

        self.regen_frame = Frame(self.master, width=3*self.width_screen/6-self.space*2, height=self.height_screen/4-self.space)
        self.regen_frame.grid(column=0, row=2, columnspan=3)
        self.regen_frame.configure(bg="black")
        self.regen_frame.grid_propagate(0)

        self.turn_regen_frame = Frame(self.regen_frame, width=self.width_screen/8-self.space,
                                      height=self.height_screen/4-self.space, bg='white')
        self.turn_regen_frame.grid(column=0, row=0)
        self.turn_regen_frame.pack_propagate(0)

        self.turn_regen_label = Label(self.turn_regen_frame, text='TURN')
        self.turn_regen_label.configure(font=self.font_etat_clutch, bg=self.turn_regen_frame["bg"])
        self.turn_regen_label.pack()

        self.num_turn_regen_label = Label(self.turn_regen_frame, text=str(self.turn_regen))
        self.num_turn_regen_label.configure(font=self.font_turn, bg=self.turn_regen_frame["bg"])
        self.num_turn_regen_label.pack(expand=True)

        self.speed_regen_frame = Frame(self.regen_frame, width=3*self.width_screen/8-self.space,
                                       height=self.height_screen/4-self.space, bg=self.regen_frame["bg"])
        self.speed_regen_frame.grid(column=1, row=0)
        self.speed_regen_frame.configure(highlightbackground="white", highlightthickness=2)
        self.speed_regen_frame.pack_propagate(0)

        self.speed_regen_label = Label(self.speed_regen_frame, text='REGEN')
        self.speed_regen_label.configure(font=self.font_titre_ice, bg=self.speed_regen_frame["bg"], fg="white")
        self.speed_regen_label.pack(anchor='nw')

        self.num_speed_regen_label = Label(self.speed_regen_frame, text=str(self.value_regen)+'%')
        self.num_speed_regen_label.configure(font=self.font_donnees_track, bg=self.speed_regen_frame["bg"], fg="yellow")
        self.num_speed_regen_label.pack(expand=True)

        self.ICE_frame = Frame(self.master, width=3*self.width_screen/6-self.space*2, height=self.height_screen/4-self.space,
                               bg='black')
        self.ICE_frame.grid(column=3, row=2, columnspan=3)
        self.ICE_frame.grid_propagate(0)

        self.turn_ICE_frame = Frame(self.ICE_frame, width=self.width_screen/8-self.space, height=self.height_screen/4-self.space,
                                    bg='white')
        self.turn_ICE_frame.grid(column=0, row=0)
        self.turn_ICE_frame.pack_propagate(0)

        self.turn_ICE_label = Label(self.turn_ICE_frame, text='TURN')
        self.turn_ICE_label.configure(font=self.font_etat_clutch, bg=self.turn_ICE_frame["bg"])
        self.turn_ICE_label.pack()

        self.num_turn_ICE_label = Label(self.turn_ICE_frame, text=str(self.turn_ice))
        self.num_turn_ICE_label.configure(font=self.font_turn, bg=self.turn_ICE_frame["bg"])
        self.num_turn_ICE_label.pack(expand=True)

        self.speed_ICE_frame = Frame(self.ICE_frame, width=3*self.width_screen/8-self.space,
                                     height=self.height_screen/4-self.space, bg=self.ICE_frame["bg"])
        self.speed_ICE_frame.grid(column=1, row=0)
        self.speed_ICE_frame.configure(highlightbackground="white", highlightthickness=2)
        self.speed_ICE_frame.grid_propagate(0)
        # self.ICE_frame.columnconfigure(0, minsize=(3*self.width_screen/8-self.space)/2)

        self.speed_ICE_label = Label(self.speed_ICE_frame, text='ICE')
        self.speed_ICE_label.configure(font=self.font_titre_ice, bg=self.speed_ICE_frame["bg"], fg="white")
        self.speed_ICE_label.grid(column=0, row=0)
        self.speed_ICE_frame.columnconfigure(0)

        self.int_speed_ICE_label = Label(self.speed_ICE_frame, text=str(int(self.target_speed)))
        self.int_speed_ICE_label.grid(row=1, column=5, sticky='ns')
        self.int_speed_ICE_label.configure(bg=self.speed_ICE_frame["bg"], fg="yellow", font=self.font_vitesse)
        self.dec_speed_ICE_label = Label(self.speed_ICE_frame,
                                         text="."+str(int(self.target_speed*10 % 10))+" km/h")
        self.dec_speed_ICE_label.grid(row=1, column=6)
        self.dec_speed_ICE_label.configure(bg=self.speed_ICE_frame["bg"], fg="yellow", font=self.font_donnees)

        self.spacer_frame = Frame(self.master, width=self.width_screen, height=2)
        self.spacer_frame.grid(column=0, row=3, columnspan=6)
        self.spacer_frame.configure(bg="white")

        self.breaks_mode_frame = Frame(self.master, width=self.width_screen/6, height=self.height_screen/4-self.space)
        self.breaks_mode_frame.grid(column=0, row=4)
        self.breaks_mode_frame.pack_propagate(0)
        self.breaks_mode_frame.configure(bg="black")

        self.breaks_label = Label(self.breaks_mode_frame, text="BRK")
        self.breaks_label.pack(expand=True)
        self.breaks_label.configure(bg=self.breaks_background, fg="white", font=self.font_etat_clutch)

        self.mode_label = Label(self.breaks_mode_frame, text="HY")
        self.mode_label.pack(anchor="sw", side=BOTTOM)
        self.mode_label.configure(bg=self.hy_background, fg=self.hy_police, font=self.font_hy)

        self.time_frame = Frame(self.master, width=3*self.width_screen/6, height=self.height_screen/4-self.space)
        self.time_frame.grid(column=1, row=4, columnspan=3)
        self.time_frame.configure(bg="black")
        self.time_frame.pack_propagate(0)

        self.time_label = Label(self.time_frame, text="TIME")
        self.time_label.pack(anchor='nw')
        self.time_label.configure(bg=self.time_frame["bg"], fg="white", font=self.font_titre)

        self.num_time_label = Label(self.time_frame, text="00:02:11")
        self.num_time_label.pack(expand=True, anchor='nw')
        self.num_time_label.configure(bg=self.time_frame["bg"], fg="yellow", font=self.font_time)

        self.speed_frame = Frame(self.master, width=2*self.width_screen/6-self.space, height=self.height_screen/4-self.space)
        self.speed_frame.grid(column=4, row=4, columnspan=2)
        self.speed_frame.configure(bg="black")
        self.speed_frame.grid_propagate(0)

        self.speed_label = Label(self.speed_frame, text="SPEED")
        self.speed_label.grid(row=0, column=0)
        self.speed_label.configure(bg=self.speed_frame["bg"], fg="white", font=self.font_titre)

        self.int_speed_label = Label(self.speed_frame, text=str(int(self.speed)))
        self.int_speed_label.grid(row=1, column=0, sticky='ns')
        self.int_speed_label.configure(bg=self.speed_frame["bg"], fg="yellow", font=self.font_vitesse_track)
        self.dec_speed_label = Label(self.speed_frame, text="."+str(int(self.speed*10 % 10))+" km/h")
        self.dec_speed_label.grid(row=1, column=1)
        self.dec_speed_label.configure(bg=self.speed_frame["bg"], fg="yellow", font=self.font_donnees)
        self.master.after(1000, self.update_Frame)

