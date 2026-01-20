import tkinter as tk
from tkinter import messagebox
import sqlite3
import random

# ---------------- Database ----------------
conn = sqlite3.connect("passwords.db")
cursor = conn.cursor()
cursor.execute(
    "CREATE TABLE IF NOT EXISTS passwords (key TEXT PRIMARY KEY, password TEXT)"
)
conn.commit()

chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890@#!$&"

# ---------------- App Window ----------------
root = tk.Tk()
root.title("Password Manager")
root.geometry("900x500")
root.configure(bg="#121212")
root.resizable(False, False)

FONT_TITLE = ("Segoe UI", 18, "bold")
FONT = ("Segoe UI", 11)
FONT_BTN = ("Segoe UI", 10, "bold")

# ---------------- Helpers ----------------
def clear_center():
    for widget in center.winfo_children():
        widget.destroy()

def refresh_saved():
    saved_box.delete(1.0, tk.END)
    cursor.execute("SELECT * FROM passwords")
    rows = cursor.fetchall()
    if not rows:
        saved_box.insert(tk.END, "No passwords saved\n")
    else:
        for k, p in rows:
            saved_box.insert(tk.END, f"{k} → {p}\n")

def back_button():
    tk.Button(
        center, text="← Back",
        command=show_home,
        bg="#2a2a2a", fg="white",
        activebackground="#3a3a3a",
        font=FONT_BTN, bd=0, padx=12, pady=6
    ).pack(anchor="w", pady=5, padx=5)

def entry(label):
    tk.Label(center, text=label, bg="#1e1e1e",
             fg="#bbbbbb", font=FONT).pack(pady=(10, 2))
    e = tk.Entry(center, width=35)
    e.pack(ipady=5)
    return e

def btn(text, command):
    tk.Button(
        center, text=text, command=command,
        bg="#2a2a2a", fg="white",
        activebackground="#3a3a3a",
        font=FONT_BTN, width=28, bd=0, pady=8
    ).pack(pady=6)

# ---------------- Screens ----------------
def show_home():
    clear_center()

    tk.Label(center, text="Welcome to Password Manager",
             bg="#1e1e1e", fg="white",
             font=FONT_TITLE).pack(pady=30)

    btn("Generate Password", show_generate)
    btn("Save Your Own Password", show_save)
    btn("Update Saved Password", show_update)
    btn("Delete Saved Password", show_delete)

def show_generate():
    clear_center()
    back_button()

    tk.Label(center, text="Generate Password",
             bg="#1e1e1e", fg="white",
             font=FONT_TITLE).pack(pady=15)

    length_entry = entry("Password Length")
    key_entry = entry("Key")

    def generate():
        try:
            length = int(length_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Enter valid length")
            return
        pwd = "".join(random.choice(chars) for _ in range(length))
        pwd_entry.delete(0, tk.END)
        pwd_entry.insert(0, pwd)

    btn("Generate", generate)

    pwd_entry = entry("Generated Password")

    def save():
        if not key_entry.get() or not pwd_entry.get():
            return
        cursor.execute(
            "INSERT OR REPLACE INTO passwords VALUES (?, ?)",
            (key_entry.get(), pwd_entry.get())
        )
        conn.commit()
        refresh_saved()
        messagebox.showinfo("Saved", "Password saved")

    btn("Save Password", save)

def show_save():
    clear_center()
    back_button()

    tk.Label(center, text="Save Your Own Password",
             bg="#1e1e1e", fg="white",
             font=FONT_TITLE).pack(pady=15)

    key_entry = entry("Key")
    pwd_entry = entry("Password")

    def save():
        cursor.execute(
            "INSERT OR REPLACE INTO passwords VALUES (?, ?)",
            (key_entry.get(), pwd_entry.get())
        )
        conn.commit()
        refresh_saved()
        messagebox.showinfo("Saved", "Password saved")

    btn("Save", save)

def show_update():
    clear_center()
    back_button()

    tk.Label(center, text="Update Password",
             bg="#1e1e1e", fg="white",
             font=FONT_TITLE).pack(pady=15)

    key_entry = entry("Key")
    pwd_entry = entry("New Password")

    def update():
        cursor.execute(
            "REPLACE INTO passwords VALUES (?, ?)",
            (key_entry.get(), pwd_entry.get())
        )
        conn.commit()
        refresh_saved()
        messagebox.showinfo("Updated", "Password updated")

    btn("Update", update)

def show_delete():
    clear_center()
    back_button()

    tk.Label(center, text="Delete Saved Password",
             bg="#1e1e1e", fg="white",
             font=FONT_TITLE).pack(pady=15)

    key_entry = entry("Key to Delete")

    def delete():
        cursor.execute(
            "DELETE FROM passwords WHERE key = ?",
            (key_entry.get(),)
        )
        conn.commit()
        refresh_saved()
        messagebox.showinfo("Deleted", "Password deleted")

    btn("Delete", delete)

# ---------------- Layout ----------------
left = tk.Frame(root, bg="#1e1e1e")
left.pack(side="left", fill="both", expand=True)

right = tk.Frame(root, bg="#181818", width=300)
right.pack(side="right", fill="y")

center = tk.Frame(left, bg="#1e1e1e")
center.pack(expand=True)

# ---------------- Saved Panel ----------------
tk.Label(right, text="Saved Passwords",
         bg="#181818", fg="white",
         font=("Segoe UI", 14, "bold")).pack(pady=10)

saved_box = tk.Text(
    right, bg="#101010", fg="#00ffcc",
    font=("Consolas", 10),
    width=32, height=22, bd=0
)
saved_box.pack(padx=10)

refresh_saved()
show_home()

root.mainloop()
# ---------------- Signature ----------------
try:
    signature_img = Image.open("Signature.jpg")
    signature_img = signature_img.resize((140, 50))  # adjust if needed
    signature_photo = ImageTk.PhotoImage(signature_img)

    signature_label = tk.Label(
        root,
        image=signature_photo,
        bg="#121212",
        bd=0
    )
    signature_label.image = signature_photo
    signature_label.place(
        relx=1.0, rely=1.0,
        anchor="se",
        x=-15, y=-15
    )
except Exception as e:
    print("Signature image not loaded:", e)
