import customtkinter as ctk

from swaplator.interface.conversor_view import ConversorView
from swaplator.conversores.comprimento import FATORES_COMPRIMENTO
from swaplator.conversores.area import FATORES_AREA


janela = ctk.CTk()
janela.geometry("800x600")
janela.title("Swaplator")

janela.grid_rowconfigure(0, weight=1)
janela.grid_columnconfigure(0, weight=1)

conversor = ConversorView(
    janela,
    FATORES_COMPRIMENTO
)

janela.mainloop()