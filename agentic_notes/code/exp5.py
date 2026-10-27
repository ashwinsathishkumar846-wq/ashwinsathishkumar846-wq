import json
import re


def generate(request):
    text = request.lower()
    priority = "medium"
    for level in ("low", "medium", "high"):
        if level in text:
            priority = level
    match = re.search(r"(\d+\.?\d*)\s*hours?", text)
    duration = float(match.group(1)) if match else None
    task = re.split(r",| for \d", request)[0].strip()
    return {
        "task": task,
        "priority": priority,
        "duration_hours": duration,
        "status": "pending"
    }


def validate(data):
    errors = []
    if not data["task"]:
        errors.append("Task cannot be empty")
    if data["priority"] not in ("low", "medium", "high"):
        errors.append("Invalid priority")
    if data["duration_hours"] is None or data["duration_hours"] <= 0:
        errors.append("Duration must be positive")
    return errors


print("=== Structured Output Generator ===")

while True:
    request = input("\nStudy request (or exit): ").strip()
    if request.lower() == "exit":
        print("Generator stopped.")
        break
    data = generate(request)
    errors = validate(data)
    if errors:
        print("Validation FAILED:", errors)
    else:
        print("Validation PASSED")
        print(json.dumps(data, indent=2))
