import unittest

from swaplator.conversores.registro import CONVERSOES, converter_por_tipo


class TestRegistro(unittest.TestCase):

    def test_tipos_disponiveis(self):
        self.assertEqual(
            set(CONVERSOES),
            {"comprimento", "area", "massa", "volume", "temperatura"}
        )

    def test_cada_tipo_tem_ao_menos_duas_unidades(self):
        for tipo, (funcao, unidades) in CONVERSOES.items():
            with self.subTest(tipo=tipo):
                self.assertGreaterEqual(len(list(unidades)), 2)

    def test_temperatura_celsius_para_fahrenheit(self):
        self.assertEqual(converter_por_tipo("temperatura", 100, "°C", "°F"), 212)

    def test_comprimento_km_para_m(self):
        self.assertEqual(converter_por_tipo("comprimento", 1, "km", "m"), 1000)

    def test_unidade_invalida_levanta_value_error(self):
        with self.assertRaises(ValueError):
            converter_por_tipo("comprimento", 1, "xyz", "m")

    def test_tipo_invalido_levanta_value_error(self):
        with self.assertRaises(ValueError) as contexto:
            converter_por_tipo("xyz", 1, "m", "km")

        self.assertEqual(str(contexto.exception), "Tipo de conversão inválido.")


if __name__ == "__main__":
    unittest.main()
