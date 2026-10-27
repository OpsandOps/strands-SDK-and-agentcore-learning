"""
Simple Agent with Strands SDK
Using Grok AI via LiteLLM
"""

from strands import Agent, tool
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("🚀 Initializing agent...")
print(f"📦 Model: {os.getenv('MODEL_NAME', 'not set')}")

# Configure to use LiteLLM (not AWS Bedrock)
os.environ["STRANDS_PROVIDER"] = "litellm"


# ============================================================================
# Define Tools
# ============================================================================

@tool
def answer_question(question: str) -> str:
    """Answer common customer questions about passwords, hours, shipping, returns"""
    knowledge = {
        "password": "To reset your password: Go to Settings → Security → Reset Password",
        "hours": "We're open Monday-Friday, 9AM-5PM EST",
        "shipping": "Standard shipping takes 3-5 business days",
        "return": "Returns accepted within 30 days with receipt",
    }
    
    question_lower = question.lower()
    for key, answer in knowledge.items():
        if key in question_lower:
            return answer
    
    return "I don't have specific information about that."


@tool
def create_support_ticket(description: str) -> str:
    """Create a support ticket for issues that need human help"""
    ticket_id = f"TICKET-{hash(description) % 10000}"
    return f"✅ Created ticket {ticket_id}. Our team will respond within 24 hours."


# ============================================================================
# Create Agent
# ============================================================================

MODEL_NAME = os.getenv("MODEL_NAME", "grok/openai/gpt-oss-120b")

agent = Agent(
    model=MODEL_NAME,
    system_prompt="""
    You are a helpful customer support assistant.
    
    You can:
    - Answer questions using the answer_question tool
    - Create tickets using the create_support_ticket tool
    
    Be friendly, concise, and helpful. Always use tools when appropriate.
    """,
    tools=[answer_question, create_support_ticket]
)

print("✅ Agent ready!")


# ============================================================================
# Handler Function
# ============================================================================

def handler(event, context=None):
    """
    Main entry point - called when someone messages your agent
    """
    user_message = event.get("prompt", "")
    user_id = event.get("user_id", "anonymous")
    
    if not user_message:
        return {
            "statusCode": 400,
            "response": "Error: No message provided"
        }
    
    print(f"\n💬 User ({user_id}): {user_message}")
    
    try:
        # Call the agent - Strands SDK uses simple function call
        response = agent(user_message)
        
        print(f"🤖 Agent: {response}")
        
        return {
            "statusCode": 200,
            "response": response,
            "user_id": user_id
        }
    
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        print(f"❌ {error_msg}")
        
        return {
            "statusCode": 500,
            "response": "Sorry, I encountered an error. Please try again.",
            "error": error_msg
        }


# ============================================================================
# Local Testing
# ============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🧪 Testing Agent Locally")
    print("=" * 60)
    
    test_messages = [
        "Hello! What can you help me with?",
        "I forgot my password",
        "What are your business hours?",
        "I need help with a complex issue"
    ]
    
    for i, msg in enumerate(test_messages, 1):
        print(f"\n--- Test {i}/{len(test_messages)} ---")
        result = handler({"prompt": msg, "user_id": "test_user"})
        
        if result["statusCode"] == 200:
            print(f"✅ Success")
        else:
            print(f"❌ Failed: {result.get('error', 'Unknown error')}")
    
    print("\n" + "=" * 60)
    print("✅ Testing complete!")
    print("=" * 60)
