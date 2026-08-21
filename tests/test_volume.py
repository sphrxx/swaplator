from swaplator.conversores.conversor import converter
from swaplator.conversores.volume import FATORES_VOLUME
import unittest

class TestConversorvolume(unittest.TestCase):

    def test_metros3_centimetros3(self):
        resultado = converter(1, 'm³', 'cm³', FATORES_VOLUME)
        self.assertEqual(resultado, 1000000)

    def test_decametro3_milimetro3(self):
        resultado = converter(1, 'dm³', 'mm³', FATORES_VOLUME)
        self.assertEqual(resultado, 1000000)

    def test_mesma_unidade(self):
        resultado = converter(1, 'mm³', "mm³", FATORES_VOLUME)
        self.assertEqual(resultado, 1)

    def test_galao_metros3(self):
        resultado = converter(1, 'gal', 'm³', FATORES_VOLUME)
        self.assertAlmostEqual(resultado, 0.004546, places=4)

    def test_centimetros3_oncafluida(self):
        resultado = converter(1, 'cm³', 'fl oz', FATORES_VOLUME)
        self.assertAlmostEqual(resultado, 0.03519, places=4)

    def test_unidade_inicial_invalida(self):
        with self.assertRaises(ValueError):
            converter(1, "tudo bom", "cm³", FATORES_VOLUME)

    def test_unidade_final_invalida(self):
        with self.assertRaises(ValueError):
            converter(1, "m³", "sim tudo e voce", FATORES_VOLUME)

    def test_litros_metros3(self):
        resultado = converter(1, 'L', 'm³', FATORES_VOLUME)
        self.assertEqual(resultado, 0.001)

    def test_centimetros3_mililitros(self):
        resultado = converter(1, 'cm³', 'ml', FATORES_VOLUME)
        self.assertEqual(resultado, 1)

if __name__ == '__main__':
    unittest.main()