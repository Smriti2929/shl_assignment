# SHL Assessment Recommendation Agent

An AI-powered conversational recommendation agent for SHL Individual Test Solutions.

The agent helps recruiters identify appropriate SHL assessments based on hiring requirements through a stateless conversational API built with FastAPI.

---

## Live API

Base URL:

https://shl-assignment-10.onrender.com

### Endpoints

GET /health

https://shl-assignment-10.onrender.com/health

POST /chat

https://shl-assignment-10.onrender.com/chat

Interactive API Docs:

https://shl-assignment-10.onrender.com/docs

## Features

- Conversational recommendation agent
- Retrieval-Augmented Generation (RAG)
- Semantic search using FAISS
- Gemini-powered reasoning
- Clarification for vague hiring requests
- Assessment recommendation (1–10 tests)
- Recommendation refinement
- Assessment comparison
- Off-topic request handling
- Stateless API design

---

## API Endpoints

### Health Check

GET `/health`

Response

```json
{
  "status": "ok"
}
```

---

### Chat

POST `/chat`

Request

```json
{
  "messages": [
    {
      "role": "user",
      "content": "I need assessments for a Java developer."
    }
  ]
}
```

Response

```json
{
  "reply": "...",
  "recommendations": [],
  "end_of_conversation": false
}
```

---

## Tech Stack

- FastAPI
- FAISS
- Sentence Transformers (all-MiniLM-L6-v2)
- Google Gemini 2.5 Flash
- Python

---

## Project Structure

```
app/
│
├── agent.py
├── retriever.py
├── prompts.py
│
data/
├── metadata.json
├── faiss.index
│
main.py
requirements.txt
```

---

## Retrieval Pipeline

1. User query
2. Semantic embedding
3. FAISS retrieval
4. Prompt construction
5. Gemini response generation

---

## Deployment

Deployed using Render.

```
GET  /health
POST /chat
```

---