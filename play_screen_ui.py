import customtkinter as ctk
import tkinter as tk
import tkinter.messagebox as tkmb
import pickle
import mysql.connector

sqlPass = "CH3-CH2-CH2-CH3"

worlds = [
    [123, "world1"],
    [430, "new world"],
    [373, "world2"],
    [970, "world3"],
    [260, "aaaa"],
]


def get_data(uname, uid):
    mydb = mysql.connector.connect(
        host="localhost", user="root", passwd=sqlPass, database="project"
    )
    mycursor = mydb.cursor()

    query = f"select world_id ,world_name from worlds where id = {uid};"

    mycursor.execute(query)
    res = mycursor.fetchall()

    print(res)

    mycursor.close()
    mydb.close()
    return res


def a(event):
    print(event)


def stat_screen(uname, uid):
    # Selecting GUI theme - dark, light , system
    ctk.set_appearance_mode("dark")
    # Selecting color theme - blue, green, dark-blue
    ctk.set_default_color_theme("theme\solaris_theme_dark.json")

    app = ctk.CTk()
    app.geometry("600x600")
    app.title("stats screen")

    label = ctk.CTkLabel(app, text="statistics")
    label.pack(pady=20)

    frame = ctk.CTkScrollableFrame(master=app, width=440)
    frame.pack(pady=10, padx=10, fill="y", expand=True)

    worlds_list = []  # (worlds, range(len(worlds)))
    worlds_dict = {}

    index = 0
    for w_id, w_na in worlds:
        worlds_dict[index] = [w_id, w_na]
        index += 1

    print(list(worlds_dict.items()))
    for index ,w_temp in worlds_dict.items():
        w_id,w_na = w_temp
        
        print(w_id,w_na)
        in_frame = ctk.CTkFrame(frame, fg_color="#4ec999", bg_color="black")
        in_frame.pack(pady=5, fill="x")

        b1 = ctk.CTkLabel(master=in_frame, text=f"{w_na}", font=("", 25))
        b1.pack(side="top", pady=1)
        b2 = ctk.CTkLabel(master=in_frame, text=f"id: {w_id} ", font=("", 18))
        b2.pack(side="top", pady=2, padx=10)

        in_frame.bind("<Button-1>", a)

    buttons_frame = ctk.CTkFrame(master=app, width=300)
    buttons_frame.pack()

    ub_frame = ctk.CTkFrame(master=buttons_frame, width=300, height=10)
    ub_frame.pack(pady=15)

    back_button = ctk.CTkButton(
        master=ub_frame,
        text="back",
        bg_color="transparent",
        fg_color="transparent",
        width=200,
        command=None,
    )
    back_button.pack(pady=5, padx=2, side="left")

    new_world_button = ctk.CTkButton(
        master=ub_frame,
        text="new world",
        # bg_color="transparent",
        fg_color="transparent",
        width=200,
        command=None,
    )

    new_world_button.pack(pady=5, padx=2, side="right")

    #

    lb_frame = ctk.CTkFrame(master=buttons_frame, width=300)
    lb_frame.pack()

    back_button = ctk.CTkButton(
        master=lb_frame,
        text="back",
        bg_color="transparent",
        fg_color="transparent",
        command=None,
    )
    back_button.pack(pady=5, side="left")

    delete_button = ctk.CTkButton(
        master=lb_frame,
        text="delete",
        bg_color="transparent",
        fg_color="transparent",
    )

    delete_button.pack(side="right", padx=5)

    stats_button = ctk.CTkButton(
        master=lb_frame,
        text="stats",
        # bg_color="transparent",
        fg_color="transparent",
        command=None,
    )
    stats_button.pack(side="right", pady=5)

    app.mainloop()


stat_screen(0, 0)
