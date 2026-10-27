
import hashlib
import os
 
from dotenv import load_dotenv
from strands import Agent, tool
from strands.models.litellm import LiteLLMModel
from typing import Dict
 
load_dotenv()
 
# LiteLLM routes on the "groq/" prefix; the rest is Groq's own model ID.
# llama-3.1-70b-versatile and llama-3.3-70b-versatile have both been retired
# on Groq, so default to a current model and confirm against Groq's model list.
MODEL_NAME = os.getenv("MODEL_NAME", "groq/openai/gpt-oss-120b")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
 
print("🚀 Initializing agent...")
print(f"📦 Model: {MODEL_NAME}")
print(f"🔑 API Key loaded: {'Yes' if GROQ_API_KEY else 'No'}")
 
if not GROQ_API_KEY:
    raise SystemExit("❌ ERROR: GROQ_API_KEY not found in .env file!")
 
 
# ============================================================================
# Tools: the @tool decorator builds the schema from the type hints and
# docstring, so there is no hand-written JSON tool definition or manual loop.
# ============================================================================
 
KNOWLEDGE = {
    "password": "To reset your password: Go to Settings → Security → Reset Password",
    "hours": "We're open Monday-Friday, 9AM-5PM EST",
    "shipping": "Standard shipping takes 3-5 business days",
    "return": "Returns accepted within 30 days with receipt",
}
 
 
@tool
def answer_question(question: str) -> str:
    """Answer common customer questions about passwords, hours, shipping and returns.
 
    Args:
        question: The customer's question.
    """
    question_lower = question.lower()
    for key, answer in KNOWLEDGE.items():
        if key in question_lower:
            return answer
    return "I don't have specific information about that."
 
 
@tool
def create_support_ticket(description: str) -> str:
    """Create a support ticket for issues that need human help.
 
    Args:
        description: Description of the issue.
    """
    # hashlib instead of hash(): the built-in is randomized per process,
    # so the same description would get a different ID on every run.
    digest = hashlib.sha256(description.encode()).hexdigest()
    ticket_id = f"TICKET-{int(digest, 16) % 10000:04d}"
    return f"✅ Created ticket {ticket_id}. Our team will respond within 24 hours."
 
 
SYSTEM_PROMPT = """
You are a helpful customer support assistant.
 
You can:
- Answer questions using the answer_question tool
- Create tickets using the create_support_ticket tool
 
Be friendly, concise, and helpful. Always use tools when appropriate.
"""
 
# The model object is stateless, so build it once and share it.
model = LiteLLMModel(
    client_args={"api_key": GROQ_API_KEY},
    model_id=MODEL_NAME,
    params={
        "max_tokens": 500,
        "temperature": 0.3,
        # gpt-oss models accept "low", "medium" or "high"
        "reasoning_effort": os.getenv("REASONING_EFFORT", "low"),
    },
    
)
 
print("✅ Agent ready!")
 
 
# ============================================================================
# Agent logic
# ============================================================================
 
def call_agent(user_message: str) -> str:
    """Run one request through a fresh agent and return the final text."""
    # A new Agent per request keeps conversation history from leaking between
    # users. Reuse a single Agent instead if you want multi-turn memory.
    # callback_handler=None silences Strands' default streaming print-out so
    # the output below stays under our own logging.
    agent = Agent(
        model=model,
        tools=[answer_question, create_support_ticket],
        system_prompt=SYSTEM_PROMPT,
        callback_handler=None
        
    )
    result = agent(user_message)
    return str(result)
 

if __name__ == '__main__':
    print("f\n 😀 sending message to agent..,")

    user = input(f"enter your message here: ")
    print(call_agent(user))

    print(f"\n Agent action done ...")