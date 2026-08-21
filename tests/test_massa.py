from src.swaplator.conversores.conversor import converter
from src.swaplator.conversores.massa import FATORES_MASSA
import unittest

class TestConversorMassa(unittest.TestCase):

    def test_grama_quilograma(self):
        resultado = converter(1, "g", "kg", FATORES_MASSA)
        self.assertEqual(resultado, 0.001)

    def test_quilograma_miligrama(self):
        resultado = converter(1, "kg", "mg", FATORES_MASSA)
        self.assertEqual(resultado, 1000000)

    def test_mesma_unidade(self):
        resultado = converter(1, "g", "g", FATORES_MASSA)
        self.assertEqual(resultado, 1)

    def test_libras_gramas(self):
        resultado = converter(1, "lb", "g", FATORES_MASSA)
        self.assertAlmostEqual(resultado, 453.592, places=4)

    def test_quilogramas_oncas(self):
        resultado = converter(1, "kg", "oz", FATORES_MASSA)
        self.assertAlmostEqual(resultado, 35.2739907, places=4)

    def test_unidade_inicial_invalida(self):
        with self.assertRaises(ValueError):
            converter(1, "banana", "g", FATORES_MASSA)

    def test_unidade_inicial_invalida(self):
        with self.assertRaises(ValueError):
            converter(1, "g", "bananinha", FATORES_MASSA)

if __name__ == '__main__':
    unittest.main()