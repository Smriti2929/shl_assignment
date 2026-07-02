from typing import List
from fastapi import FastAPI
from pydantic import BaseModel

from app.agent import SHLAgent

app = FastAPI()

agent = None

def get_agent():
    global agent
    if agent is None:
        agent = SHLAgent()
    return agent


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]


class Recommendation(BaseModel):
    name: str
    url: str
    test_type: str


class ChatResponse(BaseModel):
    reply: str
    recommendations: List[Recommendation]
    end_of_conversation: bool


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    agent = get_agent()
    conversation = [
        message.model_dump()
        for message in request.messages
    ]

    reply = agent.run(conversation)

    recommendations = []

    clarification_phrases = [
        "could you",
        "please specify",
        "please provide",
        "what is",
        "which",
        "can you tell me"
    ]
    
    needs_more_info = any(
        phrase in reply.lower()
        for phrase in clarification_phrases
    )
    
    if not needs_more_info:

        search_query = agent.build_search_query(conversation)
        docs = agent.retriever.retrieve(search_query, top_k=5)

        for doc in docs:

            category = "K"

            categories_text = " ".join(doc["categories"]).lower()

            if "personality" in categories_text:
                category = "P"

            recommendations.append(
                Recommendation(
                    name=doc["name"],
                    url=doc["url"],
                    test_type=category
                )
            )

    return ChatResponse(
        reply=reply,
        recommendations=recommendations,
        end_of_conversation=not needs_more_info
    )