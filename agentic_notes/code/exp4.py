import re


def calculator(a, b, op):
    if op == "+": return a + b
    if op == "-": return a - b
    if op == "*": return a * b
    if op == "/": return a / b if b != 0 else "Division by zero"


def convert(value, unit):
    if unit == "km":
        return f"{value * 0.621371:.2f} miles"
    if unit == "kg":
        return f"{value * 2.20462:.2f} pounds"
    if unit == "c":
        return f"{value * 9 / 5 + 32:.1f} F"


def weather(city):
    data = {
        "chennai": "32 C, humid",
        "coimbatore": "27 C, cloudy"
    }
    return data.get(city, "No data available")


print("=== Tool Calling Agent ===")

while True:
    request = input("\nRequest (or exit): ").lower().strip()
    if request == "exit":
        print("Agent stopped.")
        break

    if "convert" in request:
        m = re.search(r"(\d+\.?\d*)\s*(km|kg|c)\b", request)
        print("Tool selected: unit converter")
        if m:
            print("Result:", convert(float(m.group(1)), m.group(2)))
        else:
            print("Result: Invalid conversion request")
    elif "weather" in request:
        city = request.split()[-1]
        print("Tool selected: weather")
        print("Result:", weather(city))
    else:
        m = re.search(r"(\d+\.?\d*)\s*([+\-*/])\s*(\d+\.?\d*)", request)
        if m:
            print("Tool selected: calculator")
            print("Result:", calculator(float(m.group(1)),
                                        float(m.group(3)), m.group(2)))
        else:
            print("No suitable tool found")
