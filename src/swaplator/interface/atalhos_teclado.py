import customtkinter as ctk

DIGITOS = "0123456789"
OPERADORES = "+-*/"

# keysym -> ação, para as teclas que não têm um caractere próprio confiável.
_POR_NOME = {
    "Return": "calcular",
    "KP_Enter": "calcular",
    "Escape": "limpar",
    "Delete": "limpar",
    "BackSpace": "apagar",
}


def traduzir_tecla(evento):
    """Traduz uma tecla em (ação, valor), ou None se a calculadora a ignora.

    Ações: "digitar" (valor = dígito ou "."), "operador" (valor = + - * /),
    "calcular", "limpar" e "apagar" (valor = None).
    """
    # Se o foco está num campo de texto (a caixa de unidade é um), a tecla
    # pertence a ele: senão digitar "km" apertaria o C da calculadora.
    winfo_class = getattr(evento.widget, "winfo_class", None)
    if winfo_class is not None and winfo_class() == "Entry":
        return None

    if evento.keysym in _POR_NOME:
        return (_POR_NOME[evento.keysym], None)

    char = evento.char

    if char and char in DIGITOS:
        return ("digitar", char)

    if char in (".", ","):      # teclado brasileiro: o decimal é a vírgula
        return ("digitar", ".")

    if char and char in OPERADORES:
        return ("operador", char)

    if char in ("x", "X"):
        return ("operador", "*")

    if char == "=":
        return ("calcular", None)

    if char in ("c", "C"):
        return ("limpar", None)

    return None


class AtalhosTeclado(ctk.CTkFrame):
    """Liga o teclado físico à calculadora, sem aparecer na tela.

    É um widget filho da tela só para ser destruído junto com ela: o bind
    fica na janela (é lá que as teclas chegam) e é desfeito no destroy(),
    senão a tela antiga continuaria reagindo ao teclado depois de trocada.

    `ao_acao(acao, valor)` recebe o que `traduzir_tecla` devolveu.
    """

    def __init__(self, master, ao_acao):
        super().__init__(master)
        self._ao_acao = ao_acao
        self._janela = self.winfo_toplevel()
        self._id_do_bind = self._janela.bind("<Key>", self._ao_tecla, add="+")

    def _ao_tecla(self, evento):
        traducao = traduzir_tecla(evento)

        if traducao is not None:
            self._ao_acao(*traducao)

    def destroy(self):
        try:
            self._janela.unbind("<Key>", self._id_do_bind)
        except Exception:
            pass  # a janela inteira já foi destruída (TclError do Tk)

        super().destroy()
