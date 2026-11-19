import customtkinter as ctk

from swaplator.interface import tema


# (nome interno da tela, texto exibido no botão), na ordem em que aparecem.
ITENS = [
    ("comprimento", "Comprimento"),
    ("area", "Área"),
    ("massa", "Massa"),
    ("volume", "Volume"),
    ("temperatura", "Temperatura"),
    ("calculadora", "Calculadora"),
    ("moedas", "Moedas"),
]


class Sidebar:

    def __init__(self, master, selecionar_view):
        self.frame = ctk.CTkFrame(
            master,
            fg_color=tema.COR_SUPERFICIE,
            corner_radius=tema.RAIO_CARTAO
        )

        self.selecionar_view = selecionar_view

        self.criar_widgets()
        self.configurar_layout()


    def criar_widgets(self):
        self.label_titulo = ctk.CTkLabel(
            self.frame,
            text="Swaplator",
            font=tema.fonte(tema.TAM_GRANDE, "bold"),
            text_color=tema.COR_TEXTO
        )

        self.botoes = {}

        for view, texto in ITENS:
            self.botoes[view] = ctk.CTkButton(
                self.frame,
                text=texto,
                width=180,
                anchor="w",
                fg_color="transparent",
                hover_color=tema.COR_DIGITO,
                text_color=tema.COR_TEXTO,
                font=tema.fonte(tema.TAM_TEXTO),
                corner_radius=tema.RAIO_CARTAO,
                command=lambda view=view: self.selecionar_view(view)
            )


    def configurar_layout(self):
        self.frame.grid(row=0, column=0, padx=tema.ESPACO, pady=tema.ESPACO, sticky="ns")

        self.label_titulo.grid(row=0, column=0, padx=16, pady=(20, 16))

        for linha, view in enumerate(self.botoes, start=1):
            self.botoes[view].grid(row=linha, column=0, padx=12, pady=4, sticky="ew")


    def marcar_ativo(self, view):
        for nome, botao in self.botoes.items():
            if nome == view:
                botao.configure(
                    fg_color=tema.COR_DESTAQUE,
                    hover_color=tema.COR_DESTAQUE_HOVER
                )
            else:
                botao.configure(
                    fg_color="transparent",
                    hover_color=tema.COR_DIGITO
                )
