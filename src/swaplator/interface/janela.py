import customtkinter as ctk

from swaplator.interface.conversor_view import ConversorView
from swaplator.interface.calculadora_view import CalculadoraView
from swaplator.interface.conversor_moedas_view import ConversorMoedasView
from swaplator.interface.sidebar import Sidebar
from swaplator.interface import tema
from swaplator.conversores.registro import CONVERSOES
from swaplator.conversores.moedas import converter_moedas, obter_cotacoes

class Janela:
    
    def __init__(self):
        tema.aplicar_tema()
        self.janela = ctk.CTk()

        self.configurar_janela()
        self.criar_widgets()
        self.configurar_layout()
        

    def configurar_janela(self):
        # Tamanho preferido, mas limitado ao espaço real da tela. A escala (125%,
        # 150%...) converte os pixels da tela nas unidades que o geometry() usa.
        escala = ctk.ScalingTracker.get_window_scaling(self.janela)
        largura, altura = tema.tamanho_inicial_janela(
            self.janela.winfo_screenwidth(),
            self.janela.winfo_screenheight(),
            escala
        )

        self.janela.geometry(f"{largura}x{altura}")
        # Sem um mínimo, dá para encolher a janela até cortar os botões.
        self.janela.minsize(tema.JANELA_LARGURA_MINIMA, tema.JANELA_ALTURA_MINIMA)
        self.janela.title("Swaplator")
        self.janela.configure(fg_color=tema.COR_FUNDO)

        self.janela.grid_rowconfigure(0, weight=1)
        self.janela.grid_columnconfigure(0, weight=0)
        self.janela.grid_columnconfigure(1, weight=1)


    def criar_widgets(self):
        self.sidebar = Sidebar(
            self.janela,
            self.selecionar_view
        )

        self.sidebar.marcar_ativo("calculadora")

        self.frame_conteudo = ctk.CTkFrame(self.janela, fg_color=tema.COR_FUNDO)

        # O app abre na calculadora conversora (que começa em Comprimento).
        self.view_atual = CalculadoraView(self.frame_conteudo)


    def configurar_layout(self):
        self.frame_conteudo.grid_rowconfigure(0, weight=1)
        self.frame_conteudo.grid_columnconfigure(0, weight=1)
        self.frame_conteudo.grid(row=0, column=1, padx=tema.ESPACO, pady=tema.ESPACO, sticky="nsew")


    def selecionar_view(self, view):
        self.sidebar.marcar_ativo(view)

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