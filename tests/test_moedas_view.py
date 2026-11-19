import unittest

from tests import fake_ctk


def setUpModule():
    fake_ctk.instalar()

    global ConversorMoedasView
    from swaplator.interface.conversor_moedas_view import ConversorMoedasView


def tearDownModule():
    fake_ctk.remover()


class TestTentarNovamente(unittest.TestCase):

    def setUp(self):
        self.janela = fake_ctk.Fake()
        self.agendados = []
        self.chamadas = 0

        # A janela guarda o que foi agendado, em vez de esperar o relógio.
        self.janela.after = lambda ms, funcao=None, *args: self.agendados.append(funcao)

    def obter_cotacoes_que_funciona_na_segunda(self):
        self.chamadas += 1

        if self.chamadas == 1:
            raise ValueError("sem internet")

        return {"USD": 1.0, "BRL": 5.0}

    def obter_cotacoes_que_sempre_falha(self):
        raise ValueError("sem internet")

    def criar_view(self, obter_cotacoes):
        return ConversorMoedasView(self.janela, lambda *args: 0, obter_cotacoes)

    def test_botao_nao_e_destruido_dentro_do_proprio_clique(self):
        view = self.criar_view(self.obter_cotacoes_que_funciona_na_segunda)
        botao = view.button_retry

        botao.opcoes["command"]()

        self.assertIn(botao, view.cartao.filhos)
        self.assertEqual(len(self.agendados), 1)

    def test_botao_fica_desativado_para_o_duplo_clique_nao_buscar_duas_vezes(self):
        view = self.criar_view(self.obter_cotacoes_que_funciona_na_segunda)

        view.button_retry.opcoes["command"]()

        self.assertEqual(view.button_retry.opcoes["state"], "disabled")

    def test_tela_e_reconstruida_depois_do_clique(self):
        view = self.criar_view(self.obter_cotacoes_que_funciona_na_segunda)
        cartao_antigo = view.cartao

        view.button_retry.opcoes["command"]()
        self.agendados[0]()

        self.assertEqual(view.cotacoes, {"USD": 1.0, "BRL": 5.0})
        self.assertTrue(hasattr(view, "combobox_moeda_inicial"))
        self.assertNotIn(cartao_antigo, view.frame.filhos)

    def test_se_falhar_de_novo_mostra_a_tela_de_erro_outra_vez(self):
        view = self.criar_view(self.obter_cotacoes_que_sempre_falha)
        botao_antigo = view.button_retry

        botao_antigo.opcoes["command"]()
        self.agendados[0]()

        self.assertIsNone(view.cotacoes)
        self.assertIsNot(view.button_retry, botao_antigo)
        self.assertIn(view.button_retry, view.cartao.filhos)


if __name__ == "__main__":
    unittest.main()
