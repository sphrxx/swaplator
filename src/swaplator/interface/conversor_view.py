import customtkinter as ctk

from swaplator.conversores.conversor import converter


class ConversorView:

    def __init__(self, master, fatores):
        self.frame = ctk.CTkFrame(master)

        self.fatores = fatores

        self.criar_widgets()
        self.configurar_layout()


    def criar_widgets(self):
        self.label_titulo = ctk.CTkLabel(self.frame, text="Swaplator", font=("Arial", 30))

        self.label_entrada = ctk.CTkLabel(self.frame, text="Informe o valor:")
        self.entrada = ctk.CTkEntry(self.frame, width=250)

        self.label_unidade_inicial = ctk.CTkLabel(self.frame, text="Informe a unidade inicial:")
        self.combobox_unidade_inicial = ctk.CTkComboBox(self.frame, values=list(self.fatores.keys()), width=250)

        self.label_unidade_final = ctk.CTkLabel(self.frame, text="Informe a unidade final:")
        self.combobox_unidade_final = ctk.CTkComboBox(self.frame, values=list(self.fatores.keys()), width=250)

        self.button = ctk.CTkButton(self.frame, text="Converter", command=self.fazer_conversao)

        self.label_resultado = ctk.CTkLabel(self.frame, text="Resultado: ", font=("Arial", 20))


    def configurar_layout(self):
        self.frame.grid(row=0, column=0, sticky="nsew")
        self.frame.grid_columnconfigure(0, weight=1)

        self.label_titulo.grid(row=0, column=0, padx=10, pady=10)

        self.label_entrada.grid(row=1, column=0, padx=10, pady=10)
        self.entrada.grid(row=2, column=0, padx=10, pady=10)

        self.label_unidade_inicial.grid(row=3, column=0, padx=10, pady=10)
        self.combobox_unidade_inicial.grid(row=4, column=0, padx=10, pady=10)

        self.label_unidade_final.grid(row=5, column=0, padx=10, pady=10)
        self.combobox_unidade_final.grid(row=6, column=0, padx=10, pady=10)

        self.button.grid(row=7, column=0, padx=10, pady=10)

        self.label_resultado.grid(row=8, column=0, padx=10, pady=10)


    def fazer_conversao(self):
        try:
            valor = float(self.entrada.get())
            unidade_inicial = self.combobox_unidade_inicial.get()
            unidade_final = self.combobox_unidade_final.get()

            resultado = converter(valor, unidade_inicial, unidade_final, self.fatores)

            self.label_resultado.configure(text=f"Resultado: {resultado}")

        except ValueError as erro:
            self.label_resultado.configure(text=f"Erro: {erro}")