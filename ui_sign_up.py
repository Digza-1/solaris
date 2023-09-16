import customtkinter as ctk
import tkinter.messagebox as tkmb
import pickle
import mysql.connector

from ui_login import login_screen
# import settings_ui_script as settingsui

sqlPass = "CH3-CH2-CH2-CH3"
user_valid = False
app = None
user_pass = None
user_entry = None
u_valid_text = None
confirm_user_pass = None
checkbox = None


def rem_user(username, password, uid):
    d = {"username": username, "password": password, "uid": uid}
    with open("rem_user.pkl", "wb") as f:
        pickle.dump(d, f)


def check_username(event):
    global user_valid
    mydb = mysql.connector.connect(
        host="localhost", user="root", passwd=sqlPass, database="project_solaris"
    )
    mycursor = mydb.cursor()

    uname = event.widget.get()

    # to check is username exists
    q = f"select username from users where username = '{uname}'; "
    mycursor.execute(q)
    res = mycursor.fetchone()

    if res != None and len(uname) > 0:
        u_valid_text.configure(text="username already taken", text_color="#ee4b4c")
        user_valid = False
    else:
        u_valid_text.configure(text="username valid", text_color="#34a853")
        user_valid = True


def register_user(username, passwd):
    global user_valid
    mydb = mysql.connector.connect(
        host="localhost", user="root", passwd=sqlPass, database="project_solaris"
    )
    mycursor = mydb.cursor()

    # to check is username exists
    res = None
    if user_valid == True:
        q = f"insert into users (username,passwd) values ('{username}','{passwd}'); "
        print(q)
        mycursor.execute(q)
        mydb.commit()

        q = f"select player_id from users where username = '{username}'and passwd = '{passwd}'; "
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


def screen_sign_up(app):
    global user_entry, user_pass, confirm_user_pass, u_valid_text, checkbox
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("theme\solaris_theme_dark.json")

    app = ctk.CTk()
    app.geometry("450x600")
    app.title("sign in")

    label = ctk.CTkLabel(app, text="register user")

    label.pack(pady=20)

    frame0 = ctk.CTkFrame(master=app, width=1200)
    frame0.pack(fill="both", pady=10, padx=10, expand=True)

    frame = ctk.CTkFrame(master=frame0, width=1200, fg_color="#020202")
    frame.pack(pady=10, padx=10, fill="both", expand=True)

    label = ctk.CTkLabel(master=frame, text="enter user crentials")
    label.pack(pady=12, padx=10)

    user_entry = ctk.CTkEntry(master=frame, placeholder_text="Username", width=220)
    user_entry.pack(pady=3, padx=15)
    user_entry.bind("<KeyRelease>", check_username)

    u_valid_text = ctk.CTkLabel(master=frame, text="")
    u_valid_text.pack(pady=1, padx=10)

    user_pass = ctk.CTkEntry(
        master=frame, placeholder_text="Password", show="*", width=220
    )
    user_pass.pack(pady=12, padx=10)

    confirm_user_pass = ctk.CTkEntry(
        master=frame, placeholder_text="confirm Password", show="*", width=220
    )
    confirm_user_pass.pack(pady=12, padx=10)

    button = ctk.CTkButton(master=frame, text="register", command=register)
    button.pack(pady=12, padx=10)

    button = ctk.CTkButton(
        master=frame,
        text="login instead",
        bg_color="transparent",
        fg_color="transparent",
        width=100,
        command=login_screen
    )
    button.pack(pady=12, padx=10)

    checkbox = ctk.CTkCheckBox(master=frame, text="Remember Me")
    checkbox.pack(pady=12, padx=10)

    app.mainloop()


# screen_sign_in(app)
