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


    def selecionar_operador(self, operador):
        if(self.entrada_atual == ""):
            raise ValueError("Primeiro número não informado.")

        self.operador = operador

        self.num1 = float(self.entrada_atual)
        self.entrada_atual = ""
        self.novo_numero = False
            

    def calcular(self):
        if(self.entrada_atual == ""):
            raise ValueError("Segundo número não informado.")
        
        if self.novo_numero:
            raise ValueError("Cálculo pressionado múltiplas vezes.")
        
        num2 = float(self.entrada_atual)

        if(self.operador == "+"):
            resultado = self.num1 + num2
        
        elif(self.operador == "-"):
            resultado = self.num1 - num2

        elif(self.operador == "*" or self.operador == "x"):
            resultado = self.num1 * num2

        elif(self.operador == "/" or self.operador == ":"):
            resultado = self.num1 / num2

        self.entrada_atual = str(resultado)
        self.novo_numero = True