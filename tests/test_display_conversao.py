import unittest

from tests import fake_ctk


def setUpModule():
    fake_ctk.instalar()

    global DisplayConversao, tema
    from swaplator.interface import tema
    from swaplator.interface.display_conversao import DisplayConversao


def tearDownModule():
    fake_ctk.remover()


UNIDADES = ["mm", "cm", "m"]


class TestDisplayConversao(unittest.TestCase):

    def setUp(self):
        self.avisos = []
        self.display = DisplayConversao(
            fake_ctk.Fake(), UNIDADES,
            ao_mudar_unidade=lambda: self.avisos.append(True))

    def test_mostrar_escreve_as_duas_linhas(self):
        self.display.mostrar("12", "1.2")

        self.assertEqual(self.display.label_entrada.opcoes["text"], "12")
        self.assertEqual(self.display.label_resultado.opcoes["text"], "1.2")

    def test_fonte_da_linha_de_cima_encolhe_com_numeros_longos(self):
        texto = "1" * 16
        self.display.mostrar(texto, "0")

        self.assertEqual(self.display.label_entrada.opcoes["font"],
                         tema.fonte(tema.tamanho_fonte_display(texto)))

    def test_linha_de_baixo_nunca_passa_do_titulo(self):
        self.display.mostrar("5", "5")

        esperado = min(tema.tamanho_fonte_display("5"), tema.TAM_TITULO)
        self.assertEqual(self.display.label_resultado.opcoes["font"],
                         tema.fonte(esperado))

    def test_alturas_das_linhas_sao_fixas(self):
        for texto in ("1", "1" * 25):
            self.display.mostrar(texto, texto)

            self.assertEqual(self.display.label_entrada.opcoes["height"],
                             tema.ALTURA_LINHA_DISPLAY)
            self.assertEqual(self.display.label_resultado.opcoes["height"],
                             tema.ALTURA_LINHA_DISPLAY)

    def test_comeca_com_as_duas_primeiras_unidades(self):
        self.assertEqual(self.display.unidade_inicial(), "mm")
        self.assertEqual(self.display.unidade_final(), "cm")

    def test_definir_unidades_seleciona_as_duas_primeiras(self):
        self.display.definir_unidades(["a", "b", "c"])

        self.assertEqual(self.display.unidade_inicial(), "a")
        self.assertEqual(self.display.unidade_final(), "b")
        self.assertEqual(
            self.display.combobox_unidade_inicial.opcoes["values"], ["a", "b", "c"])
        self.assertEqual(
            self.display.combobox_unidade_final.opcoes["values"], ["a", "b", "c"])

    def test_trocar_unidade_avisa(self):
        self.display.combobox_unidade_final.opcoes["command"]("m")
        self.display.combobox_unidade_inicial.opcoes["command"]("cm")

        self.assertEqual(len(self.avisos), 2)

    def test_caixas_usam_largura_e_altura_do_tema(self):
        for caixa in (self.display.combobox_unidade_inicial,
                      self.display.combobox_unidade_final):
            self.assertEqual(caixa.opcoes["width"], tema.LARGURA_COMBOBOX_UNIDADE)
            self.assertEqual(caixa.opcoes["height"], tema.ALTURA_CONTROLE)
