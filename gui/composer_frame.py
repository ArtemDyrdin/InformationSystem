import tkinter as tk
from tkinter import messagebox
from db import fetch_all_composers, insert_composer, update_composer, delete_composer

class ComposerFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack()

        self.listbox = tk.Listbox(self, width=80)
        self.listbox.pack()
        self.listbox.bind("<<ListboxSelect>>", self.on_select)

        self.entry_name = tk.Entry(self)
        self.entry_name.pack()
        self.entry_birth = tk.Entry(self)
        self.entry_birth.pack()
        self.entry_death = tk.Entry(self)
        self.entry_death.pack()

        self.btn_add = tk.Button(self, text="Добавить", command=self.add_composer)
        self.btn_add.pack()
        self.btn_edit = tk.Button(self, text="Редактировать", command=self.edit_composer)
        self.btn_edit.pack()
        self.btn_delete = tk.Button(self, text="Удалить", command=self.delete_composer)
        self.btn_delete.pack()

        self.selected_id = None
        self.refresh_list()

    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        for row in fetch_all_composers():
            self.listbox.insert(tk.END, f"{row[0]} | {row[1]} | {row[2]}–{row[3]}")

    def on_select(self, event):
        if not self.listbox.curselection():
            return
        index = self.listbox.curselection()[0]
        data = fetch_all_composers()[index]
        self.selected_id = data[0]
        self.entry_name.delete(0, tk.END)
        self.entry_name.insert(0, data[1])
        self.entry_birth.delete(0, tk.END)
        self.entry_birth.insert(0, data[2])
        self.entry_death.delete(0, tk.END)
        self.entry_death.insert(0, data[3])

    def add_composer(self):
        insert_composer(
            self.entry_name.get(),
            self.entry_birth.get(),
            self.entry_death.get()
        )
        self.refresh_list()

    def edit_composer(self):
        if self.selected_id is None:
            return
        update_composer(
            self.selected_id,
            self.entry_name.get(),
            self.entry_birth.get(),
            self.entry_death.get()
        )
        self.refresh_list()

    def delete_composer(self):
        if self.selected_id is None:
            return
        delete_composer(self.selected_id)
        self.refresh_list()
