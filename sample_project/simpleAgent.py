"""
Quickest way to pass a single message to an agent
Choose your approach and modify the message below!
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ============================================================================
# YOUR MESSAGE HERE 👇
# ============================================================================

MY_MESSAGE = "Ask a question to the Agent today!"

# ============================================================================
# OPTION 1: Strands (Recommended - easier)
# ============================================================================

def send_with_strands(message: str):
    from strands import Agent
    from strands.models.litellm import LiteLLMModel
    
    model = LiteLLMModel(
        client_args={"api_key": os.getenv("GROQ_API_KEY")},
        model_id=os.getenv("MODEL_NAME", "groq/openai/gpt-oss-120b"),
        params = {"temperature" :0.3,
        "reasoning_effort": "low",
        "max_tokens": 1000
        }

    )
    
    agent = Agent(model=model, system_prompt="You are helpful.")
    
    # Just call agent with your message!
    return agent(message)


# ============================================================================
# OPTION 2: LiteLLM Direct (More control)
# ============================================================================

def send_with_litellm(message: str):
    from litellm import completion
    
    response = completion(
        model=os.getenv("MODEL_NAME", "groq/openai/gpt-oss-120b"),
        api_key=os.getenv("GROQ_API_KEY"),
        messages=[
            {"role": "system", "content": "You are helpful."},
            {"role": "user", "content": message}
        ]
    )
    
    return response.choices[0].message.content


# ============================================================================
# Run It!
# ============================================================================

if __name__ == "__main__":
    print(f"\n📨 Sending: {MY_MESSAGE}\n")
    
    # Choose which one to use:
    
    # Option 1:
    result = send_with_strands(input("Enter a message here: "))
    
    # Option 2 (uncomment to use):
    # result = send_with_litellm(MY_MESSAGE)
    
    print(f"🤖 Response: {result}\n")
