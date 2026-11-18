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

        if isinstance(master, Fake):
            master.filhos.append(self)

    def configure(self, **kwargs):
        self.opcoes.update(kwargs)

    def grid(self, *args, **kwargs):
        self.opcoes_grid = kwargs

    def grid_columnconfigure(self, *args, **kwargs):
        pass

    def grid_rowconfigure(self, *args, **kwargs):
        pass

    def winfo_children(self):
        return list(self.filhos)

    def winfo_exists(self):
        return True

    def destroy(self):
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

    def bind(self, *args):
        pass

    def after(self, milissegundos, funcao=None, *args):
        # Sem relógio de verdade: executa na hora.
        if funcao is not None:
            funcao(*args)


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
