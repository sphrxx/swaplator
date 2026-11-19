import unittest

from tests import fake_ctk


def setUpModule():
    fake_ctk.instalar()

    global BotaoRedondo, executar_depois_do_clique, tema
    from swaplator.interface.componentes import BotaoRedondo, executar_depois_do_clique
    from swaplator.interface import tema


def tearDownModule():
    fake_ctk.remover()


class TestBotaoRedondo(unittest.TestCase):

    def test_sem_o_ajuste_o_botao_reserva_o_raio_nas_pontas(self):
        # Documenta a causa do botão "oval": o CTkButton reserva `corner_radius`
        # de largura nas colunas das pontas (o Fake imita isso).
        botao = fake_ctk.Fake(fake_ctk.Fake(), corner_radius=36)

        botao._create_grid()

        self.assertEqual(botao.colunas[(0, 4)]["minsize"], 36)

    def test_create_grid_zera_o_minsize_das_pontas(self):
        botao = BotaoRedondo(fake_ctk.Fake(), corner_radius=36)

        botao._create_grid()

        self.assertEqual(botao.colunas[(0, 4)]["minsize"], 0)

    def test_continua_zerado_quando_a_grade_e_refeita(self):
        # O CustomTkinter refaz a grade ao mudar a escala (DPI) da tela.
        botao = BotaoRedondo(fake_ctk.Fake(), corner_radius=36)

        botao._create_grid()
        botao._create_grid()

        self.assertEqual(botao.colunas[(0, 4)]["minsize"], 0)


class TestExecutarDepoisDoClique(unittest.TestCase):

    def setUp(self):
        self.janela = fake_ctk.Fake()
        self.widget = fake_ctk.Fake(self.janela)
        self.agendados = []
        self.chamadas = []

        # A janela guarda o que foi agendado, em vez de esperar o relógio.
        self.janela.after = lambda ms, funcao=None, *args: self.agendados.append((ms, funcao))

    def test_nao_executa_na_hora_e_agenda_na_janela(self):
        executar_depois_do_clique(self.widget, lambda: self.chamadas.append("rodou"))

        self.assertEqual(self.chamadas, [])
        self.assertEqual(len(self.agendados), 1)
        self.assertEqual(self.agendados[0][0], tema.TEMPO_ANIMACAO_CLIQUE)

    def test_executa_quando_o_tempo_passa(self):
        executar_depois_do_clique(self.widget, lambda: self.chamadas.append("rodou"))

        self.agendados[0][1]()

        self.assertEqual(self.chamadas, ["rodou"])

    def test_ignora_se_o_widget_ja_foi_destruido(self):
        executar_depois_do_clique(self.widget, lambda: self.chamadas.append("rodou"))
        self.widget.winfo_exists = lambda: False

        self.agendados[0][1]()

        self.assertEqual(self.chamadas, [])


if __name__ == "__main__":
    unittest.main()
