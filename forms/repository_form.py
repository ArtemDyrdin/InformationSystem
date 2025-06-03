import tkinter as tk
from tkinter import messagebox
import models.repository_model as repo_model

# Отображаемое имя → значение в БД
REPO_TYPE_CHOICES = {
    "Библиотека": "library",
    "Музей": "museum",
    "Частная коллекция": "private"
}
# Обратный словарь: значение из БД → отображаемое имя
REPO_TYPE_LABELS = {v: k for k, v in REPO_TYPE_CHOICES.items()}

def open_repository_form(parent, refresh_callback, repo=None):
    dialog = tk.Toplevel(parent)
    dialog.title("Редактировать хранилище" if repo else "Добавить хранилище")

    tk.Label(dialog, text="Название хранилища").grid(row=0, column=0, padx=5, pady=5)
    name_entry = tk.Entry(dialog)
    name_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(dialog, text="Тип хранилища").grid(row=1, column=0, padx=5, pady=5)
    type_var = tk.StringVar(dialog)
    type_menu = tk.OptionMenu(dialog, type_var, *REPO_TYPE_CHOICES.keys())
    type_menu.grid(row=1, column=1, padx=5, pady=5)

    if repo:
        name_entry.insert(0, repo["name"])
        type_label = REPO_TYPE_LABELS.get(repo["type"], list(REPO_TYPE_CHOICES.keys())[0])
        type_var.set(type_label)
    else:
        type_var.set(list(REPO_TYPE_CHOICES.keys())[0])

    def save():
        name = name_entry.get().strip()
        selected_label = type_var.get()
        db_type_value = REPO_TYPE_CHOICES[selected_label]

        if not name:
            messagebox.showwarning("Ошибка", "Название не может быть пустым")
            return

        try:
            if repo:
                repo_model.update_repository(repo["id"], name, db_type_value)
            else:
                repo_model.add_repository(name, db_type_value)
            refresh_callback()
            dialog.destroy()
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    tk.Button(dialog, text="Сохранить", command=save).grid(row=2, columnspan=2, pady=10)
