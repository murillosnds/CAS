# Aquae Attractio Calculator - 2025
# Open Source
# By @murillosnds on GitHub 
# Português do Brasil

nome = input("Qual é seu nome? ")

print(f"Olá, {nome} ")
atividade_fisica = input(f"{nome} você se considera: A - uma pessoa físicamente ativa ou B -uma pessoa sedentária? | Resposta: ")
if atividade_fisica == "A":
    print(f"Ok {nome}, você se considera uma pessoa fisicamente ativa!")
elif atividade_fisica == "B":
    print(f"Ok {nome}, você se considera uma pessoa sedentária!")

idade = int(input("Qual a sua idade? | Resposta: "))

if idade >= 66:
    print("Vamos usar 25 ml por cada kg")
elif idade >= 56:
    print("Vamos usar 30 ml por cada kg")
elif idade >= 18:
    print("Vamos usar 35 ml por cada kg")
else:
    print("Vamos usar 40 ml por cada kg")



peso = float(input(f"Ok {nome}, Quanto você pesa atualmente (em kg)? "))
confirmação_peso = input(f"Você pesa {peso:.0f}kg, {nome}? Responda SIM ou NÃO | Resposta: ")
if confirmação_peso == "SIM":
    print("Ok!")
elif confirmação_peso == "NÃO":
    float(input("Por favor, insira seu peso (em kg) | Resposta: "))
    print("Ok!")
else:
    print("ERRO CRITICO! Reinicie o programa.")

peso_jovem = peso * 40
peso_jovem_adulto = peso * 35
peso_adulto_velho = peso * 30
demais_idade = peso * 25

if atividade_fisica == "A" and idade < 18:
    print(f"Você deve ingerir {peso_jovem:.0f}ml ou {peso_jovem/1000}litros por dia")

elif atividade_fisica == "B" and idade < 18:
    print(f"Você deve ingerir {peso_jovem:.0f}ml ou {peso_jovem/1000}litros por dia")

elif atividade_fisica == "A" and idade >= 18 and 55:
    print(f"Você deve ingerir {peso_jovem_adulto:.0f}ml ou {peso_jovem_adulto/1000}litros por dia")

elif atividade_fisica == "B" and idade >= 18 and 55:
    print(f"Você deve ingerir {peso_jovem_adulto:.0f}ml ou {peso_jovem_adulto/1000}litros por dia")

elif atividade_fisica == "A" and idade >= 56 and 65:
    print(f"Você deve ingerir {peso_adulto_velho:.0f}ml ou {peso_adulto_velho/1000}litros por dia")

elif atividade_fisica == "B" and idade >= 56 and 65:
    print(f"Você deve ingerir {peso_adulto_velho:.0f}ml ou {peso_adulto_velho/1000}litros por dia")
else:
    print(f"Você deve ingerir {demais_idade:.0f}ml ou {demais_idade/1000}litros por dia")