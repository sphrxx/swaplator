from numbers import Number
import requests


def obter_cotacoes():
    cotacoes = {}

    try:
        resposta = requests.get("https://api.frankfurter.dev/v2/rates?base=USD&quotes=BRL,EUR")
        resposta.raise_for_status()

    except requests.HTTPError as e:
        raise ValueError("Um erro HTTP foi detectado.") from e

    except requests.RequestException as e:
        raise ValueError("Não foi possível conectar à API.") from e    

    dados = resposta.json()

    if not isinstance(dados, list):
        raise ValueError("Formato de resposta inesperado: 'DADOS' não é uma 'LISTA'.")

    for dado in dados:
        if not isinstance(dado, dict):
            raise ValueError("Formato de resposta inesperado: 'DADO' não é um 'DICT'.")
        
        if "quote" not in dado:
            raise ValueError("Formato de resposta inesperado: 'QUOTE' não está presente no dicionário.")
        
        if not isinstance(dado["quote"], str):
            raise ValueError("Formato de resposta inesperado: 'QUOTE' não é uma 'STRING'.")
        
        if "rate" not in dado:
            raise ValueError("Formato de resposta inesperado: 'RATE' não está presente no dicionário.")
        
        if not isinstance(dado["rate"], Number):
            raise ValueError("Formato de resposta inesperado: 'RATE' não é um 'NÚMERO'.")

        cotacoes[dado["quote"]] = dado["rate"]

    return cotacoes


def converter_moedas(valor, moeda_inicial, moeda_final, cotacoes):
    if moeda_inicial not in cotacoes:
        raise ValueError("Moeda inicial inválida.")
    
    if moeda_final not in cotacoes:
        raise ValueError("Moeda final inválida.")
    
    if moeda_inicial == moeda_final:
        return valor

    resultado = valor / cotacoes[moeda_inicial] * cotacoes[moeda_final]

    return resultado