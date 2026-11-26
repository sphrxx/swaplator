# Swaplator

Aplicação desktop desenvolvida em Python para cálculos e conversões de medidas e moedas.

## Status

Em desenvolvimento.

## Funcionalidades

- [x] Calculadora conversora
  - [x] Display de duas linhas, com a conversão ao vivo (inclusive da conta em andamento)
  - [x] Uso pelo teclado (números, `+ - * /`, `Enter`, `Esc`, `Backspace`)
  - [x] Botão **Copiar** (ou `Ctrl+C`): copia o resultado com a unidade final
  - [x] Menu de tipos de conversão por ícones (botão `⊞ Tipos`)
- [x] Conversor de medidas
  - [x] Comprimento
  - [x] Massa
  - [x] Temperatura
  - [x] Área
  - [x] Volume
- [x] Conversor de moedas (precisa de internet)

## Como usar em outro computador

Estes passos funcionam em um computador que nunca viu o projeto. Os comandos
são para o **Windows (PowerShell)**; no fim há as diferenças para macOS e Linux.

### 1. O que instalar antes

| Programa | Versão | Observação |
|---|---|---|
| [Python](https://www.python.org/downloads/) | **3.13 ou mais novo** | Na instalação, marque **"Add python.exe to PATH"** e deixe marcada a opção **tcl/tk and IDLE** (é ela que permite abrir janelas). |
| [Git](https://git-scm.com/downloads) | qualquer | Só para baixar o projeto. Sem Git, veja a alternativa abaixo. |

Para conferir, abra o PowerShell e rode `python --version`: deve mostrar 3.13 ou maior.

### 2. Baixar o projeto

```powershell
git clone https://github.com/sphrxx/swaplator.git
cd swaplator
```

*Sem Git:* na página do projeto no GitHub, clique em **Code → Download ZIP**,
extraia a pasta e abra o PowerShell dentro dela.

### 3. Criar o ambiente virtual e instalar

O ambiente virtual (`.venv`) é uma pasta só do projeto, para as bibliotecas não
se misturarem com as de outros programas.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -e .
```

Isso instala o Swaplator e as bibliotecas que ele usa (`customtkinter` e `requests`).
Você só precisa fazer este passo **uma vez** por computador.

> Se aparecer o erro *"a execução de scripts foi desabilitada neste sistema"*,
> rode `Set-ExecutionPolicy -Scope Process Bypass` e repita o `Activate.ps1`.
> Ou, no lugar da ativação, use `.venv\Scripts\python` em todos os comandos
> (ex.: `.venv\Scripts\python -m pip install -e .`).

### 4. Abrir o aplicativo

```powershell
python -m swaplator.main
```

Nas próximas vezes, basta abrir o PowerShell na pasta do projeto, ativar o
ambiente (`.venv\Scripts\Activate.ps1`) e rodar o comando acima.

### 5. Atualizar para a versão mais nova

```powershell
git pull
python -m pip install -e .
```

### Rodar os testes (opcional)

```powershell
python -m unittest
```

Deve terminar com `OK` (um teste que precisa de janela real pode aparecer como "skipped").

### macOS e Linux

```bash
git clone https://github.com/sphrxx/swaplator.git
cd swaplator
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
python -m swaplator.main
```

No Linux (Ubuntu/Debian), se faltar o Tkinter: `sudo apt install python3-tk`.
No macOS, prefira o Python do site python.org, que já inclui o Tkinter.

### Problemas comuns

| Sintoma | Causa e solução |
|---|---|
| `python` não é reconhecido | O Python não está no PATH. Reinstale marcando **Add python.exe to PATH**, ou use `py -3.13`. |
| `requires a different Python` | A versão do Python é anterior à 3.13. Instale a 3.13 ou mais nova. |
| `No module named '_tkinter'` / `tkinter` | Faltou o Tkinter: reinstale o Python com **tcl/tk** marcado (Windows) ou `sudo apt install python3-tk` (Linux). |
| `No module named 'swaplator'` | O ambiente virtual não está ativo ou o `pip install -e .` não foi feito. Repita os passos 3 e 4 na pasta do projeto. |
| O conversor de moedas mostra erro de conexão | Ele busca as cotações na internet (API Frankfurter). Conecte-se e tente de novo; as outras telas funcionam sem internet. |
| A janela aparece cortada ou grande demais | Ela se adapta à tela, mas precisa de pelo menos 720×660 (em unidades da escala do Windows). Reduza a escala de exibição ou use uma tela maior. |

## Tecnologias

- Python 3.13+
- CustomTkinter
- requests (cotações de moedas)
- unittest

## Sobre o projeto

O Swaplator é um projeto desenvolvido como atividade acadêmica,
com o objetivo de aplicar conceitos de programação em Python,
desenvolvimento de interfaces gráficas, organização de projetos,
tratamento de erros e testes automatizados.
