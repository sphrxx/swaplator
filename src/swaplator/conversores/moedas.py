import requests

def obter_cotacoes():
    dados = requests.get("https://api.frankfurter.dev/v2/rates?base=USD&quotes=BRL,EUR").json()

    DICIONARIO_MOEDAS = {}

    for dado in dados:
        DICIONARIO_MOEDAS[dado["quote"]] = dado["rate"]

    return DICIONARIO_MOEDAS


def converter_moedas(valor, moeda_inicial, moeda_final, cotacoes):
    if moeda_inicial not in cotacoes:
        raise ValueError("Moeda inicial inválida.")
    
    if moeda_final not in cotacoes:
        raise ValueError("Moeda final inválida.")
    
    if moeda_inicial == moeda_final:
        return valor

    resultado = valor / cotacoes[moeda_inicial] * cotacoes[moeda_final]

    return resultado