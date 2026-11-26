"""Display de duas linhas da calculadora conversora.

    ┌────────────────────────────────┐
    │ 12.5                 [ m  ▾ ]  │  linha de cima: o que se digita
    │ 1250                 [ cm ▾ ]  │  linha de baixo: o resultado
    └────────────────────────────────┘

Este componente só *mostra* textos e guarda as caixas de unidade. Quem
decide o que escrever em cada linha é a tela (CalculadoraView).
"""

import customtkinter as ctk

from swaplator.interface import tema


class DisplayConversao:

    def __init__(self, master, unidades, ao_mudar_unidade=None):
        self._ao_mudar_unidade = ao_mudar_unidade

        self.frame = ctk.CTkFrame(master, fg_color="transparent")
        self.frame.grid_columnconfigure(0, weight=1)

        self.label_entrada = self._criar_linha("0", tema.TAM_DISPLAY)
        self.label_resultado = self._criar_linha("0", tema.TAM_TITULO)

        self.combobox_unidade_inicial = self._criar_caixa()
        self.combobox_unidade_final = self._criar_caixa()

        self.label_entrada.grid(row=0, column=0, sticky="e", padx=(0, 8))
        self.combobox_unidade_inicial.grid(row=0, column=1, padx=(0, 4))
        self.label_resultado.grid(row=1, column=0, sticky="e", padx=(0, 8))
        self.combobox_unidade_final.grid(row=1, column=1, padx=(0, 4))

        self.definir_unidades(unidades)

    def _criar_linha(self, texto, tamanho):
        # Altura fixa: se ela acompanhasse o texto, a tela "pularia" ao digitar.
        return ctk.CTkLabel(
            self.frame,
            text=texto,
            anchor="e",
            height=tema.ALTURA_LINHA_DISPLAY,
            font=tema.fonte(tamanho),
            text_color=tema.COR_TEXTO
        )

    def _criar_caixa(self):
        return ctk.CTkComboBox(
            self.frame,
            values=[],
            width=tema.LARGURA_COMBOBOX_UNIDADE,
            height=tema.ALTURA_CONTROLE,
            # O CTk chama o comando com o valor escolhido; só precisamos avisar.
            command=lambda valor: self._avisar(),
            **tema.estilo_combobox()
        )

    def _avisar(self):
        if self._ao_mudar_unidade is not None:
            self._ao_mudar_unidade()

    def mostrar(self, texto_entrada, texto_resultado):
        """Escreve as duas linhas; a fonte encolhe para textos longos."""
        # Em cima, a fonte vai até o tamanho do visor; embaixo, o resultado
        # nunca passa do tamanho de título, para a linha de cima ter destaque.
        self.label_entrada.configure(
            text=texto_entrada,
            font=tema.fonte(tema.tamanho_fonte_display(texto_entrada)))
        self.label_resultado.configure(
            text=texto_resultado,
            font=tema.fonte(min(tema.tamanho_fonte_display(texto_resultado),
                                tema.TAM_TITULO)))

    def definir_unidades(self, unidades):
        """Troca a lista de unidades e seleciona as duas primeiras."""
        unidades = list(unidades)

        for caixa in (self.combobox_unidade_inicial, self.combobox_unidade_final):
            caixa.configure(values=unidades)

        self.combobox_unidade_inicial.set(unidades[0])
        self.combobox_unidade_final.set(unidades[1])

    def unidade_inicial(self):
        return self.combobox_unidade_inicial.get()

    def unidade_final(self):
        return self.combobox_unidade_final.get()
