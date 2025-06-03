import tkinter as tk
from tkinter import ttk, messagebox
import models.repository_model as repo_model
from forms.repository_form import open_repository_form

# Сопоставления для перевода значений из БД в отображаемые и обратно
REPO_TYPE_LABELS = {
    'library': 'Библиотека',
    'museum': 'Музей',
    'private': 'Частная коллекция'
}
REPO_TYPE_LABELS_REVERSE = {v: k for k, v in REPO_TYPE_LABELS.items()}

class RepositoryUI(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(self, columns=("id", "name", "type"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Название хранилища")
        self.tree.heading("type", text="Тип")
        self.tree.column("id", width=50)
        self.tree.column("name", width=200)
        self.tree.column("type", width=150)
        self.tree.pack(fill=tk.BOTH, expand=True)

        btns = tk.Frame(self)
        btns.pack(fill=tk.X)
        tk.Button(btns, text="Добавить", command=self.add).pack(side=tk.LEFT)
        tk.Button(btns, text="Изменить", command=self.edit).pack(side=tk.LEFT)
        tk.Button(btns, text="Удалить", command=self.delete).pack(side=tk.LEFT)
        tk.Button(btns, text="Обновить", command=self.refresh).pack(side=tk.LEFT)

        self.refresh()

    def refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for row in repo_model.get_all_repositories():
            # row = (id, type, name)
            type_label = REPO_TYPE_LABELS.get(row[1], row[1])
            self.tree.insert("", tk.END, values=(row[0], row[2], type_label))

    def get_selected(self):
        selected = self.tree.selection()
        if not selected:
            return None
        values = self.tree.item(selected[0], "values")
        return {
            "id": values[0],
            "name": values[1],
            "type": REPO_TYPE_LABELS_REVERSE.get(values[1], values[1])
        }


    def add(self):
        open_repository_form(self, self.refresh)

    def edit(self):
        selected = self.get_selected()
        if selected:
            open_repository_form(self, self.refresh, selected)
        else:
            messagebox.showinfo("Выбор", "Выберите хранилище для редактирования")

    def delete(self):
        selected = self.get_selected()
        if selected:
            confirm = messagebox.askyesno("Удаление", "Удалить хранилище?")
            if confirm:
                repo_model.delete_repository(selected["id"])
                self.refresh()
