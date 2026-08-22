import customtkinter as ctk

from swaplator.interface.conversor_view import ConversorView


janela = ctk.CTk()
janela.geometry("800x600")
janela.title("Swaplator")

janela.grid_rowconfigure(0, weight=1)
janela.grid_columnconfigure(0, weight=1)

conversor = ConversorView(janela)

janela.mainloop()