"""Peças reutilizáveis da interface que corrigem comportamentos do CustomTkinter."""

import customtkinter as ctk

from swaplator.interface import tema


class BotaoRedondo(ctk.CTkButton):
    """Botão que fica perfeitamente redondo (ou com pontas arredondadas, se largo).

    Por dentro, o CTkButton é uma grade 5x5 e reserva `corner_radius` de largura
    nas colunas 0 e 4. Num botão de 72 px com raio 36, isso consome toda a largura
    e o botão fica oval. Zeramos essa reserva.

    Só zerar depois de criar o botão não basta: o CustomTkinter refaz a grade
    (`_create_grid`) sempre que a escala da tela muda, por exemplo ao arrastar a
    janela para outro monitor, e o valor original voltaria. Por isso o ajuste mora
    dentro do próprio `_create_grid`, que roda em todas essas situações.
    """

    def _create_grid(self):
        super()._create_grid()
        self.grid_columnconfigure((0, 4), minsize=0)


def executar_depois_do_clique(widget, funcao):
    """Executa `funcao` um instante depois do clique, e só se `widget` ainda existir.

    Quando o comando de um botão destrói o próprio botão (ou a tela dele), a
    animação de clique do CustomTkinter, agendada para ~100 ms depois, tenta
    mexer num widget que já não existe e gera o erro "invalid command name".

    Dois cuidados aqui:
    - o agendamento é feito na janela (`winfo_toplevel`), que continua viva depois
      da reconstrução; agendar no widget destruído perderia o agendamento;
    - ao chegar a hora, conferimos `winfo_exists()`: o usuário pode ter trocado de
      tela nesse meio-tempo.
    """
    def executar():
        if widget.winfo_exists():
            funcao()

    widget.winfo_toplevel().after(tema.TEMPO_ANIMACAO_CLIQUE, executar)
