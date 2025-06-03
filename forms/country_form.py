import tkinter as tk
from tkinter import messagebox
import models.country_model as country_model

def open_country_form(parent, refresh_callback, country=None):
    dialog = tk.Toplevel(parent)
    dialog.title("Редактировать страну" if country else "Добавить страну")

    tk.Label(dialog, text="Название страны").grid(row=0, column=0)
    entry = tk.Entry(dialog)
    entry.grid(row=0, column=1)

    if country:
        entry.insert(0, country["name"])

    def save():
        name = entry.get()
        if not name.strip():
            messagebox.showwarning("Ошибка", "Название не может быть пустым")
            return
        try:
            if country:
                country_model.update_country(country["id"], name)
            else:
                country_model.add_country(name)
            refresh_callback()
            dialog.destroy()
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    tk.Button(dialog, text="Сохранить", command=save).grid(row=1, columnspan=2)
