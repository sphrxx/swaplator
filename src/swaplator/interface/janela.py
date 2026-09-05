import customtkinter as ctk

from swaplator.interface.conversor_view import ConversorView
from swaplator.interface.calculadora_view import CalculadoraView
from swaplator.interface.conversor_moedas_view import ConversorMoedasView
from swaplator.interface.sidebar import Sidebar
from swaplator.conversores.comprimento import conversao_comprimento, FATORES_COMPRIMENTO
from swaplator.conversores.area import conversao_area, FATORES_AREA
from swaplator.conversores.massa import conversao_massa, FATORES_MASSA
from swaplator.conversores.volume import conversao_volume, FATORES_VOLUME
from swaplator.conversores.temperatura import conversao_temperatura, UNIDADES_TEMPERATURA
from swaplator.conversores.moedas import converter_moedas, obter_cotacoes


CONVERSOES = {
    "comprimento": (conversao_comprimento, FATORES_COMPRIMENTO),
    "area": (conversao_area, FATORES_AREA),
    "massa": (conversao_massa, FATORES_MASSA),
    "volume": (conversao_volume, FATORES_VOLUME),
    "temperatura": (conversao_temperatura, UNIDADES_TEMPERATURA)
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
            self.selecionar_view
        )

        self.frame_conteudo = ctk.CTkFrame(self.janela)

        self.view_atual = ConversorView(
            self.frame_conteudo,
            conversao_comprimento,
            FATORES_COMPRIMENTO
        )


    def configurar_layout(self):
        self.frame_conteudo.grid_rowconfigure(0, weight=1)
        self.frame_conteudo.grid_columnconfigure(0, weight=1)
        self.frame_conteudo.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")


    def selecionar_view(self, view):
        if self.view_atual is not None:
            self.view_atual.frame.destroy()

        if view in CONVERSOES:
            funcao_conversao, unidades = CONVERSOES[view]

            self.view_atual = ConversorView(
                self.frame_conteudo,
                funcao_conversao,
                unidades
            )

        elif view == "moedas":
            self.view_atual = ConversorMoedasView(self.frame_conteudo, converter_moedas, obter_cotacoes)

        elif view == "calculadora":
            self.view_atual = CalculadoraView(self.frame_conteudo)


    def iniciar(self):
        self.janela.mainloop()