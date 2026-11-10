"""
ai-chatbot — a beginner-friendly command-line chatbot.

This chatbot works in two modes:

1. RULE-BASED (default, no setup needed)
   It answers using simple keyword matching. No internet connection
   and no account are required.

2. AI-POWERED (optional)
   If the environment variable OPENAI_API_KEY is set, the chatbot
   sends your message to the OpenAI chat API and prints the model's
   reply. If the API call fails for any reason, it falls back to the
   rule-based replies.

SECURITY WARNING — NEVER paste an API key into this file (or any
other file in this project), and NEVER commit a key to GitHub.
Always keep keys in environment variables or a local .env file
that is listed in .gitignore. If a key ever leaks, delete it
immediately from your provider's dashboard and create a new one.
"""

import json
import os
import random
import urllib.error
import urllib.request
from datetime import datetime

# ---------------------------------------------------------------------------
# Bot identity and small talk data
# ---------------------------------------------------------------------------

BOT_NAME = "PyBot"

JOKES = [
    "Why do programmers prefer dark mode? Because light attracts bugs!",
    "Why did the Python cross the road? To get to the other side of the code!",
    "There are only 10 types of people in the world: those who understand binary and those who don't.",
    "Why do Java developers wear glasses? Because they don't C#!",
]


def get_rule_reply(message):
    """Return a rule-based reply for *message* using keyword matching.

    The message is lower-cased first, then checked against a list of
    keyword groups in order. The first group that matches wins.
    If nothing matches, a friendly fallback reply is returned.

    Args:
        message (str): The user's raw input text.

    Returns:
        str: The chatbot's reply.
    """
    text = message.lower().strip()

    # Greetings
    if any(word in text for word in ("hello", "hi", "hey", "salam", "aoa")):
        return f"Hello! I'm {BOT_NAME}, your friendly Python chatbot. Type 'help' to see what I can do."

    # How are you?
    if "how are you" in text:
        return "I'm running perfectly, thank you! All my circuits are happy. How are you doing?"

    # Who are you / your name?
    if "your name" in text or "who are you" in text:
        return f"My name is {BOT_NAME}. I'm a small rule-based chatbot written in Python — and I can optionally talk to an AI API too!"

    # Help
    if "help" in text:
        return (
            "Here's what I can do:\n"
            "  - Say hello, ask how I am, or ask my name\n"
            "  - Ask for the time ('what time is it?') or the date ('what is the date?')\n"
            "  - Ask for a joke ('tell me a joke')\n"
            "  - Just chat — I'll do my best to keep up!\n"
            "Type 'bye', 'quit' or 'exit' to end the conversation."
        )

    # Time
    if "time" in text:
        now = datetime.now()
        return f"The time is {now.strftime('%I:%M %p')} right now."

    # Date
    if "date" in text or "today" in text:
        today = datetime.now()
        return f"Today is {today.strftime('%A, %B %d, %Y')}."

    # Jokes
    if "joke" in text:
        return random.choice(JOKES)

    # Thank you
    if "thank" in text:
        return "You're very welcome! Anything else you'd like to chat about?"

    # Fallback for anything we don't understand
    return (
        "Hmm, I'm not sure how to answer that yet. "
        "Try asking me for the time, the date, or a joke — "
        "or type 'help' to see everything I can do."
    )


def get_ai_reply(message):
    """Ask the OpenAI chat API for a reply — ONLY if a key is configured.

    The API key is read from the OPENAI_API_KEY environment variable.
    It is never written in this file and must never be committed to git.

    If no key is set, or if the API call fails for any reason, this
    function returns None so the caller can fall back to the
    rule-based replies.

    Args:
        message (str): The user's message to send to the AI.

    Returns:
        str | None: The AI's reply text, or None if AI mode is off
        or the request failed.
    """
    # Read the key from the environment only — never hardcode it.
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        return None

    payload = json.dumps({
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a friendly, helpful chatbot. Keep replies short and simple."},
            {"role": "user", "content": message},
        ],
        "max_tokens": 150,
    }).encode("utf-8")

    request = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))
        return data["choices"][0]["message"]["content"].strip()
    except (urllib.error.URLError, urllib.error.HTTPError, OSError,
            KeyError, IndexError, ValueError):
        # Any network problem (timeout, connection error, bad key / 401),
        # or unexpected response shape: fall back to rule-based replies.
        return None


def chat():
    """Run the main chat loop.

    Reads user input until the user types bye, quit, or exit.
    In AI mode (OPENAI_API_KEY set) it tries the AI first and falls
    back to rule-based replies; otherwise it uses rule-based replies.
    """
    ai_mode = bool(os.environ.get("OPENAI_API_KEY"))

    print(f"Hello! I'm {BOT_NAME}, your chatbot.")
    if ai_mode:
        print("AI mode is ON (using the OpenAI API). Type 'bye' to quit.")
    else:
        print("Rule-based mode is ON. (Set OPENAI_API_KEY to enable AI replies.)")
        print("Type 'help' to see what I can do, or 'bye' to quit.")
    print("-" * 50)

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print(f"\n{BOT_NAME}: Goodbye! Have a great day!")
            break

        if not user_input:
            continue

        if user_input.lower() in ("bye", "quit", "exit"):
            print(f"{BOT_NAME}: Goodbye! It was nice chatting with you.")
            break

        reply = None
        if ai_mode:
            reply = get_ai_reply(user_input)
            if reply is None:
                print("(AI reply failed — falling back to rule-based answers.)")

        if reply is None:
            reply = get_rule_reply(user_input)

        print(f"{BOT_NAME}: {reply}")


if __name__ == "__main__":
    chat()
