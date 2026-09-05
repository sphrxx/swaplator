import customtkinter as ctk

class ConversorMoedasView:

    def __init__(self, master, funcao_conversao, cotacoes):
        self.frame = ctk.CTkFrame(master)

        self.funcao_conversao = funcao_conversao
        self.obter_cotacoes = cotacoes
        
        try:
            self.cotacoes = self.obter_cotacoes()
        
        except ValueError as erro:
            self.cotacoes = None
            self.erro_cotacoes = erro

        if self.cotacoes is None:
            self.criar_tela_erro(self.erro_cotacoes)
    
        else:
            self.criar_widgets()
            self.configurar_layout()
            self.configuracoes_adicionais()    
        

    def criar_widgets(self):
        self.label_titulo = ctk.CTkLabel(self.frame, text="Swaplator", font=("Arial", 30))

        self.label_entrada = ctk.CTkLabel(self.frame, text="Informe o valor:")
        self.entrada = ctk.CTkEntry(self.frame, width=250)

        self.label_moeda_inicial = ctk.CTkLabel(self.frame, text="Informe a moeda inicial:")
        self.combobox_moeda_inicial = ctk.CTkComboBox(self.frame, values=list(self.cotacoes.keys()), width=250)

        self.label_moeda_final = ctk.CTkLabel(self.frame, text="Informe a moeda final:")
        self.combobox_moeda_final = ctk.CTkComboBox(self.frame, values=list(self.cotacoes.keys()), width=250)

        self.frame_botoes = ctk.CTkFrame(self.frame)
        self.button_converter = ctk.CTkButton(self.frame_botoes, text="Converter", width=120, command=self.fazer_conversao)
        self.button_limpar = ctk.CTkButton(self.frame_botoes, text="Limpar", width=120, command=self.limpar)

        self.label_resultado = ctk.CTkLabel(self.frame, text="O resultado aparecerá aqui.", font=("Arial", 20))


    def configurar_layout(self):
        self.frame.grid(row=0, column=0, sticky="nsew")
        self.frame.grid_columnconfigure(0, weight=1)

        self.label_titulo.grid(row=0, column=0, padx=10, pady=10)

        self.label_entrada.grid(row=1, column=0, padx=10, pady=10)
        self.entrada.grid(row=2, column=0, padx=10, pady=10)

        self.label_moeda_inicial.grid(row=3, column=0, padx=10, pady=10)
        self.combobox_moeda_inicial.grid(row=4, column=0, padx=10, pady=10)

        self.label_moeda_final.grid(row=5, column=0, padx=10, pady=10)
        self.combobox_moeda_final.grid(row=6, column=0, padx=10, pady=10)

        self.frame_botoes.grid(row=7, column=0, padx=10, pady=10)
        self.button_converter.grid(row=0, column=0, padx=10, pady=10)
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
        
        moeda_inicial = self.combobox_moeda_inicial.get()
        moeda_final = self.combobox_moeda_final.get()

        try:
            resultado = self.funcao_conversao(valor, moeda_inicial, moeda_final, self.cotacoes)

        except ValueError as erro:
            self.label_resultado.configure(text=f"Erro: {erro}")
            self.erro_cotacoes = erro
            return
        
        valor_formatado = str(valor).replace(".", ",")
        resultado_formatado = self.formatar_resultado(resultado)

        texto_resultado = (
            f"{valor_formatado} {moeda_inicial} = "
            f"{resultado_formatado} {moeda_final}"
        )

        self.label_resultado.configure(text=texto_resultado)


    def formatar_resultado(self, valor):
        return f"{valor:.2f}".rstrip("0").rstrip(".").replace(".", ",")


    def limpar(self):
        self.entrada.delete(0, "end")

        self.combobox_moeda_inicial.set(list(self.cotacoes.keys())[0])
        self.combobox_moeda_final.set(list(self.cotacoes.keys())[1])

        self.label_resultado.configure(text="O resultado aparecerá aqui.")

        self.entrada.focus()

    
    def configuracoes_adicionais(self):
        self.entrada.bind("<Return>", lambda evento: self.fazer_conversao())

        self.combobox_moeda_inicial.set(list(self.cotacoes.keys())[0])
        self.combobox_moeda_final.set(list(self.cotacoes.keys())[1])


    def criar_tela_erro(self, erro_cotacoes):
        self.frame.grid(row=0, column=0, sticky="nsew")
        self.frame.grid_columnconfigure(0, weight=1)

        self.label_titulo = ctk.CTkLabel(self.frame, text="Swaplator", font=("Arial", 30))
        self.label_titulo.grid(row=0, column=0, padx=10, pady=10)

        self.label_erro = ctk.CTkLabel(self.frame, text=f"Não foi possível obter as cotações das moedas: {erro_cotacoes}")
        self.label_erro.grid(row=1, column=0, padx=10, pady=10)

        self.button_retry = ctk.CTkButton(self.frame, text="Tentar novamente", command=self.retry_cotacoes)
        self.button_retry.grid(row=2, column=0, padx=10, pady=10)

    
    def retry_cotacoes(self):
        try:
            self.cotacoes = self.obter_cotacoes()
        
        except ValueError as erro:
            self.cotacoes = None
            self.erro_cotacoes = erro

        if self.cotacoes is None:
            self.limpar_frame()
            self.criar_tela_erro(self.erro_cotacoes)

        else:
            self.limpar_frame()
            self.criar_widgets()
            self.configurar_layout()
            self.configuracoes_adicionais()

    
    def limpar_frame(self):
        for widget in self.frame.winfo_children():
            widget.destroy()