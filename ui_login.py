import customtkinter as ctk
import tkinter.messagebox as tkmb
import pickle
import mysql.connector
from PIL import Image

import ui_sign_in

autofill_user = False
user_info = None
sqlPass = "CH3-CH2-CH2-CH3"


def rem_user(username, password, player_id):
    d = {"username": username, "password": password, "player_id": player_id}
    with open("rem_user.pkl", "wb") as f:
        pickle.dump(d, f)


def save_user(username, password, player_id):
    d = {"username": username, "password": password, "player_id": player_id}
    with open("rem_user.pkl", "wb") as f:
        pickle.dump(d, f)


def load_user():
    global autofill_user, user_info
    try:
        autofill_user = True
        user_info = pickle.load(open("rem_user.pkl", "rb"))
        print(user_info, "u info")

    except FileNotFoundError:
        autofill_user = True


def check_user(username, passwd):
    mydb = mysql.connector.connect(
        host="localhost", user="root", passwd=sqlPass, database="proj_test"
    )
    mycursor = mydb.cursor()

    q = f"select id,username from users where username = '{username}'and passwd = '{passwd}';"
    mycursor.execute(q)
    res = mycursor.fetchone()

    print(res)

    mycursor.close()
    mydb.close()

    return res


def login():
    uname = user_entry.get()
    passw = user_pass.get()
    player_id = check_user(uname, passw)
    re_u = checkbox.get()
    if re_u == True:
        rem_user(uname, passw, player_id)

    if player_id != None:
        tkmb.showinfo(title="Login Successful", message="logged in Successfully")
        screen2()
    else:
        tkmb.showerror(title="Login Failed", message="Invalid Username or password")


def screen2():
    ui_sign_in.screen_sign_in(app)


load_user()

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("theme\solaris_theme_dark.json")

root = ctk.CTk()
root.geometry("450x600")
root.title("login screen")

bg_img = ctk.CTkImage(Image.open("solaris\\assets\\star_bg2.jpg"), size=(800, 800))

app = ctk.CTkCanvas(root, bg="black")
app.pack(fill="both", expand=True)

imglabel = ctk.CTkLabel(app, text="", image=bg_img)
imglabel.place(x=0, y=0)

label = ctk.CTkLabel(app, text="Solaris", font=("", 32), bg_color="transparent")
label.pack(pady=20)


frame = ctk.CTkFrame(
    master=app, border_width=2, bg_color="transparent", fg_color="transparent"
)
frame.pack(pady=20, padx=40, fill="both", expand=True)

label = ctk.CTkLabel(master=frame, text="enter user crentials")
label.pack(pady=12, padx=10)


user_entry = ctk.CTkEntry(master=frame, placeholder_text="Username", width=220)
user_entry.pack(pady=12, padx=15)

user_pass = ctk.CTkEntry(master=frame, placeholder_text="Password", show="*", width=220)
user_pass.pack(pady=12, padx=10)

button = ctk.CTkButton(master=frame, text="Login", command=login)
button.pack(pady=12, padx=10)

button = ctk.CTkButton(
    master=frame,
    text="sign up",
    bg_color="transparent",
    fg_color="transparent",
    width=100,
)
button.pack(pady=12, padx=10)

checkbox = ctk.CTkCheckBox(master=frame, text="Remember Me")
checkbox.pack(pady=12, padx=10)

if autofill_user == True:
    user_entry.insert(0, str(user_info["username"]))  # autofill username passwd
    user_pass.insert(0, str(user_info["password"]))
    checkbox.select()


root.mainloop()
