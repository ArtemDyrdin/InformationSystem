import tkinter as tk
from tkinter import ttk, messagebox
import models.country_model as country_model
from forms.country_form import open_country_form

class CountryUI(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(self, columns=("id", "name"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Название страны")
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
        for row in country_model.get_all_countries():
            self.tree.insert("", tk.END, values=row)

    def get_selected(self):
        selected = self.tree.selection()
        if not selected:
            return None
        values = self.tree.item(selected[0], "values")
        return {
            "id": values[0],
            "name": values[1],
        }

    def add(self):
        open_country_form(self, self.refresh)

    def edit(self):
        selected = self.get_selected()
        if selected:
            open_country_form(self, self.refresh, selected)
        else:
            messagebox.showinfo("Выбор", "Выберите страну для редактирования")

    def delete(self):
        selected = self.get_selected()
        if selected:
            confirm = messagebox.askyesno("Удаление", "Удалить страну?")
            if confirm:
                country_model.delete_country(selected["id"])
                self.refresh()
