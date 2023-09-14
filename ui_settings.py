import tkinter as tk
import customtkinter as ctk
import tkinter.messagebox as tkmb
import pickle
import mysql.connector


def worldgen_options():
    pass



def admin_options():
    pass


sqlPass = "CH3-CH2-CH2-CH3"

def save():
    mydb = mysql.connector.connect(
        host="localhost", user="root", passwd=sqlPass, database="project_solaris"
    )
    mycursor = mydb.cursor()
    q = "update settings set 'difficulty' = "
    mycursor.execute(q)

    

def reset():
    mydb = mysql.connector.connect(
        host="localhost", user="root", passwd=sqlPass, database="project_solaris"
    )
    mycursor = mydb.cursor()

    pass

def check_admin(admin_id, passwd):
    mydb = mysql.connector.connect(
        host="localhost", user="root", passwd=sqlPass, database="project_solaris"
    )
    mycursor = mydb.cursor()

    q = f"select id,username from users where admin_id = {admin_id} and passwd = '{passwd}'; "
    mycursor.execute(q)
    res = mycursor.fetchone()

    mycursor.close()
    mydb.close()

    return res


def admin_options():
    admin_id = ctk.CTkInputDialog(text="enter admin id:", title="admin id")
    print("id:", admin_id.get_input())

    admin_pass = ctk.CTkInputDialog(text="enter admin passwd:", title="admin passwd")
    print("passwd:", admin_pass.get_input())

    acc = check_admin(admin_id, admin_pass)


def settings(uname, uid):
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("theme\solaris_theme_dark.json")

    app = ctk.CTk()
    app.geometry("600x600")
    app.title("login screen")

    label = ctk.CTkLabel(app, text="settings")
    label.pack(pady=20, padx=20)

    frame = ctk.CTkFrame(master=app)
    frame.pack(pady=20, fill="both", expand=True)

    inFrame = ctk.CTkScrollableFrame(master=frame, width=500, height=350)
    inFrame.pack(padx=20)

    empty = ctk.CTkLabel(inFrame, text="")
    empty.pack()

    label = ctk.CTkLabel(inFrame, text="change diffifulty:")
    label.pack(pady=5)

    difficulty = ctk.CTkOptionMenu(
        inFrame,
        font=("", 16),
        dynamic_resizing=False,
        values=["easy", "normal", "hard"],
    )
    difficulty.pack(pady=10)

    empty = ctk.CTkLabel(inFrame, text="")
    empty.pack()

    label = ctk.CTkLabel(inFrame, text="change space craft:")
    label.pack(pady=5)

    costume = ctk.CTkOptionMenu(
        inFrame,
        font=("", 16),
        dynamic_resizing=False,
        values=["space craft 1", "space craft 2", "space craft 3"],
    )
    costume.pack(pady=10)

    empty = ctk.CTkLabel(inFrame, text="")
    empty.pack()

    admin_button = ctk.CTkButton(
        master=inFrame, text="admin settings", font=("", 16), command=admin_options
    )
    admin_button.pack(pady=10)

    f3 = ctk.CTkFrame(master=frame)
    f3.pack(side="top", pady=20)

    button = ctk.CTkButton(
        master=f3,
        text="reset",
        bg_color="transparent",
        fg_color="transparent",
        command=reset,
    )
    button.pack(pady=5, side="left")

    button = ctk.CTkButton(
        master=f3,
        text="save",
        bg_color="transparent",
        fg_color="transparent",
        command=save,
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
