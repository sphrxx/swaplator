import customtkinter as ctk

from swaplator.interface import tema
from swaplator.interface.componentes import BotaoRedondo, esconder_grid, mostrar_grid
from swaplator.interface.atalhos_teclado import AtalhosTeclado
from swaplator.interface.display_conversao import DisplayConversao
from swaplator.interface.painel_tipos import PainelTipos
from swaplator.interface.formato import converter_para_exibir, formatar_numero
from swaplator.interface.seletor_tipo import ROTULOS_TIPOS
from swaplator.conversores.registro import CONVERSOES
from swaplator.calculadora.calculadora import Calculadora


# A Calculadora continua recebendo "/", "*", "-", "+". Só o símbolo mostrado muda.
SIMBOLOS = {"/": "÷", "*": "×", "-": "−", "+": "+"}


TEXTO_BOTAO_TIPOS = "⊞ Tipos"
TEXTO_BOTAO_VOLTAR = "Voltar"


def rotulo_do_tipo(tipo):
    return ROTULOS_TIPOS.get(tipo, tipo.capitalize())


class CalculadoraView:
    """Calculadora que sempre converte: o tipo é escolhido no cabeçalho."""

    def __init__(self, master):
        self.frame = ctk.CTkFrame(master, fg_color="transparent")
        self.calculadora = Calculadora()
        self.painel_aberto = False
        self._teclado_bloqueado = False

        # Começa no primeiro tipo do registro (Comprimento).
        self.tipo_conversao = next(iter(CONVERSOES))

        self.criar_widgets()
        self.configurar_layout()
        self.atualizar_display()


    def criar_widgets(self):
        self.cabecalho = ctk.CTkFrame(
            self.frame, fg_color="transparent", height=tema.ALTURA_CABECALHO)

        self.label_tipo = ctk.CTkLabel(
            self.cabecalho,
            text=rotulo_do_tipo(self.tipo_conversao),
            anchor="w",
            font=tema.fonte(tema.TAM_GRANDE, "bold"),
            text_color=tema.COR_TEXTO
        )
        self.button_tipos = ctk.CTkButton(
            self.cabecalho,
            text=TEXTO_BOTAO_TIPOS,
            width=tema.LARGURA_BOTAO_TIPOS,
            command=self.alternar_painel,
            **tema.estilo_botao("digito", compacto=True)
        )

        # Quem muda as unidades (ou o tipo) só precisa pedir para atualizar:
        # o display avisa pelo callback e a conversão é refeita.
        self.display = DisplayConversao(
            self.frame,
            self.extrair_unidades(self.tipo_conversao),
            ao_mudar_unidade=self.atualizar_display
        )
        # Atalhos: o resto do código (e os testes) fala "a caixa de unidade".
        self.combobox_unidade_inicial = self.display.combobox_unidade_inicial
        self.combobox_unidade_final = self.display.combobox_unidade_final

        self.frame_botoes = ctk.CTkFrame(self.frame, fg_color="transparent")

        # O painel é filho da tela (e não da janela): quando a tela é destruída,
        # ele vai junto e desfaz os binds de teclado que fez na janela.
        self.painel_tipos = PainelTipos(
            self.frame,
            rotulos={tipo: rotulo_do_tipo(tipo) for tipo in CONVERSOES},
            tipo_ativo=self.tipo_conversao,
            ao_escolher=self.escolher_tipo,
            ao_fechar=self.fechar_painel
        )

        # O teclado físico faz o mesmo que os botões da tela.
        self.atalhos = AtalhosTeclado(self.frame, self.ao_acao_do_teclado)

        self.criar_botoes_numericos()
        self.criar_botoes_operadores()
        self.criar_botoes_controladores()


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


    def configurar_layout(self):
        self.frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.frame.grid_columnconfigure(0, weight=1)
        # A linha do display absorve a folga da janela; o resto fica compacto.
        self.frame.grid_rowconfigure(1, weight=1)

        # Altura fixa no cabeçalho: sem isto ele encolheria para caber o conteúdo.
        self.cabecalho.grid(row=0, column=0, padx=tema.ESPACO * 2, sticky="ew")
        self.cabecalho.grid_propagate(False)
        self.cabecalho.grid_columnconfigure(0, weight=1)
        self.cabecalho.grid_rowconfigure(0, weight=1)

        self.label_tipo.grid(row=0, column=0, sticky="w")
        self.button_tipos.grid(row=0, column=1, sticky="e")

        self.display.frame.grid(row=1, column=0, padx=tema.ESPACO * 2, pady=(0, 4), sticky="sew")

        self.frame_botoes.grid(row=2, column=0, padx=10, pady=(4, 10))

        # O painel ocupa o lugar do display + teclado (linhas 1 e 2). Ele é
        # posicionado agora e escondido: mostrar() reaproveita essa posição.
        self.painel_tipos.grid(row=1, column=0, rowspan=2, padx=10, pady=(0, 10), sticky="nsew")
        self.painel_tipos.ocultar()


    def extrair_unidades(self, tipo_conversao):
        _, unidades_disponiveis = CONVERSOES[tipo_conversao]

        return list(unidades_disponiveis)


    def atualizar_display(self):
        """Escreve as duas linhas: o que foi digitado e a conversão ao vivo."""
        calc = self.calculadora

        if calc.novo_numero:
            # Logo após "=": mostra o resultado sem o ".0" que o float traz.
            numero = calc.entrada_atual
            topo = formatar_numero(float(numero))

        elif calc.operador is None:
            numero = calc.entrada_atual
            topo = numero or "0"

        else:
            simbolo = SIMBOLOS.get(calc.operador, calc.operador)
            topo = f"{formatar_numero(calc.num1)} {simbolo}"

            if calc.entrada_atual != "":
                numero = calc.entrada_atual
                topo += f" {numero}"
            else:
                # Operador acabou de ser apertado: converte o primeiro número.
                numero = str(calc.num1)

        baixo = converter_para_exibir(
            self.tipo_conversao, numero,
            self.display.unidade_inicial(), self.display.unidade_final())

        self.display.mostrar(topo, baixo)


    def digitar(self, valor):
        if self._teclado_bloqueado:
            return

        try:
            self.calculadora.digitar(valor)
            self.atualizar_display()

        except ValueError as erro:
            print(erro)


    def selecionar_operador(self, operador):
        if self._teclado_bloqueado:
            return

        try:
            self.calculadora.selecionar_operador(operador)
            self.atualizar_display()

        except ValueError as erro:
            print(erro)


    def calcular(self):
        if self._teclado_bloqueado:
            return

        try:
            self.calculadora.calcular()

        except (ValueError, ZeroDivisionError) as erro:
            print(erro)

        self.atualizar_display()


    def apagar(self):
        if self._teclado_bloqueado:
            return

        self.calculadora.apagar()
        self.atualizar_display()


    def ao_acao_do_teclado(self, acao, valor):
        # Com o painel de tipos aberto, as teclas (Enter, Esc, setas) são dele.
        if self.painel_aberto:
            return

        if acao == "digitar":
            self.digitar(valor)

        elif acao == "operador":
            self.selecionar_operador(valor)

        elif acao == "calcular":
            self.calcular()

        elif acao == "limpar":
            self.limpar()

        elif acao == "apagar":
            self.apagar()


    def limpar(self):
        if self._teclado_bloqueado:
            return

        self.calculadora.limpar()
        self.atualizar_display()


    def abrir_painel(self):
        if self.painel_aberto:
            return

        self.painel_aberto = True
        # esconder_grid() guarda a posição para mostrar_grid() devolver igual.
        esconder_grid(self.display.frame)
        esconder_grid(self.frame_botoes)
        self.painel_tipos.mostrar()
        self.button_tipos.configure(text=TEXTO_BOTAO_VOLTAR)


    def fechar_painel(self):
        if not self.painel_aberto:
            return

        self.painel_aberto = False
        self.painel_tipos.ocultar()
        mostrar_grid(self.display.frame)
        mostrar_grid(self.frame_botoes)
        self.button_tipos.configure(text=TEXTO_BOTAO_TIPOS)


    def _bloquear_teclado_um_instante(self):
        """Ignora o teclado por um instante depois de escolher um tipo.

        O painel fecha no primeiro clique do tile; o segundo clique de um
        duplo-clique cairia no botão do teclado que ficou embaixo (o C, por
        exemplo, apagaria o número).
        """
        self._teclado_bloqueado = True

        def liberar():
            self._teclado_bloqueado = False

        self.frame.winfo_toplevel().after(tema.TEMPO_IGNORAR_CLIQUE, liberar)


    def alternar_painel(self):
        if self.painel_aberto:
            self.fechar_painel()
        else:
            self.abrir_painel()


    def escolher_tipo(self, tipo):
        if self.painel_aberto:
            self._bloquear_teclado_um_instante()
        self.fechar_painel()

        # Escolher o tipo que já está ativo não mexe nas unidades escolhidas.
        if tipo == self.tipo_conversao:
            return

        self.tipo_conversao = tipo
        self.painel_tipos.definir_ativo(tipo)
        self.label_tipo.configure(text=rotulo_do_tipo(tipo))
        self.display.definir_unidades(self.extrair_unidades(tipo))
        self.atualizar_display()
