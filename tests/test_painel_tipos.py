import unittest

from tests import fake_ctk


def setUpModule():
    fake_ctk.instalar()

    global PainelTipos, tema
    from swaplator.interface import tema
    from swaplator.interface.painel_tipos import PainelTipos


def tearDownModule():
    fake_ctk.remover()


ROTULOS = {"comprimento": "Comprimento", "area": "Área", "massa": "Massa",
           "volume": "Volume", "temperatura": "Temperatura"}
CHAVES = list(ROTULOS)
SEQUENCIAS = {"<Left>", "<Right>", "<Up>", "<Down>", "<Return>", "<Escape>"}


class PainelBase(unittest.TestCase):

    def setUp(self):
        self.janela = fake_ctk.Fake()
        self.escolhidos = []
        self.fechou = []
        self.painel = PainelTipos(
            self.janela, ROTULOS, "comprimento",
            ao_escolher=self.escolhidos.append,
            ao_fechar=lambda: self.fechou.append(True))

    def cor(self, chave):
        return self.painel.tiles[chave].opcoes["fg_color"]


class TestPainelTipos(PainelBase):

    def test_um_tile_por_tipo_em_tres_colunas(self):
        posicoes = [(self.painel.tiles[c].opcoes_grid["row"],
                     self.painel.tiles[c].opcoes_grid["column"]) for c in CHAVES]

        self.assertEqual(posicoes, [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1)])

    def test_tile_ativo_fica_laranja(self):
        self.assertEqual(self.cor("comprimento"), tema.COR_DESTAQUE)
        self.assertEqual(self.cor("area"), tema.COR_DIGITO)

        self.painel.definir_ativo("massa")

        self.assertEqual(self.cor("massa"), tema.COR_DESTAQUE)
        self.assertEqual(self.cor("comprimento"), tema.COR_DIGITO)

    def test_clicar_no_tile_escolhe(self):
        self.painel.escolher("massa")

        self.assertEqual(self.escolhidos, ["massa"])

    def test_cada_tile_tem_icone_e_nome(self):
        for chave in CHAVES:
            self.assertTrue(self.painel.icones[chave].desenhos, chave)

        textos = [f.opcoes.get("text") for f in self.painel.tiles["area"].filhos]
        self.assertIn("Área", textos)


class TestPainelTiposDpi(unittest.TestCase):

    def test_icones_seguem_a_escala(self):
        fake_ctk.Fake._get_widget_scaling = lambda self: 1.5
        self.addCleanup(delattr, fake_ctk.Fake, "_get_widget_scaling")

        painel = PainelTipos(fake_ctk.Fake(), ROTULOS, "area",
                             ao_escolher=lambda t: None, ao_fechar=lambda: None)

        lado = round(tema.TAMANHO_ICONE_PAINEL * 1.5)
        for chave in CHAVES:
            self.assertEqual(painel.icones[chave].opcoes["width"], lado)


class TestPainelTiposTeclado(PainelBase):

    def test_comeca_invisivel(self):
        self.assertFalse(self.painel.visivel)

    def test_mostrar_poe_o_foco_no_tile_ativo(self):
        self.painel.mostrar()

        self.assertTrue(self.painel.visivel)
        self.assertEqual(self.cor("comprimento"), tema.COR_DESTAQUE_HOVER)

    def test_setas_andam_pela_grade(self):
        self.painel.mostrar()

        self.painel._ao_direita()
        self.assertEqual(self.cor("area"), tema.COR_DIGITO_HOVER)
        self.assertEqual(self.cor("comprimento"), tema.COR_DESTAQUE)

        self.painel._ao_baixo()   # area (1) + 3 = temperatura (4)
        self.assertEqual(self.cor("temperatura"), tema.COR_DIGITO_HOVER)

        self.painel._ao_cima()    # volta para area (1)
        self.assertEqual(self.cor("area"), tema.COR_DIGITO_HOVER)

        self.painel._ao_esquerda()
        self.assertEqual(self.cor("comprimento"), tema.COR_DESTAQUE_HOVER)

    def test_setas_nao_passam_das_bordas(self):
        self.painel.mostrar()

        self.painel._ao_esquerda()
        self.painel._ao_cima()
        self.assertEqual(self.cor("comprimento"), tema.COR_DESTAQUE_HOVER)

        for _ in range(6):
            self.painel._ao_direita()
        self.assertEqual(self.cor("temperatura"), tema.COR_DIGITO_HOVER)

        self.painel._ao_baixo()
        self.assertEqual(self.cor("temperatura"), tema.COR_DIGITO_HOVER)

    def test_enter_escolhe_o_tile_em_foco(self):
        self.painel.mostrar()
        self.painel._ao_direita()
        self.painel._ao_direita()

        self.painel._ao_enter()

        self.assertEqual(self.escolhidos, ["massa"])

    def test_esc_pede_para_fechar(self):
        self.painel.mostrar()

        self.painel._ao_esc()

        self.assertEqual(self.fechou, [True])

    def test_ocultar_esconde_o_painel(self):
        self.painel.mostrar()
        self.painel.ocultar()

        self.assertFalse(self.painel.visivel)
        self.assertTrue(self.painel.grid_removido)

    def test_handlers_nao_fazem_nada_com_o_painel_oculto(self):
        for handler in (self.painel._ao_direita, self.painel._ao_baixo,
                        self.painel._ao_cima, self.painel._ao_esquerda,
                        self.painel._ao_enter, self.painel._ao_esc):
            handler()

        self.assertEqual(self.escolhidos, [])
        self.assertEqual(self.fechou, [])


class TestPainelTiposBinds(PainelBase):

    def test_binds_da_janela_uma_vez_so(self):
        self.painel.mostrar()
        self.painel.ocultar()
        self.painel.mostrar()

        sequencias = [seq for seq, _ in self.janela.binds]
        self.assertEqual(sorted(sequencias), sorted(SEQUENCIAS))
        self.assertEqual(self.janela.unbinds, [])

    def test_destroy_desfaz_os_binds(self):
        self.painel.mostrar()
        ids = list(self.janela.binds)

        self.painel.destroy()

        self.assertEqual(sorted(self.janela.unbinds), sorted(ids))

    def test_destruir_o_pai_tambem_desfaz_os_binds(self):
        pai = fake_ctk.Fake(self.janela)
        painel = PainelTipos(pai, ROTULOS, "area",
                             ao_escolher=lambda t: None, ao_fechar=lambda: None)
        painel.mostrar()
        ids = list(self.janela.binds)

        pai.destroy()

        self.assertEqual(sorted(self.janela.unbinds), sorted(ids))
