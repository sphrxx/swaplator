import customtkinter as ctk

from swaplator.interface import tema
from swaplator.interface.icones import ICONES


# (nome interno da tela, texto exibido no item), na ordem em que aparecem.
# O nome interno também é a chave do ícone em `ICONES`.
ITENS = [
    ("calculadora", "Calculadora"),
    ("comprimento", "Comprimento"),
    ("area", "Área"),
    ("massa", "Massa"),
    ("volume", "Volume"),
    ("temperatura", "Temperatura"),
    ("moedas", "Moedas"),
]


class ItemSidebar(ctk.CTkFrame):
    """Um item do menu lateral: ícone + texto, clicável por inteiro.

    O CTkButton só aceita imagens, e nossos ícones são desenhados num canvas.
    Por isso o item é uma moldura com o canvas do ícone e um rótulo dentro,
    e o clique é ligado nas três partes.
    """

    def __init__(self, master, chave, texto, comando):
        super().__init__(master,
                         width=tema.LARGURA_ITEM_SIDEBAR,
                         height=tema.ALTURA_CONTROLE,
                         fg_color="transparent",
                         corner_radius=tema.RAIO_CARTAO)
        self.chave = chave
        self._comando = comando
        self.ativo = False

        # Mantém o tamanho pedido em vez de encolher para caber o conteúdo.
        self.grid_propagate(False)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # O canvas é tk puro: o CTk não escala o tamanho dele nem o espaçamento.
        escala = getattr(self, "_get_widget_scaling", lambda: 1.0)()
        lado = round(tema.TAMANHO_ICONE * escala)

        self.icone = ctk.CTkCanvas(self, width=lado, height=lado,
                                   bg=tema.COR_SUPERFICIE, highlightthickness=0)
        self.icone.grid(row=0, column=0,
                        padx=(round(12 * escala), round(10 * escala)))
        ICONES[chave](self.icone, lado, tema.COR_TEXTO)

        self.texto = ctk.CTkLabel(self, text=texto, anchor="w",
                                  text_color=tema.COR_TEXTO,
                                  font=tema.fonte(tema.TAM_TEXTO))
        self.texto.grid(row=0, column=1, sticky="w")

        for parte in (self, self.icone, self.texto):
            parte.bind("<Button-1>", lambda evento: self.clicar())
            parte.bind("<Enter>", lambda evento: self._pintar(self._cor_hover()))

        # O <Leave> fica só na moldura e confere a posição do mouse: entrar no
        # ícone ou no texto também dispara <Leave> na moldura (veja
        # _ao_sair).
        self.bind("<Leave>", self._ao_sair)

    def clicar(self):
        self._comando(self.chave)

    def ativar(self, ativo):
        self.ativo = ativo
        self._pintar(self._cor_normal())

    # --- Cores --------------------------------------------------------
    def _cor_normal(self):
        return tema.COR_DESTAQUE if self.ativo else "transparent"

    def _cor_hover(self):
        return tema.COR_DESTAQUE_HOVER if self.ativo else tema.COR_DIGITO

    def _pintar(self, cor):
        """Pinta a moldura e o fundo do canvas (que não entende "transparent")."""
        self.configure(fg_color=cor)
        self.icone.configure(
            bg=tema.COR_SUPERFICIE if cor == "transparent" else cor)

    def _ao_sair(self, evento=None):
        x, y = self.winfo_pointerxy()
        esquerda = self.winfo_rootx()
        topo = self.winfo_rooty()

        dentro = (esquerda <= x < esquerda + self.winfo_width()
                  and topo <= y < topo + self.winfo_height())
        if not dentro:
            self._pintar(self._cor_normal())


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
            self.botoes[view] = ItemSidebar(
                self.frame, view, texto, self.selecionar_view)


    def configurar_layout(self):
        self.frame.grid(row=0, column=0, padx=tema.ESPACO, pady=tema.ESPACO, sticky="ns")

        self.label_titulo.grid(row=0, column=0, padx=16, pady=(20, 16))

        for linha, view in enumerate(self.botoes, start=1):
            self.botoes[view].grid(row=linha, column=0, padx=12, pady=4, sticky="ew")


    def marcar_ativo(self, view):
        for nome, item in self.botoes.items():
            item.ativar(nome == view)
