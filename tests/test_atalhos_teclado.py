import unittest
from types import SimpleNamespace

from tests import fake_ctk


def setUpModule():
    fake_ctk.instalar()

    global AtalhosTeclado, traduzir_tecla
    from swaplator.interface.atalhos_teclado import AtalhosTeclado, traduzir_tecla


def tearDownModule():
    fake_ctk.remover()


def tecla(char="", keysym="", widget=None):
    return SimpleNamespace(char=char, keysym=keysym, widget=widget or fake_ctk.Fake())


class TestTraduzirTecla(unittest.TestCase):

    def test_digitos(self):
        for d in "0123456789":
            self.assertEqual(traduzir_tecla(tecla(d, d)), ("digitar", d))

    def test_ponto_e_virgula_viram_ponto(self):
        self.assertEqual(traduzir_tecla(tecla(".", "period")), ("digitar", "."))
        self.assertEqual(traduzir_tecla(tecla(",", "comma")), ("digitar", "."))

    def test_operadores(self):
        for char in "+-*/":
            self.assertEqual(traduzir_tecla(tecla(char)), ("operador", char))

    def test_x_minusculo_multiplica(self):
        self.assertEqual(traduzir_tecla(tecla("x", "x")), ("operador", "*"))

    def test_igual_e_enter_calculam(self):
        self.assertEqual(traduzir_tecla(tecla("=", "equal")), ("calcular", None))
        self.assertEqual(traduzir_tecla(tecla("\r", "Return")), ("calcular", None))
        self.assertEqual(traduzir_tecla(tecla("\r", "KP_Enter")), ("calcular", None))

    def test_esc_delete_e_c_limpam(self):
        self.assertEqual(traduzir_tecla(tecla("\x1b", "Escape")), ("limpar", None))
        self.assertEqual(traduzir_tecla(tecla("", "Delete")), ("limpar", None))
        self.assertEqual(traduzir_tecla(tecla("c", "c")), ("limpar", None))
        self.assertEqual(traduzir_tecla(tecla("C", "C")), ("limpar", None))

    def test_backspace_apaga(self):
        self.assertEqual(traduzir_tecla(tecla("\x08", "BackSpace")), ("apagar", None))

    def test_outras_teclas_sao_ignoradas(self):
        self.assertIsNone(traduzir_tecla(tecla("a", "a")))
        self.assertIsNone(traduzir_tecla(tecla("", "Shift_L")))
        self.assertIsNone(traduzir_tecla(tecla("\t", "Tab")))

    def test_ignora_quando_o_foco_esta_num_campo_de_texto(self):
        campo = fake_ctk.Fake()
        campo.winfo_class = lambda: "Entry"

        self.assertIsNone(traduzir_tecla(tecla("5", "5", widget=campo)))


class TestAtalhosTeclado(unittest.TestCase):

    def setUp(self):
        self.janela = fake_ctk.Fake()
        self.acoes = []
        self.atalhos = AtalhosTeclado(
            self.janela, lambda acao, valor: self.acoes.append((acao, valor)))

    def apertar(self, *args, **kwargs):
        for handler in self.janela.handlers["<Key>"]:
            handler(tecla(*args, **kwargs))

    def test_liga_um_unico_bind_na_janela(self):
        self.assertEqual([seq for seq, _ in self.janela.binds], ["<Key>"])

    def test_tecla_chama_a_acao(self):
        self.apertar("7", "7")
        self.apertar("+", "plus")

        self.assertEqual(self.acoes, [("digitar", "7"), ("operador", "+")])

    def test_tecla_ignorada_nao_chama_nada(self):
        self.apertar("a", "a")

        self.assertEqual(self.acoes, [])

    def test_destroy_desfaz_o_bind(self):
        ids = list(self.janela.binds)

        self.atalhos.destroy()

        self.assertEqual(self.janela.unbinds, ids)

    def test_destruir_o_pai_desfaz_o_bind(self):
        pai = fake_ctk.Fake(self.janela)
        AtalhosTeclado(pai, lambda a, v: None)
        ligados = list(self.janela.binds[1:])

        pai.destroy()

        self.assertEqual(self.janela.unbinds, ligados)
