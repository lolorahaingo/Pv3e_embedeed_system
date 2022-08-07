# @Date:   2020-11-04T22:19:22+01:00
# @Last modified time: 2021-03-24T13:56:14+01:00


from tkinter import *
import tkinter as tk
import time


class Chrono(LabelFrame):  # use Frame if we dont need LabelFrame
    def __init__(self, master):
        LabelFrame.__init__(self, master, text="widget")
        self.titre = Label(self, text="0.0")
        self.titre.pack()

        self.play_reset_bin = 0
        self.play_reset_button = Button(self, text="Play", command=self.play_reset)
        self.play_reset_button.pack()

    def play_reset(self):
        if self.play_reset_bin == 0:
            self.start = time.time()
            self.play_reset_button.config(text="Reset")
            self.play_reset_bin = 1
            self.cunt()
        elif self.play_reset_bin == 1:
            print('Dernier Temps : ', self.compteur, 's')
            self.play_reset_button.config(text="Play")
            self.play_reset_bin = 0
            self.cunt()

    def cunt(self):
        if self.play_reset_bin == 1:
            self.compteur = int((time.time() - self.start) * 10) / 10
            self.titre.config(text=self.compteur)
            self.titre.after(100, self.cunt)
        else:
            self.titre.config(text='0.0')
