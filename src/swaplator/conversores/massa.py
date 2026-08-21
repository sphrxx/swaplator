unidades = {
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

def conversao_massa(valor_inicial, unidade_inicial, unidade_final):
    if unidade_inicial not in unidades:
        raise ValueError("Unidade inicial inválida.")

    if unidade_final not in unidades:
        raise ValueError("Unidade final inválida.")

    fator_inicial = unidades[unidade_inicial]
    fator_final = unidades[unidade_final]
    resultado = valor_inicial * fator_inicial / fator_final

    return resultado