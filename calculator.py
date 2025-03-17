# Aquae Attractio Calculator - 2025
# Open Source
# By @murillosnds on GitHub 


nome = input("Qual é seu nome? ")

print(f"Olá, {nome} ")
atividade_fisica = input(f"{nome} você se considera: A - uma pessoa físicamente ativa ou B -uma pessoa sedentária? | Resposta: ")
if atividade_fisica == "A":
    print(f"Ok {nome}, você se considera uma pessoa fisicamente ativa!")
elif atividade_fisica == "B":
    print(f"Ok {nome}, você se considera uma pessoa sedentária!")

peso = float(input(f"Ok {nome}, Quanto você pesa atualmente (em kg)? "))
confirmação_peso = input(f"Você pesa {peso:.0f}kg, {nome}? Responda SIM ou NÃO | Resposta: ")
if confirmação_peso == "SIM":
    print("Ok!")
elif confirmação_peso == "NÃO":
    float(input("Por favor, insira seu peso (em kg) | Resposta: "))
    print("Ok!")
else:
    print("ERRO CRITICO! Reinicie o programa.")

peso_ativo = peso * 50
peso_sedentario = peso * 35 

if atividade_fisica == "A":
    print(f"Você deve ingerir {peso_ativo:.0f}ml ou {peso_ativo/1000}litros por dia")
elif atividade_fisica == "B":
    print(f"Você deve ingerir {peso_sedentario:.0f}ml ou {peso_sedentario/1000}litros por dia")





