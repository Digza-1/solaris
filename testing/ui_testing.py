import tkinter as tk
import customtkinter as ctk
import tkinter.messagebox as tkmb
import pickle
import mysql.connector


def rem_settings(username, password, uid):
    d = {"username": username, "password": password, "uid": uid}
    with open("rem_user.pkl", "wb") as f:
        pickle.dump(d, f)
        print("passwd saved")


def worldgen_options():
    pass


def user_options():
    pass


def admin_options():
    pass

def admin_options():
    dialog = ctk.CTkInputDialog(text="enter admin id:", title="admin id" )
    print("id:", dialog.get_input())

    dialog = ctk.CTkInputDialog(text="enter admin passwd:", title="admin passwd" )
    print("passwd:", dialog.get_input())
    

def settings(uname, uid):
    # Selecting GUI theme - dark, light , system
    ctk.set_appearance_mode("dark")
    # Selecting color theme - blue, green, dark-blue
    ctk.set_default_color_theme("theme\solaris_theme_dark.json")

    app = ctk.CTk()
    app.geometry("600x600")
    app.title("login screen")

    label = ctk.CTkLabel(app, text="settings")
    label.pack(pady=20, padx=20)

    frame = ctk.CTkFrame(master=app)
    frame.pack(pady=20, fill="both", expand=True)

    inFrame = ctk.CTkScrollableFrame(master=frame, width=500,height=350)
    inFrame.pack(padx=20)

    button = ctk.CTkButton(master=inFrame, text="setting 1", command=None)
    button.pack(pady=15)

    button = ctk.CTkButton(master=inFrame, text="setting 2", command=None)
    button.pack(pady=15)

    button = ctk.CTkButton(master=inFrame, text="setting 3", command=None)
    button.pack(pady=15)

    button = ctk.CTkButton(master=inFrame, text="admin", command=admin_options)
    button.pack(pady=15)

    for i in range(10): #for testing
        button = ctk.CTkButton(master=inFrame, text="setting 4", command=None)
        button.pack(pady=15)

    f3 = ctk.CTkFrame(master=frame)
    f3.pack(side="top", pady=20)

    button = ctk.CTkButton(
        master=f3,
        text="reset",
        bg_color="transparent",
        fg_color="transparent",
        command=None,
    )
    button.pack(pady=5, side="left")

    button = ctk.CTkButton(
        master=f3,
        text="save",
        bg_color="transparent",
        fg_color="transparent",
    )
    button.pack(side="right", padx=5)

    button = ctk.CTkButton(
        master=frame,
        text="back",
        # bg_color="transparent",
        fg_color="transparent",
        command=None,
    )

    button.pack(side="left", pady=5)

    app.mainloop()


settings(1, 1)
