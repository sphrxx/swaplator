unidades = {
    # Sistema Internacional - Medidas Cúbicas
    'mm³': 0.000000001,
    'cm³': 0.000001,
    'dm³': 0.001,
    'm³': 1,
    'dam³': 1000,
    'hm³': 1000000,
    'km³': 1000000000,

    # Sistema Internacional - Medidas Líquidas
    'L': 0.001,
    'ml': 0.000001,

    # Sistema Imperial - Medidas Cúbicas
    'in³': 0.000016387,
    'ft³': 0.028317,
    'yd³': 0.764555,
    'mi³': 4168181825441,

    # Sistema Imperial - Medidas Líquidas
    'fl oz': 0.000028413,
    'pt': 0.000568261,
    'qt': 0.001136523,
    'gal': 0.00454609
}

def conversao_volume(valor_inicial, unidade_inicial, unidade_final):
    if unidade_inicial not in unidades:
        raise ValueError("Unidade inicial inválida.")

    if unidade_final not in unidades:
        raise ValueError("Unidade final inválida.")

    fator_inicial = unidades[unidade_inicial]
    fator_final = unidades[unidade_final]
    resultado = valor_inicial * fator_inicial / fator_final

    return resultado