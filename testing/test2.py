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
    # Your database retrieval function
    pass


world_var = None


def a():
    # Print the selected world's w_id
    print(f"Selected world's w_id: {world_var.get()}")


def stat_screen(uname, uid):
    global world_var
    # Selecting GUI theme - dark, light , system
    ctk.set_appearance_mode("dark")
    # Selecting color theme - blue, green, dark-blue
    ctk.set_default_color_theme("green")

    app = ctk.CTk()
    app.geometry("600x600")
    app.title("stats screen")

    label = ctk.CTkLabel(app, text="statistics")
    label.pack(pady=20)

    frame = ctk.CTkScrollableFrame(master=app, width=440)
    frame.pack(pady=10, padx=10, fill="y", expand=True)

    # Create an IntVar to manage the selected world
    world_var = tk.IntVar()
    print(worlds,'\n')
    for w_id, w_na in worlds:
        in_frame = ctk.CTkRadioButton(
            frame,
            text=f"{w_na} \n id: {w_id}",
            font=("", 25),
            fg_color="#4ec999",
            variable=world_var,
            value=w_id,
        )
        in_frame.pack(pady=5, fill="x")

    buttons_frame = ctk.CTkFrame(master=app, width=300)
    buttons_frame.pack()

    ub_frame = ctk.CTkFrame(master=buttons_frame, width=300, height=10)
    ub_frame.pack(pady=15)

    back_button = ctk.CTkButton(
        master=ub_frame,
        text="new world",
        bg_color="transparent",
        fg_color="transparent",
        width=200,
        command=None,
    )
    back_button.pack(pady=5, padx=2, side="left")

    new_world_button = ctk.CTkButton(
        master=ub_frame,
        text="play",
        fg_color="transparent",
        width=200,
        command=a,
    )
    new_world_button.pack(pady=5, padx=2, side="right")


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
        fg_color="transparent",
        command=None,
    )
    stats_button.pack(side="right", pady=5)

    app.mainloop()


stat_screen(0, 0)
