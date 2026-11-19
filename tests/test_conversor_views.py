import unittest

from tests import fake_ctk


def setUpModule():
    fake_ctk.instalar()

    global ConversorView, ConversorMoedasView, tema
    from swaplator.interface.conversor_view import ConversorView
    from swaplator.interface.conversor_moedas_view import ConversorMoedasView
    from swaplator.interface import tema


def tearDownModule():
    fake_ctk.remover()


class TestResultadoReservaEspaco(unittest.TestCase):
    """A altura do rótulo é só um mínimo: se o texto tiver mais linhas que
    o espaço reservado, o cartão cresce e "pula". Reservamos 3 linhas."""

    def test_conversor_de_unidades(self):
        view = ConversorView(fake_ctk.Fake(), lambda *args: 0, ["m", "cm"])

        self.assertEqual(view.label_resultado.opcoes["height"], tema.ALTURA_RESULTADO)

    def test_conversor_de_moedas(self):
        view = ConversorMoedasView(
            fake_ctk.Fake(),
            lambda *args: 0,
            lambda: {"USD": 1.0, "BRL": 5.0}
        )

        self.assertEqual(view.label_resultado.opcoes["height"], tema.ALTURA_RESULTADO)

    def test_altura_reservada_comporta_tres_linhas_da_fonte_do_resultado(self):
        # Uma linha da fonte tem cerca de 4/3 do tamanho (em pixels).
        tres_linhas = 3 * round(tema.TAM_GRANDE * 4 / 3)

        self.assertGreaterEqual(tema.ALTURA_RESULTADO, tres_linhas)


if __name__ == "__main__":
    unittest.main()
