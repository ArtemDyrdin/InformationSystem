import tkinter as tk
from tkinter import messagebox
from db import fetch_all_countries, insert_country, update_country, delete_country

class CountryFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack()

        self.listbox = tk.Listbox(self, width=50)
        self.listbox.pack()
        self.listbox.bind("<<ListboxSelect>>", self.on_select)

        self.entry_name = tk.Entry(self, width=50)
        self.entry_name.pack()

        self.btn_add = tk.Button(self, text="Добавить страну", command=self.add_country)
        self.btn_add.pack()
        self.btn_edit = tk.Button(self, text="Редактировать", command=self.edit_country)
        self.btn_edit.pack()
        self.btn_delete = tk.Button(self, text="Удалить", command=self.delete_country)
        self.btn_delete.pack()

        self.selected_id = None
        self.refresh_list()

    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        for row in fetch_all_countries():
            self.listbox.insert(tk.END, f"{row[0]} | {row[1]}")

    def on_select(self, event):
        if not self.listbox.curselection():
            return
        index = self.listbox.curselection()[0]
        data = fetch_all_countries()[index]
        self.selected_id = data[0]
        self.entry_name.delete(0, tk.END)
        self.entry_name.insert(0, data[1])

    def add_country(self):
        insert_country(self.entry_name.get())
        self.refresh_list()

    def edit_country(self):
        if self.selected_id is None:
            return
        update_country(self.selected_id, self.entry_name.get())
        self.refresh_list()

    def delete_country(self):
        if self.selected_id is None:
            return
        delete_country(self.selected_id)
        self.refresh_list()
