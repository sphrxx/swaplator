import unittest
from unittest import mock

from tests import fake_ctk


def setUpModule():
    fake_ctk.instalar()

    global Janela, tema
    from swaplator.interface.janela import Janela
    from swaplator.interface import tema


def tearDownModule():
    fake_ctk.remover()


class TestJanela(unittest.TestCase):

    def test_tamanho_inicial_e_tamanho_minimo(self):
        janela = Janela().janela

        self.assertEqual(janela.geometria, "960x760")
        self.assertEqual(
            janela.minimo,
            (tema.JANELA_LARGURA_MINIMA, tema.JANELA_ALTURA_MINIMA)
        )

    def test_tela_baixa_limita_a_altura_inicial(self):
        with mock.patch.object(fake_ctk.Fake, "winfo_screenheight", return_value=768):
            janela = Janela().janela

        self.assertEqual(janela.geometria, "960x691")

    def test_usa_a_escala_da_janela_para_calcular_o_espaco_da_tela(self):
        with mock.patch.object(fake_ctk.FakeScalingTracker, "escala", 2.0):
            janela = Janela().janela

        # 1920x1080 a 200% valem 960x540 unidades. Largura: 90% de 960 = 864.
        # Altura: 90% de 540 = 486, abaixo do mínimo, então vale o mínimo.
        self.assertEqual(janela.geometria, f"864x{tema.JANELA_ALTURA_MINIMA}")


class TestTelaInicial(unittest.TestCase):

    def setUp(self):
        from swaplator.interface.calculadora_view import CalculadoraView
        self.CalculadoraView = CalculadoraView
        self.app = Janela()

    def test_abre_na_calculadora(self):
        self.assertIsInstance(self.app.view_atual, self.CalculadoraView)
        self.assertTrue(self.app.sidebar.botoes["calculadora"].ativo)
        self.assertFalse(self.app.sidebar.botoes["comprimento"].ativo)

    def test_trocar_de_tela_libera_o_painel(self):
        raiz = self.app.janela
        self.app.view_atual.abrir_painel()
        sequencias = {seq for seq, _ in raiz.binds}

        self.app.selecionar_view("area")

        self.assertEqual({seq for seq, _ in raiz.unbinds}, sequencias)
        self.assertEqual(len(sequencias), 6)


if __name__ == "__main__":
    unittest.main()
