"""Compare human scores with judge scores. Usage: python human_agreement.py"""
import json
from scipy.stats import spearmanr

judge = json.load(open("results/judge_results.json"))
human = json.load(open("results/human_agreement_scores.json"))  # your 1-5 overall scores
hmap = {h["customer_text"]: h["overall"] for h in human}

pairs = [(hmap[s["customer_text"]], s["helpfulness"]) for s in judge
         if s["customer_text"] in hmap]
h, j = zip(*pairs)
rho, p = spearmanr(h, j)
agree = sum(1 for a, b in pairs if abs(a - b) <= 1) / len(pairs)
print(f"n={len(pairs)}  Spearman rho={rho:.2f} (p={p:.3f})  within-1-point agreement={agree:.0%}")
