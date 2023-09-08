import tkinter as tk
import customtkinter as ctk
import tkinter.messagebox as tkmb
import pickle
import mysql.connector



def _screen(uname, uid):
    # Selecting GUI theme
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")

    app = ctk.CTk()
    app.geometry("600x600")
    app.title("x screen")
    #initialise app

    label = ctk.CTkLabel(app, text="screen x")
    label.pack(pady=20)

    frame = ctk.CTkScrollableFrame(master=app)
    frame.pack(pady=10, padx=10, fill="both", expand=True)

    #add stuff here

    app.mainloop()

_screen(0,0)