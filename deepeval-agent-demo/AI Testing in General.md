# 🤖 AI Testing with DeepEval

> A concise guide to understanding how AI systems are evaluated using **DeepEval**.

---

# Why AI Testing is Different

Traditional software testing relies on **deterministic assertions**.

**Example**

| Traditional Application | AI Application |
|------------------------|----------------|
| `Order is shipped` ✅ | `Your order is on the way` ✅ |
| Exact string matching | Meaning is what matters |

LLMs are **non-deterministic**, meaning multiple different responses can all be correct. Instead of checking exact text, we evaluate the **quality** of the response.

---

# What Do We Evaluate?

AI testing focuses on semantic judgment rather than string matching.

## 1. Semantic Correctness

> Did the agent provide the correct information?

- Checks meaning, not wording
- Multiple valid phrasings should pass

**Example**

- ✅ "Order is shipped"
- ✅ "Your package is on the way"

---

## 2. Tool Behaviour

> Did the agent choose and use the correct tool?

Evaluate:

- Correct tool selection
- Correct parameters
- Appropriate tool sequence

---

## 3. Relevance

> Was the response relevant to the user's question?

The answer should remain focused on the user's intent without unnecessary or unrelated information.

---

## 4. Safety & Guardrails

> Is the output safe, unbiased, and privacy-aware?

Typical checks include:

- Toxicity
- Bias
- Privacy leakage
- Harmful instructions

---

# What Are Evals?

**Evals** are a structured and repeatable process for measuring the quality of AI systems.

Instead of asserting:

```python
assert response == "Order is shipped"
```

We evaluate:

- Relevancy
- Faithfulness
- Correctness
- Safety
- Tool usage

---

# DeepEval

> **DeepEval** is an open-source Python framework for evaluating LLM applications.

It provides reusable metrics, test cases, tracing, and seamless integration with `pytest`.

---

# Five Core Capabilities

## 1. Metrics

Pre-built evaluation criteria for measuring AI quality.

| Metric | Purpose |
|---------|----------|
| Answer Relevancy | Is the answer relevant? |
| Faithfulness | Is it grounded in context? |
| Tool Correctness | Was the correct tool used? |
| Task Completion | Did the agent complete the objective? |
| GEval | Create custom evaluation criteria |

### Score Range

All metrics return a score between:

```text
0.0  ─────────────────────────────── 1.0
 Poor                               Excellent
```

### Recommended Thresholds

| Category | Threshold | Examples |
|----------|-----------|----------|
| Quality | **0.7** | Relevancy, Faithfulness, GEval |
| Safety | **0.5** | Bias, Toxicity |
| Efficiency | **0.5** | Step Efficiency, Agent Path |

> Thresholds are **design decisions**, not fixed rules.

---

## 2. Test Cases (Goldens)

Goldens are structured containers that store everything needed for evaluation.

```python
Input
Expected Context
Expected Output
Actual Output
```

They create repeatable and version-controlled AI tests.

---

## 3. Judge LLM

DeepEval uses an LLM as a **judge** to score another LLM's output.

**Responsibilities**

- Semantic reasoning
- Quality scoring
- Explanation of failures
- Consistent evaluation

---

## 4. Tracing & Instrumentation

Automatically captures what happens inside an AI agent.

Supported integrations include:

- LangChain
- OpenAI
- Other LLM frameworks

Captured data:

- Tool calls
- Intermediate reasoning
- Retrieved documents
- Agent execution flow

---

## 5. Test Runner

Run evaluations exactly like unit tests.

### Pytest Integration

```bash
pytest tests/
```

### Standalone Evaluation

```python
evaluate(test_cases, metrics)
```

This makes AI regression testing easy to integrate into CI/CD pipelines.

---

# DeepEval Architecture

```text
                User Prompt
                     │
                     ▼
              AI Agent / LLM
                     │
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
   Tool Calls   Retrieved Docs  Final Answer
        │            │            │
        └────────────┼────────────┘
                     ▼
            DeepEval Tracing
                     ▼
               Test Case (Golden)
                     ▼
                  Metrics
                     ▼
              Judge LLM Scores
                     ▼
          Pass / Fail + Score Report
```

---

# Traditional Testing vs AI Testing

| Traditional QA | AI QA |
|---------------|-------|
| Exact assertions | Semantic evaluation |
| Deterministic | Non-deterministic |
| Expected string | Quality metrics |
| Boolean pass/fail | Scored evaluation (0–1) |
| Functional correctness | Correctness + Safety + Relevance |

---

# Key Takeaways

- AI responses are **non-deterministic**.
- We evaluate **meaning**, not exact wording.
- **Evals** provide a repeatable quality measurement process.
- **DeepEval** offers metrics, goldens, tracing, judge LLMs, and pytest integration.
- Success is measured through **quality scores**, not simple string assertions.