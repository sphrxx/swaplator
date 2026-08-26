from swaplator.conversores.conversor import converter

FATORES_MASSA = {
    # Sistema Internacional
    'ng': 0.000000001,
    'μg': 0.000001,
    'mg': 0.001,
    'cg': 0.01,
    'dg': 0.1,
    'g': 1,
    'dag': 10,
    'hg': 100,
    'kg': 1000,
    't': 1000000,

    # Sistema Imperial
    'oz': 28.3495,
    'lb': 453.592
}

def conversao_massa(valor, unidade_inicial, unidade_final):
    return converter(valor, unidade_inicial, unidade_final, FATORES_MASSA)