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


if __name__ == "__main__":
    unittest.main()
