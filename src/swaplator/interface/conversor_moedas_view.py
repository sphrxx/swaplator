import customtkinter as ctk

from swaplator.interface import tema


TEXTO_PADRAO = "O resultado aparecerá aqui."


class ConversorMoedasView:

    def __init__(self, master, funcao_conversao, cotacoes):
        self.frame = ctk.CTkFrame(master, fg_color="transparent")

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


    def criar_cartao(self):
        # Um "cartão": um frame mais claro que o fundo, onde ficam todos os widgets.
        self.cartao = ctk.CTkFrame(
            self.frame,
            fg_color=tema.COR_SUPERFICIE,
            corner_radius=tema.RAIO_CARTAO
        )

        self.label_titulo = ctk.CTkLabel(
            self.cartao,
            text="Swaplator",
            font=tema.fonte(30, "bold"),
            text_color=tema.COR_TEXTO
        )


    def criar_rotulo(self, texto):
        return ctk.CTkLabel(
            self.cartao,
            text=texto,
            anchor="w",
            font=tema.fonte(14),
            text_color=tema.COR_TEXTO_SECUNDARIO
        )


    def criar_widgets(self):
        self.criar_cartao()

        self.label_entrada = self.criar_rotulo("Informe o valor:")
        self.entrada = ctk.CTkEntry(self.cartao, width=tema.LARGURA_CAMPO, **tema.estilo_entrada())

        self.label_moeda_inicial = self.criar_rotulo("Informe a moeda inicial:")
        self.combobox_moeda_inicial = ctk.CTkComboBox(
            self.cartao,
            values=list(self.cotacoes.keys()),
            width=tema.LARGURA_CAMPO,
            height=tema.ALTURA_CONTROLE,
            **tema.estilo_combobox()
        )

        self.label_moeda_final = self.criar_rotulo("Informe a moeda final:")
        self.combobox_moeda_final = ctk.CTkComboBox(
            self.cartao,
            values=list(self.cotacoes.keys()),
            width=tema.LARGURA_CAMPO,
            height=tema.ALTURA_CONTROLE,
            **tema.estilo_combobox()
        )

        self.frame_botoes = ctk.CTkFrame(self.cartao, fg_color="transparent")
        self.button_converter = ctk.CTkButton(
            self.frame_botoes,
            text="Converter",
            command=self.fazer_conversao,
            **tema.estilo_botao("destaque", compacto=True)
        )
        self.button_limpar = ctk.CTkButton(
            self.frame_botoes,
            text="Limpar",
            command=self.limpar,
            **tema.estilo_botao("funcao", compacto=True)
        )

        # Largura e altura fixas: o cartão não "pula" quando o texto muda.
        self.label_resultado = ctk.CTkLabel(
            self.cartao,
            text=TEXTO_PADRAO,
            width=tema.LARGURA_CAMPO,
            height=72,
            wraplength=tema.LARGURA_CAMPO,
            font=tema.fonte(16),
            text_color=tema.COR_TEXTO_SECUNDARIO
        )


    def configurar_layout(self):
        self.frame.grid(row=0, column=0, sticky="nsew")
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)

        # Sem sticky: o cartão fica centralizado na área de conteúdo.
        self.cartao.grid(row=0, column=0, padx=24, pady=24)

        self.label_titulo.grid(row=0, column=0, padx=24, pady=(24, 8))

        self.label_entrada.grid(row=1, column=0, padx=24, pady=(12, 4), sticky="w")
        self.entrada.grid(row=2, column=0, padx=24, pady=(0, 4))

        self.label_moeda_inicial.grid(row=3, column=0, padx=24, pady=(12, 4), sticky="w")
        self.combobox_moeda_inicial.grid(row=4, column=0, padx=24, pady=(0, 4))

        self.label_moeda_final.grid(row=5, column=0, padx=24, pady=(12, 4), sticky="w")
        self.combobox_moeda_final.grid(row=6, column=0, padx=24, pady=(0, 4))

        self.frame_botoes.grid(row=7, column=0, padx=24, pady=(20, 8), sticky="ew")
        self.frame_botoes.grid_columnconfigure((0, 1), weight=1)
        self.button_converter.grid(row=0, column=0, padx=(0, 6), sticky="ew")
        self.button_limpar.grid(row=0, column=1, padx=(6, 0), sticky="ew")

        self.label_resultado.grid(row=8, column=0, padx=24, pady=(12, 24))


    def mostrar_resultado(self, texto):
        # Erro: fonte menor e vermelha. Resultado: fonte grande e branca.
        if texto.startswith("Erro"):
            self.label_resultado.configure(text=texto, text_color=tema.COR_ERRO, font=tema.fonte(16))
        else:
            self.label_resultado.configure(text=texto, text_color=tema.COR_TEXTO, font=tema.fonte(24, "bold"))


    def fazer_conversao(self):
        texto_valor = self.entrada.get().strip().replace(",", ".")

        if not texto_valor:
            self.mostrar_resultado("Erro: informe um valor.")
            return

        try:
            valor = float(texto_valor)

        except ValueError:
            self.mostrar_resultado("Erro: informe um valor numérico válido.")
            return

        moeda_inicial = self.combobox_moeda_inicial.get()
        moeda_final = self.combobox_moeda_final.get()

        try:
            resultado = self.funcao_conversao(valor, moeda_inicial, moeda_final, self.cotacoes)

        except ValueError as erro:
            self.mostrar_resultado(f"Erro: {erro}")
            self.erro_cotacoes = erro
            return

        valor_formatado = str(valor).replace(".", ",")
        resultado_formatado = self.formatar_resultado(resultado)

        texto_resultado = (
            f"{valor_formatado} {moeda_inicial} = "
            f"{resultado_formatado} {moeda_final}"
        )

        self.mostrar_resultado(texto_resultado)


    def formatar_resultado(self, valor):
        return f"{valor:.2f}".rstrip("0").rstrip(".").replace(".", ",")


    def limpar(self):
        self.entrada.delete(0, "end")

        self.combobox_moeda_inicial.set(list(self.cotacoes.keys())[0])
        self.combobox_moeda_final.set(list(self.cotacoes.keys())[1])

        self.label_resultado.configure(
            text=TEXTO_PADRAO,
            text_color=tema.COR_TEXTO_SECUNDARIO,
            font=tema.fonte(16)
        )

        self.entrada.focus()


    def configuracoes_adicionais(self):
        self.entrada.bind("<Return>", lambda evento: self.fazer_conversao())

        self.combobox_moeda_inicial.set(list(self.cotacoes.keys())[0])
        self.combobox_moeda_final.set(list(self.cotacoes.keys())[1])


    def criar_tela_erro(self, erro_cotacoes):
        self.frame.grid(row=0, column=0, sticky="nsew")
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)

        self.criar_cartao()
        self.cartao.grid(row=0, column=0, padx=24, pady=24)
        self.label_titulo.grid(row=0, column=0, padx=24, pady=(24, 8))

        self.label_erro = ctk.CTkLabel(
            self.cartao,
            text=f"Não foi possível obter as cotações das moedas: {erro_cotacoes}",
            wraplength=tema.LARGURA_CAMPO,
            justify="center",
            font=tema.fonte(14),
            text_color=tema.COR_ERRO
        )
        self.label_erro.grid(row=1, column=0, padx=24, pady=12)

        self.button_retry = ctk.CTkButton(
            self.cartao,
            text="Tentar novamente",
            width=200,
            command=self.retry_cotacoes,
            **tema.estilo_botao("destaque", compacto=True)
        )
        self.button_retry.grid(row=2, column=0, padx=24, pady=(8, 24))


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
