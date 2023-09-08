import customtkinter as ctk
import tkinter.messagebox as tkmb

font1 = ("bahnschrift", 18)


def screen2():
    log_win = ctk.CTkToplevel(app)

    log_win.title("New Window")

    log_win.geometry("400x400")

    label = ctk.CTkLabel(
        log_win,
        text="showFlix",
        font=("chiller", 33),
        text_color="white",
        bg_color="#242424",
    )
    label.pack(padx=0.025, pady=0.02)

    sign = ctk.CTkLabel(
        log_win,
        text="login",
        font=("calibri bold", 33),
        text_color="white",
        bg_color="#242424",
    )
    sign.place()

    userlabel = ctk.CTkLabel(
        log_win,
        text="username",
        font=font1,
        text_color="white",
        bg_color="#242424",
    )
    userlabel.pack(padx = 5, pady= 5)

    username = ctk.CTkEntry(
        log_win,
        placeholder_text="username",
        text_color="white",
        bg_color="#353638",
        fg_color="#353638",
    )
    username.pack(padx = 5, pady= 5)

    password = ctk.CTkEntry(
        log_win,
        placeholder_text="password",
        text_color="white",
        bg_color="#353638",
        fg_color="#353638",
    )
    password.pack(padx = 5, pady= 5)

    passlabel = ctk.CTkLabel(
        log_win,
        text="password",
        font=font1,
        text_color="white",
        bg_color="#242424",
    )
    passlabel.pack(padx=5,pady=5)

    button = ctk.CTkButton(
        log_win, text="log in", font=("bahnschrift", 17), command=None
    )
    button.pack(padx = 5, pady= 5)

    print(123)

    
    button.pack(pady=12, padx=10)


def next_screen():
    screen2()
    print("opened another screen")


def next_screen_2():
    print("boo")


# Selecting GUI theme - dark, light , system (for system default)
ctk.set_appearance_mode("dark")

# Selecting color theme - blue, green, dark-blue
ctk.set_default_color_theme("green")

app = ctk.CTk()
app.geometry("400x500")
app.title("title idk")

window = ctk.CTkFrame(master=app)

window.pack(pady=20, padx=40, fill="both", expand=True)


# main window
label = ctk.CTkLabel(
    window,
    text="showFlix",
    font=("chiller", 33),
    text_color="white",
    bg_color="#242424",
)
label.pack(padx=5, pady=5)

sign = ctk.CTkLabel(
    window,
    text="Sign up",
    font=("calibri bold", 33),
    text_color="white",
    bg_color="#242424",
)
sign.pack(padx=5, pady=5)

userlabel = ctk.CTkLabel(
    window,
    text="username",
    font=font1,
    text_color="white",
    bg_color="#242424",
)
userlabel.pack(padx=5, pady=5)

username = ctk.CTkEntry(
    window,
    placeholder_text="username",
    text_color="white",
    bg_color="#353638",
    fg_color="#353638",
)
username.pack(padx=5, pady=5)

password = ctk.CTkEntry(
    window,
    placeholder_text="password",
    text_color="white",
    bg_color="#353638",
    fg_color="#353638",
)
password.pack(padx=5, pady=5)

passlabel = ctk.CTkLabel(
    window,
    text="password",
    font=font1,
    text_color="white",
    bg_color="#242424",
)
passlabel.pack(padx=5, pady=5)

button = ctk.CTkButton(
    window, text="sign up", font=("bahnschrift", 17), command=next_screen_2
)
button.pack(padx=5, pady=5)

log = ctk.CTkLabel(
    window,
    text="already have an account ? ",
    font=("calibri", 15),
    text_color="white",
    bg_color="#242424",
)
log.pack(padx=5, pady=5)

button = ctk.CTkButton(window, text="log in", font=("bahnschrift", 17), command=screen2)
button.pack(padx=5, pady=5)

app.mainloop()
