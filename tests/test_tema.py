import re
import unittest

from swaplator.interface import tema


NOMES_DAS_CORES = [
    "COR_FUNDO",
    "COR_SUPERFICIE",
    "COR_DIGITO",
    "COR_DIGITO_HOVER",
    "COR_FUNCAO",
    "COR_FUNCAO_HOVER",
    "COR_DESTAQUE",
    "COR_DESTAQUE_HOVER",
    "COR_TEXTO",
    "COR_TEXTO_ESCURO",
    "COR_TEXTO_SECUNDARIO",
    "COR_ERRO",
]

CHAVES_ESTILO = {"fg_color", "hover_color", "text_color", "corner_radius", "font"}


class TestTema(unittest.TestCase):

    def test_cores_sao_hexadecimais(self):
        for nome in NOMES_DAS_CORES:
            with self.subTest(cor=nome):
                valor = getattr(tema, nome)
                self.assertRegex(valor, r"^#[0-9A-Fa-f]{6}$")

    def test_valores_da_paleta(self):
        self.assertEqual(tema.COR_DESTAQUE, "#FF9F0A")
        self.assertEqual(tema.COR_FUNDO, "#000000")
        self.assertEqual(tema.COR_DIGITO, "#333333")
        self.assertEqual(tema.COR_FUNCAO, "#A5A5A5")

    def test_fonte_retorna_tupla(self):
        self.assertEqual(tema.fonte(20, "bold"), ("Segoe UI", 20, "bold"))
        self.assertEqual(tema.fonte(14)[2], "normal")

    def test_estilo_botao_chaves(self):
        for tipo in ("digito", "funcao", "destaque"):
            with self.subTest(tipo=tipo):
                self.assertEqual(set(tema.estilo_botao(tipo)), CHAVES_ESTILO)

    def test_estilo_destaque_usa_laranja(self):
        self.assertEqual(tema.estilo_botao("destaque")["fg_color"], tema.COR_DESTAQUE)
        self.assertEqual(tema.estilo_botao("funcao")["text_color"], tema.COR_TEXTO_ESCURO)

    def test_estilo_combobox_usa_cores_do_tema(self):
        estilo = tema.estilo_combobox()

        self.assertEqual(estilo["fg_color"], tema.COR_DIGITO)
        self.assertEqual(estilo["button_color"], tema.COR_DESTAQUE)
        self.assertEqual(estilo["corner_radius"], tema.RAIO_CARTAO)

    def test_estilo_botao_compacto_e_menor_e_arredondado(self):
        estilo = tema.estilo_botao("destaque", compacto=True)

        self.assertEqual(estilo["height"], tema.ALTURA_CONTROLE)
        self.assertEqual(estilo["corner_radius"], tema.ALTURA_CONTROLE // 2)
        self.assertEqual(estilo["font"], tema.fonte(16))
        self.assertNotIn("height", tema.estilo_botao("destaque"))

    def test_estilo_entrada_usa_cores_do_tema(self):
        estilo = tema.estilo_entrada()

        self.assertEqual(estilo["fg_color"], tema.COR_DIGITO)
        self.assertEqual(estilo["text_color"], tema.COR_TEXTO)
        self.assertEqual(estilo["height"], tema.ALTURA_CONTROLE)

    def test_estilo_tipo_invalido(self):
        with self.assertRaises(ValueError):
            tema.estilo_botao("xyz")

    def test_estilos_usam_as_constantes_de_fonte(self):
        self.assertEqual(tema.estilo_botao("digito")["font"], tema.fonte(tema.TAM_GRANDE))
        self.assertEqual(tema.estilo_botao("digito", compacto=True)["font"], tema.fonte(tema.TAM_TEXTO))
        self.assertEqual(tema.estilo_entrada()["font"], tema.fonte(tema.TAM_TEXTO))
        self.assertEqual(tema.estilo_combobox()["font"], tema.fonte(tema.TAM_PEQUENO))

    def test_tamanho_fonte_display_diminui_conforme_o_texto_cresce(self):
        casos = [
            (1, tema.TAM_DISPLAY),
            (9, tema.TAM_DISPLAY),
            (10, 32),
            (15, 32),
            (16, tema.TAM_GRANDE),
            (22, tema.TAM_GRANDE),
            (23, 20),
            (30, 20),
            (31, tema.TAM_TEXTO),
            (80, tema.TAM_TEXTO),
        ]

        for quantidade, esperado in casos:
            with self.subTest(caracteres=quantidade):
                self.assertEqual(tema.tamanho_fonte_display("1" * quantidade), esperado)

    def test_tamanho_inicial_em_tela_grande_e_o_tamanho_preferido(self):
        self.assertEqual(tema.tamanho_inicial_janela(1920, 1080), (960, 760))

    def test_tamanho_inicial_respeita_margem_da_tela(self):
        # 768 px de altura x 90% = 691 px úteis, menos que os 760 preferidos.
        self.assertEqual(tema.tamanho_inicial_janela(1366, 768), (960, 691))

    def test_tamanho_inicial_considera_a_escala_da_tela(self):
        # 1080 px a 150% valem 720 unidades; 90% disso (648) fica abaixo do
        # mínimo, então vale o mínimo.
        self.assertEqual(
            tema.tamanho_inicial_janela(1920, 1080, escala=1.5),
            (960, tema.JANELA_ALTURA_MINIMA)
        )

    def test_tamanho_inicial_nunca_fica_abaixo_do_minimo(self):
        self.assertEqual(
            tema.tamanho_inicial_janela(800, 600),
            (tema.JANELA_LARGURA_MINIMA, tema.JANELA_ALTURA_MINIMA)
        )

    def test_minimo_cabe_no_tamanho_preferido(self):
        self.assertLessEqual(tema.JANELA_LARGURA_MINIMA, tema.JANELA_LARGURA_INICIAL)
        self.assertLessEqual(tema.JANELA_ALTURA_MINIMA, tema.JANELA_ALTURA_INICIAL)


    def test_tela_da_calculadora_cabe_na_janela_minima(self):
        # cabeçalho + display (2 linhas) + teclado (5 linhas de botão com
        # espaço) + ~60 de margens e respiros.
        altura = (tema.ALTURA_CABECALHO
                  + 2 * tema.ALTURA_LINHA_DISPLAY
                  + 5 * (tema.TAMANHO_BOTAO + tema.ESPACO)
                  + 60)

        self.assertLessEqual(altura, tema.JANELA_ALTURA_MINIMA)

    def test_item_da_sidebar_usa_a_largura_do_tema(self):
        self.assertEqual(tema.LARGURA_ITEM_SIDEBAR, 180)


if __name__ == "__main__":
    unittest.main()
