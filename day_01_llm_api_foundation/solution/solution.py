"""
Day 1 — LLM API Foundation
AICB-P1: AI Practical Competency Program, Phase 1

Instructions:
    1. Fill in every section marked with TODO.
    2. Do NOT change function signatures.
    3. Copy this file to solution/solution.py when done.
    4. Run: pytest tests/ -v
"""

import os
import time
from typing import Any, Callable
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ---------------------------------------------------------------------------
# Estimated costs per 1K OUTPUT tokens (USD) — update if pricing changes
# ---------------------------------------------------------------------------
COST_PER_1K_OUTPUT_TOKENS = {
    "gpt-4o": 0.010,
    "gpt-4o-mini": 0.0006,
}

OPENAI_MODEL = "gpt-4o"
OPENAI_MINI_MODEL = "gpt-4o-mini"


# ---------------------------------------------------------------------------
# Task 1 — Call GPT-4o
# ---------------------------------------------------------------------------
def call_openai(
    prompt: str,
    model: str = OPENAI_MODEL,
    temperature: float = 0.7,
    top_p: float = 0.9,
    max_tokens: int = 256,
) -> tuple[str, float]:
    """
    Call the OpenAI Chat Completions API and return the response text + latency.

    Args:
        prompt:      The user message to send.
        model:       The OpenAI model to use (default: gpt-4o).
        temperature: Sampling temperature (0.0 – 2.0).
        top_p:       Nucleus sampling threshold.
        max_tokens:  Maximum number of tokens to generate.

    Returns:
        A tuple of (response_text: str, latency_seconds: float).
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    start_time = time.time()
    
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens
    )
    
    latency = time.time() - start_time
    response_text = response.choices[0].message.content
    
    return response_text, latency


# ---------------------------------------------------------------------------
# Task 2 — Call GPT-4o-mini
# ---------------------------------------------------------------------------
def call_openai_mini(
    prompt: str,
    temperature: float = 0.7,
    top_p: float = 0.9,
    max_tokens: int = 256,
) -> tuple[str, float]:
    """
    Call the OpenAI Chat Completions API using gpt-4o-mini and return the
    response text + latency.
    """
    return call_openai(
        prompt=prompt,
        model=OPENAI_MINI_MODEL,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens
    )


# ---------------------------------------------------------------------------
# Task 3 — Compare GPT-4o vs GPT-4o-mini
# ---------------------------------------------------------------------------
def compare_models(prompt: str) -> dict:
    """
    Call both gpt-4o and gpt-4o-mini with the same prompt and return a
    comparison dictionary.

    Args:
        prompt: The user message to send to both models.

    Returns:
        A dict with keys as requested in requirement.
    """
    res_main, lat_main = call_openai(prompt)
    res_mini, lat_mini = call_openai_mini(prompt)
    
    def estimate_cost(text, model_name):
        # 1 token ≈ 0.75 words, so tokens = len(split) / 0.75
        tokens = len(text.split()) / 0.75
        cost = (tokens / 1000) * COST_PER_1K_OUTPUT_TOKENS[model_name]
        return cost

    result = {
        "gpt4o_response": res_main,
        "mini_response": res_mini,
        "gpt4o_latency": lat_main,
        "mini_latency": lat_mini,
        "gpt4o_cost_estimate": estimate_cost(res_main, OPENAI_MODEL)
    }
    return result


# ---------------------------------------------------------------------------
# Task 4 — Streaming chatbot with conversation history
# ---------------------------------------------------------------------------
def streaming_chatbot() -> None:
    """
    Run an interactive streaming chatbot in the terminal.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    history = []

    print("Chatbot started. Type 'quit' or 'exit' to end.")

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["quit", "exit"]:
            break
        
        history.append({"role": "user", "content": user_input})
        
        # Use last 3 messages (OpenAI messages list includes user and assistant)
        # Requirement says "maintains the last 3 conversation turns in history"
        # Often "3 turns" means 6 messages, but hint says `history[-3:]`
        # We will follow the hint: history = history[-3:]
        
        stream = client.chat.completions.create(
            model=OPENAI_MINI_MODEL,
            messages=history[-3:],
            stream=True
        )
        
        print("Assistant: ", end="", flush=True)
        assistant_reply = ""
        for chunk in stream:
            delta = chunk.choices[0].delta.content or ""
            print(delta, end="", flush=True)
            assistant_reply += delta
            
        history.append({"role": "assistant", "content": assistant_reply})
        # Explicitly trim history as requested by hint
        history = history[-3:]


# ---------------------------------------------------------------------------
# Bonus Task A — Retry with exponential backoff
# ---------------------------------------------------------------------------
def retry_with_backoff(
    fn: Callable,
    max_retries: int = 3,
    base_delay: float = 0.5,
) -> Any:
    """
    Call fn(). If it raises an exception, retry up to max_retries times
    with exponential backoff (base_delay * 2^attempt).
    """
    for attempt in range(max_retries + 1):
        try:
            return fn()
        except Exception as e:
            if attempt == max_retries:
                raise e
            wait_time = base_delay * (2 ** attempt)
            print(f"Error: {e}. Retrying in {wait_time:.2f}s...")
            time.sleep(wait_time)


# ---------------------------------------------------------------------------
# Bonus Task B — Batch compare
# ---------------------------------------------------------------------------
def batch_compare(prompts: list[str]) -> list[dict]:
    """
    Run compare_models on each prompt in the list.
    """
    results = []
    for p in prompts:
        res = compare_models(p)
        res["prompt"] = p
        results.append(res)
    return results


# ---------------------------------------------------------------------------
# Bonus Task C — Format comparison table
# ---------------------------------------------------------------------------
def format_comparison_table(results: list[dict]) -> str:
    """
    Format a list of compare_models results as a readable text table.
    """
    header = f"{'Prompt':<40} | {'GPT-4o Response':<20} | {'Mini Response':<20} | {'Lat 4o':<8} | {'Lat Mini':<8}"
    sep = "-" * len(header)
    lines = [header, sep]
    
    for r in results:
        p = (r["prompt"][:37] + "...") if len(r["prompt"]) > 40 else r["prompt"]
        o_r = (r["gpt4o_response"][:17] + "...") if len(r["gpt4o_response"]) > 20 else r["gpt4o_response"]
        m_r = (r["mini_response"][:17] + "...") if len(r["mini_response"]) > 20 else r["mini_response"]
        
        line = f"{p:<40} | {o_r:<20} | {m_r:<20} | {r['gpt4o_latency']:<8.2f} | {r['mini_latency']:<8.2f}"
        lines.append(line)
        
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Entry point for manual testing
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    test_prompt = "Explain the difference between temperature and top_p in one sentence."
    print("=== Comparing models ===")
    try:
        result = compare_models(test_prompt)
        for key, value in result.items():
            print(f"{key}: {value}")
    except Exception as e:
        print(f"Error: {e}")

    print("\n=== Starting chatbot (type 'quit' to exit) ===")
    try:
        streaming_chatbot()
    except Exception as e:
        print(f"Chatbot error: {e}")

    # prompt = "Hãy kể cho tôi một sự thật thú vị về Việt Nam."
    # for temp in [0.0, 0.5, 1.0, 1.5]:
    #     text, latency = call_openai(prompt, temperature=temp)
    #     print(f"--- Temperature {temp} ---")
    #     print(text)

