import unittest

from swaplator.interface.formato import formatar_numero, converter_para_exibir


class TestFormatarNumero(unittest.TestCase):

    def test_remove_zeros_a_direita(self):
        self.assertEqual(formatar_numero(1250.0), "1250")

    def test_corta_ruido_de_ponto_flutuante(self):
        self.assertEqual(formatar_numero(0.1 + 0.2), "0.3")

    def test_zero_negativo_vira_zero(self):
        self.assertEqual(formatar_numero(-0.0), "0")

    def test_extremos_usam_notacao_cientifica(self):
        self.assertEqual(formatar_numero(1e11), "1e+11")
        self.assertEqual(formatar_numero(0.00001), "1e-05")


class TestConverterParaExibir(unittest.TestCase):

    def test_converte_e_formata(self):
        self.assertEqual(converter_para_exibir("comprimento", "1", "m", "cm"), "100")
        self.assertEqual(converter_para_exibir("temperatura", "100", "°C", "°F"), "212")

    def test_entrada_vazia_converte_como_zero(self):
        self.assertEqual(converter_para_exibir("comprimento", "", "m", "cm"), "0")

    def test_entrada_com_ponto_no_fim(self):
        self.assertEqual(converter_para_exibir("comprimento", "1.", "m", "cm"), "100")

    def test_unidade_inexistente_vira_traco(self):
        self.assertEqual(converter_para_exibir("comprimento", "1", "m", "xx"), "—")
        self.assertEqual(converter_para_exibir("comprimento", "1", "xx", "m"), "—")


if __name__ == "__main__":
    unittest.main()
