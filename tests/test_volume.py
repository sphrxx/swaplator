from src.swaplator.conversores.volume import conversao_volume
import unittest

class TestConversorvolume(unittest.TestCase):

    def test_metros3_centimetros3(self):
        resultado = conversao_volume(1, 'm³', 'cm³')
        self.assertEqual(resultado, 1000000)

    def test_decametro3_milimetro3(self):
        resultado = conversao_volume(1, 'dm³', 'mm³')
        self.assertEqual(resultado, 1000000)

    def test_mesma_unidade(self):
        resultado = conversao_volume(1, 'mm³', "mm³")
        self.assertEqual(resultado, 1)

    def test_galao_metros3(self):
        resultado = conversao_volume(1, 'gal', 'm³')
        self.assertAlmostEqual(resultado, 0.004546, places=4)

    def test_centimetros3_oncafluida(self):
        resultado = conversao_volume(1, 'cm³', 'fl oz')
        self.assertAlmostEqual(resultado, 0.03519, places=4)

    def test_unidade_inicial_invalida(self):
        with self.assertRaises(ValueError):
            conversao_volume(1, "tudo bom", "cm³")

    def test_unidade_final_invalida(self):
        with self.assertRaises(ValueError):
            conversao_volume(1, "m³", "sim tudo e voce")

    def test_litros_metros3(self):
        resultado = conversao_volume(1, 'L', 'm³')
        self.assertEqual(resultado, 0.001)

    def test_centimetros3_mililitros(self):
        resultado = conversao_volume(1, 'cm³', 'ml')
        self.assertEqual(resultado, 1)

if __name__ == '__main__':
    unittest.main()