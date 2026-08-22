from swaplator.conversores.temperatura import conversao_temperatura
import unittest

class TestConversorTemperatura(unittest.TestCase):

    def test_celsius_para_fahrenheit(self):
        resultado = conversao_temperatura(1, "°C", "°F")
        self.assertAlmostEqual(resultado, 33.8, places=3)

    def test_fahrenheit_para_kelvin(self):
        resultado = conversao_temperatura(32, "°F", "K")
        self.assertAlmostEqual(resultado, 273.15, places=2)

    def test_kelvin_para_celsius(self):
        resultado = conversao_temperatura(273.15, "K", "°C")
        self.assertAlmostEqual(resultado, 0, places=3)

    def test_celsius_para_kelvin(self):
        resultado = conversao_temperatura(0, "°C", "K")
        self.assertAlmostEqual(resultado, 273.15, places=3)

    def test_fahrenheit_para_celsius(self):
        resultado = conversao_temperatura(32, "°F", "°C")
        self.assertAlmostEqual(resultado, 0, places=3)

    def test_mesma_unidade(self):
        resultado = conversao_temperatura(1, "°F", "°F")
        self.assertEqual(resultado, 1)

    def test_unidade_inicial_invalida(self):
        with self.assertRaises(ValueError):
            conversao_temperatura(1, "Ave, Santíssima Virgem!", "°F")

    def test_unidade_final_invalida(self):
        with self.assertRaises(ValueError):
            conversao_temperatura(1, "°C", "AMDG!")

    

if __name__ == "__main__":
    unittest.main()