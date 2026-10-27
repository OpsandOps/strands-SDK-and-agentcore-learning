# Simple AWS AgentCore Tutorial - Using Strands SDK

**Goal:** Build your first AI agent in 30 minutes, step by step.

No production complexity. Just the basics to get you started.

---

## What We're Building

A simple chatbot that can:
- Answer questions
- Remember what you said
- Use tools when needed

**Framework:** Strands SDK (AWS's native agent framework)

---

## Prerequisites

You need 3 things:

1. **Python 3.10 or newer**
   ```bash
   python --version
   ```

2. **AWS Account** (free tier is fine)
   
3. **AWS CLI configured**
   ```bash
   aws configure
   # Enter your AWS credentials when prompted
   ```

That's it!

---

## Step 1: Install AgentCore CLI (5 minutes)

Open your terminal and run:

```bash
# Install the AgentCore CLI
npm install -g @aws/agentcore-cli

# Verify it worked
agentcore --version
```

You should see version 0.4.0 or higher.

---

## Step 2: Create Your First Agent (2 minutes)

```bash
# Create a new agent project
agentcore init my-first-agent

# When prompted, choose:
# Language: Python
# Framework: Strands Agents  ← Pick this!
# Template: Basic
```

This creates a new folder called `my-first-agent` with everything you need.

```bash
cd my-first-agent
```

---

## Step 3: Look at What Was Created (3 minutes)

You'll see these files:

```
my-first-agent/
├── agent.py           # Your agent code (we'll edit this)
├── agentcore.yaml     # Configuration
├── requirements.txt   # Python packages
└── .env.example      # Settings template
```

Let's understand what each does:

**agent.py** = Your agent's brain (the code)  
**agentcore.yaml** = Settings (which model, how much memory, etc.)  
**requirements.txt** = Python packages needed  
**.env.example** = Local settings template

---

## Step 4: Install Python Packages (2 minutes)

```bash
# Create a virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

Your terminal should now show `(venv)` at the beginning.

---

## Step 5: Understand the Basic Agent Code (5 minutes)

Open `agent.py`. Here's a simplified version of what's inside:

```python
from strands import Agent, tool

# Create an agent
agent = Agent(
    name="My First Agent",
    model="anthropic.claude-3-5-sonnet-20241022-v2:0",
    system_prompt="You are a helpful assistant."
)

# Handle incoming messages
def handle_message(user_input):
    # Call agent like a function
    response = agent(user_input)
    return response
```

That's the basic structure! Strands makes it simple.

---

## Step 6: Write Your First Agent (10 minutes)

Let's replace the default code with something simple. Open `agent.py` and replace everything with this:

```python
"""
My First Agent - A simple chatbot using Strands SDK
"""

from strands import Agent, tool
import os

# Define a simple tool
@tool
def get_weather(location: str) -> str:
    """Get current weather for any location"""
    # In a real app, you'd call a weather API here
    return f"The weather in {location} is sunny and 72°F"

# Create the agent
agent = Agent(
    name="My First Agent",
    model="anthropic.claude-3-5-sonnet-20241022-v2:0",
    system_prompt="""
    You are a helpful assistant.
    You can answer questions and check the weather using the get_weather tool.
    Be friendly and concise.
    """,
    tools=[get_weather]
)

# Main handler function (AgentCore calls this)
def handler(event, context):
    """
    This function is called when someone sends a message to your agent
    """
    # Get the user's message
    user_message = event.get("prompt", "")
    user_id = event.get("user_id", "anonymous")
    
    # Run the agent (Strands SDK - call like a function)
    response = agent(user_message)
    
    # Return the response
    return {
        "statusCode": 200,
        "response": response
    }

# For local testing
if __name__ == "__main__":
    # Test messages
    test_messages = [
        "Hello!",
        "What's the weather like in Seattle?",
        "Tell me a joke"
    ]
    
    for msg in test_messages:
        print(f"\nUser: {msg}")
        result = handler({"prompt": msg, "user_id": "test_user"}, {})
        print(f"Agent: {result['response']}")
```

**What this code does:**
1. Imports Agent and tool decorator from Strands
2. Creates a weather tool using @tool decorator
3. Creates an agent with model and system_prompt
4. Handles messages from users
5. Returns responses

---

## Step 7: Configure Your Agent (3 minutes)

Open `agentcore.yaml` and make sure it looks like this:

```yaml
name: my-first-agent
version: "1.0.0"

runtime:
  timeout: 300      # 5 minutes max
  memory: 1024      # 1 GB memory
  python_version: "3.12"

harness:
  model: anthropic.claude-3-5-sonnet-20241022-v2:0
  system_prompt: "You are a helpful assistant."
  temperature: 0.7

memory:
  short_term: true   # Remember conversation
  long_term: false   # Don't need long-term memory yet

gateway:
  tools: []          # No external tools yet

observability:
  tracing: enabled
  log_level: INFO
```

**What these settings mean:**
- `timeout: 300` = Agent can run for 5 minutes max
- `memory: 1024` = Uses 1GB of memory
- `model: anthropic.claude-3-5-sonnet...` = Uses Claude AI
- `short_term: true` = Remembers your conversation
- `tracing: enabled` = You can see logs

---

## Step 8: Test Locally (3 minutes)

Run your agent on your computer:

```bash
python agent.py
```

You should see output like:

```
User: Hello!
Agent: Hello! How can I help you today?

User: What's the weather like in Seattle?
Agent: Let me check the weather for you... The weather in Seattle is sunny and 72°F

User: Tell me a joke
Agent: Why did the programmer quit his job? Because he didn't get arrays! 😄
```

**It works!** 🎉

---

## Step 9: Deploy to AWS (5 minutes)

Now let's put your agent on AWS so anyone can use it.

### First, enable Bedrock model access (one-time setup):

1. Go to: https://console.aws.amazon.com/bedrock/
2. Click "Model access" on the left
3. Click "Request model access"
4. Check "Claude 3.5 Sonnet"
5. Click "Request access"

Wait a few seconds for approval.

### Deploy your agent:

```bash
agentcore deploy --region us-east-1
```

This will:
1. Package your code
2. Upload to AWS
3. Create your agent
4. Give you an endpoint URL

Takes about 3-5 minutes. You'll see:

```
✅ Deployment successful!

Agent ARN: arn:aws:bedrock-agentcore:us-east-1:123456789012:agent/my-first-agent
Endpoint: https://abc123.agentcore.us-east-1.amazonaws.com
```

**Save that endpoint URL!**

---

## Step 10: Test Your Live Agent (2 minutes)

Test your agent running on AWS:

```bash
agentcore invoke --payload '{
  "prompt": "Hello! What can you do?",
  "user_id": "test_user_1"
}'
```

You should get a response from your agent running on AWS!

Try more messages:

```bash
agentcore invoke --payload '{
  "prompt": "Whats the weather in Paris?",
  "user_id": "test_user_1"
}'
```

---

## Step 11: View Logs (2 minutes)

See what your agent is doing:

```bash
agentcore logs --follow
```

This shows you live logs. Press Ctrl+C to stop.

---

## Congratulations! 🎉

You just:
1. ✅ Created an AI agent
2. ✅ Tested it locally
3. ✅ Deployed it to AWS
4. ✅ Tested it in production

---

## What's Next?

Now that you have the basics working, you can:

### 1. Add a Real Tool

Replace the fake weather tool with a real API:

```python
import requests

def get_weather(location: str) -> str:
    """Get real weather from an API"""
    # Sign up for a free API key at weatherapi.com
    api_key = "your-api-key"
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={location}"
    
    response = requests.get(url)
    data = response.json()
    
    temp = data['current']['temp_f']
    condition = data['current']['condition']['text']
    
    return f"The weather in {location} is {condition} and {temp}°F"
```

### 2. Add Memory

Make your agent remember things across conversations:

```python
from strands import Agent

# Create agent with memory
agent = Agent(
    name="My First Agent",
    model="anthropic.claude-3-5-sonnet-20241022-v2:0",
    system_prompt="You are a helpful assistant.",
    # Memory is configured in agentcore.yaml
)

# Use the agent - just call it!
response = agent("Hello!")
```

### 3. Add More Tools

Create tools for:
- Searching documentation
- Looking up data
- Sending emails
- Creating calendar events
- Anything you need!

```python
@tool
def search_docs(query: str) -> str:
    """Search our documentation"""
    # Your search logic here
    return "Search results..."

@tool
def send_email(to: str, subject: str, body: str) -> str:
    """Send an email"""
    # Your email logic here
    return f"Email sent to {to}"

# Add to agent
agent = Agent(
    name="My Agent",
    model="anthropic.claude-3-5-sonnet-20241022-v2:0",
    system_prompt="You are a helpful assistant.",
    tools=[get_weather, search_docs, send_email]
)
```

### 4. Make Changes and Redeploy

After making changes:

```bash
# Test locally first
python agent.py

# If it works, deploy
agentcore deploy --region us-east-1
```

---

## Common Issues & Fixes

### "ImportError: No module named 'strands'"

**Fix:**
```bash
# Make sure your virtual environment is activated
# You should see (venv) in your terminal
pip install -r requirements.txt
```

### "AccessDeniedException" when deploying

**Fix:**
```bash
# Make sure you requested Bedrock model access
# Go to: https://console.aws.amazon.com/bedrock/
# Click "Model access" and request Claude access
```

### "Agent not responding"

**Fix:**
```bash
# Check the logs
agentcore logs --since 10m

# Look for error messages
```

### "My changes aren't showing up"

**Fix:**
```bash
# Redeploy after making changes
agentcore deploy --region us-east-1
```

---

## Quick Reference

### Test Locally
```bash
python agent.py
```

### Deploy to AWS
```bash
agentcore deploy --region us-east-1
```

### Test on AWS
```bash
agentcore invoke --payload '{"prompt": "Hello", "user_id": "test"}'
```

### View Logs
```bash
agentcore logs --follow
```

### Check Status
```bash
agentcore status
```

### Update Agent
```bash
# Make your changes, then:
agentcore deploy --region us-east-1
```

---

## You Did It! 🎉

You now understand:
- How to create an agent with Strands SDK
- How to add tools
- How to test locally
- How to deploy to AWS
- How to view logs

**This is all you need to get started!**

The production complexity in the other guides is for later when you need:
- Multiple regions
- Auto-scaling
- Advanced monitoring
- CI/CD pipelines
- etc.

But for now, you have a working agent. Build on this foundation!

---

## Need Help?

If you get stuck:
1. Check the "Common Issues & Fixes" section above
2. Run `agentcore logs` to see what's happening
3. Make sure your AWS credentials are configured: `aws sts get-caller-identity`

---

**Happy building! Start simple, then add complexity as you need it. 🚀**
