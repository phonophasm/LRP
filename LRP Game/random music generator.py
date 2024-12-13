import random
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

def generate_random_key():
    keys = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    modes = [
        "Major", "Minor", "Dorian", "Phrygian", "Lydian", "Mixolydian", "Locrian", 
        "Harmonic Minor", "Melodic Minor", "Pentatonic Major", "Pentatonic Minor", "Blues"
    ]
    
    random_key = random.choice(keys)
    random_mode = random.choice(modes)
    
    return f"{random_key} {random_mode}"

def generate_random_style():
    styles = [
        "Jazz",
        "Blues",
        "Rock",
        "Classical",
        "Pop",
        "Funk",
        "Electronic",
        "Hip-Hop",
        "Reggae",
        "Folk",
        "Country",
        "Ambient",
        "Metal",
        "Latin",
        "Soul",
    ]
    
    return random.choice(styles)

def get_random_image():
    image_folder = "images"  # Folder containing images
    images = os.listdir(image_folder)
    random_image = random.choice(images)
    return os.path.join(image_folder, random_image)

def display_random_selection():
    key = generate_random_key()
    style = generate_random_style()

    # Get a random image
    image_path = get_random_image()
    img = Image.open(image_path)
    img = img.resize((200, 200), Image.LANCZOS)  # Updated to use LANCZOS
    img = ImageTk.PhotoImage(img)

    # Create a new window to display results
    result_window = tk.Toplevel()
    result_window.title("Random Music Generator")
    result_window.geometry("300x400")
    result_window.configure(bg="black")

    # Display text
    text_label = tk.Label(result_window, text=f"Key: {key}\nStyle: {style}", font=("Helvetica", 16), bg="black", fg="white")
    text_label.pack(pady=10)

    # Display image
    image_label = tk.Label(result_window, image=img, bg="black")
    image_label.image = img  # Keep a reference to avoid garbage collection
    image_label.pack(pady=10)

def main():
    # Create the main window
    root = tk.Tk()
    root.title("Random Music Generator")
    root.geometry("300x200")
    root.configure(bg="black")

    # Create and pack widgets
    label = tk.Label(root, text="Welcome to the Random Music Generator!", font=("Helvetica", 12), bg="black", fg="white")
    label.pack(pady=20)

    generate_button = tk.Button(
        root, 
        text="Generate Random Music", 
        command=display_random_selection, 
        font=("Helvetica", 10), 
        bg="#333333", 
        fg="white",
        activebackground="#444444", 
        highlightbackground="#333333"
    )
    generate_button.pack(pady=10)

    exit_button = tk.Button(
        root, 
        text="Exit", 
        command=root.destroy, 
        font=("Helvetica", 10), 
        bg="#333333", 
        fg="white", 
        activebackground="#444444", 
        highlightbackground="#333333"
    )
    exit_button.pack(pady=10)

    # Run the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    main()
