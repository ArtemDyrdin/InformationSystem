import tkinter as tk
from db import (
    fetch_all_composers_short,
    fetch_all_countries_short,
    fetch_countries_by_composer,
    set_composer_countries
)

class ComposerCountryFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack()

        self.composer_list = fetch_all_composers_short()
        self.composer_var = tk.StringVar()

        if self.composer_list:
            composer_options = [f"{c[0]} | {c[1]}" for c in self.composer_list]
            self.composer_var.set(composer_options[0])  # Устанавливаем значение по умолчанию

            # ПРАВИЛЬНЫЙ вызов OptionMenu: передаем сначала выбранное значение
            self.composer_menu = tk.OptionMenu(
                self, self.composer_var,
                *composer_options
            )
            self.composer_menu.pack()

            # Привязываем обработчик изменения выбора
            self.composer_var.trace_add("write", self.on_composer_select)
        else:
            tk.Label(self, text="Нет композиторов в базе данных.").pack()
            return

        # Страны (чекбоксы)
        self.country_list = fetch_all_countries_short()
        self.country_vars = {}
        for cid, name in self.country_list:
            var = tk.IntVar()
            chk = tk.Checkbutton(self, text=name, variable=var)
            chk.pack(anchor='w')
            self.country_vars[cid] = var

        # Кнопка сохранения
        self.save_btn = tk.Button(self, text="Сохранить связь", command=self.save_links)
        self.save_btn.pack()

        self.selected_composer_id = None
        self.on_composer_select()

    def on_composer_select(self, *args):
        selected = self.composer_var.get()
        if not selected:
            return
        try:
            self.selected_composer_id = int(selected.split(" | ")[0])
        except ValueError:
            return

        linked_ids = fetch_countries_by_composer(self.selected_composer_id)
        for cid in self.country_vars:
            self.country_vars[cid].set(1 if cid in linked_ids else 0)

    def save_links(self):
        if self.selected_composer_id is None:
            return
        selected_country_ids = [cid for cid, var in self.country_vars.items() if var.get() == 1]
        set_composer_countries(self.selected_composer_id, selected_country_ids)
