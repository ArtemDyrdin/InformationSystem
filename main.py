import tkinter as tk
from gui.composer_frame import ComposerFrame
from gui.country_frame import CountryFrame
from gui.composer_country_frame import ComposerCountryFrame
from gui.work_frame import WorkFrame

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Музыкальная база данных")

        self.menu = tk.Menu(self)
        self.config(menu=self.menu)

        self.frame = None

        self.data_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Таблицы", menu=self.data_menu)
        self.data_menu.add_command(label="Композиторы", command=self.show_composers)
        self.data_menu.add_command(label="Страны", command=self.show_countries)
        self.data_menu.add_command(label="Связь Композитор–Страна", command=self.show_composer_country)
        self.data_menu.add_command(label="Произведения", command=self.show_work_frame)

        self.show_composers()

        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.current_frame = None

    def clear_frame(self):
        if self.frame:
            self.frame.destroy()

    def show_composers(self):
        self.clear_frame()
        self.frame = ComposerFrame(self)
        self.frame.pack()

    def show_countries(self):
        self.clear_frame()
        self.frame = CountryFrame(self)
        self.frame.pack()

    def show_composer_country(self):
        self.clear_frame()
        self.frame = ComposerCountryFrame(self)
        self.frame.pack()

    def show_work_frame(self):
        self.clear_current_frame()
        self.current_frame = WorkFrame(self.container)
        self.current_frame.pack(fill="both", expand=True)

    def clear_current_frame(self):
        if self.current_frame is not None:
            self.current_frame.destroy()
            self.current_frame = None

if __name__ == "__main__":
    app = App()
    app.mainloop()
