import customtkinter as ctk

class ConversorView:

    def __init__(self, master, funcao_conversao, unidades):
        self.frame = ctk.CTkFrame(master)

        self.funcao_conversao = funcao_conversao
        self.unidades = list(unidades)

        self.criar_widgets()
        self.configurar_layout()
        self.configuracoes_adicionais()


    def criar_widgets(self):
        self.label_titulo = ctk.CTkLabel(self.frame, text="Swaplator", font=("Arial", 30))

        self.label_entrada = ctk.CTkLabel(self.frame, text="Informe o valor:")
        self.entrada = ctk.CTkEntry(self.frame, width=250)

        self.label_unidade_inicial = ctk.CTkLabel(self.frame, text="Informe a unidade inicial:")
        self.combobox_unidade_inicial = ctk.CTkComboBox(self.frame, values=self.unidades, width=250)

        self.label_unidade_final = ctk.CTkLabel(self.frame, text="Informe a unidade final:")
        self.combobox_unidade_final = ctk.CTkComboBox(self.frame, values=self.unidades, width=250)

        self.frame_botoes = ctk.CTkFrame(self.frame)
        self.button_resultado = ctk.CTkButton(self.frame_botoes, text="Converter", width=120, command=self.fazer_conversao)
        self.button_limpar = ctk.CTkButton(self.frame_botoes, text="Limpar", width=120, command=self.limpar)

        self.label_resultado = ctk.CTkLabel(self.frame, text="O resultado aparecerá aqui.", font=("Arial", 20))


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

        self.frame_botoes.grid(row=7, column=0, padx=10, pady=10)
        self.button_resultado.grid(row=0, column=0, padx=10, pady=10)
        self.button_limpar.grid(row=0, column=1, padx=10, pady=10)

        self.label_resultado.grid(row=8, column=0, padx=10, pady=10)


    def fazer_conversao(self):
        texto_valor = self.entrada.get().strip().replace(",", ".")

        if not texto_valor:
            self.label_resultado.configure(text="Erro: informe um valor.")
            return

        try:
            valor = float(texto_valor)
        
        except ValueError:
            self.label_resultado.configure(text="Erro: informe um valor numérico válido.")
            return
        
        unidade_inicial = self.combobox_unidade_inicial.get()
        unidade_final = self.combobox_unidade_final.get()

        try:
            resultado = self.funcao_conversao(valor, unidade_inicial, unidade_final)

        except ValueError as erro:
            self.label_resultado.configure(text=f"Erro: {erro}")
            return
        
        valor_formatado = str(valor).replace(".", ",")
        resultado_formatado = self.formatar_resultado(resultado)
        
        
        texto_resultado = (
            f"{valor_formatado} {unidade_inicial} = "
            f"{resultado_formatado} {unidade_final}"
        )

        self.label_resultado.configure(text=texto_resultado)


    def formatar_resultado(self, valor):
        return f"{valor:.6f}".rstrip("0").rstrip(".").replace(".", ",")
    

    def limpar(self):
        self.entrada.delete(0, "end")

        self.combobox_unidade_inicial.set(self.unidades[0])
        self.combobox_unidade_final.set(self.unidades[1])

        self.label_resultado.configure(text="O resultado aparecerá aqui.")

        self.entrada.focus()


    def configuracoes_adicionais(self):
        self.entrada.bind("<Return>", lambda evento: self.fazer_conversao())

        self.combobox_unidade_inicial.set(self.unidades[0])
        self.combobox_unidade_final.set(self.unidades[1])
