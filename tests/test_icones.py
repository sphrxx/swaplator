import unittest

from swaplator.conversores.registro import CONVERSOES
from swaplator.interface.icones import ICONES, desenhar_seta
from tests.fake_ctk import FakeCanvas


def _numeros(coords):
    """Achata as coordenadas (que podem vir em listas) numa lista de números."""
    for item in coords:
        if isinstance(item, (list, tuple)):
            yield from _numeros(item)
        else:
            yield item


class TestIcones(unittest.TestCase):

    def test_todo_tipo_de_conversao_tem_icone(self):
        for tipo in CONVERSOES:
            self.assertIn(tipo, ICONES)

    def test_menu_lateral_tem_icones_de_calculadora_e_moedas(self):
        self.assertIn("calculadora", ICONES)
        self.assertIn("moedas", ICONES)

    def test_novos_icones_desenham_varias_formas(self):
        for chave in ("calculadora", "moedas"):
            canvas = FakeCanvas()
            ICONES[chave](canvas, 24, "#FFFFFF")

            self.assertGreaterEqual(len(canvas.desenhos), 3, chave)

    def test_cada_icone_desenha_formas_dentro_do_quadrado(self):
        funcoes = list(ICONES.values()) + [desenhar_seta]

        for tamanho in (24, 36):
            for funcao in funcoes:
                canvas = FakeCanvas()
                funcao(canvas, tamanho, "#FFFFFF")

                self.assertTrue(canvas.desenhos)
                for nome, coords, _ in canvas.desenhos:
                    for numero in _numeros(coords):
                        self.assertGreaterEqual(numero, 0, (funcao, nome))
                        self.assertLessEqual(numero, tamanho, (funcao, nome))

    def test_icone_usa_a_cor_recebida(self):
        for funcao in list(ICONES.values()) + [desenhar_seta]:
            canvas = FakeCanvas()
            funcao(canvas, 24, "#FF0000")

            for nome, _, opcoes in canvas.desenhos:
                cores = (opcoes.get("fill"), opcoes.get("outline"))
                self.assertIn("#FF0000", cores, (funcao, nome))


if __name__ == "__main__":
    unittest.main()
