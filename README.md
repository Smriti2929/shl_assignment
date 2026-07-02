# SHL Assessment Recommendation Agent

## Overview

This project implements a Retrieval-Augmented Generation (RAG) based conversational agent for recommending SHL assessments. The agent uses semantic search over the SHL Product Catalog and Gemini to generate grounded responses while ensuring that all recommendations come directly from the official catalog.

The service exposes a stateless FastAPI API with the required endpoints:

* **GET** `/health`
* **POST** `/chat`

---

## Features

* Semantic retrieval using FAISS and Sentence Transformers
* Conversation-aware Retrieval-Augmented Generation (RAG)
* Clarifies vague hiring requests before recommending assessments
* Recommends 1–10 SHL assessments with official catalog URLs
* Supports refinement when users modify hiring requirements
* Supports comparison of SHL assessments using retrieved catalog data
* Refuses off-topic requests and prompt injection attempts
* Stateless API design

---

## Tech Stack

* Python 3.12
* FastAPI
* Uvicorn
* Sentence Transformers (`all-MiniLM-L6-v2`)
* FAISS
* Google Gemini (`google-genai`)
* NumPy
* Pydantic

---

## Project Structure

```text
app/
    agent.py
    prompts.py
    retriever.py

data/
    documents.json
    metadata.json
    shl_product_catalog.json
    embeddings.npy
    faiss.index

scripts/
    build_documents.py
    build_index.py
    catalog_analysis.py

evaluation/

main.py
requirements.txt
README.md
```

---

## Installation

Create and activate a virtual environment.

Install the required packages:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```text
GEMINI_API_KEY=YOUR_API_KEY
```

---

## Running the Application

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

## API Endpoints

### Health Check

**GET**

```
/health
```

Response

```json
{
  "status": "ok"
}
```

---

### Chat

**POST**

```
/chat
```

Example request:

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Hiring a mid-level Java developer."
    }
  ]
}
```

Example response:

```json
{
  "reply": "Here are the most relevant SHL assessments...",
  "recommendations": [
    {
      "name": "Java 8 (New)",
      "url": "https://www.shl.com/...",
      "test_type": "K"
    }
  ],
  "end_of_conversation": false
}
```

---

## Retrieval Pipeline

1. SHL catalog is converted into structured documents.
2. Documents are embedded using Sentence Transformers.
3. Embeddings are indexed with FAISS.
4. User conversation is converted into a semantic search query.
5. Top matching assessments are retrieved.
6. Gemini generates grounded responses using only retrieved catalog information.

---

## Supported Behaviors

* Clarification for incomplete hiring requests
* SHL assessment recommendation
* Recommendation refinement
* Assessment comparison
* Off-topic request refusal

---

## Notes

* Recommendations always originate from the scraped SHL catalog.
* Assessment URLs are never hallucinated.
* The API is completely stateless; every `/chat` request includes the full conversation history.
