# 🔎 RAG — Retrieval-Augmented Generation

**RAG** stands for **Retrieval-Augmented Generation**.

It combines two major capabilities:

* **Retrieval** → Find relevant information from a knowledge base.
* **Generation** → Use an LLM to generate an answer using the retrieved information.

A simple way to think about RAG is:

> **Retrieve relevant context → Augment the prompt → Generate an answer**

---

# 🏗️ RAG Architecture

```text
                    PROPRIETARY DATA
                           │
                           ▼
                ┌─────────────────────┐
                │   Embedding Model   │
                │                     │
                │ Convert data into   │
                │ vector embeddings   │
                └──────────┬──────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ Vector Database │
                  │                 │
                  │ Optimized for   │
                  │ search/retrieval│
                  └────────┬────────┘
                           │
                           │
USER QUESTION              │
      │                    │
      ▼                    │
┌───────────────┐          │
│   Embedding   │          │
│     Model     │          │
│               │          │
│ Convert query│          │
│ into vector   │          │
└───────┬───────┘          │
        │                  │
        └─────── Search ───┘
                  │
                  ▼
        ┌─────────────────────┐
        │ Top-K Relevant      │
        │ Information         │
        └──────────┬──────────┘
                   │
                   ▼
        ┌────────────────────────────┐
        │          PROMPT            │
        │                            │
        │ Original Question          │
        │            +               │
        │ Retrieved Context          │
        └─────────────┬──────────────┘
                      │
                      ▼
                    ┌─────┐
                    │ LLM │
                    └──┬──┘
                       │
                       ▼
                    ANSWER
```

---

# 🔄 RAG Flow

### Step 1 — Prepare Proprietary Data

Your organization's private data could include:

* PDFs
* Documentation
* Policies
* Database records
* Knowledge bases
* Internal documents

The data is processed and converted into **vector embeddings**.

```text
Proprietary Data
       ↓
Embedding Model
       ↓
Vector Representation
       ↓
Vector Database
```

---

### Step 2 — Store Embeddings

The generated embeddings are stored in a **Vector Database**.

The vector database is optimized for **similarity search and retrieval**.

Examples include:

* Pinecone
* Chroma
* FAISS
* Weaviate
* Milvus

---

### Step 3 — Convert User Question

When a user asks a question, the question is also converted into a vector using the embedding model.

```text
User Question
      ↓
Embedding Model
      ↓
Query Vector
```

---

### Step 4 — Retrieve Relevant Context

The query vector is used to search the vector database.

The system retrieves the **Top-K most relevant pieces of information**.

```text
Query Vector
     ↓
Vector Database
     ↓
Similarity Search
     ↓
Top-K Relevant Context
```

---

### Step 5 — Augment the Prompt

The original question is combined with the retrieved context.

```text
┌──────────────────────────────┐
│          PROMPT              │
│                              │
│ Original Question            │
│            +                 │
│ Retrieved Context            │
└──────────────────────────────┘
```

This augmented prompt is sent to the LLM.

---

### Step 6 — Generate the Answer

The LLM uses the retrieved context to generate the final response.

```text
Question + Retrieved Context
             ↓
            LLM
             ↓
          Answer
```

---

# 🧠 RAG in One Line

```text
Query → Embedding Model → Vector DB → Retrieved Context → LLM → Response
```

---

# 📊 Important RAG Evaluation Metrics

When testing a RAG application, we need to evaluate both the **retrieval quality** and the **generated answer**.

## 1. Contextual Precision

**Contextual Precision** measures the quality of the RAG pipeline's **retriever**.

It evaluates whether relevant nodes in the `retrieval_context` are ranked higher than irrelevant nodes.

### In simple terms:

> **Did we put the most useful information near the top of the retrieved results?**

```text
Query
  ↓
Retrieved Results

1. Relevant     ✅
2. Relevant     ✅
3. Irrelevant   ❌
4. Relevant     ✅

Higher precision → Better ranking
```

---

## 2. Contextual Recall

**Contextual Recall** measures how well the retrieved context aligns with the information required to produce the expected answer.

### In simple terms:

> **Did we retrieve enough of the information needed to answer the question correctly?**

```text
Expected Answer
       │
       ▼
Required Information
       │
       ▼
Retrieved Context
       │
       ▼
How much relevant information was retrieved?
```

High recall means the retriever successfully found the information necessary for answering the question.

---

## 3. Contextual Relevance

**Contextual Relevance** evaluates whether the retrieved context is relevant to the user's question.

### In simple terms:

> **Did we retrieve useful information instead of irrelevant information?**

Example:

```text
Question:
"What is the company's vacation policy?"

Retrieved Context:

Vacation Policy       ✅ Relevant
Benefits Policy       ⚠️ Partially relevant
Office Parking        ❌ Irrelevant
```

The goal is to maximize useful context while minimizing irrelevant content.

---

# 4. Answer Relevancy

**Answer Relevancy** evaluates whether the generated answer actually addresses the user's question.

### In simple terms:

> **Did the LLM answer the question that was asked?**

Example:

```text
Question:
"What is the vacation allowance?"

Answer:
"Employees receive 20 vacation days per year."

                ↓

Answer Relevancy = High ✅
```

An answer can be factually correct but still have poor relevancy if it doesn't directly address the user's question.

---

# 5. Faithfulness

**Faithfulness** evaluates whether the generated answer is supported by the retrieved context.

### In simple terms:

> **Did the LLM generate the answer from the retrieved information, or did it hallucinate information?**

```text
Retrieved Context:
"Employees receive 20 vacation days."

LLM Answer:
"Employees receive 20 vacation days."

              ↓

Faithfulness = High ✅
```

But:

```text
Retrieved Context:
"Employees receive 20 vacation days."

LLM Answer:
"Employees receive 30 vacation days."

              ↓

Faithfulness = Low ❌
```

This metric is especially important for detecting **RAG hallucinations**.

---

# 🎯 RAG Metrics Overview

| Metric                   | What Does It Measure?                        | Focus     |
| ------------------------ | -------------------------------------------- | --------- |
| **Contextual Precision** | Are relevant results ranked higher?          | Retriever |
| **Contextual Recall**    | Did we retrieve enough required information? | Retriever |
| **Contextual Relevance** | Is the retrieved context relevant?           | Retriever |
| **Answer Relevancy**     | Does the answer address the question?        | Generator |
| **Faithfulness**         | Is the answer supported by context?          | Generator |

---

# 🧪 Testing RAG with DeepEval

DeepEval can be used to evaluate different parts of a RAG pipeline.

```text
                     RAG APPLICATION
                           │
             ┌─────────────┴─────────────┐
             │                           │
         Retrieval                   Generation
             │                           │
             ▼                           ▼
   Contextual Precision          Answer Relevancy
   Contextual Recall             Faithfulness
   Contextual Relevance
```

This allows us to identify **where the RAG system is failing**.

For example:

```text
Contextual Precision  → 0.90 ✅
Contextual Recall     → 0.85 ✅
Contextual Relevance  → 0.92 ✅
Answer Relevancy      → 0.88 ✅
Faithfulness          → 0.45 ❌
```

In this example, the retriever appears to be working well, but the **LLM is not consistently grounding its answers in the retrieved context**.

---

# 🔑 Key Takeaways

* **RAG = Retrieval + Augmentation + Generation**
* Proprietary data is converted into vector embeddings.
* Embeddings are stored in a vector database.
* User questions are also converted into vectors.
* Similarity search retrieves the **Top-K relevant context**.
* The original question and retrieved context are combined into a prompt.
* The LLM generates the final answer.
* RAG testing should evaluate both **retrieval** and **generation**.
* **Contextual Precision, Contextual Recall, and Contextual Relevance** primarily evaluate retrieval.
* **Answer Relevancy and Faithfulness** evaluate the generated answer.
* DeepEval can automate these evaluations as part of an AI testing pipeline.

---

## 🚀 RAG Model — Quick Reference

```text
                    USER QUERY
                         │
                         ▼
                ┌────────────────┐
                │ Embedding Model│
                └───────┬────────┘
                        │
                        ▼
                 ┌──────────────┐
                 │ Vector DB    │
                 └──────┬───────┘
                        │
                        ▼
              Retrieved Context
                        │
                        ▼
                ┌──────────────┐
                │     LLM      │
                └──────┬───────┘
                       │
                       ▼
                    RESPONSE
```
