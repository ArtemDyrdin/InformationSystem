import tkinter as tk
from ui.composer_ui import ComposerUI
from ui.country_ui import CountryUI
from ui.genre_ui import GenreUI
from ui.repository_ui import RepositoryUI

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Музыкальная информационная система")
        self.geometry("1200x500")

        notebook = tk.ttk.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True)

        notebook.add(ComposerUI(notebook), text="Композиторы")
        notebook.add(CountryUI(notebook), text="Страны")
        notebook.add(GenreUI(notebook), text="Жанры")
        notebook.add(RepositoryUI(notebook), text="Хранилища")

if __name__ == "__main__":
    MainApp().mainloop()
