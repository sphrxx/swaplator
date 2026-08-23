import customtkinter as ctk

class Sidebar:

    def __init__(self, master, selecionar_conversao):
        self.frame = ctk.CTkFrame(master)

        self.selecionar_conversao = selecionar_conversao

        self.criar_widgets()
        self.configurar_layout()
        
        
    def criar_widgets(self):
        self.label_titulo = ctk.CTkLabel(self.frame, text="Swaplator", font=("Arial", 24))

        self.button_comprimento = ctk.CTkButton(self.frame, text="Comprimento", command=lambda: self.selecionar_conversao("comprimento"))
        self.button_area = ctk.CTkButton(self.frame, text="Área", command=lambda: self.selecionar_conversao("area"))
        self.button_massa = ctk.CTkButton(self.frame, text="Massa", command=lambda: self.selecionar_conversao("massa"))
        self.button_volume = ctk.CTkButton(self.frame, text="Volume", command=lambda: self.selecionar_conversao("volume"))

    def configurar_layout(self):
        self.frame.grid(row=0, column=0, padx=5, pady=5, sticky="ns")
        self.frame.configure(width=200)

        self.label_titulo.grid(row=0, column=0, padx=10, pady=10)

        self.button_comprimento.grid(row=1, column=0, padx=10, pady=10)
        self.button_area.grid(row=2, column=0, padx=10, pady=10)
        self.button_massa.grid(row=3, column=0, padx=10, pady=10)
        self.button_volume.grid(row=4, column=0, padx=10, pady=10)

