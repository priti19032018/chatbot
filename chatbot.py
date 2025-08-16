from datetime import datetime
import re
import random

EXIT_WORDS = {"quit", "exit", "bye", "stop"}

JOKES = [
    "Why do Python devs wear glasses? Because they can't C.",
    "There are 10 kinds of people: those who understand binary and those who don't.",
    "I told my computer I needed a break, and it said 'No problem, I'll go to sleep.'",
]

def clean(text: str) -> str:
    # Lowercase + keep simple characters so comparisons are easy
    return re.sub(r"[^a-z0-9 +:?.]", " ", text.lower()).strip()

def respond_single(text: str) -> str:
    t = clean(text)

    if not t:
        return "Say something and I'll try to help 🙂"

    # ---- simple if-elif-else rules ----
    if any(w in t for w in ("hello", "hi", "hey")):
        return random.choice(["Hi!", "Hello!", "Hey there!"])

    elif "help" in t or "what can you do" in t:
        return ("I can chat, tell the date/time, crack a joke, do tiny math like 2+2, "
                "and say bye. Try: 'time', 'date', 'joke', 'what is 12/3', or 'bye'.")

    elif "time" in t:
        return f"It's {datetime.now().strftime('%I:%M %p')}."

    elif "date" in t or "day" in t:
        return f"Today is {datetime.now().strftime('%A, %d %B %Y')}."

    elif "your name" in t:
        return "I'm RuleBot—built with if/elif/else."

    elif "joke" in t:
        return random.choice(JOKES)

    elif re.search(r"\d+\s*[\+\-\*/]\s*\d+", t):
        # tiny safe calculator for "2+3", "10 / 4", etc.
        m = re.search(r"(\d+)\s*([\+\-\*/])\s*(\d+)", t)
        a, op, b = int(m.group(1)), m.group(2), int(m.group(3))
        if op == "+": return f"{a + b}"
        if op == "-": return f"{a - b}"
        if op == "*": return f"{a * b}"
        if op == "/":
            return "Can't divide by zero!" if b == 0 else f"{a / b:.2f}"

    elif "thanks" in t or "thank you" in t:
        return "You're welcome!"

    else:
        return "Sorry, I didn't get that. Type 'help' to see what I understand."

def respond(text: str) -> str:
    # tiny multi-intent support: split on the word "and"
    parts = [p.strip() for p in re.split(r"\band\b", text, flags=re.I) if p.strip()]
    if len(parts) > 1:
        return " | ".join(respond_single(p) for p in parts)
    return respond_single(text)

def main():
    print("RuleBot 🤖: Hi! Type 'help' to see options. Type 'bye' to exit.")
    while True:
        user = input("You: ").strip()
        if user.lower() in EXIT_WORDS:
            print("RuleBot 🤖: Bye! 👋")
            break
        print("RuleBot 🤖:", respond(user))

if __name__ == "__main__":
    main()
