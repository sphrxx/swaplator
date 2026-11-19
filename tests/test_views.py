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


class TestTrocaDeModoAdiada(unittest.TestCase):
    """O seletor de modo é destruído pela própria troca de modo.

    Por isso a reconstrução precisa esperar o clique terminar (a animação
    do botão roda até ~100 ms depois do comando).
    """

    def setUp(self):
        self.janela = fake_ctk.Fake()
        self.agendados = []

        # A janela guarda o que foi agendado, em vez de esperar o relógio.
        self.janela.after = lambda ms, funcao=None, *args: self.agendados.append(funcao)

        self.view = CalculadoraView(self.janela)

    def test_selecionar_modo_nao_reconstroi_dentro_do_proprio_clique(self):
        seletor_modo = self.view.seletor_modo

        self.view.selecionar_modo("Conversor")

        self.assertEqual(self.view.modo, "calculo")
        self.assertIn(seletor_modo, self.view.frame.filhos)
        self.assertEqual(len(self.agendados), 1)

    def test_modo_muda_quando_o_tempo_passa(self):
        seletor_modo_antigo = self.view.seletor_modo

        self.view.selecionar_modo("Conversor")
        self.agendados[0]()

        self.assertEqual(self.view.modo, "conversao")
        self.assertNotIn(seletor_modo_antigo, self.view.frame.filhos)

    def test_nao_muda_o_modo_se_a_tela_ja_foi_destruida(self):
        self.view.selecionar_modo("Conversor")
        self.view.frame.winfo_exists = lambda: False

        self.agendados[0]()

        self.assertEqual(self.view.modo, "calculo")


class TestBotoesRedondosDaCalculadora(unittest.TestCase):

    def test_todos_os_botoes_da_grade_sao_redondos(self):
        from swaplator.interface.componentes import BotaoRedondo

        view = CalculadoraView(fake_ctk.Fake())

        # Procura só no quadro dos botões: o visor também tem o texto "0".
        for texto in ("7", "0", ".", "C", "=", "÷"):
            botao = fake_ctk.achar_botao(view.frame_botoes, texto)
            self.assertIsInstance(botao, BotaoRedondo, texto)


if __name__ == "__main__":
    unittest.main()
