from src.swaplator.conversores.conversor import converter
from src.swaplator.conversores.comprimento import FATORES_COMPRIMENTO
import unittest

class TestConversorComprimento(unittest.TestCase):

    def test_metros_centimetros(self):
        resultado = converter(1, "m", "cm", FATORES_COMPRIMENTO)
        self.assertEqual(resultado, 100)

    def test_quilometros_metros(self):
        resultado = converter(1, "km", "m", FATORES_COMPRIMENTO)
        self.assertEqual(resultado, 1000)

    def test_ft_metros(self):
        resultado = converter(1, "ft", "m", FATORES_COMPRIMENTO)
        self.assertAlmostEqual(resultado, 0.3048, places=4)

    def test_quilometros_milhas(self):
        resultado = converter(1, "km", "mi", FATORES_COMPRIMENTO)
        self.assertAlmostEqual(resultado, 0.62137, places=4)

    def test_mesma_unidade(self):
        resultado = converter(1, "m", "m", FATORES_COMPRIMENTO)
        self.assertEqual(resultado, 1)

    def test_unidade_inicial_invalida(self):
        with self.assertRaises(ValueError):
            converter(1, "banana", "m", FATORES_COMPRIMENTO)

    def test_unidade_final_invalida(self):
        with self.assertRaises(ValueError):
            converter(1, "m", "banana", FATORES_COMPRIMENTO)

if __name__ == "__main__":
    unittest.main()