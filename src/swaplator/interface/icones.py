"""Ícones dos tipos de conversão, desenhados com linhas e formas.

Em vez de usar imagens (que precisariam de arquivos e de biblioteca extra),
cada ícone é desenhado num canvas. Todos pensam numa grade de 24 unidades
e multiplicam por `k = tamanho / 24`; assim o mesmo desenho serve para
qualquer tamanho. Este arquivo não importa tkinter: só chama métodos do
canvas recebido, o que também facilita os testes.
"""


def _escala(tamanho):
    """Devolve o fator de escala e a espessura da linha para o tamanho."""
    k = tamanho / 24
    return k, max(1, round(2 * k))


def _linha(canvas, k, espessura, cor, *pontos):
    """Linha entre pontos da grade de 24 (x1, y1, x2, y2, ...)."""
    canvas.create_line(*[p * k for p in pontos], fill=cor, width=espessura)


def desenhar_regua(canvas, tamanho, cor):
    """Comprimento: uma régua com marcações."""
    k, e = _escala(tamanho)
    canvas.create_rectangle(2 * k, 8 * k, 22 * k, 16 * k,
                            outline=cor, fill="", width=e)

    # Traços alternando curto (4) e longo (6), saindo de cima para baixo.
    for x, comprimento in ((6, 4), (10, 6), (14, 4), (18, 6)):
        _linha(canvas, k, e, cor, x, 8, x, 8 + comprimento)


def desenhar_area(canvas, tamanho, cor):
    """Área: um quadrado com uma diagonal."""
    k, e = _escala(tamanho)
    canvas.create_rectangle(4 * k, 4 * k, 20 * k, 20 * k,
                            outline=cor, fill="", width=e)
    _linha(canvas, k, e, cor, 4, 20, 20, 4)


def desenhar_massa(canvas, tamanho, cor):
    """Massa: um peso de balança (trapézio com alça)."""
    k, e = _escala(tamanho)
    pontos = (5, 21, 8, 9, 16, 9, 19, 21)
    canvas.create_polygon(*[p * k for p in pontos],
                          outline=cor, fill="", width=e)
    canvas.create_oval(9 * k, 3 * k, 15 * k, 10 * k,
                       outline=cor, fill="", width=e)


def desenhar_volume(canvas, tamanho, cor):
    """Volume: um cubo visto de lado (hexágono com três arestas)."""
    k, e = _escala(tamanho)
    pontos = (12, 2, 21, 7, 21, 17, 12, 22, 3, 17, 3, 7)
    canvas.create_polygon(*[p * k for p in pontos],
                          outline=cor, fill="", width=e)

    # As três arestas partem do centro e vão a três vértices.
    for x, y in ((3, 7), (21, 7), (12, 22)):
        _linha(canvas, k, e, cor, 12, 12, x, y)


def desenhar_temperatura(canvas, tamanho, cor):
    """Temperatura: um termômetro (tubo e bulbo)."""
    k, e = _escala(tamanho)
    canvas.create_rectangle(10 * k, 2 * k, 14 * k, 15 * k,
                            outline=cor, fill="", width=e)
    canvas.create_oval(7 * k, 13 * k, 17 * k, 23 * k,
                       outline=cor, fill="", width=e)


def desenhar_seta(canvas, tamanho, cor):
    """Seta para baixo (indica que o seletor abre uma lista)."""
    k, e = _escala(tamanho)
    _linha(canvas, k, e, cor, 6, 9, 12, 15)
    _linha(canvas, k, e, cor, 12, 15, 18, 9)


# Chave = mesmo nome usado em CONVERSOES, para achar o ícone pelo tipo.
ICONES = {
    "comprimento": desenhar_regua,
    "area": desenhar_area,
    "massa": desenhar_massa,
    "volume": desenhar_volume,
    "temperatura": desenhar_temperatura,
}
