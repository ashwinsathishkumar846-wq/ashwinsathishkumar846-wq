scores = {
    "Revise notes": 85,
    "Practice programs": 55,
    "Mock test": 70
}


def plan(hours):
    tasks = [("Revise notes", 2),
             ("Practice programs", 3),
             ("Mock test", 2)]
    if sum(h for _, h in tasks) > hours:
        tasks = [(name, max(1, h - 1)) for name, h in tasks]
    print("PLANNING:", tasks)
    return tasks


def react(task, hours):
    print("\nTask:", task)
    print("Thought: I need", hours, "hours.")
    print("Action: Start", task)
    result = scores[task]
    print("Observation: Score =", result)
    return result


def reflect(task, score):
    if score < 60:
        print("Reflection: Low score. Revision needed.")
        return task
    print("Reflection: Score acceptable.")
    return None


print("=== ReAct, Reflection and Planning ===")
hours = int(input("Enter available hours: "))
revise = []

for task, h in plan(hours):
    score = react(task, h)
    weak = reflect(task, score)
    if weak:
        revise.append(weak)

print("\nREFLECTION SUMMARY")
if revise:
    print("Add revision for:", ", ".join(revise))
else:
    print("No extra revision needed")
print("Study plan completed.")
