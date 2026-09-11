# Amazon AI Customer Support Agent — Evaluation Report

## 1. Problem Framing

This project builds and evaluates an AI customer-support agent for Amazon using the Customer Support on Twitter dataset.

The agent has three main responsibilities:

1. **Intent classification**  
   Classify an incoming customer message into a small set of support intents derived from Amazon's historical customer-support conversations.

2. **Reply drafting**  
   Retrieve historically similar Amazon support interactions and use them as grounding evidence for drafting a response.

3. **Routing decision**  
   Decide whether the issue should be:
   - `AUTO_HANDLE`
   - `ESCALATE`

The goal is not to build a production-ready Amazon support system. The goal is to demonstrate a measurable, reproducible prototype and understand where such an agent succeeds and fails.

---

## 2. Dataset and Brand Selection

The project uses the **Customer Support on Twitter** dataset from Kaggle.

Dataset:

`thoughtvector/customer-support-on-twitter`

Amazon was selected as the target brand.

The Amazon subset contains approximately 113,439 customer-support tweets after filtering and preprocessing.

The dataset contains historical customer messages and responses between customers and support accounts. These conversations provide both intent examples and historical response evidence.

---

## 3. Intent Taxonomy

Instead of using a large predefined intent taxonomy, a small taxonomy was derived from Amazon's own support conversations.

The final intent categories are:

| Intent | Description |
|---|---|
| `delivery_issue` | Late, missing, delayed, or delivery-related problems |
| `damaged_item_or_product_issue` | Damaged, defective, broken, or problematic products |
| `prime_membership_issue` | Amazon Prime membership, subscription, or Prime-related issues |
| `support_process_complaint` | Complaints about customer service, support processes, or previous interactions |
| `other` | Messages that do not confidently fit the four primary intents |

### Taxonomy derivation

Semantic embeddings were generated and clustering was evaluated across different values of `k`.

The selected taxonomy used four primary clusters.

The best observed silhouette score was approximately:

`0.049`

The relatively low silhouette score indicates that customer-support conversations do not naturally form perfectly separated semantic clusters. Human review was therefore required to assign meaningful names to the clusters.

The `other` category was introduced during evaluation to avoid forcing uncertain messages into an unrelated support intent.

---

## 4. System Architecture

The agent follows this pipeline:

```text
Incoming customer message
          |
          v
   Text preprocessing
          |
          v
 Sentence Transformer
 (all-MiniLM-L6-v2)
          |
          v
 Intent similarity
          |
          +--------------------+
          |                    |
          v                    v
 Intent classification     Confidence check
          |                    |
          +---------+----------+
                    |
                    v
          Escalation rules
                    |
          +---------+---------+
          |                   |
          v                   v
      ESCALATE           AUTO_HANDLE
                              |
                              v
                  Historical reply retrieval
                              |
                              v
                       Drafted response
