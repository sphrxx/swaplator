import customtkinter as ctk

from swaplator.interface import tema
from swaplator.interface.componentes import esconder_grid, mostrar_grid
from swaplator.interface.icones import ICONES

COLUNAS = 3  # os tiles ficam numa grade de 3 colunas (3 + 2 para 5 tipos)


class PainelTipos(ctk.CTkFrame):
    """Grade de tiles com ícone + nome: o "menu de tipos" da calculadora.

    Ele ocupa o lugar do display+teclado enquanto está visível. Quem o usa
    (a CalculadoraView) decide onde ele fica na grade; aqui só cuidamos de
    mostrar/ocultar, pintar e navegar pelo teclado.

    - `rotulos`: dict {chave do tipo: nome exibido}, na ordem dos tiles.
    - `ao_escolher(chave)`: chamado ao clicar num tile (ou Enter).
    - `ao_fechar()`: chamado ao apertar Esc.
    """

    def __init__(self, master, rotulos, tipo_ativo, ao_escolher, ao_fechar):
        super().__init__(master, fg_color="transparent")
        self._chaves = list(rotulos)
        self._ao_escolher = ao_escolher
        self._ao_fechar = ao_fechar
        self.tipo_ativo = tipo_ativo
        self.visivel = False
        self._foco = None               # índice do tile com o "cursor" do teclado
        self._ids_de_bind = {}          # sequência -> id devolvido pelo bind

        self.tiles = {}
        self.icones = {}

        # O canvas é tk puro: o CTk não escala o tamanho dele.
        escala = getattr(self, "_get_widget_scaling", lambda: 1.0)()
        lado = round(tema.TAMANHO_ICONE_PAINEL * escala)

        for coluna in range(COLUNAS):
            self.grid_columnconfigure(coluna, weight=1, uniform="tiles")

        for indice, chave in enumerate(self._chaves):
            tile = ctk.CTkFrame(self, fg_color=tema.COR_DIGITO,
                                corner_radius=tema.RAIO_CARTAO)
            tile.grid(row=indice // COLUNAS, column=indice % COLUNAS,
                      padx=tema.ESPACO, pady=tema.ESPACO, sticky="nsew")
            tile.grid_columnconfigure(0, weight=1)

            icone = ctk.CTkCanvas(tile, width=lado, height=lado,
                                  bg=tema.COR_DIGITO, highlightthickness=0)
            icone.grid(row=0, column=0, pady=(round(16 * escala), round(6 * escala)))
            ICONES[chave](icone, lado, tema.COR_TEXTO)

            nome = ctk.CTkLabel(tile, text=rotulos[chave],
                                text_color=tema.COR_TEXTO,
                                font=tema.fonte(tema.TAM_TEXTO))
            nome.grid(row=1, column=0, pady=(0, round(16 * escala)))

            for parte in (tile, icone, nome):
                parte.bind("<Button-1>", lambda evento, c=chave: self.escolher(c))
                parte.bind("<Enter>", lambda evento, i=indice: self._focar(i))

            self.tiles[chave] = tile
            self.icones[chave] = icone

        self._pintar()

    # --- API pública ---------------------------------------------------
    def mostrar(self):
        self.visivel = True
        self._foco = self._chaves.index(self.tipo_ativo)
        self._pintar()
        mostrar_grid(self)

        # O CTkFrame liga os binds no canvas interno: é ele que recebe o foco.
        getattr(self, "_canvas", self).focus_set()

        # Binds da janela feitos UMA vez só e desfeitos no destroy(): enquanto
        # o painel está oculto, os handlers simplesmente não fazem nada.
        if not self._ids_de_bind:
            janela = self.winfo_toplevel()
            for sequencia, handler in (
                    ("<Left>", self._ao_esquerda),
                    ("<Right>", self._ao_direita),
                    ("<Up>", self._ao_cima),
                    ("<Down>", self._ao_baixo),
                    ("<Return>", self._ao_enter),
                    ("<Escape>", self._ao_esc)):
                self._ids_de_bind[sequencia] = janela.bind(
                    sequencia, handler, add="+")

    def ocultar(self):
        self.visivel = False
        self._foco = None
        self._pintar()
        esconder_grid(self)

    def escolher(self, tipo):
        self._ao_escolher(tipo)

    def definir_ativo(self, tipo):
        self.tipo_ativo = tipo
        self._pintar()

    def destroy(self):
        try:
            janela = self.winfo_toplevel()
            for sequencia, id_do_bind in self._ids_de_bind.items():
                janela.unbind(sequencia, id_do_bind)
        except Exception:
            pass  # a janela inteira já foi destruída (TclError do Tk)

        self._ids_de_bind = {}
        super().destroy()

    # --- Pintura -------------------------------------------------------
    def _pintar(self):
        for indice, chave in enumerate(self._chaves):
            ativo = chave == self.tipo_ativo
            em_foco = indice == self._foco

            if ativo:
                cor = tema.COR_DESTAQUE_HOVER if em_foco else tema.COR_DESTAQUE
            else:
                cor = tema.COR_DIGITO_HOVER if em_foco else tema.COR_DIGITO

            self.tiles[chave].configure(fg_color=cor)
            # O canvas não entende "transparent": pinta o fundo igual ao tile.
            self.icones[chave].configure(bg=cor)

    def _focar(self, indice):
        self._foco = indice
        self._pintar()

    def _mover(self, passo):
        """Move o cursor, sem passar das bordas (não dá a volta)."""
        if not self.visivel:
            return None

        novo = max(0, min(len(self._chaves) - 1, self._foco + passo))
        self._focar(novo)
        return "break"   # a tecla não segue para outros handlers da janela

    # --- Teclado -------------------------------------------------------
    def _ao_esquerda(self, evento=None):
        return self._mover(-1)

    def _ao_direita(self, evento=None):
        return self._mover(1)

    def _ao_cima(self, evento=None):
        return self._mover(-COLUNAS)

    def _ao_baixo(self, evento=None):
        return self._mover(COLUNAS)

    def _ao_enter(self, evento=None):
        if not self.visivel:
            return None

        self.escolher(self._chaves[self._foco])
        return "break"

    def _ao_esc(self, evento=None):
        if not self.visivel:
            return None

        self._ao_fechar()
        return "break"
