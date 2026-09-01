from swaplator.conversores.moedas import converter_moedas
import unittest

cotacoes = {
    "USD": 1,
    "BRL": 5,
    "EUR": 0.8
}

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

if __name__ == '__main__':
    unittest.main()