import tkinter as tk
from tkinter import messagebox
from db import (
    fetch_all_works,
    insert_work,
    update_work,
    delete_work,
    fetch_all_genres_short,
    fetch_all_composers_short
)

class WorkFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack()

        # Заголовок
        tk.Label(self, text="Произведения", font=("Arial", 16)).pack()

        # Список всех произведений
        self.work_listbox = tk.Listbox(self, width=70)
        self.work_listbox.pack()
        self.work_listbox.bind("<<ListboxSelect>>", self.on_select)

        # Поля ввода
        self.title_entry = self._labeled_entry("Название произведения:")
        self.year_entry = self._labeled_entry("Год написания:")

       # Жанры
        self.genre_list = fetch_all_genres_short()
        genre_options = [f"{g[0]} | {g[1]}" for g in self.genre_list]
        self.genre_var = tk.StringVar()

        tk.Label(self, text="Жанр:").pack()

        if genre_options:
            self.genre_var.set(genre_options[0])
            self.genre_menu = tk.OptionMenu(self, self.genre_var, *genre_options)
        else:
            self.genre_var.set("Нет жанров")
            self.genre_menu = tk.OptionMenu(self, self.genre_var, "Нет жанров")

        self.genre_menu.pack()


        # Композиторы
        self.composer_list = fetch_all_composers_short()
        composer_options = [f"{c[0]} | {c[1]}" for c in self.composer_list]
        self.composer_var = tk.StringVar()

        tk.Label(self, text="Композитор:").pack()

        if composer_options:
            self.composer_var.set(composer_options[0])
            self.composer_menu = tk.OptionMenu(self, self.composer_var, *composer_options)
        else:
            self.composer_var.set("Нет композиторов")
            self.composer_menu = tk.OptionMenu(self, self.composer_var, "Нет композиторов")

        self.composer_menu.pack()


        # Кнопки
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Добавить", command=self.add_work).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Обновить", command=self.update_work).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Удалить", command=self.delete_work).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Очистить", command=self.clear_fields).pack(side="left", padx=5)

        # Текущий выбранный ID
        self.selected_work_id = None

        # Обновить список
        self.refresh_list()

    def _labeled_entry(self, label_text):
        tk.Label(self, text=label_text).pack()
        entry = tk.Entry(self)
        entry.pack()
        return entry

    def refresh_list(self):
        self.work_listbox.delete(0, tk.END)
        for w in fetch_all_works():
            self.work_listbox.insert(tk.END, f"{w[0]} | {w[1]} ({w[2]})")

    def clear_fields(self):
        self.title_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)
        if self.genre_list:
            genre_options = [f"{g[0]} | {g[1]}" for g in self.genre_list]
            self.genre_var.set(genre_options[0])
        if self.composer_list:
            composer_options = [f"{c[0]} | {c[1]}" for c in self.composer_list]
            self.composer_var.set(composer_options[0])
        self.selected_work_id = None
        self.work_listbox.selection_clear(0, tk.END)

    def on_select(self, event):
        if not self.work_listbox.curselection():
            return
        index = self.work_listbox.curselection()[0]
        selected_text = self.work_listbox.get(index)
        self.selected_work_id = int(selected_text.split(" | ")[0])

        works = fetch_all_works()
        for w in works:
            if w[0] == self.selected_work_id:
                self.title_entry.delete(0, tk.END)
                self.title_entry.insert(0, w[1])
                self.year_entry.delete(0, tk.END)
                self.year_entry.insert(0, str(w[2]))

                # Найдём полную строку для выпадающих списков
                for comp in self.composer_list:
                    if comp[1] == w[3]:
                        self.composer_var.set(f"{comp[0]} | {comp[1]}")
                        break
                for gen in self.genre_list:
                    if gen[1] == w[4]:
                        self.genre_var.set(f"{gen[0]} | {gen[1]}")
                        break
                break

    def add_work(self):
        title = self.title_entry.get().strip()
        year = self.year_entry.get().strip()
        if not title or not year.isdigit():
            messagebox.showerror("Ошибка", "Введите корректные данные.")
            return
        composer_id = int(self.composer_var.get().split(" | ")[0])
        genre_id = int(self.genre_var.get().split(" | ")[0])
        insert_work(title, int(year), composer_id, genre_id)
        self.refresh_list()
        self.clear_fields()

    def update_work(self):
        if self.selected_work_id is None:
            messagebox.showwarning("Внимание", "Выберите произведение для обновления.")
            return
        title = self.title_entry.get().strip()
        year = self.year_entry.get().strip()
        if not title or not year.isdigit():
            messagebox.showerror("Ошибка", "Введите корректные данные.")
            return
        composer_id = int(self.composer_var.get().split(" | ")[0])
        genre_id = int(self.genre_var.get().split(" | ")[0])
        update_work(self.selected_work_id, title, int(year), composer_id, genre_id)
        self.refresh_list()
        self.clear_fields()

    def delete_work(self):
        if self.selected_work_id is None:
            messagebox.showwarning("Внимание", "Выберите произведение для удаления.")
            return
        delete_work(self.selected_work_id)
        self.refresh_list()
        self.clear_fields()
