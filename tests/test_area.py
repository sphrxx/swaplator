from src.swaplator.conversores.conversor import converter
from src.swaplator.conversores.area import FATORES_AREA
import unittest

class TestConversorArea(unittest.TestCase):

    def test_metros2_centimetros2(self):
        resultado = converter(1, 'm²', 'cm²', FATORES_AREA)
        self.assertEqual(resultado, 10000)

    def test_decametro2_milimetro2(self):
        resultado = converter(1, 'dm²', 'mm²', FATORES_AREA)
        self.assertEqual(resultado, 10000)

    def test_mesma_unidade(self):
        resultado = converter(1, 'mm²', "mm²", FATORES_AREA)
        self.assertEqual(resultado, 1)

    def test_acre_quilometros2(self):
        resultado = converter(1, 'ac', 'km²', FATORES_AREA)
        self.assertAlmostEqual(resultado, 0.004047, places=4)

    def test_metros2_pe2(self):
        resultado = converter(1, 'm²', 'ft²', FATORES_AREA)
        self.assertAlmostEqual(resultado, 10.7639, places=4)

    def test_unidade_inicial_invalida(self):
        with self.assertRaises(ValueError):
            converter(1, "bananinha", "ft²", FATORES_AREA)

    def test_unidade_final_invalida(self):
        with self.assertRaises(ValueError):
            converter(1, "m²", "oiiii", FATORES_AREA)

if __name__ == '__main__':
    unittest.main()