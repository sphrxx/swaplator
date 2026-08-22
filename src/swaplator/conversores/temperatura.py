def fahrenheit_to_celsius(valor):
    return (valor - 32) * 5/9

def kelvin_to_celsius(valor):
    return valor - 273.15

def celsius_to_fahrenheit(valor):
    return (valor * 9/5) + 32

def celsius_to_kelvin(valor):
    return valor + 273.15

def celsius_to_celsius(valor):
    return valor

# --------------------------------

CONVERSORES_PARA_CELSIUS = {
    "°C": celsius_to_celsius,
    "°F": fahrenheit_to_celsius,
    "K": kelvin_to_celsius
}

CONVERSORES_DE_CELSIUS = {
    "°C": celsius_to_celsius,
    "°F": celsius_to_fahrenheit,
    "K": celsius_to_kelvin
}

# --------------------------------

def conversao_temperatura(valor, unidade_inicial, unidade_final):

    if unidade_inicial not in CONVERSORES_PARA_CELSIUS:
        raise ValueError("Unidade inicial inválida.")
    
    if unidade_final not in CONVERSORES_DE_CELSIUS:
        raise ValueError("Unidade final inválida.")

    para_celsius = CONVERSORES_PARA_CELSIUS[unidade_inicial]
    valor_em_celsius = para_celsius(valor)

    de_celsius = CONVERSORES_DE_CELSIUS[unidade_final]
    resultado = de_celsius(valor_em_celsius)

    return resultado