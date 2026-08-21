from src.swaplator.conversores.comprimento import conversor_comprimento
import unittest

class TestConversorComprimento(unittest.TestCase):

    def test_metros_centimetros(self):
        resultado = conversor_comprimento(1, "m", "cm")
        self.assertEqual(resultado, 100)

    def test_quilometros_metros(self):
        resultado = conversor_comprimento(1, "km", "m")
        self.assertEqual(resultado, 1000)

    def test_ft_metros(self):
        resultado = conversor_comprimento(1, "ft", "m")
        self.assertAlmostEqual(resultado, 0.3048, places=4)

    def test_quilometros_milhas(self):
        resultado = conversor_comprimento(1, "km", "mi")
        self.assertAlmostEqual(resultado, 0.62137, places=4)

    def test_mesma_unidade(self):
        resultado = conversor_comprimento(1, "m", "m")
        self.assertEqual(resultado, 1)

    def test_unidade_inicial_invalida(self):
        with self.assertRaises(ValueError):
            conversor_comprimento(1, "banana", "m")

    def test_unidade_final_invalida(self):
        with self.assertRaises(ValueError):
            conversor_comprimento(1, "m", "banana")

if __name__ == "__main__":
    unittest.main()