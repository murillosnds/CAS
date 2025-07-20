import tkinter as tk
from tkinter import messagebox

def calcular_consumo():
    nome = entrada_nome.get()
    idade = int(entrada_idade.get())
    peso = float(entrada_peso.get())
    atividade = var_atividade.get()

    # Verifica confirmação do peso
    if not var_confirmar_peso.get():
        messagebox.showerror("Erro", "Você precisa confirmar seu peso.")
        return

    # Define fator de multiplicação
    if idade >= 66:
        fator = 25
    elif idade >= 56:
        fator = 30
    elif idade >= 18:
        fator = 35
    else:
        fator = 40

    ml_por_dia = peso * fator
    litros_por_dia = ml_por_dia / 1000

    resultado = f"{nome}, você deve ingerir {ml_por_dia:.0f} ml ou {litros_por_dia:.2f} litros de água por dia."

    messagebox.showinfo("Resultado", resultado)

# Criação da Janela
janela = tk.Tk()
janela.title("Aquae Attractio Calculator - 2025")
janela.geometry("400x450")
janela.resizable(False, False)

# Nome
tk.Label(janela, text="Qual é seu nome?").pack()
entrada_nome = tk.Entry(janela)
entrada_nome.pack()

# Idade
tk.Label(janela, text="Qual a sua idade?").pack()
entrada_idade = tk.Entry(janela)
entrada_idade.pack()

# Peso
tk.Label(janela, text="Qual o seu peso (kg)?").pack()
entrada_peso = tk.Entry(janela)
entrada_peso.pack()

# Confirmação de peso
var_confirmar_peso = tk.BooleanVar()
tk.Checkbutton(janela, text="Confirmo que meu peso está correto", variable=var_confirmar_peso).pack()

# Atividade Física
tk.Label(janela, text="Você se considera:").pack()
var_atividade = tk.StringVar(value="A")
tk.Radiobutton(janela, text="Fisicamente Ativo (A)", variable=var_atividade, value="A").pack()
tk.Radiobutton(janela, text="Sedentário (B)", variable=var_atividade, value="B").pack()

# Botão Calcular
tk.Button(janela, text="Calcular Ingestão de Água", command=calcular_consumo).pack(pady=20)

# Rodapé
tk.Label(janela, text="Por @murillosnds | GitHub", fg="gray").pack(side="bottom", pady=10)

# Iniciar loop da interface
janela.mainloop()
