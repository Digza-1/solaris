import customtkinter as ctk
import tkinter.messagebox as tkmb
import pickle
import mysql.connector

from random import randint
from PIL import Image

import solaris.game_script

bg_img = ctk.CTkImage(Image.open("solaris\\assets\\star_bg2.jpg"), size=(800, 800))

bg_img2 = ctk.CTkImage(Image.open("solaris\\assets\\star_bg2.jpg"), size=(800, 800))

chat_image = (
    None  # ctk.CTkImage(Image.open("solaris\\assets\\star_bg2.jpg"), size=(80, 80))
)
add_user_image = None  # ctk.CTkImage(
# Image.open("solaris\\assets\\star_bg2.jpg"), size=(80, 80))


autofill_user = False
user_info = None
uid = None
world_id = None
app_scr = ctk.CTk()

worlds = []
difficulty = 1
costume = 1
costume_dict = {"space craft 1": 1, "space craft 2": 2, "space craft 3": 3}
diff_dict = {"easy": 1, "normal": 2, "hard": 3}
refresh_worlds = True
world_var = None
sqlPass = "123"


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
    except:
        autofill_user = False

    if user_info != None:
        autofill_user = True
        uid = user_info["uid"][0]


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


def check_sql_database():
    mydb = mysql.connector.connect(
        host="localhost", user="root", passwd=sqlPass, database=""
    )
    cursor = mydb.cursor()

    q1 = "use project_solaris;"

    try:
        cursor.execute(q1)
        res = cursor.fetchone()
    except:
        import setup.db_init


def close_root_screen():
    global app_scr
    app_scr.quit()


def login():
    global uid, uname, passw, checkbox
    uname = luser_entry.get()
    passw = luser_pass.get()
    player_id = check_user(uname, passw)
    re_u = checkbox.get()
    if re_u == True:
        rem_user(uname, passw, player_id)

    if player_id != None:
        uname = luser_entry.get()
        passw = luser_pass.get()
        uid = player_id[0]
        tkmb.showinfo(title="Login Successful", message="logged in Successfully")
        print("restart program to continue")
        exit()
    else:
        tkmb.showerror(title="Login Failed", message="Invalid Username or password")


# --------------------------login screen --------------------------
def login_screen():
    global luser_entry, user_info, luser_pass, checkbox, app_scr
    load_user()
    app_scr.geometry("450x600")
    app_scr.title("login screen")

    bg_img = ctk.CTkImage(Image.open("solaris\\assets\\star_bg2.jpg"), size=(800, 800))

    app = ctk.CTkCanvas(app_scr, bg="black")
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

    luser_entry = ctk.CTkEntry(master=frame, placeholder_text="Username", width=220)
    luser_entry.pack(pady=12, padx=15)

    luser_pass = ctk.CTkEntry(
        master=frame, placeholder_text="Password", show="*", width=220
    )
    luser_pass.pack(pady=12, padx=10)

    button = ctk.CTkButton(master=frame, text="Login", command=login)
    button.pack(pady=12, padx=10)

    button = ctk.CTkButton(
        master=frame,
        text="sign up",
        bg_color="transparent",
        fg_color="transparent",
        width=100,
        command=sign_up_screen,
    )
    button.pack(pady=12, padx=10)

    checkbox = ctk.CTkCheckBox(master=frame, text="Remember Me")
    checkbox.pack(pady=12, padx=10)

    if autofill_user == True and user_info != None:
        luser_entry.insert(0, str(user_info["username"]))  # autofill username passwd
        luser_pass.insert(0, str(user_info["password"]))
        checkbox.select()

    app_scr.mainloop()


# ----------------------sign in------------------------------

user_valid = False

suser_pass = None
suser_entry = None
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
    uname = suser_entry.get()
    passw = suser_pass.get()
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


def sign_up_screen():
    global suser_entry, suser_pass, confirm_user_pass, u_valid_text, checkbox, app_scr
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("theme\solaris_theme_dark.json")

    app_scr = ctk.CTkToplevel()
    app_scr.geometry("450x600")
    app_scr.title("sign up")

    bg_img3 = ctk.CTkImage(Image.open("solaris\\assets\\star_bg3.png"), size=(800, 800))
    label = ctk.CTkLabel(app_scr, image=bg_img3, text="")
    label.place(x=0, y=0)

    label = ctk.CTkLabel(app_scr, font=("", 32), text="sign up")
    label.pack(pady=20)

    frame0 = ctk.CTkFrame(master=app_scr, height=570, width=400)
    frame0.pack(fill="x", pady=10, padx=10, expand=False)

    frame = ctk.CTkFrame(master=frame0, height=570, width=400, fg_color="#020202")
    frame.pack(pady=10, padx=10, fill="x", expand=False)

    label = ctk.CTkLabel(master=frame, text="enter user crentials")
    label.pack(pady=12, padx=10)

    suser_entry = ctk.CTkEntry(master=frame, placeholder_text="Username", width=220)
    suser_entry.pack(pady=3, padx=15)
    suser_entry.bind("<KeyRelease>", check_username)

    u_valid_text = ctk.CTkLabel(master=frame, text="")
    u_valid_text.pack(pady=1, padx=10)

    suser_pass = ctk.CTkEntry(
        master=frame, placeholder_text="Password", show="*", width=220
    )
    suser_pass.pack(pady=12, padx=10)

    confirm_user_pass = ctk.CTkEntry(
        master=frame, placeholder_text="confirm Password", show="*", width=220
    )
    confirm_user_pass.pack(pady=12, padx=10)

    button = ctk.CTkButton(master=frame, text="register", command=register)
    button.pack(pady=12, padx=10)

    button = ctk.CTkButton(
        master=frame,
        text="back to login",
        bg_color="transparent",
        fg_color="transparent",
        width=100,
        command=app_scr.destroy,
    )
    button.pack(pady=20, padx=10)

    app_scr.mainloop()


# -----------------------settings--------------------------
def save_admin_settings():
    global difficulty, admin_settings_dict
    mydb = mysql.connector.connect(
        host="localhost", user="root", passwd=sqlPass, database="project_solaris"
    )
    mycursor = mydb.cursor()
 
collect new data from text input :
    # ====


    print(admin_settings_dict)
    q = f"""update game_settings set difficulty = {difficulty}, speed = {admin_settings_dict['speed']},
      grey_threshold = {admin_settings_dict['grey_threshold']},
      red_threshold ={admin_settings_dict['red_threshold']}, 
      blue_threshold = {admin_settings_dict['blue_threshold']} where player_id = {uid};"""

    mycursor.execute(q)
    mydb.commit()
    print("settings saved")


def save_user_settings():
    global difficulty, costume
    mydb = mysql.connector.connect(
        host="localhost", user="root", passwd=sqlPass, database="project_solaris"
    )
    mycursor = mydb.cursor()
    q = "update game_settings set difficulty = {},costume = {} where player_id = {};".format(
        difficulty, costume, uid
    )
    mycursor.execute(q)
    mydb.commit()


def reset():
    global difficulty, costume
    difficulty = 1
    costume = 1

    mydb = mysql.connector.connect(
        host="localhost", user="root", passwd=sqlPass, database="project_solaris"
    )
    cursor = mydb.cursor()

    q = "update game_settings set difficulty = {}, costume = {} ;".format(
        difficulty, costume
    )


def reset_admin():
    global difficulty
    difficulty = 1
    mydb = mysql.connector.connect(
        host="localhost", user="root", passwd=sqlPass, database="project_solaris"
    )
    cursor = mydb.cursor()

    q1_1 = f"""select speed,grey_threshold,red_threshold,blue_threshold,difficulty,costume
      from game_default_settings; """

    cursor.execute(q1_1)
    res1 = cursor.fetchone()
    (
        speed,
        grey_threshold,
        red_threshold,
        blue_threshold,
        difficulty,
        costume,
    ) = res1

    q1_2 = f"""update game_settings
    speed = {speed},grey_threshold = {grey_threshold},
    red_threshold = {red_threshold}, blue_threshold = {blue_threshold},
    difficulty = {difficulty},costume = {costume} 
    where player_id ={uid};"""

    cursor.execute(q1_2)
    mydb.commit()


def check_admin(admin_name, passwd):
    print(admin_name, passwd)
    mydb = mysql.connector.connect(
        host="localhost", user="root", passwd=sqlPass, database="project_solaris"
    )
    mycursor = mydb.cursor()

    q = f"select admin_id,username from admins where username = '{admin_name}' and passwd = '{passwd}'; "
    print(q)
    mycursor.execute(q)
    res = mycursor.fetchone()
    print(res)
    mycursor.close()
    mydb.close()

    return res


admin = False
difficulty_text_val = None
costume_val = None


def diff_update(x):
    print(x)
    global difficulty, difficulty_text_val
    difficulty = diff_dict.get(difficulty_text_val.get())


def costume_update(x):
    print(x)
    global costume, costume_val
    costume = costume_dict.get(costume_val.get())


admin_settings_dict = {}


def admin_settings_screen():
    global difficulty_text_val, app_scr

    app_scr = ctk.CTkToplevel()
    app_scr.geometry("450x600")
    app_scr.title("admin settings screen")
    difficulty_text_val = ctk.Variable(app_scr)
    difficulty_text_val.set("normal")
    label = ctk.CTkLabel(app_scr, text="settings")
    label.pack(pady=20, padx=20)

    frame = ctk.CTkFrame(master=app_scr)
    frame.pack(pady=20, fill="both", expand=True)

    inFrame = ctk.CTkScrollableFrame(master=frame, width=500, height=350)
    inFrame.pack(padx=20)

    label = ctk.CTkLabel(inFrame, text="change difficulty:")
    label.pack(pady=5)

    difficulty_box = ctk.CTkOptionMenu(
        inFrame,
        font=("", 16),
        dynamic_resizing=False,
        variable=difficulty_text_val,
        values=["easy", "normal", "hard"],
        command=diff_update,
    )
    difficulty_box.pack(pady=10)

    label = ctk.CTkLabel(inFrame, text="admin settings:")
    label.pack(pady=4)

    label = ctk.CTkLabel(inFrame, text="player speed:")
    label.pack(pady=4)
    sp = ctk.CTkEntry(master=inFrame, placeholder_text="player speed", width=220)
    sp.pack(pady=12, padx=15)

    label = ctk.CTkLabel(inFrame, text="red offset:")
    label.pack(pady=4)
    r_off = ctk.CTkEntry(master=inFrame, placeholder_text="red offset", width=220)
    r_off.pack(pady=12, padx=15)

    label = ctk.CTkLabel(inFrame, text="red offset:")
    label.pack(pady=4)
    b_off = ctk.CTkEntry(master=inFrame, placeholder_text="red offset", width=220)
    b_off.pack(pady=12, padx=15)

    label = ctk.CTkLabel(inFrame, text="red offset:")
    label.pack(pady=4)
    g_off = ctk.CTkEntry(master=inFrame, placeholder_text="red offset", width=220)
    g_off.pack(pady=12, padx=15)

    admin_data = solaris.game_script.get_settings_sql_player(uid)
    # speed, grey_thershold, red_threshold, blue_thershold, difficulty, costume

    sp.insert(0, str(admin_data[0]))

    r_off.insert(0, str(admin_data[2]))
    b_off.insert(0, str(admin_data[3]))
    g_off.insert(0, str(admin_data[1]))

    f3 = ctk.CTkFrame(master=frame)
    f3.pack(side="top", pady=20)

    button = ctk.CTkButton(
        master=f3,
        text="reset",
        bg_color="transparent",
        fg_color="transparent",
        command=reset_admin,
    )
    button.pack(pady=5, side="left")

    admin_settings_dict["speed"] = sp.get()
    admin_settings_dict["red_threshold"] = r_off.get()
    admin_settings_dict["grey_threshold"] = g_off.get()
    admin_settings_dict["blue_threshold"] = sp.get()

    button = ctk.CTkButton(
        master=f3,
        text="save",
        bg_color="transparent",
        fg_color="transparent",
        command=save_admin_settings,
    )
    button.pack(side="right", padx=5)

    button = ctk.CTkButton(
        master=frame,
        text="back",
        # bg_color="transparent",
        fg_color="transparent",
        command=app_scr.destroy,
    )

    button.pack(side="left", pady=5)


def admin_options():
    global app_scr
    admin_name = ctk.CTkInputDialog(text="enter admin name:", title="admin id")
    admin_name = admin_name.get_input()

    admin_pass = ctk.CTkInputDialog(text="enter admin passwd:", title="admin passwd")
    admin_pass = admin_pass.get_input()

    acc = check_admin(admin_name, admin_pass)

    if acc != None:
        app_scr.destroy()
        admin_settings_screen()
    else:
        tkmb.showerror(
            title="admin login Failed",
            message="Invalid username or password",
        )


def logout():
    forget_user()
    print("logged out")
    print("\n\n restart app ")
    app_scr.destroy()
    exit()


def settings_screen():
    global difficulty_text_val, costume_val, app_scr

    app_scr = ctk.CTkToplevel()
    app_scr.geometry("450x600")
    app_scr.title("settings screen")

    difficulty_text_val = ctk.Variable(app_scr)
    difficulty_text_val.set("normal")

    costume_val = ctk.Variable(app_scr)
    costume_val.set("space craft 1")

    label = ctk.CTkLabel(app_scr, text="settings")
    label.pack(pady=20, padx=20)

    frame = ctk.CTkFrame(master=app_scr)
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
        variable=difficulty_text_val,
        command=diff_update,
        values=["easy", "normal", "hard"],
    )
    difficulty.pack(pady=10)
    difficulty = diff_dict.get(difficulty_text_val.get())

    label = ctk.CTkLabel(inFrame, text="change space craft:")
    label.pack(pady=5)

    costumes = ctk.CTkOptionMenu(
        inFrame,
        font=("", 16),
        dynamic_resizing=False,
        variable=costume_val,
        command=costume_update,
        values=["space craft 1", "space craft 2", "space craft 3"],
    )
    costumes.pack(pady=10)

    logout_button = ctk.CTkButton(
        master=inFrame,
        text="logout",
        font=("", 16),
        command=logout,
    )
    logout_button.pack(pady=10)

    empty = ctk.CTkLabel(inFrame, text="")
    empty.pack()

    admin_button = ctk.CTkButton(
        master=inFrame,
        text="admin settings",
        font=("", 16),
        command=admin_options,
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
        command=app_scr.destroy,
    )

    button.pack(side="left", pady=5)


def get_worlds_data():
    print(uid)

    mydb = mysql.connector.connect(
        host="localhost", user="root", passwd=sqlPass, database="project_solaris"
    )
    mycursor = mydb.cursor()

    query = f"select world_id ,world_name from game_worlds where player_id = {uid};"
    mycursor.execute(query)

    res = mycursor.fetchall()
    print(res)
    mycursor.close()
    mydb.close()

    return res


def seed_limit(num):
    or_seed = str(num)
    if len(or_seed) > 13:
        return int(or_seed[:13])
    return num


def convert_num(str1):
    num = 0
    for i in str1:
        num += ord(i) * 10
    print("conv", num)
    num = seed_limit(num)
    return num


def create_world():
    global uid, app_scr, worlds

    mydb = mysql.connector.connect(
        host="localhost", user="root", passwd=sqlPass, database="project_solaris"
    )
    mycursor = mydb.cursor()

    name_inp = ctk.CTkInputDialog(text="enter world name: ", title="world name")
    world_name = name_inp.get_input()

    seed_inp = ctk.CTkInputDialog(text="enter worlds seed:", title="seed")
    seed = seed_inp.get_input()
    if world_name != None:
        if seed == None:
            seed = randint(-500000, 500000)
        seed = convert_num(seed)

        print("w name:", world_name, "seed:", seed)

        q1 = f"insert into game_worlds (world_name,seed,player_id) values('{world_name}',{seed},{uid});"

        mycursor.execute(q1)
        mydb.commit()

        mycursor.close()
        mydb.close()

        app_scr.update()

        app_scr.destroy()
        worlds = get_worlds_data()
        play_screen()


def delete_world():
    global uid, app_scr, worlds

    mydb = mysql.connector.connect(
        host="localhost", user="root", passwd=sqlPass, database="project_solaris"
    )
    mycursor = mydb.cursor()

    name_inp = ctk.CTkInputDialog(text="enter world name: ", title="world name")
    world_name = str(name_inp.get_input())
    print(world_id, uid, world_name)
    if world_name != None:
        query = f"delete from game_worlds where world_name = '{world_name}' and player_id = {uid};"
        mycursor.execute(query)
        mydb.commit()

        mycursor.close()
        mydb.close()

        app_scr.update()
        app_scr.update_idletasks()
        app_scr.destroy()
        play_screen()
        worlds = get_worlds_data()


def play_world():
    global world_id, uid
    world_id = int(world_var.get())
    solaris.game_script.player_id = uid
    solaris.game_script.world_id = world_id
    app_scr.destroy()
    solaris.game_script.main(uid, world_id)


# ---------------------- play screen -------------------


def play_screen():
    global worlds, refresh_worlds, world_var, app_scr

    app_scr = ctk.CTkToplevel()
    app_scr.geometry("600x600")
    app_scr.title("play screen")

    label = ctk.CTkLabel(app_scr, text="play")
    label.pack(pady=20)

    bg_img3 = ctk.CTkImage(Image.open("solaris\\assets\\star_bg3.png"), size=(800, 800))

    label = ctk.CTkLabel(app_scr, image=bg_img3, text="")
    label.place(x=0, y=0)

    frame = ctk.CTkScrollableFrame(master=app_scr, width=440)
    frame.pack(pady=10, padx=10, fill="y", expand=True)

    if refresh_worlds == True:
        worlds = get_worlds_data()

        # IntVar to manage the selected world
        world_var = ctk.IntVar()
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

        #

    buttons_frame = ctk.CTkFrame(master=app_scr, width=300)
    buttons_frame.pack()

    ub_frame = ctk.CTkFrame(master=buttons_frame, width=300, height=10)
    ub_frame.pack(pady=15)

    play_button = ctk.CTkButton(
        master=ub_frame,
        text="play",
        bg_color="transparent",
        fg_color="transparent",
        width=200,
        command=play_world,
    )
    play_button.pack(pady=5, padx=2, side="left")

    new_world_button = ctk.CTkButton(
        master=ub_frame,
        text="new world",
        # bg_color="transparent",
        fg_color="transparent",
        width=200,
        command=create_world,
    )

    new_world_button.pack(pady=5, padx=2, side="right")

    lb_frame = ctk.CTkFrame(master=buttons_frame, width=300)
    lb_frame.pack()

    back_button = ctk.CTkButton(
        master=lb_frame,
        text="back",
        bg_color="transparent",
        fg_color="transparent",
        command=app_scr.destroy,
    )
    back_button.pack(pady=5, side="left")

    delete_button = ctk.CTkButton(
        master=lb_frame,
        text="delete",
        bg_color="transparent",
        fg_color="transparent",
        command=delete_world,  # delete_world
    )

    delete_button.pack(side="right", padx=5)

    stats_button = ctk.CTkButton(
        master=lb_frame,
        text="stats",
        # bg_color="transparent",
        fg_color="transparent",
        command=stats_screen,
    )
    stats_button.pack(side="right", pady=5)

    # app.mainloop()


# ---------------------stats screen -------------------------------
stats_n = "distance_moved,dist_from_obj,collisions"


def stats_to_dict(stats):
    # list to dict
    d = {}
    ind = 0
    for i in stats_n.split(","):
        d[i] = stats[ind]
        ind += 1


def get_stats_data(uid):
    if uid != None:
        mydb = mysql.connector.connect(
            host="localhost", user="root", passwd=sqlPass, database="project_solaris"
        )
        mycursor = mydb.cursor()

        query = f"select {stats_n} from player_stats where player_id = {uid};"

        mycursor.execute(query)
        res = mycursor.fetchall()

        print(res)

        mycursor.close()
        mydb.close()
    else:
        res = {}
    return res


stats_d = {}

stat_d = get_stats_data(uid)


def stats_screen():
    global app_scr
    stat_li = get_stats_data(uid)
    print(stat_li)

    app_scr = ctk.CTkToplevel()
    app_scr.geometry("450x600")
    app_scr.title("stats screen")

    label = ctk.CTkLabel(app_scr, text="statistics")
    label.pack(pady=20)

    frame = ctk.CTkScrollableFrame(master=app_scr, bg_color="transparent")
    frame.pack(pady=10, padx=10, fill="both", expand=True)

    for k, j in stats_d.items():
        print(k, j)
        in_frame = ctk.CTkFrame(frame)

        stat = ctk.CTkLabel(master=in_frame, text=f"{k}")
        stat.pack(side="left", pady=10)

        stat = ctk.CTkLabel(master=in_frame, text=f"{j}")
        stat.pack(side="right", pady=10, padx=10)

        in_frame.pack(side="top")

    button.pack(side="right", padx=20)

    button = ctk.CTkButton(
        master=frame,
        text="back",
        # bg_color="transparent",
        fg_color="transparent",
        command=None,
    )

    button.pack(side="top", pady=30)
    # app.mainloop()


def title_screen():
    global app_scr

    app_scr.destroy()
    app_scr = ctk.CTk()

    app_scr.geometry("450x400")
    app_scr.title("title screen")

    bg_img3 = ctk.CTkImage(Image.open("solaris\\assets\\star_bg2.jpg"), size=(800, 800))

    bg_lablel = ctk.CTkLabel(app_scr, image=bg_img3, text="")
    bg_lablel.place(x=0, y=0)

    label = ctk.CTkLabel(app_scr, font=("", 32), text="Solaris")
    label.pack(pady=20)

    frame = ctk.CTkFrame(master=app_scr)
    frame.pack(pady=5, padx=5, fill="none", expand=True)

    fr3 = ctk.CTkFrame(master=frame)
    fr3.pack(pady=5)
    settings_button = ctk.CTkButton(master=fr3, text="Play", command=play_screen)
    settings_button.pack(pady=10, padx=2)

    fr1 = ctk.CTkFrame(
        master=frame,
    )
    fr1.pack(padx=5)
    # buttons load game, new game
    load_button = ctk.CTkButton(master=fr1, text="options", command=settings_screen)
    load_button.pack(side="left", pady=10, padx=10)

    new_button = ctk.CTkButton(master=fr1, text="quit game", command=app_scr.destroy)
    new_button.pack(side="right", pady=10, padx=10)

    app_scr.mainloop()


check_sql_database()
load_user()
print(user_info)

if user_info == None:
    login_screen()
else:
    title_screen()
