import unittest

from tests import fake_ctk


def setUpModule():
    # As telas importam o customtkinter ao serem carregadas, então o de mentira
    # precisa estar instalado antes do import.
    fake_ctk.instalar()

    global CalculadoraView
    from swaplator.interface.calculadora_view import CalculadoraView


def tearDownModule():
    fake_ctk.remover()


class TestCalculadoraView(unittest.TestCase):

    def setUp(self):
        self.view = CalculadoraView(fake_ctk.Fake())

    def apertar(self, *textos):
        for texto in textos:
            botao = fake_ctk.achar_botao(self.view.frame, texto)
            botao.opcoes["command"]()

    def display(self):
        return self.view.display.opcoes["text"]

    def test_igual_calcula_no_modo_calculadora(self):
        self.apertar("7", "+", "3", "=")

        self.assertEqual(self.display(), "10.0")

    def test_ponto_duplicado_e_ignorado(self):
        self.apertar("1", ".", ".")

        self.assertEqual(self.display(), "1.")

    def test_conversao_de_comprimento_continua_funcionando(self):
        self.view.mudar_modo("conversao")
        self.apertar("1", "=")

        self.assertEqual(self.display(), "1.0 mm = 0.1 cm")

    def test_conversao_de_temperatura(self):
        self.view.mudar_modo("conversao")
        self.view.combobox_tipo_conversao.set("temperatura")
        self.view.atualizar_unidades("temperatura")
        self.apertar("1", "0", "0", "=")

        self.assertEqual(self.display(), "100.0 °C = 212.0 °F")

    def test_escolher_tipo_no_seletor_atualiza_unidades_e_converte(self):
        self.view.mudar_modo("conversao")
        self.view.combobox_tipo_conversao.escolher("temperatura")
        self.apertar("1", "0", "0", "=")

        self.assertEqual(self.display(), "100.0 °C = 212.0 °F")

    def test_trocar_de_modo_com_lista_aberta_nao_deixa_lista_orfa(self):
        janela = self.view.frame.winfo_toplevel()
        self.view.mudar_modo("conversao")
        seletor = self.view.combobox_tipo_conversao
        seletor.abrir()
        lista = seletor._lista
        self.assertIn(lista, janela.filhos)

        self.view.mudar_modo("calculo")

        self.assertNotIn(lista, janela.filhos)


if __name__ == "__main__":
    unittest.main()
