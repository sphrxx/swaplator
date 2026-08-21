from src.swaplator.conversores.massa import conversao_massa
import unittest

class TestConversorMassa(unittest.TestCase):

    def test_grama_quilograma(self):
        resultado = conversao_massa(1, "g", "kg")
        self.assertEqual(resultado, 0.001)

    def test_quilograma_miligrama(self):
        resultado = conversao_massa(1, "kg", "mg")
        self.assertEqual(resultado, 1000000)

    def test_mesma_unidade(self):
        resultado = conversao_massa(1, "g", "g")
        self.assertEqual(resultado, 1)

    def test_libras_gramas(self):
        resultado = conversao_massa(1, "lb", "g")
        self.assertAlmostEqual(resultado, 453.592, places=4)

    def test_quilogramas_oncas(self):
        resultado = conversao_massa(1, "kg", "oz")
        self.assertAlmostEqual(resultado, 35.2739907, places=4)

    def test_unidade_inicial_invalida(self):
        with self.assertRaises(ValueError):
            conversao_massa(1, "banana", "g")

    def test_unidade_inicial_invalida(self):
        with self.assertRaises(ValueError):
            conversao_massa(1, "g", "bananinha")

if __name__ == '__main__':
    unittest.main()