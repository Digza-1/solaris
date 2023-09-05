import tkinter as tk
import customtkinter as ctk
import tkinter.messagebox as tkmb
import pickle
import mysql.connector



def title_screen(uname, uid):
    # Selecting GUI theme - dark, light , system
    ctk.set_appearance_mode("dark")
    # Selecting color theme - blue, green, dark-blue
    ctk.set_default_color_theme("green")

    app = ctk.CTk()
    app.geometry("600x600")
    app.title("screen")

    label = ctk.CTkLabel(app, text="pyrraria")
    label.pack(pady=20)

    frame = ctk.CTkFrame(master=app)
    frame.pack(pady=10, padx=10, fill="both", expand=True)

    

    fr3 = ctk.CTkFrame(master = frame)
    fr3.pack(pady = 15)
    
    settings_button = ctk.CTkButton(master=fr3, text="Play", command=None)
    settings_button.pack(pady=15)
    

    fr1= ctk.CTkFrame(master= frame)
    fr1.pack()
    # buttons load game, new game 
    load_button = ctk.CTkButton(master=fr1, text="options", command=None)
    load_button.pack(side ="left",pady = 15, padx= 5)
    
    new_button = ctk.CTkButton(master=fr1, text="quit game", command=None)
    new_button.pack(side= "right",pady = 15, padx= 5)
 
    
    app.mainloop()

title_screen(0,0)
