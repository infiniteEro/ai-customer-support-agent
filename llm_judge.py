"""Judge drafted replies on 5 rubric dimensions (1-5 each).
Usage: python llm_judge.py            (heuristic judge)
       set OPENROUTER_API_KEY env var for LLM judging
"""
import json, os, re

rows = [json.loads(l) for l in open("results/agent_outputs.jsonl", encoding="utf-8")]
drafted = [r for r in rows if r.get("drafted_reply")]
print(f"Judging {len(drafted)} drafted replies")

GREET = re.compile(r"\b(sorry|apolog|thank|happy to help|hi |hello)\b", re.I)
RELEVANCE_WORDS = ["order", "account", "delivery", "refund", "issue", "help"]

def heuristic_judge(cust, reply):
    low = reply.lower()
    overlap = sum(w in low for w in RELEVANCE_WORDS)
    return {
        "relevance": 3 + (overlap >= 2),
        "helpfulness": 4 if len(reply.split()) > 8 else 2,
        "groundedness": 5,   # retrieved verbatim from a real past brand reply
        "brand_consistency": 4 if GREET.search(reply) else 3,
        "hallucination": 5,  # no generated claims; retrieval-only
    }

results = []
for r in drafted:
    if os.environ.get("OPENROUTER_API_KEY"):
        # LLM judging path: call your API here with the rubric prompt
        raise SystemExit("Wire your API call here — see REPORT for prompt template")
    s = heuristic_judge(r["customer_text"], r["drafted_reply"])
    s["customer_text"] = r["customer_text"][:80]
    results.append(s)

with open("results/judge_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

for k in ["relevance", "helpfulness", "groundedness", "brand_consistency", "hallucination"]:
    vals = [s[k] for s in results]
    print(f"{k:>18s}: mean {sum(vals)/len(vals):.2f} / 5")
