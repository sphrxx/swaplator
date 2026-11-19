"""Seletor de tipo de conversão: um botão que abre uma lista com ícones.

O combobox padrão não aceita imagens, então este widget é feito à mão:
um "gatilho" (o botão sempre visível) e uma "lista" que aparece por cima
das outras coisas da janela quando o gatilho é clicado.
"""

import customtkinter as ctk

from swaplator.interface import tema
from swaplator.interface.icones import ICONES, desenhar_seta

ROTULOS_TIPOS = {
    "comprimento": "Comprimento",
    "area": "Área",
    "massa": "Massa",
    "volume": "Volume",
    "temperatura": "Temperatura",
}

_TRANSPARENTE = "transparent"
_NENHUM = object()  # "ainda não pintei nenhum destaque" (None já significa "sem destaque")


def _cor_do_canvas(cor):
    """O canvas é tk puro e não entende "transparent": usa a cor da lista."""
    return tema.COR_SUPERFICIE if cor == _TRANSPARENTE else cor


class SeletorTipo(ctk.CTkFrame):
    """Gatilho + lista sobreposta para escolher um tipo.

    Os nomes `opcoes`, `filhos`, `valor` e `master` são usados pelo widget
    de mentira dos testes, por isso o estado interno usa nomes com "_".
    """

    def __init__(self, master, opcoes, command=None,
                 width=tema.LARGURA_SELETOR_TIPO):
        super().__init__(master, width=width, height=tema.ALTURA_CONTROLE,
                         fg_color=tema.COR_DIGITO,
                         corner_radius=tema.RAIO_CARTAO)
        self._rotulos = dict(opcoes)        # chave -> texto mostrado
        self._valor = next(iter(self._rotulos))
        self._command = command
        self._lista = None                  # criada só na primeira abertura
        self.linhas = {}                    # chave -> linha da lista
        self._icones_das_linhas = {}        # chave -> canvas do ícone
        self._ids_de_bind = {}              # sequência -> id devolvido pelo bind
        self._largura = width
        self._aberto = False                # a lista está visível?
        self._destacado = _NENHUM           # linha com a cor de hover agora

        self._montar_gatilho()
        self._redesenhar_atual()

    # --- Escala -------------------------------------------------------
    def _escala(self):
        """Fator de tela (1.0, 1.25, 1.5...). Frames e labels do CTk já usam
        isso sozinhos; canvas e grid_columnconfigure são tk puro e não."""
        return getattr(self, "_get_widget_scaling", lambda: 1.0)()

    def _lado_icone(self):
        """Lado do ícone em pixels reais (o canvas não é escalado pelo CTk)."""
        return round(tema.TAMANHO_ICONE * self._escala())

    def _px(self, valor):
        """Converte um espaçamento para pixels reais (uso em canvas)."""
        return round(valor * self._escala())

    # --- Gatilho ------------------------------------------------------
    def _montar_gatilho(self):
        # Mantém o tamanho pedido em vez de encolher para caber o conteúdo.
        self.grid_propagate(False)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        lado = self._lado_icone()
        self._icone = ctk.CTkCanvas(self, width=lado, height=lado,
                                    bg=tema.COR_DIGITO, highlightthickness=0)
        self._icone.grid(row=0, column=0,
                         padx=(self._px(12), self._px(8)))

        self._texto = ctk.CTkLabel(self, text="", anchor="w",
                                   text_color=tema.COR_TEXTO,
                                   font=tema.fonte(tema.TAM_PEQUENO))
        self._texto.grid(row=0, column=1, sticky="w")

        seta = ctk.CTkCanvas(self, width=lado, height=lado,
                             bg=tema.COR_DIGITO, highlightthickness=0)
        seta.grid(row=0, column=2, padx=(self._px(8), self._px(12)))
        desenhar_seta(seta, lado, tema.COR_TEXTO_SECUNDARIO)

        # Clicar em qualquer parte do gatilho abre/fecha a lista.
        for parte in (self, self._icone, self._texto, seta):
            parte.bind("<Button-1>", lambda evento: self.alternar())

    def _redesenhar_atual(self):
        """Mostra no gatilho o ícone e o nome do tipo escolhido."""
        self._icone.delete("all")
        ICONES[self._valor](self._icone, self._lado_icone(), tema.COR_TEXTO)
        self._texto.configure(text=self._rotulos[self._valor])

    # --- Valor --------------------------------------------------------
    def get(self):
        return self._valor

    def set(self, valor):
        if valor not in self._rotulos:
            raise ValueError(f"Tipo desconhecido: {valor!r}")

        self._valor = valor
        self._redesenhar_atual()

    def escolher(self, valor):
        """Escolha do usuário: troca o valor, fecha e avisa quem usa."""
        self.set(valor)
        self.fechar()

        if self._command is not None:
            self._command(valor)

    # --- Abrir e fechar -----------------------------------------------
    @property
    def esta_aberto(self):
        return self._aberto

    def alternar(self):
        if self._aberto:
            self.fechar()
        else:
            self.abrir()

    def abrir(self):
        if self._aberto:
            return

        if self._lista is None:
            self._montar_lista()

        self._pintar_linhas_da_lista()
        self._posicionar_lista()
        self._lista.lift()
        self._aberto = True

        # Clique fora e Esc fecham a lista. Os binds da janela são feitos
        # UMA vez só e ficam até o destroy(): desligá-los dentro do próprio
        # clique deixaria o Tk chamar um comando já apagado. Enquanto a lista
        # está fechada, os handlers simplesmente não fazem nada.
        if not self._ids_de_bind:
            janela = self.winfo_toplevel()
            self._ids_de_bind["<Button-1>"] = janela.bind(
                "<Button-1>", self._ao_clicar, add="+")
            self._ids_de_bind["<Escape>"] = janela.bind(
                "<Escape>", self._ao_esc, add="+")

    def fechar(self):
        if not self._aberto:
            return

        # A lista só é escondida, não destruída: este método pode rodar
        # dentro do clique numa linha, e destruir o widget ali dá erro.
        self._lista.place_forget()
        self._aberto = False

    def destroy(self):
        # Sem isto, a lista (filha da janela) ficaria órfã ao trocar de tela.
        try:
            self.fechar()

            janela = self.winfo_toplevel()
            for sequencia, id_do_bind in self._ids_de_bind.items():
                janela.unbind(sequencia, id_do_bind)
        except Exception:
            pass  # a janela inteira já foi destruída (TclError do Tk)

        self._ids_de_bind = {}

        if self._lista is not None:
            self._lista.destroy()
            self._lista = None

        super().destroy()

    def _ao_clicar(self, evento):
        """Clique em qualquer lugar da janela: fecha se foi fora."""
        if not self._aberto:
            return

        if not (self._pertence_a(evento.widget, self)
                or self._pertence_a(evento.widget, self._lista)):
            self.fechar()

    def _ao_esc(self, evento=None):
        if self._aberto:
            self.fechar()

    @staticmethod
    def _pertence_a(widget, ancestral):
        """True se `widget` é `ancestral` ou está dentro dele."""
        while widget is not None:
            if widget is ancestral:
                return True
            widget = getattr(widget, "master", None)
        return False

    # --- Lista --------------------------------------------------------
    def _montar_lista(self):
        # Filha da janela (e não do gatilho) para aparecer por cima de tudo.
        self._lista = ctk.CTkFrame(self.winfo_toplevel(),
                                   width=self._largura,
                                   fg_color=tema.COR_SUPERFICIE,
                                   corner_radius=tema.RAIO_CARTAO)
        # O frame encolhe ao conteúdo e ignora `width`; a largura mínima da
        # coluna garante lista tão larga quanto o gatilho. grid_columnconfigure
        # é tk puro (não escalado pelo CTk), então multiplicamos à mão. O
        # padx=4 das linhas fica dentro da coluna, então as linhas a preenchem.
        self._lista.grid_columnconfigure(
            0, weight=1, minsize=round(self._largura * self._escala()))
        self._lista.bind("<Leave>", self._ao_sair_da_lista)

        for numero, (chave, rotulo) in enumerate(self._rotulos.items()):
            self._montar_linha(numero, chave, rotulo)

    def _montar_linha(self, numero, chave, rotulo):
        linha = ctk.CTkFrame(self._lista, fg_color=_TRANSPARENTE,
                             corner_radius=tema.RAIO_CARTAO)
        linha.grid(row=numero, column=0, sticky="ew", padx=4, pady=2)
        linha.grid_columnconfigure(1, weight=1)

        lado = self._lado_icone()
        icone = ctk.CTkCanvas(linha, width=lado, height=lado,
                              bg=_cor_do_canvas(_TRANSPARENTE),
                              highlightthickness=0)
        icone.grid(row=0, column=0, padx=(self._px(8), self._px(8)),
                   pady=self._px(6))

        texto = ctk.CTkLabel(linha, text=rotulo, anchor="w",
                             font=tema.fonte(tema.TAM_PEQUENO))
        texto.grid(row=0, column=1, sticky="w")

        self.linhas[chave] = linha
        self._icones_das_linhas[chave] = icone
        linha._rotulo = texto

        # O <Enter> é ligado na linha e nos filhos, porque o mouse "entra"
        # no filho sem passar pelo <Enter> da linha. O <Leave> fica só na
        # lista inteira (veja _ao_sair_da_lista), para a cor não piscar.
        for parte in (linha, icone, texto):
            parte.bind("<Enter>", lambda evento, c=chave: self._destacar(c))
            parte.bind("<Button-1>", lambda evento, c=chave: self.escolher(c))

    def _pintar_linhas_da_lista(self):
        """Marca o tipo atual em laranja e tira qualquer destaque antigo."""
        self._destacar(None)

        for chave, linha in self.linhas.items():
            cor = tema.COR_DESTAQUE if chave == self._valor else tema.COR_TEXTO
            linha._rotulo.configure(text_color=cor)

            icone = self._icones_das_linhas[chave]
            icone.delete("all")
            ICONES[chave](icone, self._lado_icone(), cor)

    def _destacar(self, valor):
        """Pinta de cinza só a linha `valor` (a do mouse); as outras ficam limpas."""
        # Cada linha dispara vários <Enter> (linha, ícone, texto): se nada
        # mudou, não há o que repintar.
        if valor == self._destacado:
            return
        self._destacado = valor

        for chave, linha in self.linhas.items():
            cor = tema.COR_DIGITO if chave == valor else _TRANSPARENTE
            linha.configure(fg_color=cor)
            self._icones_das_linhas[chave].configure(bg=_cor_do_canvas(cor))

    def _ao_sair_da_lista(self, evento=None):
        """Tira o destaque quando o mouse realmente saiu da lista.

        Entrar num filho (ícone/texto) também gera <Leave> na lista, então
        comparamos a posição do mouse com o retângulo da lista na tela.
        """
        x, y = self._lista.winfo_pointerxy()
        esquerda = self._lista.winfo_rootx()
        topo = self._lista.winfo_rooty()

        dentro = (esquerda <= x < esquerda + self._lista.winfo_width()
                  and topo <= y < topo + self._lista.winfo_height())
        if not dentro:
            self._destacar(None)

    def _posicionar_lista(self):
        # winfo_* devolve pixels físicos, mas o place do CustomTkinter
        # multiplica x/y pela escala da tela (125%, 150%...). Dividir aqui
        # compensa e deixa a lista exatamente embaixo do gatilho.
        escala = self._escala()
        janela = self.winfo_toplevel()

        x = (self.winfo_rootx() - janela.winfo_rootx()) / escala
        y = (self.winfo_rooty() - janela.winfo_rooty()
             + self.winfo_height()) / escala + tema.ESPACO / 2

        self._lista.place(x=x, y=y)
