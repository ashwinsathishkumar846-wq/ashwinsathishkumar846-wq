import re
import sqlite3

knowledge = [
    ("RAG", "RAG retrieves documents and uses them to answer questions."),
    ("MemGPT", "MemGPT-style agents use core and archival memory."),
    ("Tool calling", "Tool calling selects a function and passes arguments.")
]

db = sqlite3.connect("rag_memory.db")
db.execute("CREATE TABLE IF NOT EXISTS memory "
           "(key TEXT PRIMARY KEY, value TEXT)")
db.commit()


def remember(key, value):
    db.execute("INSERT OR REPLACE INTO memory VALUES (?, ?)",
               (key, value))
    db.commit()


def recall(key):
    row = db.execute("SELECT value FROM memory WHERE key=?",
                     (key,)).fetchone()
    return row[0] if row else None


def retrieve(question):
    q = question.lower()
    for title, text in knowledge:
        if title.lower() in q:
            return f"[Retrieved: {title}] {text}"
    words = set(re.findall(r"\w+", q))
    for title, text in knowledge:
        if words & set(re.findall(r"\w+", text.lower())) - {"and", "the", "a"}:
            return f"[Retrieved: {title}] {text}"
    return "No relevant knowledge found."


print("=== RAG Agent with Memory ===")
print("Stored style:", recall("style"))
print("Stored topic:", recall("topic"))

while True:
    msg = input("\nYou: ").strip()
    low = msg.lower()
    if low == "exit":
        print("Session ended. Memory saved.")
        break
    if low.startswith("remember "):
        key, _, value = msg[9:].partition("=")
        remember(key.strip(), value.strip())
        print("Agent: Saved", key.strip(), "=", value.strip())
    elif low.startswith("what is my "):
        print("Agent:", recall(low[11:].strip()) or "I do not know yet.")
    else:
        print("Agent:", retrieve(msg))
