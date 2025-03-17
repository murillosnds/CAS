# Aquae Attractio Calculator - 2025
# Open Source


nome = input("Qual é seu nome? ")

print(f"Olá, {nome} ")
atividade_fisica = input(f"{nome} você se considera: A - uma pessoa físicamente ativa ou B -uma pessoa sedentária? ")
if "A":
    print(f"Ok {nome}, você se considera uma pessoa fisicamente ativa!")
elif "B":
    print(f"Ok {nome}, você se considera uma pessoa sedentária!")

peso = float(input(f"Ok {nome}, Quanto você pesa atualmente (em kg)? "))
print(f"Você pesa {peso}kg, {nome}? Responda SIM ou NÃO ")
if "SIM":
    print("Ok!")
elif "NÂO":
    print("Por favor, insira seu peso.")
    print("Escreva V para voltar!")
