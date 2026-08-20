unidades = {
        # Sistema Métrico
        "mm": 0.001,
        "cm": 0.01,
        "dm": 0.1,
        "m": 1,
        "dam": 10,
        "hm": 100,
        "km": 1000,

        # Sistema Imperial
        "in": 0.0254,
        "ft": 0.3048,
        "yd": 0.9144,
        "mi": 1609.34
    }

def conversor_comprimento(valor_inicial, unidade_inicial, unidade_final):
    if unidade_inicial not in unidades:
        raise ValueError("Unidade inicial inválida.")
    
    if unidade_final not in unidades:
        raise ValueError("Unidade final inválida.")

    fator_inicial = unidades[unidade_inicial]
    fator_final = unidades[unidade_final]
    resultado = valor_inicial * fator_inicial / fator_final

    return resultado