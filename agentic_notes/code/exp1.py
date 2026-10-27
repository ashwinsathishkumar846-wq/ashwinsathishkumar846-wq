def observe():
    print("\n--- OBSERVE ---")
    temp = float(input("Enter temperature (C): "))
    rain = input("Is it raining? (yes/no): ").lower() == "yes"
    hours = float(input("Enter free hours: "))
    return temp, rain, hours


def orient(temp, rain, hours):
    outdoor = not rain and temp <= 35
    long_study = hours >= 3
    print("--- ORIENT ---")
    print("Outdoor suitable:", outdoor)
    print("Long study possible:", long_study)
    return outdoor, long_study


def decide(outdoor, study):
    print("--- DECIDE ---")
    if outdoor and study:
        return "Study in library, then take a walk"
    elif outdoor:
        return "Take a short walk and revise notes"
    elif study:
        return "Stay indoors and study for three hours"
    else:
        return "Stay indoors and revise for one hour"


def act(decision):
    print("--- ACT ---")
    print("Executing:", decision)


print("=== OODA Study Assistant ===")
for cycle in range(1, 3):
    print("\nCycle", cycle)
    temp, rain, hours = observe()
    outdoor, study = orient(temp, rain, hours)
    decision = decide(outdoor, study)
    print("Decision:", decision)
    act(decision)

print("\nOODA loop completed.")
