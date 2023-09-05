import customtkinter as ctk
import tkinter.messagebox as tkmb
import pickle
import mysql.connector

# import settings_ui_script as settingsui

sqlPass = "CH3-CH2-CH2-CH3"

user_valid = False


def rem_user(username, password, uid):
    d = {"username": username, "password": password, "uid": uid}
    with open("rem_user.pkl", "wb") as f:
        pickle.dump(d, f)


def check_username(event):
    global user_valid
    mydb = mysql.connector.connect(
        host="localhost", user="root", passwd=sqlPass, database="proj_test"
    )
    mycursor = mydb.cursor()

    uname = event.widget.get()

    # to check is username exists
    q = f"select username from users where username = '{uname}'; "
    mycursor.execute(q)
    res = mycursor.fetchone()

    if res != None and len(uname) > 0:
        u_valid.configure(text="username already taken", text_color="#ee4b4c")
        user_valid = False
    else:
        u_valid.configure(text="username valid", text_color="#34a853")
        user_valid = True


def register_user(username, passwd):
    global user_valid
    mydb = mysql.connector.connect(
        host="localhost", user="root", passwd=sqlPass, database="proj_test"
    )
    mycursor = mydb.cursor()

    # to check is username exists
    res = None
    if user_valid == True:
        q = f"insert into users (username,passwd) values ('{username}','{passwd}'); "
        print(q)
        mycursor.execute(q)
        mydb.commit()

        q = f"select id from users where username = '{username}'and passwd = '{passwd}'; "
        mycursor.execute(q)
        res = mycursor.fetchone()

        user_valid = False
    else:
        tkmb.showerror(
            title="registration Failed",
            message="Username already exists",
        )
    mycursor.close()
    mydb.close()

    return res


def register():
    uname = user_entry.get()
    passw = user_pass.get()
    conf_passw = confirm_user_pass.get()

    if passw == conf_passw:
        if user_valid and len(uname) > 0:
            uid = register_user(uname, passw)

            re_u = checkbox.get()
            if re_u == True:
                rem_user(uname, passw, uid)

            if uid != None:
                tkmb.showinfo(
                    title="registration Successful",
                    message="You have registered Successfully",
                )
                screen2()
        else:
            tkmb.showerror(
                title="registration Failed",
                message="username invalid",
            )
    else:
        tkmb.showerror(
            title="registration Failed",
            message="password not matching",
        )


def screen2():
    new_window = ctk.CTkToplevel(app)
    new_window.title("New Window")
    new_window.geometry("350x150")
    ctk.CTkLabel(new_window, text="main screen stuff.......").pack()


# Selecting GUI theme - dark, light , system (for system default)
ctk.set_appearance_mode("dark")

# Selecting color theme - blue, green, dark-blue
ctk.set_default_color_theme("green")

app = ctk.CTk()
app.geometry("600x600")
app.title("register screen")

label = ctk.CTkLabel(app, text="register user")

label.pack(pady=20)


frame = ctk.CTkFrame(master=app)
frame.pack(pady=20, padx=40, fill="both", expand=True)

label = ctk.CTkLabel(master=frame, text="enter user crentials")
label.pack(pady=12, padx=10)


user_entry = ctk.CTkEntry(master=frame, placeholder_text="Username", width=220)
user_entry.pack(pady=12, padx=15)
user_entry.bind("<KeyRelease>", check_username)

u_valid = ctk.CTkLabel(master=frame, text="")
u_valid.pack(pady=12, padx=10)

user_pass = ctk.CTkEntry(master=frame, placeholder_text="Password", show="*", width=220)
user_pass.pack(pady=12, padx=10)

confirm_user_pass = ctk.CTkEntry(
    master=frame, placeholder_text="Password", show="*", width=220
)
confirm_user_pass.pack(pady=12, padx=10)

button = ctk.CTkButton(master=frame, text="register", command=register)
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

app.mainloop()
