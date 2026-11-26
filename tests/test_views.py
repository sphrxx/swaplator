import unittest

from tests import fake_ctk


def setUpModule():
    # As telas importam o customtkinter ao serem carregadas, então o de mentira
    # precisa estar instalado antes do import.
    fake_ctk.instalar()

    global CalculadoraView, tema
    from swaplator.interface.calculadora_view import CalculadoraView
    from swaplator.interface import tema


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


class TestMenusDasUnidadesComALista(unittest.TestCase):
    """O menu de uma combobox é uma janelinha própria, sempre acima de tudo:
    se ficasse aberto, taparia a lista de tipos."""

    def setUp(self):
        self.view = CalculadoraView(fake_ctk.Fake())
        self.view.mudar_modo("conversao")

    def _menu_aberto_em(self, combobox):
        fechado = []
        menu = fake_ctk.Fake()
        menu.close = lambda: fechado.append(True)
        combobox._dropdown_menu = menu
        combobox._close_on_next_click = True
        return fechado

    def test_abrir_a_lista_fecha_o_menu_das_duas_unidades(self):
        inicial = self.view.combobox_unidade_inicial
        final = self.view.combobox_unidade_final
        fechou_inicial = self._menu_aberto_em(inicial)
        fechou_final = self._menu_aberto_em(final)

        self.view.combobox_tipo_conversao.abrir()

        self.assertEqual(fechou_inicial, [True])
        self.assertEqual(fechou_final, [True])
        # Senão o próximo clique na combobox "fecharia" um menu já fechado
        # em vez de abrir o dela.
        self.assertFalse(inicial._close_on_next_click)
        self.assertFalse(final._close_on_next_click)

    def test_combobox_sem_menu_interno_nao_quebra_a_abertura(self):
        # O Fake não tem _dropdown_menu: simula uma versão do CTk diferente.
        self.view.combobox_tipo_conversao.abrir()

        self.assertTrue(self.view.combobox_tipo_conversao.esta_aberto)


class TestAparenciaDaCalculadora(unittest.TestCase):

    def setUp(self):
        self.view = CalculadoraView(fake_ctk.Fake())

    def test_fonte_do_visor_diminui_para_numeros_longos(self):
        for digito in "1234567891234567":   # 16 dígitos, sem zero (o visor também é "0")
            fake_ctk.achar_botao(self.view.frame_botoes, digito).opcoes["command"]()

        self.assertEqual(self.view.display.opcoes["font"], tema.fonte(tema.TAM_GRANDE))

    def test_fonte_do_visor_e_grande_para_numeros_curtos(self):
        fake_ctk.achar_botao(self.view.frame_botoes, "7").opcoes["command"]()

        self.assertEqual(self.view.display.opcoes["font"], tema.fonte(tema.TAM_DISPLAY))

    def test_controles_da_linha_de_conversao_tem_a_mesma_altura(self):
        self.view.mudar_modo("conversao")
        controles = (
            self.view.combobox_tipo_conversao,
            self.view.combobox_unidade_inicial,
            self.view.combobox_unidade_final,
        )

        for controle in controles:
            self.assertEqual(controle.opcoes["height"], tema.ALTURA_CONTROLE)

    def test_caixas_de_unidade_sao_estreitas_para_caber_na_janela_minima(self):
        self.view.mudar_modo("conversao")

        for caixa in (self.view.combobox_unidade_inicial, self.view.combobox_unidade_final):
            self.assertEqual(caixa.opcoes["width"], tema.LARGURA_COMBOBOX_UNIDADE)

    def test_linha_de_conversao_cabe_na_largura_minima_da_janela(self):
        # Largura da linha (seletor + 2 caixas + 3x2x4 de espaço + 10 de borda),
        # mais bordas da tela (20 + 16) e da barra lateral (~220).
        linha = tema.LARGURA_SELETOR_TIPO + 2 * tema.LARGURA_COMBOBOX_UNIDADE + 24 + 10
        necessario = linha + 20 + 16 + 220

        self.assertLessEqual(necessario, tema.JANELA_LARGURA_MINIMA)


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
