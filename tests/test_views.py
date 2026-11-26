import unittest

from tests import fake_ctk


def setUpModule():
    # As telas importam o customtkinter ao serem carregadas, então o de mentira
    # precisa estar instalado antes do import.
    fake_ctk.instalar()

    global CalculadoraView, SIMBOLOS, tema
    from swaplator.interface.calculadora_view import CalculadoraView, SIMBOLOS
    from swaplator.interface import tema


def tearDownModule():
    fake_ctk.remover()


class ViewBase(unittest.TestCase):

    def setUp(self):
        self.view = CalculadoraView(fake_ctk.Fake())

    def apertar(self, *textos):
        # Os operadores aparecem como ÷ × − +, mas aqui escrevemos / * - +.
        for texto in textos:
            botao = fake_ctk.achar_botao(self.view.frame_botoes,
                                         SIMBOLOS.get(texto, texto))
            botao.opcoes["command"]()

    def topo(self):
        return self.view.display.label_entrada.opcoes["text"]

    def baixo(self):
        return self.view.display.label_resultado.opcoes["text"]


class TestCalculadoraConversora(ViewBase):

    def test_abre_como_conversora_de_comprimento(self):
        self.assertFalse(hasattr(self.view, "seletor_modo"))
        self.assertEqual(self.view.tipo_conversao, "comprimento")
        self.assertEqual(self.view.combobox_unidade_inicial.get(), "mm")
        self.assertEqual(self.view.combobox_unidade_final.get(), "cm")
        self.assertEqual(self.view.label_tipo.opcoes["text"], "Comprimento")

    def test_cabecalho_tem_o_botao_de_tipos(self):
        self.assertEqual(self.view.button_tipos.opcoes["text"], "⊞ Tipos")

    def test_converte_enquanto_digita(self):
        self.apertar("1", "0")
        self.assertEqual((self.topo(), self.baixo()), ("10", "1"))

        self.apertar("0")
        self.assertEqual((self.topo(), self.baixo()), ("100", "10"))

    def test_operador_pendente_e_igual(self):
        self.apertar("7", "+")
        self.assertEqual((self.topo(), self.baixo()), ("7 +", "0.7"))

        self.apertar("3")
        # A linha de baixo converte a conta toda (7 + 3 = 10 mm = 1 cm).
        self.assertEqual((self.topo(), self.baixo()), ("7 + 3", "1"))

        self.apertar("=")
        self.assertEqual((self.topo(), self.baixo()), ("10", "1"))

    def test_divisao_mostra_resultado_sem_ruido(self):
        self.apertar("1", "0", "/", "4", "=")

        self.assertEqual(self.topo(), "2.5")

    def test_ponto_duplicado_e_ignorado(self):
        self.apertar("1", ".", ".")

        self.assertEqual((self.topo(), self.baixo()), ("1.", "0.1"))

    def test_numero_digitado_aparece_como_digitado(self):
        self.apertar("1", ".", "0", "5")

        self.assertEqual(self.topo(), "1.05")

    def test_limpar_zera_as_duas_linhas(self):
        self.apertar("5", "C")

        self.assertEqual((self.topo(), self.baixo()), ("0", "0"))

    def test_trocar_unidade_reconverte(self):
        self.apertar("1")

        self.view.display.combobox_unidade_final.set("m")
        self.view.display.combobox_unidade_final.opcoes["command"]("m")

        self.assertEqual(self.baixo(), "0.001")

    def test_unidade_inexistente_mostra_traco(self):
        self.apertar("1")

        self.view.display.combobox_unidade_final.set("xx")
        self.view.display.combobox_unidade_final.opcoes["command"]("xx")

        self.assertEqual(self.baixo(), "—")

    def test_escolher_tipo_troca_unidades_e_mantem_o_numero(self):
        self.apertar("1", "0", "0")

        self.view.escolher_tipo("temperatura")

        self.assertEqual(self.view.combobox_unidade_inicial.get(), "°C")
        self.assertEqual(self.view.combobox_unidade_final.get(), "°F")
        self.assertEqual((self.topo(), self.baixo()), ("100", "212"))
        self.assertEqual(self.view.label_tipo.opcoes["text"], "Temperatura")

    def test_escolher_o_tipo_ativo_nao_reseta_unidades(self):
        self.view.combobox_unidade_inicial.set("km")

        self.view.escolher_tipo("comprimento")

        self.assertEqual(self.view.combobox_unidade_inicial.get(), "km")

    def test_divisao_por_zero_nao_quebra(self):
        self.apertar("1", "/", "0", "=")   # não deve levantar exceção

    def test_numeros_enormes_usam_notacao_cientifica(self):
        self.apertar(*"8" * 15, "*", *"8" * 15, "=")

        self.assertIn("e+29", self.topo())
        self.assertLessEqual(len(self.topo()), 15)
        self.assertEqual(
            self.view.display.label_entrada.opcoes["font"],
            tema.fonte(tema.tamanho_fonte_display(self.topo())))


class TestAparenciaDaCalculadora(ViewBase):

    def test_fonte_do_display_diminui_para_numero_longo(self):
        self.apertar(*"1234567891234567")   # 16 dígitos, sem zero

        self.assertEqual(self.view.display.label_entrada.opcoes["font"],
                         tema.fonte(tema.tamanho_fonte_display(self.topo())))
        self.assertLess(tema.tamanho_fonte_display(self.topo()), tema.TAM_DISPLAY)

    def test_fonte_do_display_e_grande_para_numero_curto(self):
        self.apertar("7")

        self.assertEqual(self.view.display.label_entrada.opcoes["font"],
                         tema.fonte(tema.TAM_DISPLAY))

    def test_zero_e_limpar_ocupam_varias_colunas(self):
        zero = fake_ctk.achar_botao(self.view.frame_botoes, "0")
        limpar = fake_ctk.achar_botao(self.view.frame_botoes, "C")

        self.assertEqual(zero.opcoes_grid["columnspan"], 2)
        self.assertEqual(limpar.opcoes_grid["columnspan"], 3)

    def test_cabecalho_tem_altura_do_tema(self):
        self.assertEqual(self.view.cabecalho.opcoes["height"], tema.ALTURA_CABECALHO)

    def test_display_fica_entre_o_cabecalho_e_o_teclado(self):
        linhas = (self.view.cabecalho.opcoes_grid["row"],
                  self.view.display.frame.opcoes_grid["row"],
                  self.view.frame_botoes.opcoes_grid["row"])

        self.assertEqual(linhas, (0, 1, 2))


class TestPainelDeTipos(unittest.TestCase):

    def setUp(self):
        self.janela = fake_ctk.Fake()
        self.view = CalculadoraView(self.janela)

    def abrir(self):
        self.view.button_tipos.opcoes["command"]()

    def test_painel_comeca_fechado_e_escondido(self):
        self.assertFalse(self.view.painel_aberto)
        self.assertFalse(self.view.painel_tipos.visivel)
        self.assertTrue(self.view.painel_tipos.grid_removido)
        self.assertFalse(self.view.frame_botoes.grid_removido)

    def test_botao_tipos_abre_o_painel_no_lugar_do_teclado(self):
        self.abrir()

        self.assertTrue(self.view.painel_aberto)
        self.assertTrue(self.view.painel_tipos.visivel)
        self.assertTrue(self.view.display.frame.grid_removido)
        self.assertTrue(self.view.frame_botoes.grid_removido)
        self.assertEqual(self.view.button_tipos.opcoes["text"], "Voltar")

    def test_botao_de_novo_volta_ao_teclado(self):
        self.abrir()
        self.abrir()

        self.assertFalse(self.view.painel_aberto)
        self.assertFalse(self.view.painel_tipos.visivel)
        self.assertFalse(self.view.display.frame.grid_removido)
        self.assertFalse(self.view.frame_botoes.grid_removido)
        self.assertEqual(self.view.button_tipos.opcoes["text"], "⊞ Tipos")

    def test_escolher_no_painel_troca_o_tipo_e_fecha(self):
        self.abrir()

        self.view.painel_tipos.escolher("massa")

        self.assertEqual(self.view.tipo_conversao, "massa")
        self.assertFalse(self.view.painel_aberto)
        self.assertEqual(self.view.label_tipo.opcoes["text"], "Massa")
        from swaplator.conversores.registro import CONVERSOES
        primeira = list(CONVERSOES["massa"][1])[0]
        self.assertEqual(self.view.combobox_unidade_inicial.get(), primeira)

    def test_escolher_o_tipo_ativo_so_fecha_o_painel(self):
        self.view.combobox_unidade_inicial.set("km")
        self.abrir()

        self.view.painel_tipos.escolher("comprimento")

        self.assertFalse(self.view.painel_aberto)
        self.assertEqual(self.view.combobox_unidade_inicial.get(), "km")

    def test_esc_fecha_o_painel(self):
        self.abrir()

        self.view.painel_tipos._ao_esc()

        self.assertFalse(self.view.painel_aberto)
        self.assertFalse(self.view.frame_botoes.grid_removido)

    def test_painel_marca_o_tipo_ativo(self):
        self.view.escolher_tipo("area")

        tile = self.view.painel_tipos.tiles["area"]
        self.assertEqual(tile.opcoes["fg_color"], tema.COR_DESTAQUE)

    def test_painel_ocupa_o_lugar_do_display_e_do_teclado(self):
        grade = self.view.painel_tipos.opcoes_grid

        self.assertEqual((grade["row"], grade["rowspan"]), (1, 2))

    def test_destruir_a_tela_com_o_painel_aberto_libera_os_binds(self):
        self.abrir()
        sequencias = {seq for seq, _ in self.janela.binds}

        self.view.frame.destroy()

        self.assertEqual({seq for seq, _ in self.janela.unbinds}, sequencias)
        self.assertEqual(len(sequencias), 7)   # 6 do painel + <Key> do teclado


class TestEscalaDaTelaComPainel(unittest.TestCase):
    """O CTk refaz o último grid() de cada widget quando a escala da tela muda.
    Widgets escondidos não podem deixar esse registro para trás, senão voltam
    à tela sozinhos (e o painel reapareceria por cima do teclado)."""

    def setUp(self):
        self.view = CalculadoraView(fake_ctk.Fake())

    def test_painel_fechado_nao_deixa_registro_de_geometria(self):
        self.assertIsNone(self.view.painel_tipos._last_geometry_manager_call)

    def test_painel_aberto_esconde_display_e_teclado_sem_registro(self):
        self.view.abrir_painel()

        self.assertIsNone(self.view.display.frame._last_geometry_manager_call)
        self.assertIsNone(self.view.frame_botoes._last_geometry_manager_call)

    def test_fechar_devolve_display_e_teclado_com_o_mesmo_espacamento(self):
        antes = dict(self.view.frame_botoes._last_geometry_manager_call["kwargs"])

        self.view.abrir_painel()
        self.view.fechar_painel()

        self.assertEqual(
            self.view.frame_botoes._last_geometry_manager_call["kwargs"], antes)
        self.assertIn("pady", antes)

    def test_reabrir_o_painel_usa_a_mesma_posicao(self):
        self.view.abrir_painel()

        grade = self.view.painel_tipos._last_geometry_manager_call["kwargs"]
        self.assertEqual((grade["row"], grade["rowspan"]), (1, 2))


class TestCliqueDuploNoTile(unittest.TestCase):
    """O painel fecha no primeiro clique; o segundo clique do duplo-clique cairia
    no botão do teclado que está debaixo do tile."""

    def setUp(self):
        self.janela = fake_ctk.Fake()
        self.agendados = []
        self.janela.after = lambda ms, funcao=None, *args: self.agendados.append(funcao)
        self.view = CalculadoraView(self.janela)

    def apertar(self, texto):
        fake_ctk.achar_botao(self.view.frame_botoes, SIMBOLOS.get(texto, texto)).opcoes["command"]()

    def test_teclado_ignora_cliques_logo_depois_de_escolher_no_painel(self):
        self.apertar("5")
        self.view.abrir_painel()
        self.view.painel_tipos.escolher("massa")

        self.apertar("C")   # o "segundo clique"

        self.assertEqual(self.view.display.label_entrada.opcoes["text"], "5")

    def test_teclado_volta_a_funcionar_depois_do_intervalo(self):
        self.apertar("5")
        self.view.abrir_painel()
        self.view.painel_tipos.escolher("massa")

        for funcao in self.agendados:
            funcao()
        self.apertar("C")

        self.assertEqual(self.view.display.label_entrada.opcoes["text"], "0")

    def test_voltar_pelo_botao_nao_trava_o_teclado(self):
        self.apertar("5")
        self.view.abrir_painel()
        self.view.fechar_painel()

        self.apertar("C")

        self.assertEqual(self.view.display.label_entrada.opcoes["text"], "0")


class TestTecladoFisico(unittest.TestCase):

    def setUp(self):
        self.janela = fake_ctk.Fake()
        self.agendados = []
        self.janela.after = lambda ms, funcao=None, *args: self.agendados.append(funcao)
        self.view = CalculadoraView(self.janela)

    def tecla(self, char="", keysym=""):
        from types import SimpleNamespace
        evento = SimpleNamespace(char=char, keysym=keysym, widget=self.janela)
        for handler in self.janela.handlers["<Key>"]:
            handler(evento)

    def digitar(self, texto):
        for char in texto:
            self.tecla(char, char)

    def topo(self):
        return self.view.display.label_entrada.opcoes["text"]

    def baixo(self):
        return self.view.display.label_resultado.opcoes["text"]

    def test_digitar_e_converter_pelo_teclado(self):
        self.digitar("10")

        self.assertEqual((self.topo(), self.baixo()), ("10", "1"))

    def test_conta_completa_pelo_teclado(self):
        self.digitar("7")
        self.tecla("+", "plus")
        self.digitar("3")
        self.tecla("\r", "Return")

        self.assertEqual(self.topo(), "10")

    def test_virgula_vira_ponto_decimal(self):
        self.digitar("1")
        self.tecla(",", "comma")
        self.digitar("5")

        self.assertEqual(self.topo(), "1.5")

    def test_backspace_apaga_e_reconverte(self):
        self.digitar("12")
        self.tecla("\x08", "BackSpace")

        self.assertEqual((self.topo(), self.baixo()), ("1", "0.1"))

    def test_esc_limpa(self):
        self.digitar("12")
        self.tecla("\x1b", "Escape")

        self.assertEqual((self.topo(), self.baixo()), ("0", "0"))

    def test_operador_sem_numero_nao_quebra(self):
        self.tecla("+", "plus")   # não deve levantar exceção

        self.assertEqual(self.topo(), "0")

    def test_teclado_ignorado_com_o_painel_aberto(self):
        self.digitar("5")
        self.view.abrir_painel()

        self.digitar("9")
        self.tecla("\x1b", "Escape")

        self.view.fechar_painel()
        self.assertEqual(self.topo(), "5")

    def test_teclado_ignorado_logo_apos_escolher_um_tipo(self):
        self.digitar("5")
        self.view.abrir_painel()
        self.view.painel_tipos.escolher("massa")

        self.digitar("9")

        self.assertEqual(self.topo(), "5")

    def test_destruir_a_tela_desfaz_o_bind_do_teclado(self):
        ligados = [(seq, i) for seq, i in self.janela.binds if seq == "<Key>"]

        self.view.frame.destroy()

        self.assertEqual(
            [u for u in self.janela.unbinds if u[0] == "<Key>"], ligados)


class TestConversaoDaContaEmAndamento(ViewBase):

    def test_converte_o_resultado_da_conta_e_nao_so_o_ultimo_numero(self):
        self.apertar("2", "3", "3", "/", "3")

        self.assertEqual(self.topo(), "233 ÷ 3")
        self.assertEqual(self.baixo(), "7.766666667")   # 77.67 mm em cm

    def test_conta_com_soma_ja_converte_a_soma(self):
        self.apertar("1", "0", "+", "5")

        self.assertEqual(self.baixo(), "1.5")   # 15 mm em cm

    def test_divisao_por_zero_em_andamento_mostra_traco(self):
        self.apertar("1", "/", "0")

        self.assertEqual(self.baixo(), "—")

    def test_apos_o_igual_converte_o_resultado(self):
        self.apertar("2", "3", "3", "/", "3", "=")

        self.assertEqual(self.baixo(), "7.766666667")

    def test_trocar_a_unidade_reconverte_a_conta_em_andamento(self):
        self.apertar("2", "0", "/", "4")

        self.view.display.combobox_unidade_final.set("m")
        self.view.display.combobox_unidade_final.opcoes["command"]("m")

        self.assertEqual(self.baixo(), "0.005")   # 5 mm em m


class TestCopiarResultado(unittest.TestCase):

    def setUp(self):
        self.janela = fake_ctk.Fake()
        self.agendados = []
        self.janela.after = lambda ms, funcao=None, *args: self.agendados.append(funcao)
        self.view = CalculadoraView(self.janela)

    def apertar(self, *textos):
        for texto in textos:
            fake_ctk.achar_botao(self.view.frame_botoes,
                                 SIMBOLOS.get(texto, texto)).opcoes["command"]()

    def copiado(self):
        return getattr(self.view.frame, "clipboard_texto", None)

    def test_botao_copiar_copia_a_linha_de_baixo(self):
        self.apertar("2", "3", "3", "/", "3")

        self.view.button_copiar.opcoes["command"]()

        self.assertEqual(self.copiado(), "7.766666667 cm")

    def test_copia_o_numero_com_a_unidade_final(self):
        self.apertar("1", "0")

        self.view.copiar_resultado()

        self.assertEqual(self.copiado(), "1 cm")

    def test_copia_a_unidade_final_escolhida(self):
        self.apertar("1", "0")
        self.view.display.combobox_unidade_final.set("m")
        self.view.display.combobox_unidade_final.opcoes["command"]("m")

        self.view.copiar_resultado()

        self.assertEqual(self.copiado(), "0.01 m")

    def test_nao_copia_o_traco(self):
        self.apertar("1", "/", "0")

        self.view.copiar_resultado()

        self.assertIsNone(self.copiado())

    def test_botao_copiar_fica_no_cabecalho_ao_lado_do_tipos(self):
        self.assertEqual(self.view.button_copiar.opcoes["text"], "Copiar")
        self.assertEqual(self.view.button_copiar.opcoes_grid["column"], 1)
        self.assertEqual(self.view.button_tipos.opcoes_grid["column"], 2)

    def test_botao_mostra_copiado_e_volta_ao_normal(self):
        self.apertar("5")

        self.view.copiar_resultado()
        self.assertEqual(self.view.button_copiar.opcoes["text"], "Copiado ✓")

        for funcao in self.agendados:
            funcao()
        self.assertEqual(self.view.button_copiar.opcoes["text"], "Copiar")

    def test_ctrl_c_copia(self):
        from types import SimpleNamespace
        self.apertar("1", "0")
        evento = SimpleNamespace(char="\x03", keysym="c", widget=self.janela, state=4)

        for handler in self.janela.handlers["<Key>"]:
            handler(evento)

        self.assertEqual(self.copiado(), "1 cm")

    def test_ctrl_c_nao_limpa_a_calculadora(self):
        from types import SimpleNamespace
        self.apertar("1", "0")
        evento = SimpleNamespace(char="\x03", keysym="c", widget=self.janela, state=4)

        for handler in self.janela.handlers["<Key>"]:
            handler(evento)

        self.assertEqual(self.view.display.label_entrada.opcoes["text"], "10")

    def test_copiar_com_o_painel_aberto_nao_faz_nada(self):
        self.apertar("5")
        self.view.abrir_painel()

        self.view.ao_acao_do_teclado("copiar", None)

        self.assertIsNone(self.copiado())


class TestBotoesRedondosDaCalculadora(unittest.TestCase):

    def test_todos_os_botoes_da_grade_sao_redondos(self):
        from swaplator.interface.componentes import BotaoRedondo

        view = CalculadoraView(fake_ctk.Fake())

        for texto in ("7", "0", ".", "C", "=", "÷"):
            botao = fake_ctk.achar_botao(view.frame_botoes, texto)
            self.assertIsInstance(botao, BotaoRedondo, texto)


if __name__ == "__main__":
    unittest.main()
