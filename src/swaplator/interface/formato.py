"""Formatação de números e conversão "ao vivo" para o display.

Este módulo não usa tkinter: só recebe textos e devolve textos. Por isso dá
para testá-lo sem abrir janela, e a tela fica só com a parte visual.
"""

from swaplator.conversores.registro import converter_por_tipo

# Mostrado quando a conversão não é possível (por exemplo, unidade inválida).
TRACO = "—"


def formatar_numero(valor):
    """Número para exibir: no máximo 10 dígitos significativos, sem zeros à direita.

    Sem isto, o Python mostraria 1250.0 e 0.30000000000000004. O formato "g"
    tira o ".0" e corta o ruído de ponto flutuante; números muito grandes ou
    muito pequenos viram notação científica (1e+11).
    """
    if valor == 0:
        return "0"  # também cobre -0.0, que o formato "g" mostraria como "-0"

    return f"{valor:.10g}"


def converter_para_exibir(tipo, texto, unidade_inicial, unidade_final):
    """Converte o número digitado e devolve o texto da linha de baixo do display.

    `texto` é o que o usuário digitou ("" vale 0; "1." também é aceito).
    Se a conversão falhar (unidade que não existe, por exemplo) devolve "—"
    em vez de quebrar a tela.
    """
    try:
        numero = float(texto) if texto else 0.0
        resultado = converter_por_tipo(tipo, numero, unidade_inicial, unidade_final)

    except (ValueError, KeyError, ZeroDivisionError):
        return TRACO

    return formatar_numero(resultado)
