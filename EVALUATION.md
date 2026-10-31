# Evaluation

This document describes how FastAPI RAG was evaluated: 

## Setup

- Corpus: FastAPI documentation, 972 chunks
- Embeddings: `BAAI/bge-small-en-v1.5`, stored in ChromaDB
- Retrieval: top-8 chunks per question
- LLM: Gemini (`gemini-flash-lite-latest`, `gemini-flash-latest`)
- "Not found" threshold: top-1 distance > 0.4

## 1. Retrieval quality

15 questions, each with an expected source page. A hit means the expected page is among the top-k chunks.

| top-k | hit-rate |
|-------|----------|
| 3     | 80%      |
| 5     | 87%      |
| 8     | 93%      |

I use k=8.

## 2. Choosing the threshold

Top-1 distance (lower = closer) from `queries.log` on the 20 test questions:

| Question type | Count | Top-1 distance |
|---------------|-------|----------------|
| Normal questions | 6 | 0.17 – 0.22 |
| Russian questions | 2 | 0.33 – 0.37 |
| Trap questions (related topic, no answer in docs) | 5 | 0.18 – 0.35 |
| Off-topic questions | 3 | 0.45 – 0.54 |

The used threshold  is 0.4.

Trap questions cannot be separated by distance: for example "how to deploy FastAPI to AWS Lambda" has distance 0.18, lower than some normal questions. For these cases the system relies on the prompt, which tells the model to answer "I could not find this in the documentation."

## 3. End-to-end results on 20 questions

| Group | Result |
|-------|--------|
| Normal (6) | Correct pages in `sources_used` for all 6 |
| Traps (5) | Model answered "not found" and `sources_used` is empty: 5 / 5 |
| Off-topic (3) | Stopped by the threshold, no LLM call: 3 / 3 |
| Russian (2) | Answered in Russian, correct pages found: 2 / 2 |
| Empty question | Handled before retrieval, no LLM call |
| Two-part question | Both relevant pages used |
| Custom value in request metadata | Failed: the question uses different words than the docs |

Answers were checked manually.

## 4. Latency

- Off-topic and empty questions: about 0.0 s (no LLM call)
- Questions answered by the LLM: usually 1.5 – 5.7 s
- If Gemini was overloaded, the same questions took 12 – 17 s

## 5. Automated tests

`test_api.py` contains 5 tests for the `/query` endpoint (normal question, trap, off-topic, empty question, missing field) all pass. 

## 6. Known limitations

- The search can find the wrong page if my words are different from the docs. Example: "request metadata" (my words) vs "header parameters" (the docs' words). The system answered about the wrong page.
- The distance threshold cannot detect trap questions; the system depends on the model following the prompt.
- The model sometimes leaves excerpt numbers like `[3]` inside the answer text.
- 29 chunks are longer than 512 tokens (long code blocks); I kept them whole so code is not cut in the middle.
- The test set is small (20 questions) and answers were judged manually.