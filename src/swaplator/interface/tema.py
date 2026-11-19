"""Tema visual do Swaplator.

Toda cor, fonte e tamanho usados na interface fica aqui. As telas só
importam estes valores; assim, para mudar o visual do app inteiro,
basta editar este arquivo.
"""

# --- Cores de fundo ---------------------------------------------------
COR_FUNDO = "#000000"          # fundo da janela (preto, como no iPhone)
COR_SUPERFICIE = "#1C1C1E"     # barra lateral e cartões, um pouco mais claros

# --- Cores dos botões -------------------------------------------------
COR_DIGITO = "#333333"         # botões numéricos
COR_DIGITO_HOVER = "#4D4D4D"   # quando o mouse passa por cima
COR_FUNCAO = "#A5A5A5"         # botão C (limpar)
COR_FUNCAO_HOVER = "#C7C7C7"
COR_DESTAQUE = "#FF9F0A"       # operadores, "=" e item ativo
COR_DESTAQUE_HOVER = "#FFB340"

# --- Cores de texto ---------------------------------------------------
COR_TEXTO = "#FFFFFF"
COR_TEXTO_ESCURO = "#000000"       # texto sobre o botão cinza-claro
COR_TEXTO_SECUNDARIO = "#8E8E93"   # rótulos discretos
COR_ERRO = "#FF453A"

# --- Tamanhos ---------------------------------------------------------
TAMANHO_BOTAO = 72
RAIO_BOTAO = 36     # metade do tamanho: deixa o botão perfeitamente redondo
RAIO_CARTAO = 16
ESPACO = 8
ALTURA_CONTROLE = 44    # altura de campos e botões "compactos" dos conversores
LARGURA_CAMPO = 360     # largura dos campos dentro do cartão dos conversores
LARGURA_SELETOR_TIPO = 180  # largura do seletor de tipo de conversão
TAMANHO_ICONE = 22          # lado (em pixels) dos ícones dos tipos

FONTE_FAMILIA = "Segoe UI"


def fonte(tamanho, peso="normal"):
    """Devolve a fonte no formato que o CustomTkinter espera."""
    return (FONTE_FAMILIA, tamanho, peso)


# Para cada tipo de botão: (cor, cor ao passar o mouse, cor do texto).
_ESTILOS_BOTAO = {
    "digito": (COR_DIGITO, COR_DIGITO_HOVER, COR_TEXTO),
    "funcao": (COR_FUNCAO, COR_FUNCAO_HOVER, COR_TEXTO_ESCURO),
    "destaque": (COR_DESTAQUE, COR_DESTAQUE_HOVER, COR_TEXTO),
}


def estilo_botao(tipo, compacto=False):
    """Devolve os argumentos de estilo de um botão.

    Uso: ctk.CTkButton(master, text="7", **estilo_botao("digito"))

    Com compacto=True o botão fica baixo, de fonte menor e em formato de
    pílula (para os botões "Converter" e "Limpar" dos conversores).
    """
    if tipo not in _ESTILOS_BOTAO:
        raise ValueError(f"Tipo de botão desconhecido: {tipo!r}")

    fg_color, hover_color, text_color = _ESTILOS_BOTAO[tipo]

    estilo = {
        "fg_color": fg_color,
        "hover_color": hover_color,
        "text_color": text_color,
        "corner_radius": RAIO_BOTAO,
        "font": fonte(24),
    }

    if compacto:
        estilo["height"] = ALTURA_CONTROLE
        estilo["corner_radius"] = ALTURA_CONTROLE // 2
        estilo["font"] = fonte(16)

    return estilo


def estilo_entrada():
    """Argumentos de estilo para CTkEntry (campos de texto)."""
    return {
        "fg_color": COR_DIGITO,
        "border_width": 0,
        "text_color": COR_TEXTO,
        "corner_radius": RAIO_CARTAO,
        "height": ALTURA_CONTROLE,
        "font": fonte(16),
    }


def estilo_combobox():
    """Argumentos de estilo para CTkComboBox (listas de escolha)."""
    return {
        "fg_color": COR_DIGITO,
        "border_width": 0,
        "button_color": COR_DESTAQUE,
        "button_hover_color": COR_DESTAQUE_HOVER,
        "dropdown_fg_color": COR_SUPERFICIE,
        "dropdown_hover_color": COR_DIGITO,
        "dropdown_text_color": COR_TEXTO,
        "text_color": COR_TEXTO,
        "corner_radius": RAIO_CARTAO,
        "font": fonte(14),
        "dropdown_font": fonte(14),
    }


def aplicar_tema():
    """Liga o modo escuro do CustomTkinter. Chamar antes de criar a janela."""
    import customtkinter as ctk

    ctk.set_appearance_mode("dark")
