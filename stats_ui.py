import customtkinter as ctk
import tkinter as tk
import tkinter.messagebox as tkmb
import pickle
import mysql.connector

sqlPass = "CH3-CH2-CH2-CH3"

stats_d = {
    "dist_moved": 0,
    "lowest_height": 0,
    "ores_mined": 0,
    "blocks_broken": 0,
    "blocks_placed": 0,
}


def get_data(uname, uid):
    mydb = mysql.connector.connect(
        host="localhost", user="root", passwd=sqlPass, database="project"
    )
    mycursor = mydb.cursor()

    stats_n = "distance_moved,"

    query = f"select {stats_n} from player_stats where id = {uid};"

    mycursor.execute(query)
    res = mycursor.fetchall()

    print(res)

    mycursor.close()
    mydb.close()
    return res


def stat_screen(uname, uid):
    # Selecting GUI theme - dark, light , system
    ctk.set_appearance_mode("dark")
    # Selecting color theme - blue, green, dark-blue
    ctk.set_default_color_theme("green")

    app = ctk.CTk()
    app.geometry("600x600")
    app.title("stats screen")

    label = ctk.CTkLabel(app, text="statistics")
    label.pack(pady=20)

    frame = ctk.CTkScrollableFrame(master=app)
    frame.pack(pady=10, padx=10, fill="both", expand=True)

    for k, j in stats_d.items():
        in_frame = ctk.CTkFrame(frame)

        stat = ctk.CTkLabel(master=in_frame, text=f"{k}")
        stat.pack(side="left", pady=10)

        stat = ctk.CTkLabel(master=in_frame, text=f" {j}")
        stat.pack(side="right", pady=10, padx=10)

        in_frame.pack(side="top")

    button = ctk.CTkButton(
        master=frame,
        text="reset",
        bg_color="transparent",
        fg_color="transparent",
        command=None,
    )
    button.pack(pady=20, side="left")

    button = ctk.CTkButton(
        master=frame,
        text="save",
        bg_color="transparent",
        fg_color="transparent",
    )

    button.pack(side="right", padx=20)

    button = ctk.CTkButton(
        master=frame,
        text="back",
        # bg_color="transparent",
        fg_color="transparent",
        command=None,
    )

    button.pack(side="top", pady=30)

    app.mainloop()


stat_screen(0, 0)
