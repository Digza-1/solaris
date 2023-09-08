import time
import customtkinter as ctk
import tkinter.messagebox as tkmb

def option_1(option_number):
    # Define actions for each option here
    tkmb.showinfo("Option Selected", f"Option {option_number} selected")

def option_2(option_number):
    # Define actions for each option here
    tkmb.showinfo("Option Selected", f"Option {option_number} selected")

def option_3(option_number):
    # Define actions for each option here
    tkmb.showinfo("Option Selected", f"Option {option_number} selected")

# Define a list of options for the settings screen
settings_options = [
    ("Option 1", option_1),
    ("Option 2", option_2),
    ("Option 3", option_3),
    ("Option 4", option_1),
    ("Option 5", option_2),
    ("Option 6", option_3),
    ("Option 7", option_1),
    ("Option 8", option_2),
    ("Option 9", option_3),
    ("Option 5", option_2),
    ("Option 6", option_3),
    ("Option 7", option_1),
    ("Option 8", option_2),
    ("Option 9", option_3),
]

def next_screen():
    screen2()
    print("Opened the settings screen")

def screen2():
    new_window = ctk.CTkToplevel(app)
    new_window.title("Settings")
    new_window.geometry("400x400")

    label_1 = ctk.CTkLabel(new_window, text="Settings Screen")
    label_1.pack(pady=20)

    # Create a canvas for the scrollable area
    canvas = ctk.CTkCanvas(new_window)
    canvas.pack(side="left", fill="both", expand=True)
    
    # Create a frame to contain the settings options
    settings_frame = ctk.CTkFrame(canvas)
    canvas.create_window((0, 0), window=settings_frame, anchor="nw")

    for option_text, option_command in settings_options:
        button = ctk.CTkButton(
            master=settings_frame,
            text=option_text,
            bg_color="transparent",
            fg_color="transparent",
            command=option_command,
        )
        button.pack(pady=5)

    # Add a vertical scrollbar to the canvas
    scrollbar = ctk.CTkScrollbar(new_window, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)

# Selecting GUI theme - dark, light , system
ctk.set_appearance_mode("dark")

# Selecting color theme - blue, green, dark-blue
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("400x500")
app.title("Title - Settings Screen")

frame = ctk.CTkFrame(master=app)
frame.pack(pady=20, padx=40, fill="both", expand=True)

label = ctk.CTkLabel(master=frame, text="Open Settings Screen")
label.pack(pady=12, padx=10)

button = ctk.CTkButton(
    master=frame,
    text="Open Settings",
    bg_color="transparent",
    fg_color="transparent",
    command=next_screen,
)
button.pack(pady=12, padx=10)

app.mainloop()
