"""
DecodeLabs | AI Industrial Training Kit (Batch 2026)
Project 1  :  Rule-Based AI Chatbot  ("The Logic Skeleton")

This is a WHITE-BOX, deterministic chatbot.
Input -> Logic -> Output. No mystery, no hallucination.

Architecture (IPO Model):
    INPUT    -> Sanitization & Normalization  (lower + strip)
    PROCESS  -> Intent matching via a dictionary / hash map  (O(1) lookups)
    OUTPUT   -> Response generation + safe fallback

Why a dictionary instead of a long if-elif ladder?
    if-elif ladder  -> O(n), high technical debt, "unstable" as it grows
    dictionary (hash map) -> O(1) lookup, scales to thousands of rules,
                             handles lookup + fallback in one atomic .get() call.

Author : <YOUR NAME>     Role: AI Intern @ DecodeLabs     Week: 1
"""

import re

BOT_NAME = "DecodeBot"

# ---------------------------------------------------------------------------
# 1. THE KNOWLEDGE BASE  (5+ intents, as required by the spec)
#    Each intent = a set of trigger keywords  ->  one response.
#    This is the "hash map" the briefing keeps pointing to.
# ---------------------------------------------------------------------------
INTENTS = {
    "greeting": {
        "keywords": ["hello", "hi", "hey", "yo", "hii", "greetings",
                     "good morning", "good evening", "good afternoon"],
        "response": f"Hey there! 👋 I'm {BOT_NAME}, a rule-based assistant. "
                    f"Ask me something, or type 'help' to see what I can do.",
    },
    "how_are_you": {
        "keywords": ["how are you", "how r u", "how do you do", "whats up",
                     "what's up", "sup"],
        "response": "I'm running on pure logic, so I'm always at 100%. 😎 "
                    "How can I help you?",
    },
    "identity": {
        "keywords": ["your name", "who are you", "what are you", "who r u"],
        "response": f"I'm {BOT_NAME} — a deterministic, rule-based AI built "
                    f"during Project 1 of the DecodeLabs internship.",
    },
    "creator": {
        "keywords": ["who made you", "who built you", "your creator",
                     "decodelabs", "decode labs"],
        "response": "I was built by a DecodeLabs AI intern as their Week-1 "
                    "milestone. I'm the 'logic skeleton' that future smart "
                    "models will be built on top of.",
    },
    "capabilities": {
        "keywords": ["help", "what can you do", "options", "commands",
                     "menu"],
        "response": ("I can: \n"
                     "  • greet you  • tell you about myself\n"
                     "  • tell the time of day  • thank you back\n"
                     "  • and exit cleanly when you type 'bye' or 'exit'.\n"
                     "Try saying hello!"),
    },
    "time": {
        "keywords": ["time", "what time", "date", "day", "today"],
        "response": "I'm a rule-based bot with no clock access yet — but in "
                    "Week 2 I'll learn to read live data. ⏰",
    },
    "thanks": {
        "keywords": ["thanks", "thank you", "thx", "ty", "appreciate"],
        "response": "You're welcome! Always happy to help. 🙂",
    },
    "weather": {
        "keywords": ["weather", "rain", "temperature", "hot", "cold"],
        "response": "I can't check the weather yet — I'm a white-box logic "
                    "engine, not a forecaster. Maybe in a later project!",
    },
}

# ---------------------------------------------------------------------------
# 2. SPECIAL RESPONSES
# ---------------------------------------------------------------------------
EXIT_COMMANDS = {"bye", "exit", "quit", "goodbye", "see you", "see ya", "stop"}
GOODBYE_REPLY = f"Goodbye! 👋 Thanks for chatting with {BOT_NAME}."
EMPTY_REPLY = "You didn't type anything. Try asking me something!"
FALLBACK_REPLY = ("I do not understand that yet. 🤔 "
                  "Type 'help' to see what I can handle.")


# ---------------------------------------------------------------------------
# 3. PHASE 1 — INPUT SANITIZATION & NORMALIZATION
# ---------------------------------------------------------------------------
def sanitize(raw_input: str) -> str:
    """Lower-case, strip whitespace.  'HeLLo  ' -> 'hello'."""
    return raw_input.lower().strip()


def tokenize(text: str) -> set:
    """Split clean text into a set of words for boundary-safe matching."""
    return set(re.findall(r"[a-z']+", text))


# ---------------------------------------------------------------------------
# 4. PHASE 2 — THE LOGIC SKELETON (intent matching)
# ---------------------------------------------------------------------------
def get_response(raw_input: str):
    """
    Returns (reply_text, should_exit).

    Flow:  sanitize -> empty check -> exit check -> intent scan -> fallback
    """
    text = sanitize(raw_input)

    if not text:
        return EMPTY_REPLY, False

    words = tokenize(text)

    # Exit strategy: clean break command
    if text in EXIT_COMMANDS or (words & EXIT_COMMANDS):
        return GOODBYE_REPLY, True

    # Intent scan. Multi-word keywords are matched as phrases,
    # single words are matched on word boundaries (so "hi" != "this").
    for intent in INTENTS.values():
        for kw in intent["keywords"]:
            if " " in kw:
                if kw in text:
                    return intent["response"], False
            else:
                if kw in words:
                    return intent["response"], False

    # Fallback — the .get()-style default for unknown input
    return FALLBACK_REPLY, False


# ---------------------------------------------------------------------------
# 5. PHASE 3 — THE HEARTBEAT (the infinite loop)
# ---------------------------------------------------------------------------
def run_chat():
    """Interactive loop. Stays alive until a 'kill command' (exit)."""
    print(f"{BOT_NAME}: Hello! I'm online. Type 'help' for options or "
          f"'bye' to leave.")
    while True:
        raw = input("You: ")
        reply, should_exit = get_response(raw)
        print(f"{BOT_NAME}: {reply}")
        if should_exit:
            break


# ---------------------------------------------------------------------------
# 6. DEMO MODE (for non-interactive environments like a Kaggle commit
#    run, where input() has no keyboard attached).
# ---------------------------------------------------------------------------
def run_demo():
    """Replays a scripted conversation so the bot can be tested anywhere."""
    sample_conversation = [
        "Hello",
        "What is your name?",
        "  HELP  ",
        "How are you?",
        "Who built you?",
        "thanks!",
        "asdfghjkl",   # triggers fallback
        "bye",
    ]
    print(f"{BOT_NAME}: (demo mode) replaying a sample conversation\n")
    for raw in sample_conversation:
        print(f"You: {raw}")
        reply, should_exit = get_response(raw)
        print(f"{BOT_NAME}: {reply}\n")
        if should_exit:
            break


if __name__ == "__main__":
    # Try interactive mode; fall back to demo if no stdin is available.
    try:
        run_chat()
    except (EOFError, OSError):
        run_demo()
