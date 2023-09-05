import customtkinter as ctk
import tkinter.messagebox as tkmb
import pickle
import mysql.connector

sqlPass = "CH3-CH2-CH2-CH3"


def rem_user(username, password, uid):
    d = {"username": username, "password": password, "uid": uid}
    with open("rem_user.pkl", "wb") as f:
        pickle.dump(d, f)


def load_user():
    b = pickle.load(open("rem_user.pkl", "rb"))
    return b


def check_user(username, passwd):
    mydb = mysql.connector.connect(
        host="localhost", user="root", passwd=sqlPass, database="proj_test"
    )
    mycursor = mydb.cursor()

    q = f"select id,username from users where username = '{username}'and passwd = '{passwd}'; "
    mycursor.execute(q)
    res = mycursor.fetchone()

    print(res)

    mycursor.close()
    mydb.close()

    return res


def login():
    uname = user_entry.get()
    passw = user_pass.get()
    uid = check_user(uname, passw)
    re_u = checkbox.get()
    if re_u == True:
        rem_user(uname, passw, uid)

    if uid != None:
        tkmb.showinfo(
            title="Login Successful", message="You have logged in Successfully"
        )
        screen2()

    else:
        tkmb.showerror(title="Login Failed", message="Invalid Username and password")


def screen2():
    new_window = ctk.CTkToplevel(app)
    new_window.title("New Window")
    new_window.geometry("350x150")
    ctk.CTkLabel(new_window, text="main screen stuff.......").pack()


# Selecting GUI theme - dark, light , system (for system default)
ctk.set_appearance_mode("dark")

# Selecting color theme - blue, green, dark-blue
ctk.set_default_color_theme("theme\solaris_theme_dark.json")

app = ctk.CTk()
app.geometry("600x600")
app.title("login screen")

label = ctk.CTkLabel(app, text="login screen")

label.pack(pady=20)


frame = ctk.CTkFrame(master=app)
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

try:
    user_info = load_user()
    print(user_info, "u info")
    user_entry.insert(0, str(user_info["username"]))  # autofill username passwd
    user_pass.insert(0, str(user_info["password"]))
    checkbox.select()
except FileNotFoundError:
    pass

app.mainloop()
