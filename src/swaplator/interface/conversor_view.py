import customtkinter as ctk

from swaplator.interface import tema


TEXTO_PADRAO = "O resultado aparecerá aqui."


class ConversorView:

    def __init__(self, master, funcao_conversao, unidades):
        self.frame = ctk.CTkFrame(master, fg_color="transparent")

        self.funcao_conversao = funcao_conversao
        self.unidades = list(unidades)

        self.criar_widgets()
        self.configurar_layout()
        self.configuracoes_adicionais()


    def criar_rotulo(self, texto):
        return ctk.CTkLabel(
            self.cartao,
            text=texto,
            anchor="w",
            font=tema.fonte(tema.TAM_PEQUENO),
            text_color=tema.COR_TEXTO_SECUNDARIO
        )


    def criar_widgets(self):
        self.cartao = ctk.CTkFrame(
            self.frame,
            fg_color=tema.COR_SUPERFICIE,
            corner_radius=tema.RAIO_CARTAO
        )

        self.label_titulo = ctk.CTkLabel(
            self.cartao,
            text="Swaplator",
            font=tema.fonte(tema.TAM_TITULO, "bold"),
            text_color=tema.COR_TEXTO
        )

        self.label_entrada = self.criar_rotulo("Informe o valor:")
        self.entrada = ctk.CTkEntry(self.cartao, width=tema.LARGURA_CAMPO, **tema.estilo_entrada())

        self.label_unidade_inicial = self.criar_rotulo("Informe a unidade inicial:")
        self.combobox_unidade_inicial = ctk.CTkComboBox(
            self.cartao,
            values=self.unidades,
            width=tema.LARGURA_CAMPO,
            height=tema.ALTURA_CONTROLE,
            **tema.estilo_combobox()
        )

        self.label_unidade_final = self.criar_rotulo("Informe a unidade final:")
        self.combobox_unidade_final = ctk.CTkComboBox(
            self.cartao,
            values=self.unidades,
            width=tema.LARGURA_CAMPO,
            height=tema.ALTURA_CONTROLE,
            **tema.estilo_combobox()
        )

        self.frame_botoes = ctk.CTkFrame(self.cartao, fg_color="transparent")
        self.button_resultado = ctk.CTkButton(
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

        self.label_resultado = ctk.CTkLabel(
            self.cartao,
            text=TEXTO_PADRAO,
            width=tema.LARGURA_CAMPO,
            height=tema.ALTURA_RESULTADO,
            wraplength=tema.LARGURA_CAMPO,
            font=tema.fonte(tema.TAM_TEXTO),
            text_color=tema.COR_TEXTO_SECUNDARIO
        )


    def configurar_layout(self):
        self.frame.grid(row=0, column=0, sticky="nsew")
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)

        self.cartao.grid(row=0, column=0, padx=24, pady=24)

        self.label_titulo.grid(row=0, column=0, padx=24, pady=(24, 8))

        self.label_entrada.grid(row=1, column=0, padx=24, pady=(12, 4), sticky="w")
        self.entrada.grid(row=2, column=0, padx=24, pady=(0, 4))

        self.label_unidade_inicial.grid(row=3, column=0, padx=24, pady=(12, 4), sticky="w")
        self.combobox_unidade_inicial.grid(row=4, column=0, padx=24, pady=(0, 4))

        self.label_unidade_final.grid(row=5, column=0, padx=24, pady=(12, 4), sticky="w")
        self.combobox_unidade_final.grid(row=6, column=0, padx=24, pady=(0, 4))

        self.frame_botoes.grid(row=7, column=0, padx=24, pady=(20, 8), sticky="ew")
        self.frame_botoes.grid_columnconfigure((0, 1), weight=1)
        self.button_resultado.grid(row=0, column=0, padx=(0, 6), sticky="ew")
        self.button_limpar.grid(row=0, column=1, padx=(6, 0), sticky="ew")

        self.label_resultado.grid(row=8, column=0, padx=24, pady=(12, 24))


    def mostrar_resultado(self, texto):
        if texto.startswith("Erro"):
            self.label_resultado.configure(text=texto, text_color=tema.COR_ERRO, font=tema.fonte(tema.TAM_TEXTO))
        else:
            self.label_resultado.configure(text=texto, text_color=tema.COR_TEXTO, font=tema.fonte(tema.TAM_GRANDE, "bold"))


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

        unidade_inicial = self.combobox_unidade_inicial.get()
        unidade_final = self.combobox_unidade_final.get()

        try:
            resultado = self.funcao_conversao(valor, unidade_inicial, unidade_final)

        except ValueError as erro:
            self.mostrar_resultado(f"Erro: {erro}")
            return

        valor_formatado = str(valor).replace(".", ",")
        resultado_formatado = self.formatar_resultado(resultado)


        texto_resultado = (
            f"{valor_formatado} {unidade_inicial} = "
            f"{resultado_formatado} {unidade_final}"
        )

        self.mostrar_resultado(texto_resultado)


    def formatar_resultado(self, valor):
        return f"{valor:.6f}".rstrip("0").rstrip(".").replace(".", ",")


    def limpar(self):
        self.entrada.delete(0, "end")

        self.combobox_unidade_inicial.set(self.unidades[0])
        self.combobox_unidade_final.set(self.unidades[1])

        self.label_resultado.configure(
            text=TEXTO_PADRAO,
            text_color=tema.COR_TEXTO_SECUNDARIO,
            font=tema.fonte(tema.TAM_TEXTO)
        )

        self.entrada.focus()


    def configuracoes_adicionais(self):
        self.entrada.bind("<Return>", lambda evento: self.fazer_conversao())

        self.combobox_unidade_inicial.set(self.unidades[0])
        self.combobox_unidade_final.set(self.unidades[1])
