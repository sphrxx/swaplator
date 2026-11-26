import customtkinter as ctk

from swaplator.interface import tema
from swaplator.interface.componentes import BotaoRedondo, executar_depois_do_clique
from swaplator.interface.seletor_tipo import SeletorTipo, ROTULOS_TIPOS
from swaplator.conversores.registro import CONVERSOES, converter_por_tipo
from swaplator.calculadora.calculadora import Calculadora


# Nomes dos modos como constantes: se alguém digitar um nome errado, o Python
# avisa na hora (NameError), em vez de a comparação falhar em silêncio.
MODO_CALCULO = "calculo"
MODO_CONVERSAO = "conversao"

# Nome interno do modo -> texto exibido no seletor (e o caminho inverso).
MODOS = {MODO_CALCULO: "Calculadora", MODO_CONVERSAO: "Conversor"}
MODOS_INVERSO = {nome: modo for modo, nome in MODOS.items()}

# A Calculadora continua recebendo "/", "*", "-", "+". Só o símbolo mostrado muda.
SIMBOLOS = {"/": "÷", "*": "×", "-": "−", "+": "+"}


class CalculadoraView:

    def __init__(self, master):
        self.frame = ctk.CTkFrame(master, fg_color="transparent")
        self.calculadora = Calculadora()

        self.modo = MODO_CALCULO
        self.tipo_conversao = None
        self.unidade_inicial = None
        self.unidade_final = None

        self.criar_widgets()
        self.configurar_layout()


    def criar_widgets(self):
        self.seletor_modo = ctk.CTkSegmentedButton(
            self.frame,
            values=list(MODOS_INVERSO),
            command=self.selecionar_modo,
            selected_color=tema.COR_DESTAQUE,
            selected_hover_color=tema.COR_DESTAQUE_HOVER,
            unselected_color=tema.COR_DIGITO,
            unselected_hover_color=tema.COR_DIGITO_HOVER,
            text_color=tema.COR_TEXTO,
            font=tema.fonte(tema.TAM_TEXTO),
            corner_radius=tema.RAIO_CARTAO
        )

        self.seletor_modo.set(MODOS[self.modo])

        self.display = ctk.CTkLabel(
            self.frame,
            text="0",
            anchor="e",
            font=tema.fonte(tema.TAM_DISPLAY),
            text_color=tema.COR_TEXTO
        )
        self.frame_botoes = ctk.CTkFrame(self.frame, fg_color="transparent")

        self.criar_botoes_numericos()
        self.criar_botoes_operadores()
        self.criar_botoes_controladores()

        if self.modo == MODO_CONVERSAO:
            self.criar_widgets_conversao()


    def criar_botao(self, texto, tipo, linha, coluna, comando, colunas=1):
        botao = BotaoRedondo(
            self.frame_botoes,
            text=texto,
            width=tema.TAMANHO_BOTAO,
            height=tema.TAMANHO_BOTAO,
            command=comando,
            **tema.estilo_botao(tipo)
        )

        botao.grid(
            row=linha,
            column=coluna,
            columnspan=colunas,
            sticky="ew" if colunas > 1 else "",
            padx=tema.ESPACO // 2,
            pady=tema.ESPACO // 2
        )

        return botao


    def criar_botoes_numericos(self):
        self.botoes_numericos = [
            ["7", "8", "9"],
            ["4", "5", "6"],
            ["1", "2", "3"]
        ]

        # Linha 0 é de C e do operador de divisão, então os dígitos começam na 1.
        for linha, botoes_numericos in enumerate(self.botoes_numericos, start=1):
            for coluna, valor in enumerate(botoes_numericos):
                self.criar_botao(valor, "digito", linha, coluna, lambda valor=valor: self.digitar(valor))

        self.button_zero = self.criar_botao("0", "digito", 4, 0, lambda: self.digitar("0"), colunas=2)
        self.button_decimal = self.criar_botao(".", "digito", 4, 2, lambda: self.digitar("."))


    def criar_botoes_operadores(self):
        self.botoes_operadores = ["/", "*", "-", "+"]

        for linha, operador in enumerate(self.botoes_operadores):
            self.criar_botao(
                SIMBOLOS[operador],
                "destaque",
                linha,
                3,
                lambda operador=operador: self.selecionar_operador(operador)
            )


    def criar_botoes_controladores(self):
        self.button_limpar = self.criar_botao("C", "funcao", 0, 0, self.limpar, colunas=3)
        self.button_calcular = self.criar_botao("=", "destaque", 4, 3, self.calcular)


    def criar_widgets_conversao(self):
        self.frame_comboboxes_conversao = ctk.CTkFrame(self.frame, fg_color="transparent")
        # Seletor com ícones no lugar da combobox; mantém o mesmo nome e a
        # mesma interface (get/set/command), então o resto do código não muda.
        self.combobox_tipo_conversao = SeletorTipo(
            self.frame_comboboxes_conversao,
            opcoes={tipo: ROTULOS_TIPOS.get(tipo, tipo.capitalize())
                    for tipo in CONVERSOES},
            command=self.atualizar_unidades,
            ao_abrir=self.fechar_menus_das_unidades,
        )

        unidades = self.extrair_unidades(self.combobox_tipo_conversao.get())

        self.combobox_unidade_inicial = ctk.CTkComboBox(
            self.frame_comboboxes_conversao,
            values=unidades,
            width=tema.LARGURA_COMBOBOX_UNIDADE,
            height=tema.ALTURA_CONTROLE,
            **tema.estilo_combobox()
        )
        self.combobox_unidade_final = ctk.CTkComboBox(
            self.frame_comboboxes_conversao,
            values=unidades,
            width=tema.LARGURA_COMBOBOX_UNIDADE,
            height=tema.ALTURA_CONTROLE,
            **tema.estilo_combobox()
        )

        self.combobox_unidade_inicial.set(unidades[0])
        self.combobox_unidade_final.set(unidades[1])


    def fechar_menus_das_unidades(self):
        """Fecha o menu aberto de qualquer combobox de unidade.

        O menu é uma janelinha do sistema, sempre desenhada acima da lista de
        tipos. O CTkComboBox não tem um método público para fechá-lo, então
        usamos os atributos internos dele; se uma versão futura os renomear,
        a lista continua abrindo normalmente (só o menu fica aberto).
        """
        for combobox in (self.combobox_unidade_inicial,
                         self.combobox_unidade_final):
            menu = getattr(combobox, "_dropdown_menu", None)
            if menu is not None:
                menu.close()
                combobox._close_on_next_click = False


    def configurar_layout(self):
        self.frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.frame.grid_columnconfigure(0, weight=1)
        # A linha do display absorve a folga da janela; o resto fica compacto.
        self.frame.grid_rowconfigure(2, weight=1)

        self.seletor_modo.grid(row=0, column=0, padx=10, pady=(8, 4))

        self.display.grid(row=2, column=0, padx=tema.ESPACO * 2, pady=(0, 4), sticky="sew")

        self.frame_botoes.grid(row=3, column=0, padx=10, pady=(4, 10))

        if self.modo == MODO_CONVERSAO:
            self.frame_comboboxes_conversao.grid(row=1, column=0, padx=5, pady=4)

            # Lado a lado (e não empilhados) para caber na altura da janela.
            self.combobox_tipo_conversao.grid(row=0, column=0, padx=4)
            self.combobox_unidade_inicial.grid(row=0, column=1, padx=4)
            self.combobox_unidade_final.grid(row=0, column=2, padx=4)


    def mostrar_no_display(self, texto):
        texto = texto or "0"

        # Quanto mais longo o texto, menor a fonte, para nunca estourar a tela.
        self.display.configure(text=texto, font=tema.fonte(tema.tamanho_fonte_display(texto)))


    def atualizar_display(self):
        if self.calculadora.novo_numero:
            texto = self.calculadora.entrada_atual

        elif self.calculadora.operador is None:
            texto = self.calculadora.entrada_atual

        else:
            simbolo = SIMBOLOS.get(self.calculadora.operador, self.calculadora.operador)
            texto = f"{self.calculadora.num1} {simbolo}"

            if self.calculadora.entrada_atual != "":
                texto += f" {self.calculadora.entrada_atual}"

        self.mostrar_no_display(texto)


    def digitar(self, valor):
        try:
            self.calculadora.digitar(valor)
            self.atualizar_display()

        except ValueError as erro:
            print(erro)


    def selecionar_operador(self, operador):
        try:
            self.calculadora.selecionar_operador(operador)
            self.atualizar_display()

        except ValueError as erro:
            print(erro)


    def calcular(self):
        try:
            if self.modo == MODO_CALCULO:
                self.calculadora.calcular()
                self.atualizar_display()

            elif self.modo == MODO_CONVERSAO:
                resultado = self.calculadora.calcular()
                unidade_inicial = self.combobox_unidade_inicial.get()
                unidade_final = self.combobox_unidade_final.get()
                tipo = self.combobox_tipo_conversao.get()

                resultado_conversao = converter_por_tipo(tipo, resultado, unidade_inicial, unidade_final)
                self.mostrar_no_display(f"{resultado} {unidade_inicial} = {resultado_conversao} {unidade_final}")

        except ValueError as erro:
            print(erro)

        except ZeroDivisionError as erro:
            print(erro)


    def limpar(self):
        self.calculadora.limpar()
        self.atualizar_display()


    def atualizar_modo(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        self.criar_widgets()
        self.configurar_layout()
        self.atualizar_display()


    def selecionar_modo(self, nome_exibido):
        # Este método é o comando do seletor de modo, e a troca de modo destrói
        # esse mesmo seletor. Esperamos o clique terminar antes de reconstruir.
        modo = MODOS_INVERSO[nome_exibido]
        executar_depois_do_clique(self.frame, lambda: self.mudar_modo(modo))


    def mudar_modo(self, modo):
        self.modo = modo
        self.atualizar_modo()


    def extrair_unidades(self, tipo_conversao):
        _, unidades_disponiveis = CONVERSOES[tipo_conversao]
        unidades = list(unidades_disponiveis)

        return unidades


    def atualizar_unidades(self, tipo_conversao):
        unidades = self.extrair_unidades(tipo_conversao)

        self.combobox_unidade_inicial.configure(values=unidades)
        self.combobox_unidade_final.configure(values=unidades)

        self.combobox_unidade_inicial.set(unidades[0])
        self.combobox_unidade_final.set(unidades[1])
