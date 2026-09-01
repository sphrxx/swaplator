import customtkinter as ctk

from swaplator.calculadora.calculadora import Calculadora

class CalculadoraView:

    def __init__(self, master):
        self.frame = ctk.CTkFrame(master)
        self.calculadora = Calculadora()

        self.criar_widgets()
        self.configurar_layout()

        
    def criar_widgets(self):
        self.display = ctk.CTkLabel(self.frame, text="Display")

        self.frame_botoes = ctk.CTkFrame(self.frame)
        self.botoes_numericos = [
            ["7", "8", "9"],
            ["4", "5", "6"],
            ["1", "2", "3"],
            ["0"]
        ]

        for linha, botoes_numericos in enumerate(self.botoes_numericos):
            for coluna, valor in enumerate(botoes_numericos):
                button = ctk.CTkButton(self.frame_botoes, text=valor, command=lambda valor=valor: self.digitar(valor))
                button.grid(row=linha, column=coluna, padx=3, pady=3, sticky="nsew")

        self.botoes_operadores = ["/", "*", "-", "+"]

        for coluna, operador in enumerate(self.botoes_operadores):
            button = ctk.CTkButton(self.frame_botoes, text=operador, command=lambda operador=operador: self.selecionar_operador(operador))
            button.grid(row=coluna, column=3, padx=3, pady=3, sticky="nsew")

        self.button_decimal = ctk.CTkButton(self.frame_botoes, text=".", command=lambda: self.digitar("."))
        self.button_decimal.grid(row=3, column=1, padx=3, pady=3, sticky="nsew")

        self.button_calcular = ctk.CTkButton(self.frame_botoes, text="=", command=self.calcular)
        self.button_calcular.grid(row=3, column=2, padx=3, pady=3, sticky="nsew")

        self.button_limpar = ctk.CTkButton(self.frame, text="Limpar", command=self.limpar)
        self.button_limpar.grid(row=1, column=0, padx=13, pady=3, sticky="ew")

        
    def configurar_layout(self):
        self.frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_rowconfigure(2, weight=1)

        self.display.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        self.frame_botoes.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        for i in range(4):
            self.frame_botoes.grid_columnconfigure(i, weight=1)
            self.frame_botoes.grid_rowconfigure(i, weight=1)


    def atualizar_display(self):
        if self.calculadora.novo_numero:
            texto = self.calculadora.entrada_atual

        elif self.calculadora.operador is None:
            texto = self.calculadora.entrada_atual

        else:
            texto = f"{self.calculadora.num1} {self.calculadora.operador}"

            if self.calculadora.entrada_atual != "":
                texto += f" {self.calculadora.entrada_atual}"

        self.display.configure(text=texto)
        

    def digitar(self, valor):
        self.calculadora.digitar(valor)
        self.atualizar_display()


    def selecionar_operador(self, operador):
        try:
            self.calculadora.selecionar_operador(operador)
            self.atualizar_display()

        except ValueError as erro:
            print(erro)


    def calcular(self):
        try:
            self.calculadora.calcular()
            self.atualizar_display()

        except ValueError as erro:
            print(erro)

        except ZeroDivisionError as erro:
            print(erro)


    def limpar(self):
        self.calculadora.limpar()
        self.atualizar_display()