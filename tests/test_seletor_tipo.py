import unittest
from types import SimpleNamespace

from tests import fake_ctk


def setUpModule():
    # O módulo importa o customtkinter ao carregar, então o de mentira
    # precisa estar instalado antes do import.
    fake_ctk.instalar()

    global SeletorTipo, tema
    from swaplator.interface import tema
    from swaplator.interface.seletor_tipo import SeletorTipo


def tearDownModule():
    fake_ctk.remover()


OPCOES = {"comprimento": "Comprimento", "area": "Área",
          "temperatura": "Temperatura"}


class TestSeletorTipo(unittest.TestCase):

    def setUp(self):
        self.janela = fake_ctk.Fake()
        self.escolhas = []
        self.seletor = SeletorTipo(self.janela, OPCOES,
                                   command=self.escolhas.append)

    def test_valor_inicial_e_o_primeiro_tipo(self):
        self.assertEqual(self.seletor.get(), "comprimento")

    def test_set_troca_o_valor_sem_chamar_command(self):
        self.seletor.set("area")

        self.assertEqual(self.seletor.get(), "area")
        self.assertEqual(self.escolhas, [])

    def test_set_com_chave_inexistente_levanta_value_error(self):
        with self.assertRaises(ValueError):
            self.seletor.set("massa")

    def test_abrir_fechar_e_alternar(self):
        self.assertFalse(self.seletor.esta_aberto)

        self.seletor.abrir()
        self.assertTrue(self.seletor.esta_aberto)

        self.seletor.fechar()
        self.assertFalse(self.seletor.esta_aberto)

        self.seletor.alternar()
        self.assertTrue(self.seletor.esta_aberto)

        self.seletor.alternar()
        self.assertFalse(self.seletor.esta_aberto)

    def test_escolher_atualiza_valor_fecha_e_chama_command_uma_vez(self):
        self.seletor.abrir()

        self.seletor.escolher("area")

        self.assertEqual(self.seletor.get(), "area")
        self.assertFalse(self.seletor.esta_aberto)
        self.assertEqual(self.escolhas, ["area"])

    def test_escolher_o_tipo_atual_ainda_chama_command(self):
        self.seletor.abrir()

        self.seletor.escolher("comprimento")

        self.assertEqual(self.escolhas, ["comprimento"])

    def test_clique_fora_fecha_mas_clique_na_lista_nao(self):
        self.seletor.abrir()

        filho_da_lista = fake_ctk.Fake(self.seletor.linhas["area"])
        self.seletor._ao_clicar(SimpleNamespace(widget=filho_da_lista))
        self.assertTrue(self.seletor.esta_aberto)

        self.seletor._ao_clicar(SimpleNamespace(widget=fake_ctk.Fake()))
        self.assertFalse(self.seletor.esta_aberto)

    def test_clique_no_gatilho_nao_fecha_pelo_clique_fora(self):
        self.seletor.abrir()

        filho_do_gatilho = fake_ctk.Fake(self.seletor)
        self.seletor._ao_clicar(SimpleNamespace(widget=filho_do_gatilho))

        self.assertTrue(self.seletor.esta_aberto)

    def test_esc_fecha(self):
        self.seletor.abrir()

        self.seletor._ao_esc()

        self.assertFalse(self.seletor.esta_aberto)

    def test_destacar_pinta_so_a_linha_alvo(self):
        self.seletor.abrir()

        self.seletor._destacar("area")

        for chave, linha in self.seletor.linhas.items():
            esperado = tema.COR_DIGITO if chave == "area" else "transparent"
            self.assertEqual(linha.opcoes["fg_color"], esperado)

    def test_destroy_remove_a_lista_da_janela(self):
        self.seletor.abrir()
        lista = self.seletor.linhas["area"].master
        self.assertIn(lista, self.janela.filhos)

        self.seletor.destroy()

        self.assertNotIn(lista, self.janela.filhos)


class TestSeletorTipoDpi(unittest.TestCase):
    """Com tela a 150%, o que é tk puro precisa ser multiplicado à mão."""

    def setUp(self):
        # O Fake não tem escala própria; o CTk de verdade tem este método.
        fake_ctk.Fake._get_widget_scaling = lambda self: 1.5
        self.addCleanup(delattr, fake_ctk.Fake, "_get_widget_scaling")
        self.janela = fake_ctk.Fake()
        self.seletor = SeletorTipo(self.janela, OPCOES)

    def _canvases(self, pai):
        achados = []
        for filho in pai.filhos:
            if isinstance(filho, fake_ctk.FakeCanvas):
                achados.append(filho)
            achados.extend(self._canvases(filho))
        return achados

    def test_coluna_da_lista_tem_largura_minima_do_gatilho(self):
        self.seletor.abrir()
        lista = self.seletor.linhas["area"].master

        self.assertEqual(lista.colunas[0]["minsize"],
                         round(tema.LARGURA_SELETOR_TIPO * 1.5))

    def test_canvases_e_desenhos_seguem_a_escala(self):
        self.seletor.abrir()
        lado = round(tema.TAMANHO_ICONE * 1.5)
        canvases = self._canvases(self.janela)
        self.assertTrue(canvases)

        for canvas in canvases:
            self.assertEqual(canvas.opcoes["width"], lado)
            self.assertEqual(canvas.opcoes["height"], lado)
            self.assertTrue(canvas.desenhos)
            for _, coords, _ in canvas.desenhos:
                for valor in coords:
                    self.assertTrue(0 <= valor <= lado, valor)

    def test_paddings_dos_canvases_sao_multiplicados(self):
        self.assertEqual(self.seletor._icone.opcoes_grid["padx"], (18, 12))


class TestSeletorTipoBinds(unittest.TestCase):

    def setUp(self):
        self.janela = fake_ctk.Fake()
        self.seletor = SeletorTipo(self.janela, OPCOES)

    def test_abrir_fechar_abrir_nao_repete_os_binds_da_janela(self):
        self.seletor.abrir()
        self.seletor.fechar()
        self.seletor.abrir()

        self.assertEqual(len(self.janela.binds), 2)
        self.assertEqual(self.janela.unbinds, [])

    def test_handlers_da_janela_ignoram_eventos_com_a_lista_fechada(self):
        self.seletor.abrir()
        self.seletor.fechar()

        # Não pode dar erro nem reabrir/fechar nada.
        self.seletor._ao_clicar(SimpleNamespace(widget=fake_ctk.Fake()))
        self.seletor._ao_esc()
        self.assertFalse(self.seletor.esta_aberto)

    def test_destroy_desfaz_os_binds_guardados(self):
        self.seletor.abrir()
        ids = list(self.janela.binds)

        self.seletor.destroy()

        self.assertEqual(sorted(self.janela.unbinds), sorted(ids))


class TestSeletorTipoHover(unittest.TestCase):

    def setUp(self):
        self.janela = fake_ctk.Fake()
        self.seletor = SeletorTipo(self.janela, OPCOES)
        self.seletor.abrir()
        self.lista = self.seletor.linhas["area"].master

    def _contar_configure(self):
        chamadas = []
        for linha in self.seletor.linhas.values():
            original = linha.configure
            linha.configure = (lambda original=original, **kw:
                               (chamadas.append(kw), original(**kw)))
        return chamadas

    def test_destacar_a_mesma_linha_de_novo_nao_reconfigura(self):
        self.seletor._destacar("area")
        chamadas = self._contar_configure()

        self.seletor._destacar("area")

        self.assertEqual(chamadas, [])

    def test_sair_da_lista_limpa_o_destaque(self):
        self.seletor._destacar("area")

        self.seletor._ao_sair_da_lista(SimpleNamespace())

        for linha in self.seletor.linhas.values():
            self.assertEqual(linha.opcoes["fg_color"], "transparent")

    def test_sair_para_um_filho_da_lista_mantem_o_destaque(self):
        self.seletor._destacar("area")
        self.lista.winfo_pointerxy = lambda: (10, 10)
        self.lista.winfo_width = lambda: 100
        self.lista.winfo_height = lambda: 100

        self.seletor._ao_sair_da_lista(SimpleNamespace())

        self.assertEqual(self.seletor.linhas["area"].opcoes["fg_color"],
                         tema.COR_DIGITO)
