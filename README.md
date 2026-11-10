# 🤖 AI Chatbot

A beginner-friendly command-line chatbot written in Python. It answers with simple keyword matching out of the box, and can optionally use the OpenAI API for smarter replies.

## ✨ Features

- **Rule-based replies** — works offline, no account or API key needed
- **Keyword matching** — understands greetings, "how are you", help, time, date, jokes, and more
- **Friendly fallback** — politely handles messages it doesn't understand
- **Optional AI mode** — set one environment variable to switch to OpenAI-powered replies
- **Graceful fallback** — if the AI request fails, it automatically returns to rule-based answers
- **Clean exit** — type `bye`, `quit`, or `exit` (or press `Ctrl+C`)
- **Standard library only** — no packages to install

## 📋 Requirements

- Python 3.8 or newer (no external packages required)

## 🚀 Installation

```bash
git clone https://github.com/<your-username>/ai-chatbot.git
cd ai-chatbot
```

That's it — there are no dependencies to install. (Replace `<your-username>` with your GitHub username.)

## 💬 Usage

Run the chatbot:

```bash
python chatbot.py
```

### Sample conversation

```
Hello! I'm PyBot, your chatbot.
Rule-based mode is ON. (Set OPENAI_API_KEY to enable AI replies.)
Type 'help' to see what I can do, or 'bye' to quit.
--------------------------------------------------
You: hello
PyBot: Hello! I'm PyBot, your friendly Python chatbot. Type 'help' to see what I can do.
You: help
PyBot: Here's what I can do:
  - Say hello, ask how I am, or ask my name
  - Ask for the time ('what time is it?') or the date ('what is the date?')
  - Ask for a joke ('tell me a joke')
  - Just chat — I'll do my best to keep up!
Type 'bye', 'quit' or 'exit' to end the conversation.
You: what time is it?
PyBot: The time is 08:15 PM right now.
You: tell me a joke
PyBot: Why do programmers prefer dark mode? Because light attracts bugs!
You: what is the meaning of life?
PyBot: Hmm, I'm not sure how to answer that yet. Try asking me for the time, the date, or a joke — or type 'help' to see everything I can do.
You: bye
PyBot: Goodbye! It was nice chatting with you.
```

## 🧠 How it works

The rule-based engine is deliberately simple so beginners can read and extend it:

1. The user's message is converted to lowercase and stripped of extra spaces.
2. `get_rule_reply()` checks the message against keyword groups **in order** — greetings, "how are you", name, help, time, date, jokes, thanks. The first group that matches wins.
3. If no keyword group matches, a friendly fallback reply is returned instead of an error.
4. `chat()` runs the loop: read input → check for `bye`/`quit`/`exit` → get a reply → print it.

To teach the bot something new, add another `if` block in `get_rule_reply()` — for example, a block that checks for `"weather"` and returns a weather reply.

## 🔌 Optional AI integration (OpenAI)

The chatbot can use the OpenAI chat API for real AI replies. This is **optional** — the rule-based mode works fine without it, and no paid API is required to run the basic demo.

### Step 1 — Create an OpenAI account

Sign up at [platform.openai.com](https://platform.openai.com) and add a payment method if you plan to use the paid API.

### Step 2 — Create an API key

In the OpenAI dashboard, go to **API keys** and create a new key. Copy it once — you won't be able to see it again.

### Step 3 — Set the key as an environment variable

**Linux / macOS:**

```bash
export OPENAI_API_KEY="paste-your-key-here"
```

**Windows (PowerShell):**

```powershell
$env:OPENAI_API_KEY="paste-your-key-here"
```

To make it permanent, add the line to your shell profile (`~/.bashrc`, `~/.zshrc`) or set it in your operating system's environment settings.

### Step 4 — Run the chatbot again

```bash
python chatbot.py
```

You'll see `AI mode is ON (using the OpenAI API)`. Your messages are now sent to the model, and if the API call ever fails, the chatbot automatically falls back to its rule-based replies.

> ⚠️ **NEVER paste an API key into the code, and NEVER commit a key to GitHub.** Keys belong in environment variables only. This project reads the key with `os.environ.get("OPENAI_API_KEY")` — it is never written in any file. If a key ever leaks, delete it from the OpenAI dashboard immediately and create a new one.

## 📁 Project structure

```
ai-chatbot/
├── chatbot.py        # The chatbot: rule engine + optional AI + chat loop
├── README.md         # This file
├── requirements.txt  # No external dependencies (standard library only)
└── .gitignore        # Keeps cache files, virtualenvs and secrets out of git
```

## 📄 License

MIT License — free to use, modify, and share. See the `LICENSE` file if included, or use the standard MIT text.
