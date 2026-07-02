from app.retriever import Retriever

from google import genai
import os

from dotenv import load_dotenv

from app.prompts import (
    SYSTEM_PROMPT,
    CLARIFICATION_GUIDELINES,
    RECOMMENDATION_GUIDELINES,
    COMPARISON_GUIDELINES,
    REFINEMENT_GUIDELINES,
    REFUSAL_GUIDELINES,
)

load_dotenv()


class SHLAgent:

    def __init__(self):

        # Lazy loaded to reduce Render startup memory
        self.retriever = None

        self.client = genai.Client(
            api_key=os.getenv("GEMINI_API_KEY")
        )

    def get_retriever(self):
        """
        Lazily loads Retriever only when retrieval
        is actually required.
        """

        if self.retriever is None:
            self.retriever = Retriever()

        return self.retriever

    def get_latest_user_message(self, conversation):
        """
        Returns the latest user message.
        """

        for message in reversed(conversation):

            if message["role"] == "user":
                return message["content"]

        return ""

    def build_search_query(self, conversation):
        """
        Build a retrieval query using the
        entire conversation history.
        """

        query_parts = []

        for message in conversation:

            if message["role"] == "user":
                query_parts.append(message["content"])

        return " ".join(query_parts)

    def needs_clarification(self, message):
        """
        Decide whether enough hiring context exists.
        """

        message = message.lower()

        role_keywords = [
            "developer",
            "engineer",
            "analyst",
            "manager",
            "graduate",
            "intern",
            "sales",
            "customer service",
            "call center",
            "finance",
            "accountant",
            "marketing",
            "executive",
            "technician",
            "consultant",
            "operator",
        ]

        has_role = any(
            keyword in message
            for keyword in role_keywords
        )

        return not has_role

    def ask_clarification(self):
        """
        Ask for missing hiring context.
        """

        return (
            "Could you please tell me the job role or position "
            "you are hiring for?"
        )

    def is_off_topic(self, message):
        """
        Detect requests outside SHL scope.
        """

        message = message.lower()

        hiring_keywords = [
            "hire",
            "hiring",
            "candidate",
            "assessment",
            "assessment test",
            "test",
            "screen",
            "screening",
            "recruit",
            "recruitment",
            "graduate",
            "developer",
            "engineer",
            "analyst",
            "manager",
            "sales",
            "customer service",
            "finance",
            "java",
            "python",
            "leadership",
            "personality",
        ]

        return not any(
            keyword in message
            for keyword in hiring_keywords
        )

    def off_topic_response(self):
        """
        Refuse unrelated requests.
        """

        return (
            "I'm designed to help recommend SHL assessments "
            "for hiring and talent evaluation. "
            "Please ask a recruitment or assessment-related question."
        )

    def is_comparison(self, message):
        """
        Detect comparison requests.
        """

        message = message.lower()

        comparison_keywords = [
            "compare",
            "difference",
            "vs",
            "versus",
            "better than",
        ]

        return any(
            keyword in message
            for keyword in comparison_keywords
        )

    def generate_llm_response(self, prompt):
        """
        Call Gemini.
        """

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        return response.text
    
    def format_retrieved_documents(self, retrieved_documents):
        """
        Converts retrieved SHL assessments into
        clean text for Gemini.
        """

        formatted_text = ""

        for i, doc in enumerate(retrieved_documents, start=1):

            formatted_text += (
                f"Assessment {i}\n\n"

                f"Name:\n"
                f"{doc['name']}\n\n"

                f"Categories:\n"
                f"{', '.join(doc['categories'])}\n\n"

                f"Duration:\n"
                f"{doc['duration']}\n\n"

                f"Languages:\n"
                f"{', '.join(doc['languages'])}\n\n"

                f"URL:\n"
                f"{doc['url']}\n\n"

                + "-" * 60
                + "\n\n"
            )

        return formatted_text

    def build_prompt(
        self,
        conversation,
        retrieved_context,
    ):
        """
        Builds the recommendation prompt.
        """

        conversation_text = ""

        for message in conversation:

            role = message["role"].capitalize()

            conversation_text += (
                f"{role}: {message['content']}\n"
            )

        prompt = f"""
{SYSTEM_PROMPT}

--------------------------------------------------

Conversation

{conversation_text}

--------------------------------------------------

Relevant SHL Assessments

{retrieved_context}

--------------------------------------------------

Instructions

{RECOMMENDATION_GUIDELINES}

{REFINEMENT_GUIDELINES}

Use ONLY the retrieved assessments.

Never invent assessment names.

Never invent URLs.

Recommend only assessments relevant to the hiring requirement.

If insufficient information exists,
ask a clarification question.
"""

        return prompt

    def comparison_prompt(
        self,
        conversation,
        retrieved_context,
    ):
        """
        Builds a comparison prompt.
        """

        conversation_text = ""

        for message in conversation:

            conversation_text += (
                f"{message['role'].capitalize()}: "
                f"{message['content']}\n"
            )

        prompt = f"""
{SYSTEM_PROMPT}

{COMPARISON_GUIDELINES}

Conversation

{conversation_text}

--------------------------------------------------

Relevant SHL Assessments

{retrieved_context}

--------------------------------------------------

Compare ONLY using the retrieved assessment information.

Do not invent capabilities,
features,
or differences.

If information is unavailable,
say so explicitly.
"""

        return prompt
    
    def run(self, conversation):
        """
        Main orchestration workflow.
        """

        # Latest user message
        latest_message = self.get_latest_user_message(
            conversation
        )

        # Off-topic handling
        if self.is_off_topic(latest_message):
            return self.off_topic_response()

        # Clarification handling
        if self.needs_clarification(latest_message):
            return self.ask_clarification()

        # Build retrieval query
        search_query = self.build_search_query(
            conversation
        )

        # Lazy-loaded retrieval
        retrieved_documents = self.get_retriever().retrieve(
            search_query,
            top_k=5
        )

        # Format retrieved assessments
        retrieved_context = self.format_retrieved_documents(
            retrieved_documents
        )

        # Build appropriate prompt
        if self.is_comparison(latest_message):

            prompt = self.comparison_prompt(
                conversation,
                retrieved_context
            )

        else:

            prompt = self.build_prompt(
                conversation,
                retrieved_context
            )

        # Generate final answer
        response = self.generate_llm_response(
            prompt
        )

        return response


if __name__ == "__main__":

    agent = SHLAgent()

    conversation = [
        {
            "role": "user",
            "content": "Hiring a mid-level Java developer with stakeholder interaction."
        }
    ]

    print("\n==============================")
    print("Agent Response")
    print("==============================\n")

    print(
        agent.run(conversation)
    )