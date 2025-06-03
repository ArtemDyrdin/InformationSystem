import tkinter as tk
from tkinter import messagebox
import models.composer_model as composer_model

def open_composer_form(parent, refresh_callback, composer=None):
    dialog = tk.Toplevel(parent)
    dialog.title("Редактировать композитора" if composer else "Добавить композитора")

    fields = ["Имя", "Фамилия", "Отчество", "Дата рождения", "Дата смерти"]
    entries = {}

    for i, label in enumerate(fields):
        tk.Label(dialog, text=label).grid(row=i, column=0)
        entry = tk.Entry(dialog)
        entry.grid(row=i, column=1)
        entries[label] = entry

    if composer:
        for key, entry in zip(fields, entries.values()):
            entry.insert(0, composer[keys_to_columns[key]])

    def save():
        values = [entries[f].get() or None for f in fields]
        try:
            if composer:
                composer_model.update_composer(composer["id"], *values)
            else:
                composer_model.add_composer(*values)
            refresh_callback()
            dialog.destroy()
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    tk.Button(dialog, text="Сохранить", command=save).grid(row=len(fields), columnspan=2)

keys_to_columns = {
    "Имя": "first_name",
    "Фамилия": "last_name",
    "Отчество": "middle_name",
    "Дата рождения": "birth_date",
    "Дата смерти": "death_date"
}
