def converter(valor_inicial, unidade_inicial, unidade_final, fatores):
    if unidade_inicial not in fatores:
        raise ValueError("Unidade inicial inválida.")
    
    if unidade_final not in fatores:
        raise ValueError("Unidade final inválida.")

    fator_inicial = fatores[unidade_inicial]
    fator_final = fatores[unidade_final]
    resultado = valor_inicial * fator_inicial / fator_final

    return resultado