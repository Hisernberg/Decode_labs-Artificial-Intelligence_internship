# 🤖 Rule-Based AI Chatbot — DecodeLabs Project 1

> **AI Industrial Training Kit · Batch 2026 · Week 1**
> Internship track: Artificial Intelligence Engineer @ DecodeLabs

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Type](https://img.shields.io/badge/AI-Rule--Based-green)
![Status](https://img.shields.io/badge/Project%201-Complete-success)
![Dependencies](https://img.shields.io/badge/dependencies-none-lightgrey)

A deterministic, **white-box** chatbot built entirely with control flow and a
dictionary-based knowledge base. No machine learning, no neural network, **no
hallucination** — every output is traceable: **Input → Logic → Output**.

This is the *logic skeleton* that more advanced, learning-based AI is later
built on top of.

---

## 🎯 What it does

`DecodeBot` reads what you type, normalizes it, matches it against a set of
intents stored in a dictionary, and replies. If it doesn't recognise the
input, it gives a safe fallback instead of guessing.

```
You: HELLO
DecodeBot: Hey there! 👋 I'm DecodeBot, a rule-based assistant...

You: what is your name?
DecodeBot: I'm DecodeBot — a deterministic, rule-based AI...

You: asdfghjkl
DecodeBot: I do not understand that yet. 🤔 Type 'help' to see what I can handle.

You: bye
DecodeBot: Goodbye! 👋 Thanks for chatting with DecodeBot.
```

---

## ✅ Spec checklist

The brief required five things. All are implemented:

| Requirement | Status | How |
|---|---|---|
| **Input loop** — continuous cycle | ✅ | `while True` loop (the "heartbeat") |
| **Sanitization** — case & whitespace | ✅ | `raw_input.lower().strip()` |
| **Knowledge base** — 5+ intents | ✅ | dictionary with **8 intents** |
| **Fallback** — default for unknowns | ✅ | a default reply instead of crashing |
| **Exit strategy** — clean break | ✅ | `break` on `bye` / `exit` / `quit` … |

---

## 🧠 Architecture — the IPO model

```
   INPUT                 PROCESS                  OUTPUT
┌───────────┐        ┌───────────────┐        ┌──────────────┐
│ raw text  │  ───▶  │ sanitize      │  ───▶  │ matched reply│
│ from user │        │ + match intent│        │ or fallback  │
└───────────┘        └───────────────┘        └──────────────┘
 .lower().strip()      dictionary lookup        printed to user
```

### Why a dictionary instead of a long `if-elif` ladder?

| Approach | Lookup cost | Maintenance |
|---|---|---|
| `if-elif` ladder | **O(n)** — slower with every new rule | high technical debt, "unstable" |
| dictionary / hash map | **O(1)** — constant time regardless of size | clean, scalable |

A hash map gives near-instant lookups no matter how many rules exist, which is
why this project uses a dictionary as its knowledge base. The same key→value
idea later evolves into *semantic vector matching* in more advanced projects.

---

## 📂 Project structure

```
.
├── chatbot.py                 # the bot (run this)
├── rule_based_chatbot.ipynb   # Kaggle / Jupyter notebook version
└── README.md
```

No external libraries — pure Python standard library.

---

## ▶️ How to run

### Locally

```bash
python chatbot.py
```

Then type messages. Say `bye`, `exit`, or `quit` to leave.

### On Kaggle

1. Create a new Notebook and upload `rule_based_chatbot.ipynb`.
2. **Run All** — the demo cell replays a scripted conversation, so it works
   even in a committed run (where there's no keyboard for `input()`).
3. To chat live, open the notebook in the editor and uncomment `run_chat()`.

> ℹ️ **Note on Kaggle & `input()`** — committed/batch runs have no stdin, so
> the script auto-detects this and falls back to a scripted demo conversation.
> This keeps the notebook reproducible.

---

## 🔍 The intents

| Intent | Example triggers |
|---|---|
| greeting | hello, hi, hey, good morning |
| how_are_you | how are you, what's up |
| identity | who are you, your name |
| creator | who built you, decodelabs |
| capabilities | help, what can you do |
| time | time, date, today |
| thanks | thanks, thank you |
| weather | weather, rain, temperature |

Plus a global **exit** handler and a **fallback** for anything unrecognised.

---

## 🚀 Ideas for going further

Suggested in the brief's conclusion, easy to add to this skeleton:

- Expand the vocabulary with more intents and synonyms.
- Add nested conditions for context-aware, multi-turn replies.
- Give the bot a stronger personality.
- Eventually wrap it as a **guardrail layer** in front of an LLM — rules
  answer the known stuff instantly; anything unmatched is passed to a
  generative model (the *hybrid architecture*).

---

##  Internship roadmap

| Week | Project | Status |
|---|---|---|
| **1** | **Rule-Based AI Chatbot** | ✅ **Done (this repo)** |
| 2 | _to be assigned_ | 🔒 |
| 3 | _to be assigned_ | 🔒 |
| 4 | _to be assigned_ | 🔒 |

---

## 👤 Author

**\<Your Name\>** — AI Intern @ DecodeLabs (Batch 2026)

*Built as the Week-1 milestone of the DecodeLabs AI Industrial Training Kit.*
