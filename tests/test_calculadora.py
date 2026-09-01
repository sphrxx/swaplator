from swaplator.calculadora.calculadora import Calculadora
import unittest

class TestCalculadora(unittest.TestCase):

    def test_estado_inicial(self):
        calculadora = Calculadora()

        self.assertIsNone(calculadora.num1)
        self.assertIsNone(calculadora.operador)
        self.assertEqual(calculadora.entrada_atual, "")
        self.assertFalse(calculadora.novo_numero)


    def test_digitar(self):
        calculadora = Calculadora()

        calculadora.digitar("1")
        calculadora.digitar("2")
        calculadora.digitar("3")

        self.assertEqual(calculadora.entrada_atual, "123")


    def test_digitar_ponto_inicial(self):
        calculadora = Calculadora()

        calculadora.digitar(".")
        calculadora.digitar("5")

        self.assertEqual(calculadora.entrada_atual, "0.5")


    def test_digitar_dois_pontos(self):
        calculadora = Calculadora()

        calculadora.digitar("1")
        calculadora.digitar(".")
        
        with self.assertRaises(ValueError):
            calculadora.digitar(".")


    def test_selecionar_operador(self):
        calculadora = Calculadora()

        calculadora.digitar("5")
        calculadora.digitar("0")
        calculadora.selecionar_operador("+")

        self.assertEqual(calculadora.num1, 50)
        self.assertEqual(calculadora.operador, "+")
        self.assertEqual(calculadora.entrada_atual, "")


    def test_selecionar_operador_sem_numero(self):
        calculadora = Calculadora()

        with self.assertRaises(ValueError):
            calculadora.selecionar_operador("+")


    def test_calcular_soma(self):
        calculadora = Calculadora()

        calculadora.digitar("5")
        calculadora.selecionar_operador("+")
        calculadora.digitar("2")
        calculadora.calcular()

        self.assertEqual(calculadora.entrada_atual, "7.0")


    def test_calcular_subtracao(self):
        calculadora = Calculadora()

        calculadora.digitar("5")
        calculadora.selecionar_operador("-")
        calculadora.digitar("2")
        calculadora.calcular()

        self.assertEqual(calculadora.entrada_atual, "3.0")


    def test_calcular_multiplicacao(self):
        calculadora = Calculadora()

        calculadora.digitar("5")
        calculadora.selecionar_operador("*")
        calculadora.digitar("5")
        calculadora.calcular()

        self.assertEqual(calculadora.entrada_atual, "25.0")


    def test_calcular_divisao(self):
        calculadora = Calculadora()

        calculadora.digitar("7")
        calculadora.digitar("0")
        calculadora.selecionar_operador("/")
        calculadora.digitar("1")
        calculadora.digitar("0")
        calculadora.calcular()

        self.assertEqual(calculadora.entrada_atual, "7.0")


    def test_divisao_por_zero(self):
        calculadora = Calculadora()

        calculadora.digitar("5")
        calculadora.selecionar_operador("/")
        calculadora.digitar("0")

        with self.assertRaises(ZeroDivisionError):
            calculadora.calcular()


    def test_calcular_sem_segundo_numero(self):
        calculadora = Calculadora()

        calculadora.digitar("5")
        calculadora.selecionar_operador("+")
        
        with self.assertRaises(ValueError):
            calculadora.calcular()


    def test_calcular_soma(self):
        calculadora = Calculadora()

        calculadora.digitar("2")
        calculadora.selecionar_operador("+")
        calculadora.digitar("3")
        calculadora.calcular()

        self.assertEqual(calculadora.entrada_atual, "5.0")
        self.assertTrue(calculadora.novo_numero)


    def test_digitar_novo_numero_apos_resultado(self):
        calculadora = Calculadora()

        calculadora.digitar("7")
        calculadora.selecionar_operador("+")
        calculadora.digitar("3")
        calculadora.calcular()

        calculadora.digitar("1")

        self.assertEqual(calculadora.entrada_atual, "1")
        self.assertFalse(calculadora.novo_numero)


    def test_operacao_encadeada(self):
        calculadora = Calculadora()

        calculadora.digitar("3")
        calculadora.selecionar_operador("*")
        calculadora.digitar("1")
        calculadora.digitar("0")
        calculadora.calcular()

        calculadora.selecionar_operador("+")
        calculadora.digitar("3")
        calculadora.calcular()

        self.assertEqual(calculadora.entrada_atual, "33.0")


    def test_limpar(self):
        calculadora = Calculadora()

        calculadora.digitar("3")
        calculadora.selecionar_operador("+")
        calculadora.digitar("5")
        calculadora.calcular()

        calculadora.selecionar_operador("-")
        calculadora.digitar("7")
        calculadora.calcular()

        calculadora.limpar()

        self.assertIsNone(calculadora.num1)
        self.assertIsNone(calculadora.operador)
        self.assertEqual(calculadora.entrada_atual, "")
        self.assertFalse(calculadora.novo_numero)


    def test_calculo_multiplo(self):
        calculadora = Calculadora()

        calculadora.digitar("5")
        calculadora.selecionar_operador("+")
        calculadora.digitar("5")
        calculadora.calcular()

        with self.assertRaises(ValueError):
            calculadora.calcular()

if __name__ == '__main__':
    unittest.main()