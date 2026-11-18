"""Registro dos tipos de conversão de medidas.

Cada tipo guarda (função de conversão, unidades disponíveis). Assim, quem
precisa converter não precisa saber *como* cada tipo converte: comprimento
usa uma tabela de fatores, temperatura usa fórmulas próprias.
"""

from swaplator.conversores.comprimento import conversao_comprimento, FATORES_COMPRIMENTO
from swaplator.conversores.area import conversao_area, FATORES_AREA
from swaplator.conversores.massa import conversao_massa, FATORES_MASSA
from swaplator.conversores.volume import conversao_volume, FATORES_VOLUME
from swaplator.conversores.temperatura import conversao_temperatura, UNIDADES_TEMPERATURA


CONVERSOES = {
    "comprimento": (conversao_comprimento, FATORES_COMPRIMENTO),
    "area": (conversao_area, FATORES_AREA),
    "massa": (conversao_massa, FATORES_MASSA),
    "volume": (conversao_volume, FATORES_VOLUME),
    "temperatura": (conversao_temperatura, UNIDADES_TEMPERATURA)
}


def converter_por_tipo(tipo, valor, unidade_inicial, unidade_final):
    if tipo not in CONVERSOES:
        raise ValueError("Tipo de conversão inválido.")

    funcao_conversao, _ = CONVERSOES[tipo]

    return funcao_conversao(valor, unidade_inicial, unidade_final)
