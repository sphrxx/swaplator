from swaplator.conversores.conversor import converter

FATORES_AREA = {
    # Sistema Internacional
    'mm²': 0.000001,
    'cm²': 0.0001,
    'dm²': 0.01,
    'm²': 1,
    'dam²': 100,
    'hm²': 10000,
    'km²': 1000000,

    # Sistema Imperial
    'in²': 0.00064516,
    'ft²': 0.092903,
    'yd²': 0.836127,
    'ac': 4046.856,
    'mi²': 2589988.11
}

def conversao_area(valor, unidade_inicial, unidade_final):
    return converter(valor, unidade_inicial, unidade_final, FATORES_AREA)