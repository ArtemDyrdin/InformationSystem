import tkinter as tk
from tkinter import messagebox
import models.genre_model as genre_model

def open_genre_form(parent, refresh_callback, genre=None):
    dialog = tk.Toplevel(parent)
    dialog.title("Редактировать жанр" if genre else "Добавить жанр")

    tk.Label(dialog, text="Название жанра").grid(row=0, column=0)
    entry = tk.Entry(dialog)
    entry.grid(row=0, column=1)

    if genre:
        entry.insert(0, genre["name"])

    def save():
        name = entry.get()
        if not name.strip():
            messagebox.showwarning("Ошибка", "Название не может быть пустым")
            return
        try:
            if genre:
                genre_model.update_genre(genre["id"], name)
            else:
                genre_model.add_genre(name)
            refresh_callback()
            dialog.destroy()
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    tk.Button(dialog, text="Сохранить", command=save).grid(row=1, columnspan=2)
