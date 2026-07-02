from app.retriever import Retriever

from google import genai
from google.genai import types
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

# Load environment variables
load_dotenv()

class SHLAgent:

    def __init__(self):

        self.retriever = Retriever()

        self.client = genai.Client(
            api_key=os.getenv("GEMINI_API_KEY")    
        )

    def get_latest_user_message(self, conversation):

        """
        Returns the latest user message from the conversation.
        """

        for message in reversed(conversation):

            if message["role"] == "user":

                return message["content"]

        return ""
    
    def build_search_query(self, conversation):
        """
        Builds a retrieval query using recent conversation history.
        This helps refinement requests like:
        - Add personality
        - Remove OPQ
        - Add simulations
        """

        query_parts = []

        for message in conversation:

            if message["role"] == "user":
                query_parts.append(message["content"])

        return " ".join(query_parts)
    
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
            "better than"
        ]

        return any(keyword in message for keyword in comparison_keywords)
    
    def comparison_prompt(
        self,
        conversation,
        retrieved_context
    ):
        """
        Builds a prompt specifically for comparison questions.
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

Relevant SHL Assessments

{retrieved_context}

Compare ONLY using the information in the retrieved assessments.

Do not invent features, capabilities or differences.
If information is missing, explicitly say so.
"""

        return prompt
    
    def needs_clarification(self, message):

        """
        Decide whether enough hiring context exists
        before retrieving assessments.
        """

        message = message.lower()

        # Hiring role keywords
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
            "operator"
        ]

        has_role = any(keyword in message for keyword in role_keywords)

        if not has_role:
            return True

        return False
    
    def ask_clarification(self):

        """
        Returns a clarification question.
        """

        return (
            "Could you please tell me the job role or position "
            "you are hiring for?"
        )
    
    def is_off_topic(self, message):
         """
         Detect whether the user's request is unrelated
         to SHL assessments or hiring.
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
            "personality"

        ]

         for keyword in hiring_keywords:

            if keyword in message:

                return False
         return True
    
    def off_topic_response(self):

        """
        Response for unrelated questions.
        """

        return (
            "I'm designed to help recommend SHL assessments "
            "for hiring and talent evaluation. "
            "Please ask a recruitment or assessment-related question."
        )
    
    def generate_llm_response(self, prompt):

        """
        Sends a prompt to Gemini and returns the response text.
        """

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
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
        Builds the complete prompt
        sent to Gemini.
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

Use ONLY the retrieved assessments.

Never invent assessment names.

Never invent URLs.

Recommend only assessments relevant to the hiring requirement.

If insufficient information exists,
ask a clarification question.
"""

        return prompt
    
    
    def run(self, conversation):

        """
        Main orchestration function.
        """

        # Step 1: Latest user message
        latest_message = self.get_latest_user_message(conversation)

        # Step 2: Refuse off-topic requests
        if self.is_off_topic(latest_message):
            return self.off_topic_response()

        # Step 3: Ask clarification if needed
        if self.needs_clarification(latest_message):
            return self.ask_clarification()

        # Step 4: Build retrieval query from full conversation
        search_query = self.build_search_query(conversation)

        # Step 5: Retrieve assessments
        retrieved_documents = self.retriever.retrieve(
            search_query,
            top_k=5
        )

        # Step 6: Format retrieved assessments
        retrieved_context = self.format_retrieved_documents(
            retrieved_documents
        )

        # Step 7: Build prompt
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

        # Step 8: Generate Gemini response
        response = self.generate_llm_response(prompt)

        # Step 9: Return response
        return response

    

    





    

if __name__ == "__main__":

    agent = SHLAgent()

    conversation = [
        {
            "role": "user",
            "content": "Who won yesterday's cricket match?"
        }
    ]

    response = agent.run(conversation)

    print("\n==============================")
    print("Agent Response")
    print("==============================\n")

    print(response)
    

