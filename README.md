# AI Agent Testing with DeepEval

A comprehensive Python-based framework for automated evaluation of AI agents using **DeepEval**, featuring tool-calling agents, RAG systems, and multi-turn chatbots with advanced metrics for hallucination detection, answer relevancy, faithfulness, and LLM regression testing.

## 🎯 Overview

This project demonstrates production-grade evaluation patterns for:

- **Phase 1**: Tool-calling support agents with task completion and tool correctness metrics
- **Phase 2**: RAG-powered customer support agents with retrieval and contextual evaluation
- **Phase 3**: Multi-turn chatbots with conversational and knowledge retention metrics
- **Safety**: Bias, toxicity, and PII leakage detection

Perfect for teams building reliable AI systems that need comprehensive evaluation frameworks.

## 📋 Prerequisites

- Python 3.10+
- OpenAI API key (GPT-4o for agent LLM and judge LLM)

## 🚀 Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Set up environment

Create a `.env` file in the project root (already gitignored):

```env
OPENAI_API_KEY=sk-...               # agent LLM + judge LLM (GPT-4o)
CONFIDENT_API_KEY=confident_us_...  # optional: stream traces to Confident AI dashboard
```

### 3. Run your first eval

```bash
# Sanity check Phase 1 agent
python agent_instrumented.py

# Run Phase 1 evals
python test_agent.py
```

## 📁 Project Structure

### Phase 1: Tool-Calling Support Agent

Core agent with two tools: `get_order_status` and `get_refund_policy`.

| File | Purpose |
|---|---|
| `agent_plain.py` | Baseline agent implementation (no eval code) |
| `agent_instrumented.py` | Agent with 4-line DeepEval instrumentation |
| `test_agent.py` | `TaskCompletionMetric` + `ToolCorrectnessMetric` evals |
| `test_agent_extended.py` | `AnswerRelevancyMetric`, `PromptAlignmentMetric`, `StepEfficiencyMetric` |
| `test_agent_correctness.py` | `GEval` correctness evaluation against expected output |

**Run Phase 1:**
```bash
python agent_instrumented.py          # sanity-check
python test_agent.py                  # TaskCompletion + ToolCorrectness
python test_agent_extended.py         # AnswerRelevancy + PromptAlignment + StepEfficiency
python test_agent_correctness.py      # GEval Correctness
```

### Phase 2: RAG-Powered Agent

Customer-support agent with semantic search over a 9-document knowledge base.

| File | Purpose |
|---|---|
| `rag_agent.py` | RAG agent with `search_policies` tool backed by vector store |
| `test_rag_agent.py` | `AnswerRelevancyMetric`, `FaithfulnessMetric`, `ContextualPrecisionMetric`, `ContextualRecallMetric` |

**Run Phase 2:**
```bash
python rag_agent.py                   # sanity-check
python test_rag_agent.py              # RAG-specific evals
```

### Phase 3: Multi-Turn Chatbot

Interactive customer-support chatbot with conversational evaluation.

| File | Purpose |
|---|---|
| `chatbot.py` | Multi-turn chatbot with OpenAI function-calling API |
| `test_chatbot.py` | Conversational metrics: `KnowledgeRetentionMetric`, `RoleAdherenceMetric`, `TurnRelevancyMetric`, `ConversationalGEval` |

**Run Phase 3:**
```bash
python chatbot.py                     # interactive chatbot (type 'quit' to exit)
python test_chatbot.py                # conversational evals
```

### Safety Evaluations

Edge case detection using bias, toxicity, and PII metrics.

| File | Purpose |
|---|---|
| `test_safety.py` | `BiasMetric`, `ToxicityMetric`, `PIILeakageMetric` on edge cases |

**Run Safety Evals:**
```bash
python test_safety.py
```

## 🏗️ Architecture

### Agent Instrumentation Pattern

All agents follow the same instrumentation approach:

```python
from deepeval.tracing import observe, update_current_trace
from deepeval.tracing.callback import CallbackHandler

@observe(name="agent_name")
def agent_wrapper(input_text, golden):
    # Set up DeepEval callback
    deepeval_callback = CallbackHandler()
    
    # Run LangChain agent with callback
    response = agent.invoke(
        {"input": input_text},
        config={"callbacks": [deepeval_callback]}
    )
    
    # Update trace with golden metadata
    update_current_trace(
        output=response,
        expected_output=golden.expected_output,
        expected_tools=golden.expected_tools,
        retrieval_context=golden.retrieval_context
    )
    
    return response
```

**Key Components:**
- **`CallbackHandler()`** — Captures LangChain LLM/tool spans automatically
- **`@observe(name="...")`** — Creates top-level trace
- **`update_current_trace(...)`** — Copies golden metadata to trace for metrics to read
- **Confident AI integration** — Optional cloud tracing via `CONFIDENT_API_KEY` in `.env`

### Conversational Evaluation Pattern (Phase 3)

Uses `ConversationalTestCase` + `Turn` objects instead of `Golden`:

```python
from deepeval.test_case import ConversationalTestCase, Turn

# Create test case
turns = [
    Turn(role="user", content="..."),
    Turn(role="assistant", content="...", tools_called=["tool_name"])
]
test_case = ConversationalTestCase(turns=turns)

# Run chatbot live
run_conversation(test_case)

# Evaluate
evaluate(test_case, metrics=[...])
```

## 📊 Metric Reference

| Metric | Needs `expected_output`? | Needs `retrieval_context`? | LLM Judge? | Phase |
|---|---|---|---|---|
| `TaskCompletionMetric` | No | No | Yes | 1 |
| `ToolCorrectnessMetric` | No | No | No | 1 |
| `AnswerRelevancyMetric` | No | No | Yes | 1, 2 |
| `PromptAlignmentMetric` | No | No | Yes | 1 |
| `StepEfficiencyMetric` | No | No | Yes | 1 |
| `GEval` (Correctness) | **Yes** | No | Yes | 1 |
| `FaithfulnessMetric` | No | **Yes** | Yes | 2 |
| `ContextualPrecisionMetric` | **Yes** | **Yes** | Yes | 2 |
| `ContextualRecallMetric` | **Yes** | **Yes** | Yes | 2 |
| `KnowledgeRetentionMetric` | No | No | Yes | 3 |
| `RoleAdherenceMetric` | No | No | Yes | 3 |
| `TurnRelevancyMetric` | No | No | Yes | 3 |
| `ConversationalGEval` | No | No | Yes | 3 |
| `BiasMetric` | No | No | Yes | Safety |
| `ToxicityMetric` | No | No | Yes | Safety |
| `PIILeakageMetric` | No | No | Yes | Safety |

## 🔍 Key Features

### ✅ Comprehensive Metrics
- **Semantic Evaluation**: Answer relevancy, faithfulness, and contextual precision/recall
- **Tool Correctness**: Validates agent tool selection and parameters
- **Task Completion**: GPT-4o judge evaluates goal fulfillment
- **Safety**: Detects bias, toxicity, and PII leakage
- **Conversational**: Knowledge retention, role adherence, turn relevancy

### 🔗 RAG Evaluation
- Retrieval context tracking
- Contextual precision/recall for semantic search
- Faithfulness checking against retrieved documents

### 💬 Conversational Features
- Multi-turn chat management
- Tool call history tracking
- Live evaluation without pre-computed goldens

### ☁️ Cloud Integration
- **Confident AI**: Optional cloud tracing via environment variable
- Zero code changes needed — DeepEval reads `CONFIDENT_API_KEY` automatically

## 📝 Example: Running Phase 1 Evals

```bash
# 1. Start with a sanity check
$ python agent_instrumented.py
Agent response: I've retrieved the order status for you...

# 2. Run core metrics (tool + task completion)
$ python test_agent.py
Metric: TaskCompletionMetric
✓ PASSED: Agent successfully completed the task
✓ PASSED: Correct tool selected (get_order_status)

# 3. Run extended metrics
$ python test_agent_extended.py
✓ AnswerRelevancyMetric: 0.92
✓ PromptAlignmentMetric: 0.88
✓ StepEfficiencyMetric: 0.85

# 4. Run correctness eval
$ python test_agent_correctness.py
✓ GEval Correctness: 0.95
```

## 🐛 Known Issues & Patches

### DeepEval 4.0.4 `_make_hashable` Bug
`ToolMessage` objects in `tools_called` are unhashable, causing `ToolCorrectnessMetric` to crash. This is patched directly in `.venv/lib/python3.12/site-packages/deepeval/...` (see CLAUDE.md for details).

### `create_react_agent` Deprecation
Migrated from deprecated LangChain API:
```python
# Old (deprecated)
from langchain.agents import create_react_agent
agent = create_react_agent(..., prompt=...)

# New
from langchain.agents import create_agent
agent = create_agent(..., system_prompt=...)
```

Requires: `langchain` base package (added to `requirements.txt`).

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

## 📚 Learn More

- **[DeepEval Documentation](https://docs.confident-ai.com/)** — Comprehensive metric reference
- **[LangChain Docs](https://python.langchain.com/)** — Agent and RAG patterns
- **[OpenAI API Reference](https://platform.openai.com/docs/api-reference)** — GPT-4o models


---

**Built with ❤️ using DeepEval, LangChain, and OpenAI**
