class Calculadora:

    def __init__(self):
        self.limpar()


    def limpar(self):
        self.num1 = None
        self.operador = None
        self.entrada_atual = ""

        self.novo_numero = False


    def digitar(self, valor):
        if(self.novo_numero):
            self.entrada_atual = ""
            self.novo_numero = False

        if(valor == "." and self.entrada_atual == ""):
            self.entrada_atual = "0."
            return

        if(valor == "." and "." in self.entrada_atual):
            raise ValueError("A entrada já possui um ponto decimal")

        self.entrada_atual += valor


    def apagar(self):
        """Apaga o último caractere digitado (Backspace)."""
        # O resultado de uma conta não é "digitado": não se apaga pedaço dele.
        if self.novo_numero:
            return

        self.entrada_atual = self.entrada_atual[:-1]


    def selecionar_operador(self, operador):
        if(self.entrada_atual == ""):
            raise ValueError("Primeiro número não informado.")

        self.operador = operador

        self.num1 = float(self.entrada_atual)
        self.entrada_atual = ""
        self.novo_numero = False
            

    def _operar(self, num2):
        if(self.operador == "+"):
            return self.num1 + num2

        if(self.operador == "-"):
            return self.num1 - num2

        if(self.operador == "*" or self.operador == "x"):
            return self.num1 * num2

        if(self.operador == "/" or self.operador == ":"):
            return self.num1 / num2


    def resultado_parcial(self):
        """Valor da conta como está agora, sem alterar nada (para o display).

        Ex.: com "233 / 3" digitado, devolve 77.666... mesmo antes do "=".
        Pode levantar ZeroDivisionError (ex.: "1 / 0").
        """
        if self.novo_numero or self.operador is None:
            return float(self.entrada_atual) if self.entrada_atual else 0.0

        if self.entrada_atual == "":
            return self.num1    # operador acabou de ser apertado

        return self._operar(float(self.entrada_atual))


    def calcular(self):
        if(self.novo_numero):
            resultado = float(self.entrada_atual)

        elif self.operador is None:
            if(self.entrada_atual == ""):
                raise ValueError("Número não informado.")

            resultado = float(self.entrada_atual)

        else:
            if(self.entrada_atual == ""):
                raise ValueError("Segundo número não informado.")

            resultado = self._operar(float(self.entrada_atual))

        self.entrada_atual = str(resultado)
        self.novo_numero = True

        return resultado