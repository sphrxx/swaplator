import unittest

from tests import fake_ctk


def setUpModule():
    fake_ctk.instalar()

    global Sidebar, ITENS, tema
    from swaplator.interface import tema
    from swaplator.interface.sidebar import Sidebar, ITENS


def tearDownModule():
    fake_ctk.remover()


class TestSidebar(unittest.TestCase):

    def setUp(self):
        self.escolhidas = []
        self.sidebar = Sidebar(fake_ctk.Fake(), self.escolhidas.append)

    def test_ordem_dos_itens(self):
        self.assertEqual(
            [view for view, _ in ITENS],
            ["calculadora", "comprimento", "area", "massa",
             "volume", "temperatura", "moedas"])

    def test_cada_item_tem_icone_desenhado_e_texto(self):
        for view, texto in ITENS:
            item = self.sidebar.botoes[view]

            self.assertTrue(item.icone.desenhos, view)
            self.assertEqual(item.texto.opcoes["text"], texto)

    def test_clicar_chama_o_callback_com_a_chave(self):
        self.sidebar.botoes["massa"].clicar()

        self.assertEqual(self.escolhidas, ["massa"])

    def test_marcar_ativo_destaca_so_o_escolhido(self):
        self.sidebar.marcar_ativo("area")

        for view, item in self.sidebar.botoes.items():
            esperado = tema.COR_DESTAQUE if view == "area" else "transparent"
            self.assertEqual(item.opcoes["fg_color"], esperado, view)
            self.assertEqual(item.ativo, view == "area", view)

    def test_trocar_o_ativo_limpa_o_anterior(self):
        self.sidebar.marcar_ativo("area")
        self.sidebar.marcar_ativo("massa")

        self.assertFalse(self.sidebar.botoes["area"].ativo)
        self.assertEqual(self.sidebar.botoes["area"].opcoes["fg_color"], "transparent")

    def test_largura_do_item_vem_do_tema(self):
        self.assertEqual(self.sidebar.botoes["area"].opcoes["width"],
                         tema.LARGURA_ITEM_SIDEBAR)


class TestSidebarDpi(unittest.TestCase):

    def test_icone_segue_a_escala_da_tela(self):
        fake_ctk.Fake._get_widget_scaling = lambda self: 1.5
        self.addCleanup(delattr, fake_ctk.Fake, "_get_widget_scaling")

        sidebar = Sidebar(fake_ctk.Fake(), lambda view: None)

        lado = round(tema.TAMANHO_ICONE * 1.5)
        self.assertEqual(sidebar.botoes["area"].icone.opcoes["width"], lado)
