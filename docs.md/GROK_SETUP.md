# Using Grok with AgentCore & Strands SDK

Quick guide to use Grok (or any LiteLLM-supported model) with your agent.

## Step 1: Get Your Grok API Key

1. Go to https://console.x.ai/
2. Sign up or log in
3. Navigate to API Keys
4. Create a new API key
5. Copy it (starts with `xai-...`)

## Step 2: Set Up Environment Variables

```bash
# Copy the example file
cp .env.example .env

# Edit .env file
# On Windows: notepad .env
# On Mac/Linux: nano .env
```

Update these lines in `.env`:

```bash
# Set your model
MODEL_NAME=grok/openai/gpt-oss-120b

# Add your Grok API key
GROK_API_KEY=xai-your-actual-api-key-here
```

## Step 3: Install Dependencies

```bash
# Make sure you have the updated requirements
pip install -r simple-requirements.txt

# This includes:
# - strands-agents (agent framework)
# - litellm (model routing)
# - python-dotenv (environment variables)
```

## Step 4: Test Locally

```bash
python agent.py
```

You should see your agent responding using Grok!

## Step 5: Deploy to AWS

```bash
# Make sure your .env is configured
# Then deploy
agentcore deploy --region us-east-1
```

AgentCore will automatically use your environment variables.

---

## Using Other Models

Want to use a different model? Just change `MODEL_NAME` in `.env`:

### Grok Models
```bash
MODEL_NAME=grok/openai/gpt-oss-120b
GROK_API_KEY=xai-...
```

### OpenAI Models
```bash
MODEL_NAME=openai/gpt-4
OPENAI_API_KEY=sk-...
```

### Anthropic Claude
```bash
MODEL_NAME=anthropic.claude-3-5-sonnet-20241022-v2:0
ANTHROPIC_API_KEY=sk-ant-...
```

### Groq (Fast inference)
```bash
MODEL_NAME=groq/llama3-70b-8192
GROQ_API_KEY=gsk_...
```

### Ollama (Local models)
```bash
MODEL_NAME=ollama/llama2
# No API key needed for local Ollama
```

### Azure OpenAI
```bash
MODEL_NAME=azure/gpt-4
AZURE_API_KEY=...
AZURE_API_BASE=https://your-instance.openai.azure.com
```

---

## How It Works

The Strands SDK automatically uses LiteLLM to route your requests:

```python
# In agent.py
MODEL_NAME = os.getenv("MODEL_NAME", "grok/openai/gpt-oss-120b")

agent = Agent(
    name="My Agent",
    model=MODEL_NAME,  # LiteLLM handles the routing
    system_prompt="...",
    tools=[...]
)
```

LiteLLM looks for the API key based on the model prefix:
- `grok/...` → Uses `GROK_API_KEY`
- `openai/...` → Uses `OPENAI_API_KEY`
- `anthropic...` → Uses `ANTHROPIC_API_KEY`
- `groq/...` → Uses `GROQ_API_KEY`

---


### Want to see what's happening?

Enable LiteLLM logging:
```bash
# In .env
LITELLM_LOG=DEBUG
```

---

## Cost Comparison

| Model | Provider | Cost per 1M tokens | Speed |
|-------|----------|-------------------|-------|
| Grok (gpt-oss-120b) | xAI | ~$5 input, ~$15 output | Fast |
| Claude 3.5 Sonnet | Anthropic | $3 input, $15 output | Medium |
| GPT-4 Turbo | OpenAI | $10 input, $30 output | Medium |
| Groq Llama3-70B | Groq | $0.59 input, $0.79 output | Very Fast |
| Ollama | Local | Free | Depends on hardware |

*Prices approximate as of Oct 2026, check provider websites for current rates*

---

## Advanced: Multiple Models

Use different models for different tasks:

```python
# Fast model for classification
classifier = Agent(
    name="Classifier",
    model="groq/llama3-8b-8192",  # Fast & cheap
    system_prompt="Classify this query as: support, sales, or general"
)

# Powerful model for complex responses
responder = Agent(
    name="Responder",
    model="grok/openai/gpt-oss-120b",  # Smart & detailed
    system_prompt="Provide detailed helpful response"
)

# Use both in your handler
def handler(event, context):
    query = event["prompt"]
    
    # Step 1: Quick classification
    category = classifier.run(query)
    
    # Step 2: Detailed response
    response = responder.run(query)
    
    return {"response": response, "category": category}
```

---

**Ready to use Grok? Update your .env and run `python agent.py`!**
    # Step 1: Quick classification
    category = classifier(query)
    
    # Step 2: Detailed response
    response = responder(query)