import customtkinter as ctk
from PIL import Image

bg_img = ctk.CTkImage(Image.open("solaris\\assets\\star_bg2.jpg"), size=(800, 800))

home_image = ctk.CTkImage(Image.open("solaris\\assets\\star_bg2.jpg"), size=(80, 80))
chat_image = ctk.CTkImage(Image.open("solaris\\assets\\star_bg2.jpg"), size=(80, 80))
add_user_image = ctk.CTkImage(
    Image.open("solaris\\assets\\star_bg2.jpg"), size=(80, 80)
)


def screen1():
    pass


def screen2():
    pass


def screen3():
    pass


# Selecting GUI theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("theme\solaris_theme_dark.json")

app = ctk.CTk()
app.geometry("600x600")
app.title("login screen")

navigation_frame = ctk.CTkFrame(app, corner_radius=0)
navigation_frame.grid(row=0, column=0, sticky="nsew")
navigation_frame.grid_rowconfigure(4, weight=1)


navigation_frame_label = ctk.CTkLabel(
    navigation_frame,
    text="  Image Example",
    image=home_image,
    compound="left",
    font=ctk.CTkFont(size=15, weight="bold"),
)
navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

home_button = ctk.CTkButton(
    navigation_frame,
    corner_radius=0,
    height=40,
    border_spacing=10,
    text="Home",
    fg_color="transparent",
    text_color=("gray10", "gray90"),
    hover_color=("gray70", "gray30"),
    image=home_image,
    anchor="w",
    command=screen1,
)
home_button.grid(row=1, column=0, sticky="ew")

frame_2_button = ctk.CTkButton(
    navigation_frame,
    corner_radius=0,
    height=40,
    border_spacing=10,
    text="Frame 2",
    fg_color="transparent",
    text_color=("gray10", "gray90"),
    hover_color=("gray70", "gray30"),
    image=chat_image,
    anchor="w",
    command=screen2,
)
frame_2_button.grid(row=2, column=0, sticky="ew")

frame_3_button = ctk.CTkButton(
    navigation_frame,
    corner_radius=0,
    height=40,
    border_spacing=10,
    text="Frame 3",
    fg_color="transparent",
    text_color=("gray10", "gray90"),
    hover_color=("gray70", "gray30"),
    image=add_user_image,
    anchor="w",
    command=screen3,
)
frame_3_button.grid(row=3, column=0, sticky="ew")

app.mainloop()
