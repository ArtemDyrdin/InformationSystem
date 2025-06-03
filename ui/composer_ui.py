import tkinter as tk
from tkinter import ttk, messagebox
import models.composer_model as composer_model
from forms.composer_form import open_composer_form

class ComposerUI(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(self, columns=("id", "Имя", "Фамилия", "Отчество", "Дата рождения", "Дата смерти"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
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
        for row in composer_model.get_all_composers():
            self.tree.insert("", tk.END, values=row)

    def get_selected(self):
        selected = self.tree.selection()
        if not selected:
            return None
        values = self.tree.item(selected[0], "values")
        return {
            "id": values[0],
            "first_name": values[1],
            "last_name": values[2],
            "middle_name": values[3],
            "birth_date": values[4],
            "death_date": values[5],
        }

    def add(self):
        open_composer_form(self, self.refresh)

    def edit(self):
        selected = self.get_selected()
        if selected:
            open_composer_form(self, self.refresh, selected)
        else:
            messagebox.showinfo("Выбор", "Выберите композитора для редактирования")

    def delete(self):
        selected = self.get_selected()
        if selected:
            confirm = messagebox.askyesno("Удаление", "Удалить композитора?")
            if confirm:
                composer_model.delete_composer(selected["id"])
                self.refresh()
