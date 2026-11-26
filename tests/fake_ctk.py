"""Um "customtkinter de mentira", só para testar a lógica das telas.

Ele finge ser os widgets (botão, rótulo, campo...) sem abrir janela nenhuma,
então os testes rodam em qualquer computador. Cada widget de mentira guarda
as opções que recebeu (`opcoes`) e a lista de filhos, para o teste poder
procurar um botão pelo texto e "apertar" o botão (chamar o `command` dele).
"""

import sys
import types


class Fake:

    def __init__(self, master=None, *args, **kwargs):
        self.master = master
        self.opcoes = dict(kwargs)
        self.filhos = []
        self.valor = None
        self.colunas = {}       # coluna -> opções de grid_columnconfigure
        self.binds = []         # (sequência, id) de cada bind feito
        self.unbinds = []       # (sequência, id) de cada unbind feito
        self._last_geometry_manager_call = None
        self.handlers = {}      # sequência -> funções ligadas por bind

        if isinstance(master, Fake):
            master.filhos.append(self)

    def configure(self, **kwargs):
        self.opcoes.update(kwargs)

    def grid(self, *args, **kwargs):
        self.opcoes_grid = kwargs
        self.grid_removido = False
        # O CTk guarda o último grid() e o refaz quando a escala da tela muda.
        self._last_geometry_manager_call = {"function": self.grid, "kwargs": kwargs}

    def grid_remove(self):
        # Como o Tk: esconde o widget mas lembra a posição para um grid() futuro.
        # (O CTk NÃO apaga o registro de geometria aqui: é a armadilha.)
        self.grid_removido = True

    def grid_forget(self):
        # Como o CTk: esconde e esquece o registro de geometria.
        self.grid_removido = True
        self._last_geometry_manager_call = None

    def grid_columnconfigure(self, coluna, **kwargs):
        # Anota para o teste conferir (ex.: o minsize da lista).
        self.colunas.setdefault(coluna, {}).update(kwargs)

    def grid_rowconfigure(self, *args, **kwargs):
        pass

    def _create_grid(self):
        # Imita o CTkButton real: ele reserva `corner_radius` de largura nas
        # colunas das pontas (0 e 4). É isso que deixa os botões ovais.
        self.grid_columnconfigure((0, 4), minsize=self.opcoes.get("corner_radius", 0))

    def winfo_children(self):
        return list(self.filhos)

    def winfo_exists(self):
        return True

    def destroy(self):
        # Como o Tk: destrói os filhos primeiro (cópia da lista, pois cada
        # filho se remove dela), depois a si mesmo.
        for filho in list(self.filhos):
            filho.destroy()

        if isinstance(self.master, Fake) and self in self.master.filhos:
            self.master.filhos.remove(self)

    def set(self, valor):
        self.valor = valor

    def get(self):
        if self.valor is not None:
            return self.valor

        valores = self.opcoes.get("values")
        return valores[0] if valores else ""

    def delete(self, *args):
        self.valor = None

    def focus(self):
        pass

    def focus_set(self):
        pass

    def bind(self, *args, **kwargs):
        # Devolve um id diferente a cada bind, como o Tk faz com add="+".
        id_do_bind = f"id-{len(self.binds)}"
        self.binds.append((args[0], id_do_bind))
        # Guarda a função para o teste "apertar a tecla" chamando-a de verdade.
        self.handlers.setdefault(args[0], []).append(args[1])
        return id_do_bind

    def unbind(self, sequencia, id_do_bind=None):
        self.unbinds.append((sequencia, id_do_bind))

    def winfo_pointerxy(self):
        return (-1, -1)  # mouse longe de tudo

    def place(self, **kwargs):
        self.opcoes_place = kwargs

    def place_forget(self):
        self.opcoes_place = None

    def lift(self):
        pass

    def grid_propagate(self, *args):
        pass

    def winfo_toplevel(self):
        # Sobe a cadeia de `master` até a raiz, como o Tk.
        raiz = self
        while isinstance(raiz.master, Fake):
            raiz = raiz.master
        return raiz

    def clipboard_clear(self):
        self.clipboard_texto = ""

    def clipboard_append(self, texto):
        self.clipboard_texto = getattr(self, "clipboard_texto", "") + texto

    def winfo_class(self):
        return "Frame"

    def winfo_rootx(self):
        return 0

    def winfo_rooty(self):
        return 0

    def winfo_width(self):
        return 0

    def winfo_height(self):
        return 0

    # --- Métodos de janela (CTk): só anotam o que foi pedido -------------
    def geometry(self, texto=None):
        self.geometria = texto

    def minsize(self, largura, altura):
        self.minimo = (largura, altura)

    def title(self, texto):
        self.titulo = texto

    def winfo_screenwidth(self):
        return 1920

    def winfo_screenheight(self):
        return 1080

    def mainloop(self):
        pass

    def after_idle(self, funcao, *args):
        funcao(*args)

    def after(self, milissegundos, funcao=None, *args):
        # Sem relógio de verdade: executa na hora.
        if funcao is not None:
            funcao(*args)


class FakeCanvas(Fake):
    """Um canvas de mentira: em vez de desenhar, anota o que foi pedido.

    Cada chamada `create_*` guarda `(nome, coordenadas, opcoes)` em
    `desenhos`, e o teste confere formas, posições e cores.
    """

    def __init__(self, master=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.desenhos = []

    def _desenhar(self, nome, coords, opcoes):
        self.desenhos.append((nome, coords, opcoes))
        return 0

    def create_line(self, *coords, **opcoes):
        return self._desenhar("line", coords, opcoes)

    def create_rectangle(self, *coords, **opcoes):
        return self._desenhar("rectangle", coords, opcoes)

    def create_oval(self, *coords, **opcoes):
        return self._desenhar("oval", coords, opcoes)

    def create_polygon(self, *coords, **opcoes):
        return self._desenhar("polygon", coords, opcoes)

    def create_arc(self, *coords, **opcoes):
        return self._desenhar("arc", coords, opcoes)

    def delete(self, *args):
        if args == ("all",):
            self.desenhos.clear()
        super().delete(*args)


class FakeScalingTracker:
    """Imita o `ctk.ScalingTracker`: a escala da tela é escolhida pelo teste."""

    escala = 1.0

    @classmethod
    def get_window_scaling(cls, janela):
        return cls.escala


NOMES_DOS_WIDGETS = (
    "CTk", "CTkFrame", "CTkLabel", "CTkButton",
    "CTkEntry", "CTkComboBox", "CTkSegmentedButton",
)

_guardados = {}


def _nome_afetado(nome):
    return nome == "customtkinter" or nome.startswith("swaplator.interface")


def instalar():
    """Coloca o customtkinter de mentira no lugar do verdadeiro."""
    for nome in [n for n in sys.modules if _nome_afetado(n)]:
        _guardados[nome] = sys.modules.pop(nome)

    modulo = types.ModuleType("customtkinter")
    for nome in NOMES_DOS_WIDGETS:
        setattr(modulo, nome, Fake)

    modulo.CTkCanvas = FakeCanvas
    modulo.ScalingTracker = FakeScalingTracker
    modulo.set_appearance_mode = lambda modo: None

    sys.modules["customtkinter"] = modulo


def remover():
    """Devolve o estado original, para não afetar outros testes."""
    for nome in [n for n in sys.modules if _nome_afetado(n)]:
        del sys.modules[nome]

    sys.modules.update(_guardados)
    _guardados.clear()


def achar_botao(pai, texto):
    """Procura, em qualquer nível, o widget cujo texto é `texto`."""
    for filho in pai.filhos:
        if filho.opcoes.get("text") == texto:
            return filho

        encontrado = achar_botao(filho, texto)
        if encontrado is not None:
            return encontrado

    return None
