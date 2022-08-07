# @Date:   2020-12-26T18:43:20+01:00
# @Last modified time: 2021-03-22T14:05:33+01:00

from tkinter import *
import os
from includes.chrono import *
import tkinter.font as font


class Dashboard:
    def __init__(self, master):
        self.master = master

        # set windows dimensions adapted to the screen
        width_screen = self.master.winfo_screenwidth()-20
        height_screen = self.master.winfo_screenheight()-20
        space = width_screen/40
        self.master.geometry(f"{width_screen}x{height_screen}")
        self.master.title("Interface Pilote")
        self.master.configure(bg="black", highlightbackground="red", highlightcolor="red", highlightthickness=10,
                              padx=0, pady=0, borderwidth=0, relief="flat")
        # get current working directory
        cwd = os.getcwd()
        # Add full path of the .ico image
        self.master.iconbitmap(cwd+"/images/estaca.ico")

        self.speed = 10.5
        self.time = 25320  # en millisecondes
        self.break_value = False
        self.turn_regen = 8
        self.value_regen = 95  # en pourcent
        self.target_speed = 34.5  # en km
        self.turn_ice = 2
        self.fuel = True
        self.mode = True  # True en mode hybride
        self.value_soc = 80  # en pourcent
        self.race_delta = -18.5
        self.live_delta = 2.5
        self.n_1_delta = -3.8
        self.target_soc = 85

        # Etat Breaks
        if self.break_value == False :
            breaks_background="black"
        else:
            breaks_background= "red"


        self.master.columnconfigure(0, minsize=width_screen/6)
        self.master.columnconfigure(1, minsize=width_screen/6)
        self.master.columnconfigure(2, minsize=width_screen/6)
        self.master.columnconfigure(3, minsize=width_screen/6)
        self.master.columnconfigure(4, minsize=width_screen/6)
        self.master.columnconfigure(5, minsize=width_screen/6)

        self.master.rowconfigure(0, minsize=height_screen/4)
        self.master.rowconfigure(1, minsize=height_screen/4)
        self.master.rowconfigure(2, minsize=height_screen/4)
        self.master.rowconfigure(3, minsize=space)
        self.master.rowconfigure(4, minsize=height_screen/4-space)

        self.lap_frame = Frame(self.master, width=width_screen/6-space, height=height_screen/4-space)
        self.lap_frame.grid(column=0, row=0)
        self.lap_frame.configure(bg="black", highlightbackground="white", highlightthickness=2)
        self.lap_frame.pack_propagate(0)

        self.lap_label = Label(self.lap_frame, text="LAP")
        self.lap_label.pack()
        self.lap_label.configure(bg=self.lap_frame["bg"], fg="white", font=("Arial 26 bold"))

        self.num_lap_label = Label(self.lap_frame, text="8/11")
        self.num_lap_label.pack(expand=True)
        self.num_lap_label.configure(bg=self.lap_frame["bg"], fg="yellow", font=("Arial 50 bold"))

        self.SOC_frame = LabelFrame(self.master, width=width_screen/6-space, height=height_screen/4-space)
        self.SOC_frame.grid(column=5, row=0)
        self.SOC_frame.configure(bg="black", highlightbackground="white", highlightthickness=2)
        self.SOC_frame.pack_propagate(0)

        self.SOC_label = Label(self.SOC_frame, text="SOC")
        self.SOC_label.pack()
        self.SOC_label.configure(bg=self.SOC_frame["bg"], fg="white", font=("Arial 25 bold"))

        self.state_label = Label(self.SOC_frame, text=str(self.value_soc)+'%')
        self.state_label.pack(expand=True)
        self.state_label.configure(bg=self.SOC_frame["bg"], fg="yellow", font=("Arial 50 bold"))

        self.TSOC_frame = Frame(self.master)
        self.TSOC_frame.grid(column=1, row=0, columnspan=4)
        self.TSOC_frame.configure(bg="black")

        self.TSOC_jauge_frame = Frame(self.TSOC_frame, width=4*width_screen/6-space,
                                      height=height_screen/10-space)
        self.TSOC_jauge_frame.grid(column=0, row=0)
        self.TSOC_jauge_frame.configure(bg="black", highlightbackground="white", highlightthickness=4)

        if self.value_soc < self.target_soc:

            self.TSOC_full_jauge_frame = Frame(self.TSOC_jauge_frame,
                                               width=self.value_soc/100*self.TSOC_jauge_frame["width"],
                                               height=height_screen/10-space)
            self.TSOC_full_jauge_frame.grid(column=0, row=0)
            self.TSOC_full_jauge_frame.configure(bg="green")

            self.TSOC_empty1_jauge_frame = Frame(self.TSOC_jauge_frame, width=(self.target_soc-self.value_soc)/100*self.TSOC_jauge_frame["width"],
                                                height=height_screen/10-space)
            self.TSOC_empty1_jauge_frame.grid(column=1, row=0)
            self.TSOC_empty1_jauge_frame.configure(bg="black")

            self.TSOC_empty2_jauge_frame = Frame(self.TSOC_jauge_frame, width=(100-self.target_soc+1)/100*self.TSOC_jauge_frame[
                                                     "width"],
                                                 height=height_screen/10-space)
            self.TSOC_empty2_jauge_frame.grid(column=3, row=0)
            self.TSOC_empty2_jauge_frame.configure(bg="black")

            self.TSOC_cursor_jauge_frame = Frame(self.TSOC_jauge_frame,
                                                width=0.01* self.TSOC_jauge_frame["width"],
                                                height=height_screen/10-space)
            self.TSOC_cursor_jauge_frame.grid(column=2, row=0)
            self.TSOC_cursor_jauge_frame.configure(bg="white")

        elif self.value_soc > self.target_soc:
            self.TSOC_full1_jauge_frame = Frame(self.TSOC_jauge_frame,
                                               width=self.target_soc/100*self.TSOC_jauge_frame["width"],
                                               height=height_screen/10-space)
            self.TSOC_full1_jauge_frame.grid(column=0, row=0)
            self.TSOC_full1_jauge_frame.configure(bg="green")

            self.TSOC_full2_jauge_frame = Frame(self.TSOC_jauge_frame,
                                                width=(self.value_soc-self.target_soc +1)/100*self.TSOC_jauge_frame["width"],
                                                height=height_screen/10-space)
            self.TSOC_full2_jauge_frame.grid(column=2, row=0)
            self.TSOC_full2_jauge_frame.configure(bg="green")

            self.TSOC_empty_jauge_frame = Frame(self.TSOC_jauge_frame,
                                                 width=(100-self.value_soc)/100*self.TSOC_jauge_frame[
                                                     "width"],
                                                 height=height_screen/10-space)
            self.TSOC_empty_jauge_frame.grid(column=3, row=0)
            self.TSOC_empty_jauge_frame.configure(bg="black")


            self.TSOC_cursor_jauge_frame = Frame(self.TSOC_jauge_frame,
                                                 width=0.01*self.TSOC_jauge_frame["width"],
                                                 height=height_screen/10-space)
            self.TSOC_cursor_jauge_frame.grid(column=1, row=0)
            self.TSOC_cursor_jauge_frame.configure(bg="white")

        elif self.value_soc == self.target_soc:
            self.TSOC_full_jauge_frame = Frame(self.TSOC_jauge_frame,
                                               width=self.value_soc/100*self.TSOC_jauge_frame["width"],
                                               height=height_screen/10-space)
            self.TSOC_full_jauge_frame.grid(column=0, row=0)
            self.TSOC_full_jauge_frame.configure(bg="green")

            self.TSOC_empty_jauge_frame = Frame(self.TSOC_jauge_frame,
                                                 width=(100-self.value_soc)/100*self.TSOC_jauge_frame[
                                                     "width"],
                                                 height=height_screen/10-space)
            self.TSOC_empty_jauge_frame.grid(column=1, row=0)
            self.TSOC_empty_jauge_frame.configure(bg="black")



        self.TSOC_num_frame = Frame(self.TSOC_frame)
        self.TSOC_num_frame.grid(column=0, row=1, sticky='w')
        self.TSOC_num_frame.configure(bg="black")

        self.TSOC_title_label = Label(self.TSOC_num_frame, text='TARGET SOC ')
        self.TSOC_title_label.configure(font=("Arial 30 bold"), bg='black', fg='white')
        self.TSOC_title_label.grid(column=0, row=0, sticky='s')

        self.TSOC_num_label = Label(self.TSOC_num_frame, text=str(self.target_soc)+'%')
        self.TSOC_num_label.configure(font=("Arial 50 bold"), bg='black', fg='yellow')
        self.TSOC_num_label.grid(column=1, row=0)




        self.others_frame = LabelFrame(self.master, text="EMPTY", bd=3, width=width_screen/6-space,
                                       height=height_screen/4-space)
        self.others_frame.grid(column=0, row=1)
        self.others_frame.configure(bg="black", fg="white")

        self.deltas_frame = Frame(self.master, width=4*width_screen/6-space*2, height=height_screen/4-space)
        self.deltas_frame.grid(column=1, row=1, columnspan=4)
        self.deltas_frame.configure(bg="black", highlightbackground="white", highlightthickness=2)
        self.deltas_frame.grid_propagate(0)

        self.liveD_frame = Frame(self.deltas_frame, width=width_screen*2/9-2-2*space/3,
                                 height=height_screen/4-space-4, bg='white')
        self.liveD_frame.grid(column=1, row=0)
        self.liveD_frame.pack_propagate(0)

        self.liveD_label = Label(self.liveD_frame, text='LIVE DELTA')
        self.liveD_label.configure(font=("Arial 25 bold"), bg='white', fg='black')
        self.liveD_label.pack()

        self.num_liveD_label = Label(self.liveD_frame, text=str(self.live_delta)+'s')
        self.num_liveD_label.configure(font=("Arial 40 bold"), bg='white', fg='red')
        self.num_liveD_label.pack(expand=True)

        self.raceD_frame = Frame(self.deltas_frame, width=width_screen*2/9-2-2*space/3,
                                 height=height_screen/4-space-4, bg='black')
        self.raceD_frame.grid(column=0, row=0)
        self.raceD_frame.pack_propagate(0)

        self.raceD_label = Label(self.raceD_frame, text='RACE DELTA')
        self.raceD_label.configure(font=("Arial 25 bold"), bg=self.deltas_frame["bg"], fg='white')
        self.raceD_label.pack()

        self.num_raceD_label = Label(self.raceD_frame, text=str(self.race_delta)+'s')
        self.num_raceD_label.configure(font=("Arial 40 bold"), bg=self.deltas_frame["bg"], fg='green')
        self.num_raceD_label.pack(expand=True)

        self.nD_frame = Frame(self.deltas_frame, width=width_screen*2/9-2-2*space/3,
                              height=height_screen/4-space-4, bg='black')
        self.nD_frame.grid(column=2, row=0)
        self.nD_frame.pack_propagate(0)

        self.nD_label = Label(self.nD_frame, text='N-1 DELTA')
        self.nD_label.configure(font=("Arial 25 bold"), bg=self.deltas_frame["bg"], fg='white')
        self.nD_label.pack()

        self.nD_label = Label(self.nD_frame, text=str(self.n_1_delta)+'s')
        self.nD_label.configure(font=("Arial 40 bold"), bg=self.deltas_frame["bg"], fg='green')
        self.nD_label.pack(expand=True)

        self.fuel_frame = Frame(self.master, width=width_screen/6-space, height=height_screen/4-space)
        self.fuel_frame.grid(column=5, row=1)
        self.fuel_frame.configure(bg="black", highlightbackground="white", highlightthickness=2)
        self.fuel_frame.pack_propagate(0)

        self.fuel_label = Label(self.fuel_frame, text="FUEL")
        self.fuel_label.pack()
        self.fuel_label.configure(bg=self.fuel_frame["bg"], fg="white", font=("Arial 25 bold"))

        self.state_label = Label(self.fuel_frame, text="ON")
        self.state_label.pack(expand=True)
        self.state_label.configure(bg=self.fuel_frame["bg"], fg="yellow", font=("Arial 50 bold"))

        self.regen_frame = Frame(self.master, width=3*width_screen/6-space*2, height=height_screen/4-space)
        self.regen_frame.grid(column=0, row=2, columnspan=3)
        self.regen_frame.configure(bg="black")
        self.regen_frame.grid_propagate(0)

        self.turn_regen_frame = Frame(self.regen_frame, width=width_screen/8-space,
                                      height=height_screen/4-space, bg='white')
        self.turn_regen_frame.grid(column=0, row=0)
        self.turn_regen_frame.pack_propagate(0)

        self.turn_regen_label = Label(self.turn_regen_frame, text='TURN')
        self.turn_regen_label.configure(font=("Arial 35 bold"), bg=self.turn_regen_frame["bg"])
        self.turn_regen_label.pack()

        self.num_turn_regen_label = Label(self.turn_regen_frame, text=str(self.turn_regen))
        self.num_turn_regen_label.configure(font=("Arial 80 bold"), bg=self.turn_regen_frame["bg"])
        self.num_turn_regen_label.pack(expand=True)

        self.speed_regen_frame = Frame(self.regen_frame, width=3*width_screen/8-space,
                                       height=height_screen/4-space, bg=self.regen_frame["bg"])
        self.speed_regen_frame.grid(column=1, row=0)
        self.speed_regen_frame.configure(highlightbackground="white", highlightthickness=2)
        self.speed_regen_frame.pack_propagate(0)

        self.speed_regen_label = Label(self.speed_regen_frame, text='REGEN')
        self.speed_regen_label.configure(font=("Arial 30 bold"), bg=self.speed_regen_frame["bg"], fg="white")
        self.speed_regen_label.pack(anchor='nw')

        self.num_speed_regen_label = Label(self.speed_regen_frame, text=str(self.value_regen)+'%')
        self.num_speed_regen_label.configure(font=("Arial 50 bold"), bg=self.speed_regen_frame["bg"], fg="yellow")
        self.num_speed_regen_label.pack(expand=True)

        self.ICE_frame = Frame(self.master, width=3*width_screen/6-space*2, height=height_screen/4-space,
                               bg='black')
        self.ICE_frame.grid(column=3, row=2, columnspan=3)
        self.ICE_frame.grid_propagate(0)
        # self.ICE_frame.rowconfigure(0, minsize=height_screen/4-30)

        self.turn_ICE_frame = Frame(self.ICE_frame, width=width_screen/8-space, height=height_screen/4-space,
                                    bg='white')
        self.turn_ICE_frame.grid(column=0, row=0)
        self.turn_ICE_frame.pack_propagate(0)

        self.turn_ICE_label = Label(self.turn_ICE_frame, text='TURN')
        self.turn_ICE_label.configure(font=("Arial 35 bold"), bg=self.turn_ICE_frame["bg"])
        self.turn_ICE_label.pack()

        self.num_turn_ICE_label = Label(self.turn_ICE_frame, text=str(self.turn_ice))
        self.num_turn_ICE_label.configure(font=("Arial 80 bold"), bg=self.turn_ICE_frame["bg"])
        self.num_turn_ICE_label.pack(expand=True)

        self.speed_ICE_frame = Frame(self.ICE_frame, width=3*width_screen/8-space,
                                     height=height_screen/4-space, bg=self.ICE_frame["bg"])
        self.speed_ICE_frame.grid(column=1, row=0)
        self.speed_ICE_frame.configure(highlightbackground="white", highlightthickness=2)
        self.speed_ICE_frame.grid_propagate(0)
        # self.ICE_frame.columnconfigure(0, minsize=(3*width_screen/8-space)/2)

        self.speed_ICE_label = Label(self.speed_ICE_frame, text='ICE')
        self.speed_ICE_label.configure(font=("Arial 30 bold"), bg=self.speed_ICE_frame["bg"], fg="white")
        self.speed_ICE_label.grid(column=0, row=0)
        self.speed_ICE_frame.columnconfigure(0)

        self.int_speed_ICE_label = Label(self.speed_ICE_frame, text=str(int(self.target_speed)))
        self.int_speed_ICE_label.grid(row=1, column=5, sticky='ns')
        self.int_speed_ICE_label.configure(bg=self.speed_ICE_frame["bg"], fg="yellow", font=("Arial 50 bold"))
        self.dec_speed_ICE_label = Label(self.speed_ICE_frame,
                                         text="."+str(int(self.target_speed*10 % 10))+" km/h")
        self.dec_speed_ICE_label.grid(row=1, column=6)
        self.dec_speed_ICE_label.configure(bg=self.speed_ICE_frame["bg"], fg="yellow", font=("Arial 25 bold"))

        self.spacer_frame = Frame(self.master, width=width_screen, height=2)
        self.spacer_frame.grid(column=0, row=3, columnspan=6)
        self.spacer_frame.configure(bg="white")

        self.breaks_mode_frame = Frame(self.master, width=width_screen/6, height=height_screen/4-2-space)
        self.breaks_mode_frame.grid(column=0, row=4)
        self.breaks_mode_frame.pack_propagate(0)
        self.breaks_mode_frame.configure(bg="black")

        self.breaks_label = Label(self.breaks_mode_frame, text="BRK")
        self.breaks_label.pack(expand=True)
        self.breaks_label.configure(bg=breaks_background, fg="white", font=("Arial 30 bold"))

        self.mode_label = Label(self.breaks_mode_frame, text="HY")
        self.mode_label.pack(anchor="sw", side=BOTTOM)
        self.mode_label.configure(bg="red", fg="white", font=("Arial 45 bold"))

        self.time_frame = Frame(self.master, width=3*width_screen/6, height=height_screen/4-2-space)
        self.time_frame.grid(column=1, row=4, columnspan=3)
        self.time_frame.configure(bg="black")
        self.time_frame.pack_propagate(0)

        self.time_label = Label(self.time_frame, text="TIME")
        self.time_label.pack(anchor='nw')
        self.time_label.configure(bg=self.time_frame["bg"], fg="white", font=("Arial 25 bold"))

        self.num_time_label = Label(self.time_frame, text="00:02:11")
        self.num_time_label.pack(expand=True, anchor='nw')
        self.num_time_label.configure(bg=self.time_frame["bg"], fg="yellow", font=("Arial 90 bold"))

        self.speed_frame = Frame(self.master, width=2*width_screen/6, height=height_screen/4-2-space)
        self.speed_frame.grid(column=4, row=4, columnspan=2)
        self.speed_frame.configure(bg="black")
        self.speed_frame.grid_propagate(0)

        self.speed_label = Label(self.speed_frame, text="SPEED")
        self.speed_label.grid(row=0, column=0)
        self.speed_label.configure(bg=self.speed_frame["bg"], fg="white", font=("Arial 25 bold"))

        # self.num_speed_frame = Frame(self.speed_frame)
        # self.num_speed_frame.pack(expand=True, anchor='nw')
        # self.num_speed_frame.configure(bg=self.speed_frame["bg"])
        # self.num_speed_frame.pack_propagate(0)
        self.int_speed_label = Label(self.speed_frame, text=str(int(self.speed)))
        self.int_speed_label.grid(row=1, column=0, sticky='ns')
        self.int_speed_label.configure(bg=self.speed_frame["bg"], fg="yellow", font=("Arial 70 bold"))
        self.dec_speed_label = Label(self.speed_frame, text="."+str(int(self.speed*10 % 10))+" km/h")
        self.dec_speed_label.grid(row=1, column=1, sticky='s')
        self.dec_speed_label.configure(bg=self.speed_frame["bg"], fg="yellow", font=("Arial 35 bold"))
