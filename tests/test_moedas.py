from swaplator.conversores.moedas import converter_moedas, obter_cotacoes
from unittest.mock import patch, Mock
import unittest
import requests

cotacoes = {
    "USD": 1,
    "BRL": 5,
    "EUR": 0.8
}

dados_esperados = [
    {
        "date": "2026-08-31",
        "base": "USD",
        "quote": "BRL",
        "rate": 5
    },
    {
        "date": "2026-08-31",
        "base": "USD",
        "quote": "EUR",
        "rate": 0.8
    }
]

class TestConversorMoedas(unittest.TestCase):

    def test_brl_para_eur(self):
        resultado = converter_moedas(100, "BRL", "EUR", cotacoes)
        self.assertEqual(resultado, 16)


    def test_eur_para_brl(self):
        resultado = converter_moedas(100, "EUR", "BRL", cotacoes)
        self.assertEqual(resultado, 625)


    def test_mesma_moeda(self):
        resultado = converter_moedas(100, "BRL", "BRL", cotacoes)
        self.assertEqual(resultado, 100)

    
    def test_moeda_inicial_invalida(self):
        with self.assertRaises(ValueError):
            converter_moedas(100, "ABC", "EUR", cotacoes)


    def test_moeda_final_invalida(self):
        with self.assertRaises(ValueError):
            converter_moedas(100, "BRL", "AMDG", cotacoes)


class TestObterCotacoes(unittest.TestCase):

    def test_obter_cotacoes(self):
        with patch("requests.get") as mock_get:
            mock_get.return_value.json.return_value = dados_esperados

            resposta = obter_cotacoes()

            self.assertEqual(resposta, {"BRL": 5, "EUR": 0.8})
            mock_get.assert_called_once_with("https://api.frankfurter.dev/v2/rates?base=USD&quotes=BRL,EUR")

    
    def test_request_http_error(self):
        with patch("requests.get") as mock_get:
            mock_get.return_value.raise_for_status.side_effect = requests.HTTPError()

            with self.assertRaises(ValueError) as contexto:
                obter_cotacoes()

            self.assertEqual(
                str(contexto.exception),
                "Um erro HTTP foi detectado."
            )


    def test_request_connection_error(self):
        with patch("requests.get") as mock_get:
            mock_get.side_effect = requests.ConnectionError()

            with self.assertRaises(ValueError) as contexto:
                obter_cotacoes()

            self.assertEqual(
                str(contexto.exception),
                "Não foi possível conectar à API."
            )


    def test_request_timeout(self):
        with patch("requests.get") as mock_get:
            mock_get.side_effect = requests.Timeout()

            with self.assertRaises(ValueError) as contexto:
                obter_cotacoes()

            self.assertEqual(
                str(contexto.exception),
                "Não foi possível conectar à API."
            )

if __name__ == '__main__':
    unittest.main()