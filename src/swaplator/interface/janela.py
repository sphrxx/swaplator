import customtkinter as ctk

from swaplator.interface.conversor_view import ConversorView
from swaplator.interface.sidebar import Sidebar
from swaplator.conversores.comprimento import FATORES_COMPRIMENTO
from swaplator.conversores.area import FATORES_AREA
from swaplator.conversores.massa import FATORES_MASSA
from swaplator.conversores.volume import FATORES_VOLUME


FATORES_CONVERSAO = {
    "comprimento": FATORES_COMPRIMENTO,
    "area": FATORES_AREA,
    "massa": FATORES_MASSA,
    "volume": FATORES_VOLUME
}

class Janela:
    
    def __init__(self):
        self.janela = ctk.CTk()

        self.configurar_janela()
        self.criar_widgets()
        self.configurar_layout()
        

    def configurar_janela(self):
        self.janela.geometry("800x600")
        self.janela.title("Swaplator")

        self.janela.grid_rowconfigure(0, weight=1)
        self.janela.grid_columnconfigure(0, weight=0)
        self.janela.grid_columnconfigure(1, weight=1)


    def criar_widgets(self):
        self.sidebar = Sidebar(
            self.janela,
            self.selecionar_conversao
        )

        self.frame_conteudo = ctk.CTkFrame(self.janela)

        self.conversor_atual = ConversorView(
            self.frame_conteudo,
            FATORES_CONVERSAO["comprimento"]
        )

    def configurar_layout(self):
        self.frame_conteudo.grid_rowconfigure(0, weight=1)
        self.frame_conteudo.grid_columnconfigure(0, weight=1)
        self.frame_conteudo.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")


    def selecionar_conversao(self, tipo_conversao):
        if self.conversor_atual is not None:
            self.conversor_atual.frame.destroy()

        fatores = FATORES_CONVERSAO[tipo_conversao]

        self.conversor_atual = ConversorView(
            self.frame_conteudo,
            fatores
        )


    def iniciar(self):
        self.janela.mainloop()