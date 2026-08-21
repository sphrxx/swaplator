from src.swaplator.conversores.area import conversao_area
import unittest

class TestConversorArea(unittest.TestCase):

    def test_metros2_centimetros2(self):
        resultado = conversao_area(1, 'm²', 'cm²')
        self.assertEqual(resultado, 10000)

    def test_decametro2_milimetro2(self):
        resultado = conversao_area(1, 'dm²', 'mm²')
        self.assertEqual(resultado, 10000)

    def test_mesma_unidade(self):
        resultado = conversao_area(1, 'mm²', "mm²")
        self.assertEqual(resultado, 1)

    def test_acre_quilometros2(self):
        resultado = conversao_area(1, 'ac', 'km²')
        self.assertAlmostEqual(resultado, 0.004047, places=4)

    def test_metros2_pe2(self):
        resultado = conversao_area(1, 'm²', 'ft²')
        self.assertAlmostEqual(resultado, 10.7639, places=4)

    def test_unidade_inicial_invalida(self):
        with self.assertRaises(ValueError):
            conversao_area(1, "bananinha", "ft²")

    def test_unidade_final_invalida(self):
        with self.assertRaises(ValueError):
            conversao_area(1, "m²", "oiiii")

if __name__ == '__main__':
    unittest.main()