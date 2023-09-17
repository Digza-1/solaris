import customtkinter as ctk
import tkinter.messagebox as tkmb
import pickle
import mysql.connector
from PIL import Image

bg_img = ctk.CTkImage(Image.open("solaris\\assets\\star_bg2.jpg"), size=(800, 800))

bg_img2 = ctk.CTkImage(Image.open("solaris\\assets\\star_bg2.jpg"), size=(80, 80))
chat_image = (
    None  # ctk.CTkImage(Image.open("solaris\\assets\\star_bg2.jpg"), size=(80, 80))
)
add_user_image = None  # ctk.CTkImage(
# Image.open("solaris\\assets\\star_bg2.jpg"), size=(80, 80))


autofill_user = False
user_info = None
uid = None
app = None

sqlPass = "CH3-CH2-CH2-CH3"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("theme\solaris_theme_dark.json")


def rem_user(username, password, player_id):
    d = {"username": username, "password": password, "player_id": player_id}
    with open("rem_user.pkl", "wb") as f:
        pickle.dump(d, f)


def forget_user():
    global autofill_user, user_info, uid
    with open("rem_user.pkl", "wb") as f:
        pickle.dump(None, f)
    autofill_user = False
    user_info = uid = None


def load_user():
    global autofill_user, user_info, uid
    try:
        user_info = pickle.load(open("rem_user.pkl", "rb"))
        print(user_info, "u info")
    except FileNotFoundError:
        autofill_user = False

    if user_info != None:
        autofill_user = True
        uid = user_info["player_id"]


def check_user(username, passwd):
    mydb = mysql.connector.connect(
        host="localhost", user="root", passwd=sqlPass, database="project_solaris"
    )
    mycursor = mydb.cursor()

    q = f"select player_id,username from users where username = '{username}'and passwd = '{passwd}';"
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
    else:
        tkmb.showerror(title="Login Failed", message="Invalid Username or password")


# --------------------------login screen --------------------------
def login_screen():
    global app, user_entry, user_info, user_pass, checkbox
    load_user()

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

    user_pass = ctk.CTkEntry(
        master=frame, placeholder_text="Password", show="*", width=220
    )
    user_pass.pack(pady=12, padx=10)

    button = ctk.CTkButton(master=frame, text="Login", command=login)
    button.pack(pady=12, padx=10)

    button = ctk.CTkButton(
        master=frame,
        text="sign up",
        bg_color="transparent",
        fg_color="transparent",
        width=100,
        command=None,
    )
    button.pack(pady=12, padx=10)

    checkbox = ctk.CTkCheckBox(master=frame, text="Remember Me")
    checkbox.pack(pady=12, padx=10)

    if autofill_user == True and user_info != None:
        user_entry.insert(0, str(user_info["username"]))  # autofill username passwd
        user_pass.insert(0, str(user_info["password"]))
        checkbox.select()

    root.mainloop()


# ----------------------sign in------------------------------

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


def sign_up_screen(app):
    global user_entry, user_pass, confirm_user_pass, u_valid_text, checkbox
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("theme\solaris_theme_dark.json")

    app = ctk.CTk()
    app.geometry("450x600")
    app.title("sign up")

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
        command=login_screen,
    )
    button.pack(pady=12, padx=10)

    checkbox = ctk.CTkCheckBox(master=frame, text="Remember Me")
    checkbox.pack(pady=12, padx=10)

    app.mainloop()


# -----------------------settings--------------------------


def save_user_settings():
    global difficulty
    mydb = mysql.connector.connect(
        host="localhost", user="root", passwd=sqlPass, database="project_solaris"
    )
    mycursor = mydb.cursor()
    q = "update settings set difficulty = '{}';".format(difficulty)
    mycursor.execute(q)


def reset():
    mydb = mysql.connector.connect(
        host="localhost", user="root", passwd=sqlPass, database="project_solaris"
    )
    mycursor = mydb.cursor()
    q = "update settings set difficulty = '{}';".format(difficulty)

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


def settings_screen():
    app = ctk.CTk()
    app.geometry("450x600")
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
        command=save_user_settings,
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


worlds = []


def get_worlds_data():
    global uid

    mydb = mysql.connector.connect(
        host="localhost", user="root", passwd=sqlPass, database="project_solaris"
    )
    mycursor = mydb.cursor()

    query = f"select world_id ,world_name from worlds where player_id = {uid};"
    mycursor.execute(query)

    res = mycursor.fetchall()
    print(res)
    mycursor.close()
    mydb.close()

    return res


# ---------------------- stats screen ------------------


# ---------------------stats screen -------------------------------
def get_stats_data(uid):
    if uid != None:
        mydb = mysql.connector.connect(
            host="localhost", user="root", passwd=sqlPass, database="project_solaris"
        )
        mycursor = mydb.cursor()

        stats_n = "distance_moved,"

        query = f"select * from player_stats where player_id = {uid};"

        mycursor.execute(query)
        res = mycursor.fetchall()

        print(res)

        mycursor.close()
        mydb.close()
    else:
        res = None
    return res


stat_d = get_stats_data(uid)


def stats_screen():
    stat_li = get_stats_data()
    print(stat_li)
    stats_d = {}

    app = ctk.CTk()
    app.geometry("450x600")
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


def title_screen():
    app = ctk.CTk()
    app.geometry("450x600")
    app.title("screen")

    label = ctk.CTkLabel(app, text="pyrraria")
    label.pack(pady=20)

    frame = ctk.CTkFrame(master=app)
    frame.pack(pady=10, padx=10, fill="both", expand=True)

    fr3 = ctk.CTkFrame(master=frame)
    fr3.pack(pady=15)

    settings_button = ctk.CTkButton(master=fr3, text="Play", command=None)
    settings_button.pack(pady=15)

    fr1 = ctk.CTkFrame(master=frame)
    fr1.pack()
    # buttons load game, new game
    load_button = ctk.CTkButton(master=fr1, text="options", command=None)
    load_button.pack(side="left", pady=15, padx=5)

    new_button = ctk.CTkButton(master=fr1, text="quit game", command=None)
    new_button.pack(side="right", pady=15, padx=5)

    app.mainloop()


load_user()
print(user_info)
if user_info == None:
    login_screen()
else:
    title_screen()
