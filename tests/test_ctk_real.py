"""Confere, no CustomTkinter de verdade, as premissas em que o projeto se apoia.

O `BotaoRedondo` sobrescreve `_create_grid`, um método interno (com "_") do
CustomTkinter. Se uma atualização da biblioteca renomear esse método, o
ajuste pararia de funcionar em silêncio e os botões voltariam a ficar ovais.
Este teste avisa antes disso.

Roda só onde o CustomTkinter real pode ser importado (precisa do tkinter);
nos outros ambientes ele é pulado.
"""

import unittest

try:
    import customtkinter as ctk_real
except Exception:
    ctk_real = None


@unittest.skipIf(ctk_real is None, "customtkinter/tkinter indisponível neste ambiente")
class TestPremissasDoCustomTkinter(unittest.TestCase):

    def test_ctkbutton_tem_create_grid(self):
        self.assertTrue(callable(getattr(ctk_real.CTkButton, "_create_grid", None)))


if __name__ == "__main__":
    unittest.main()
