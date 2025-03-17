# Aquae Attractio Calculator - 2025
# Open Source
# By @murillosnds on GitHub 
# American English

name = input("What's your name? ")

print(f"Hi, {name} ")
physical_activity = input(f"{name} do you consider yourself: A - a physically active person or B - a sedentary person? Answer: ")
if physical_activity == "A":
    print(f"Okay {name}, you consider yourself a physically active person!")
elif physical_activity == "B":
    print(f"Ok {name}, you consider yourself a sedentary person!")

weight = float(input(f"Ok {name}, How much do you currently weigh (in kg)? "))
weight_confirmation = input(f"Do you weigh {weight:.0f}kg, {name}? Answer YES or NO | Answer: ")
if weight_confirmation == "YES":
    print("Okay!")
elif weight_confirmation == "NO":
    float(input("Please enter your weight (in kg) | Answer: "))
    print("Okay!")
else:
    print("CRITICAL ERROR! Restart the program.")

activity_weight = weight * 50
sedentary_weight = weight * 35 

if physical_activity == "A":
    print(f"You should drink {activity_weight:.0f}ml or {activity_weight/1000}liters per day")
elif physical_activity == "B":
    print(f"You should drink {sedentary_weight:.0f}ml or {sedentary_weight/1000}liters per day")





