# SHL Assessment Recommendation Agent – Approach

## Overview

The objective was to build a conversational recommendation agent capable of recommending appropriate SHL assessments through a stateless FastAPI API.

The solution combines semantic retrieval with a Large Language Model to produce grounded recommendations using only the SHL catalog.

---

# System Design

The architecture consists of four major components:

1. FastAPI API
2. Retrieval Engine
3. Prompt Engineering
4. Gemini Reasoning

The API remains completely stateless. Every request includes the full conversation history, allowing recommendations and refinements without storing server-side session data.

---

# Retrieval Setup

The SHL catalog was converted into structured metadata containing:

- Assessment name
- URL
- Categories
- Duration
- Languages
- Job levels

Each assessment was embedded using the SentenceTransformer model:

```
all-MiniLM-L6-v2
```

Embeddings were indexed using FAISS for fast semantic similarity search.

For every recommendation request:

1. The current conversation is converted into a retrieval query.
2. FAISS retrieves the most relevant assessments.
3. Retrieved assessments are formatted into structured context.
4. Gemini generates grounded recommendations using only retrieved information.

---

# Prompt Design

The prompt is divided into modular sections.

These include:

- System Prompt
- Clarification Guidelines
- Recommendation Guidelines
- Comparison Guidelines
- Refinement Guidelines
- Refusal Guidelines

This modular structure keeps prompts maintainable while allowing different conversational behaviors.

---

# Conversational Behaviour

The agent supports:

- Clarifying vague hiring requests
- Recommending assessments after sufficient context
- Refining recommendations when constraints change
- Comparing assessments using retrieved catalog information
- Refusing off-topic requests

---

# Evaluation Strategy

The system was evaluated manually using representative recruiter conversations covering:

- vague hiring requests
- technical hiring roles
- refinement requests
- assessment comparison
- off-topic questions

Recommendations were verified against retrieved catalog entries to ensure URLs and assessment names were grounded in the catalog.

---

# Challenges

Several retrieval strategies were tested.

Initially, retrieval relied only on the latest user message, which performed poorly during refinement.

This was improved by constructing retrieval queries from the entire conversation history, resulting in better contextual recommendations.

Prompt instructions were also iteratively refined to reduce hallucinations and ensure recommendations remained grounded in retrieved catalog data.

---

# AI Tools Used

AI-assisted coding tools were used for:

- debugging
- code refactoring
- prompt refinement
- deployment troubleshooting

All architecture, retrieval pipeline, and implementation decisions were manually designed and integrated.