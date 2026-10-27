import re


def think(task):
    text = task.lower()
    nums = [float(n) for n in re.findall(r"\d+\.?\d*", text)]
    if "add" in text and len(nums) >= 2:
        return "Addition requested", "add", nums
    if "multiply" in text and len(nums) >= 2:
        return "Multiplication requested", "multiply", nums
    if "reverse" in text:
        return "Reverse text", "reverse", [text.split("reverse", 1)[1].strip()]
    if "count" in text and "words" in text:
        return "Count words", "count", [task.split(":", 1)[-1].strip()]
    return "No matching action", "none", []


def act(action, args):
    if action == "add":
        return sum(args)
    if action == "multiply":
        result = 1
        for n in args:
            result *= n
        return result
    if action == "reverse":
        return args[0][::-1]
    if action == "count":
        return len(args[0].split())
    return "Unable to complete task"


print("=== Thought-Action Agent ===")
print("Rule-based simulation; no LLM API used.")

while True:
    task = input("\nEnter task (or exit): ").strip()
    if task.lower() == "exit":
        print("Agent stopped.")
        break
    thought, action, args = think(task)
    print("Thought:", thought)
    print("Action:", action, args)
    print("Result:", act(action, args))
