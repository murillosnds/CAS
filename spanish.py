# Aquae Attractio Calculator - 2025
# Open Source
# By @murillosnds on GitHub 
# Español

nombre = input("¿Cómo te llamas? ")

print(f"Hola, {nombre} ")
actividad_fisica = input(f"{nombre} ¿te consideras: A - una persona físicamente activa o B - una persona sedentaria? Responda: ")
if actividad_fisica == "A":
    print(f"Vale {nombre}, ¡te consideras una persona físicamente activa!")
elif actividad_fisica == "B":
    print(f"Vale {nombre}, ¡te consideras una persona sedentaria!")

peso = float(input(f"Ok {nombre}, ¿Cuánto pesas actualmente (en kg)? "))
confirmación_peso = input(f"¿Pesa {peso:.0f}kg, {nombre}? Contesta SÍ o NO | Contesta: ")
if confirmación_peso == "SÍ":
    print("Vale!")
elif confirmación_peso == "NO":
    float(input("Por favor, introduzca su peso (en kg) | Respuesta: "))
    print("Vale!")
else:
    print("¡ERROR CRÍTICO! Reinicie el programa.")

peso_activa = peso * 50
peso_sedentaria= peso * 35 

if actividad_fisica == "A":
    print(f"Debe beber {peso_activa:.0f}ml o {peso_activa/1000}litros al día")
elif actividad_fisica == "B":
    print(f"Debe beber {peso_sedentaria:.0f}ml o {peso_sedentaria/1000}litros al día")





