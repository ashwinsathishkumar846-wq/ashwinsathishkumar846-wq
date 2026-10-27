readings = [24, 28, 33, 38, 31, 22]
fan = "OFF"

print("=== Temperature Monitoring Agent ===")

for i, temp in enumerate(readings, 1):
    print(f"Cycle {i}: Temperature = {temp} C")

    if temp < 26:
        state = "Cool"
    elif temp < 32:
        state = "Warm"
    else:
        state = "Hot"

    if state == "Hot":
        action = "Turn fan ON at HIGH speed"
        fan = "HIGH"
    elif state == "Warm" and fan == "OFF":
        action = "Turn fan ON at LOW speed"
        fan = "LOW"
    elif state == "Cool" and fan != "OFF":
        action = "Turn fan OFF"
        fan = "OFF"
    else:
        action = "No change"

    print("Interpretation:", state)
    print("Action:", action)
    print("Fan state:", fan)
    print()

print("Monitoring completed.")
