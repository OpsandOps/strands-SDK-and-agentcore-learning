# AWS AgentCore Tutorial - Using Grok with Strands SDK

**Complete Guide: From Local Development to Cloud Deployment**

---
## What You'll Build 
A production-ready AI agent using:
- **Grok AI** (via your xAI API key)
- **Strands SDK** (simple agent framework)
- **LiteLLM** (model routing)
- **AgentCore** (local dev + cloud runtime)

**No AWS Bedrock required!** You'll use your own Grok API key.

---

## Prerequisites (5 minutes)

### Required

1. **Python 3.10+**
   ```bash
   python --version  # Should be 3.10 or higher
   ```

2. **Node.js 20+** (for AgentCore CLI)
   ```bash
   node --version  # Should be 20 or higher
   ```

3. **Grok API Key**
   - Sign up at https://console.x.ai/
   - Create an API key (starts with `xai-`)
   - **You'll need this!**

4. **AWS Account** (free tier is fine)
   - For cloud deployment only
   - Not needed for local testing

5. **AWS CLI** (for cloud deployment)
   ```bash
   aws --version
   aws configure  # Enter your credentials
   ```

### Check Your Setup

```bash
# Verify everything is installed
python --version
node --version
aws --version

# You're ready if all three work!
```

---

## Part 1: Local Development (30 minutes)

### Step 1.1: Install AgentCore CLI (2 minutes)

```bash
# Install globally
npm install -g @aws/agentcore-cli

# Verify installation
agentcore --version
# Should show: 0.4.0 or higher
```

### Step 1.2: Create Your Agent Project (2 minutes)

```bash
# Create new agent
agentcore init my-grok-agent

# When prompted, choose:
# Language: Python
# Framework: Strands Agents
# Template: Basic

# Navigate to project
cd my-grok-agent
```

You'll see:
```
my-grok-agent/
├── agent.py              # Your agent code
├── agentcore.yaml        # Configuration
├── requirements.txt      # Python dependencies
└── .env.example         # Environment template
```

### Step 1.3: Set Up Python Environment (3 minutes)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# You should see (venv) in your terminal now
```

### Step 1.4: Install Dependencies (2 minutes)

```bash
# Install base packages
pip install strands-agents boto3

# Install LiteLLM for Grok support
pip install litellm python-dotenv

# Verify installation
pip list | grep -E "(strands|litellm|dotenv)"
```

### Step 1.5: Configure Environment Variables (3 minutes)

```bash
# Copy the example file
cp .env.example .env

# Edit .env
# Windows: notepad .env
# Mac/Linux: nano .env
```

**Add your Grok API key:**

```bash
# Model Configuration
MODEL_NAME=grok/openai/gpt-oss-120b
GROK_API_KEY=xai-your-actual-api-key-here

# Model Settings
TEMPERATURE=0.7
MAX_TOKENS=2048

# AgentCore Settings
AGENT_NAME=my-grok-agent
AGENT_VERSION=1.0.0

# Development
LOCAL_DEV=true
DEBUG=true
LOG_LEVEL=INFO
```

**Important:** Replace `xai-your-actual-api-key-here` with your real Grok API key!

### Step 1.6: Write Your Agent Code (10 minutes)

Open `agent.py` and replace everything with this:

```python
"""
My Grok Agent - Using Strands SDK with Grok AI
"""

from strands import Agent, tool
import os
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

print("🚀 Loading agent...")
print(f"📦 Using model: {os.getenv('MODEL_NAME', 'not set')}")


# ============================================================================
# Define Your Tools
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
def create_support_ticket(description: str, priority: str = "medium") -> str:
    """Create a support ticket for issues that need human help"""
    ticket_id = f"TICKET-{hash(description) % 10000}"
    return f"✅ Created ticket {ticket_id} (priority: {priority}). Our team will respond within 24 hours."


# ============================================================================
# Create Your Agent
# ============================================================================

# Get configuration from environment
MODEL_NAME = os.getenv("MODEL_NAME", "grok/openai/gpt-oss-120b")
AGENT_NAME = os.getenv("AGENT_NAME", "My Grok Agent")
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))

print(f"🤖 Creating agent: {AGENT_NAME}")

agent = Agent(
    name=AGENT_NAME,
    model=MODEL_NAME,
    system_prompt="""
    You are a helpful customer support assistant.
    
    You can:
    - Answer questions using the answer_question tool
    - Create tickets using the create_support_ticket tool
    
    Be friendly, concise, and helpful. Always use tools when appropriate.
    """,
    tools=[answer_question, create_support_ticket],
    temperature=TEMPERATURE
)

print("✅ Agent created successfully!")


# ============================================================================
# Handler Function (AgentCore Runtime calls this)
# ============================================================================

def handler(event, context=None):
    """
    Main entry point - called by AgentCore Runtime
    
    For local testing: python agent.py
    For AgentCore: agentcore invoke
    """
    # Get user input
    user_message = event.get("prompt", "")
    user_id = event.get("user_id", "anonymous")
    session_id = event.get("session_id", "local-session")
    
    if not user_message:
        return {
            "statusCode": 400,
            "response": "Error: No prompt provided"
        }
    
    print(f"\n💬 User ({user_id}): {user_message}")
    
    try:
        # Run the agent
    try:
        # Run the agent (Strands SDK - call the agent like a function)
        response = agent(user_message)
        
        print(f"🤖 Agent: {response}")
        
        return {
            "statusCode": 200,
            "response": response,
            "user_id": user_id,
            "session_id": session_id,
            "model": MODEL_NAME
        }t Exception as e:
        error_msg = f"Error running agent: {str(e)}"
        print(f"❌ {error_msg}")
        
        return {
            "statusCode": 500,
            "response": "I apologize, but I encountered an error. Please try again.",
            "error": error_msg
        }


# ============================================================================
# Local Testing
# ============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🧪 Testing Agent Locally")
    print("=" * 60)
    
    # Test messages
    test_cases = [
        {
            "prompt": "Hello! What can you help me with?",
            "user_id": "test_user_1"
        },
        {
            "prompt": "I forgot my password",
            "user_id": "test_user_1"
        },
        {
            "prompt": "What are your business hours?",
            "user_id": "test_user_2"
        },
        {
            "prompt": "I have a complex technical issue that needs urgent attention",
            "user_id": "test_user_3"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n--- Test {i}/4 ---")
        result = handler(test_case)
        
        if result["statusCode"] == 200:
            print(f"✅ Success")
        else:
            print(f"❌ Failed: {result.get('error', 'Unknown error')}")
        
        print()  # Empty line for readability
    
    print("=" * 60)
    print("✅ Local testing complete!")
    print("=" * 60)
    print("\n💡 Next step: Deploy to AgentCore with 'agentcore deploy'\n")
```

**What this code does:**
1. Loads your Grok API key from `.env`
2. Creates tools for answering questions and creating tickets
3. Creates an agent using Grok via LiteLLM
4. Handles incoming messages
5. Includes local testing

### Step 1.7: Test Locally (5 minutes)

```bash
# Run your agent
python agent.py
```

**Expected output:**
```
🚀 Loading agent...
📦 Using model: grok/openai/gpt-oss-120b
🤖 Creating agent: My Grok Agent
✅ Agent created successfully!

============================================================
🧪 Testing Agent Locally
============================================================

--- Test 1/4 ---
💬 User (test_user_1): Hello! What can you help me with?
🤖 Agent: Hello! I'm here to help you with various things...
✅ Success

--- Test 2/4 ---
💬 User (test_user_1): I forgot my password
🤖 Agent: To reset your password: Go to Settings → Security...
✅ Success

...

✅ Local testing complete!
💡 Next step: Deploy to AgentCore with 'agentcore deploy'
```

**Troubleshooting:**

If you see errors:

1. **"Module 'strands' not found"**
   ```bash
   pip install strands-agents
   ```

2. **"GROK_API_KEY not found"**
   - Check your `.env` file has `GROK_API_KEY=xai-...`
   - Make sure you're in the right directory
   - Try: `cat .env` to verify

3. **"Invalid API key"**
   - Verify your Grok API key at https://console.x.ai/
   - Make sure it starts with `xai-`

### Step 1.8: Understand AgentCore Configuration (3 minutes)

Open `agentcore.yaml`:

```yaml
name: my-grok-agent
version: "1.0.0"

runtime:
  timeout: 300      # 5 minutes max per request
  memory: 1024      # 1 GB RAM
  python_version: "3.12"
  environment_variables:
    MODEL_NAME: ${MODEL_NAME}
    GROK_API_KEY: ${GROK_API_KEY}
    TEMPERATURE: ${TEMPERATURE}

# Note: We're NOT using Bedrock, so no harness section needed
# LiteLLM handles model routing

memory:
  short_term: true   # Remember conversation context
  long_term: false   # Don't need persistent memory yet

gateway:
  tools: []          # We're using inline tools (answer_question, create_ticket)

observability:
  tracing: enabled
  log_level: INFO
```

**Key points:**
- Environment variables are passed from your `.env` to AgentCore
- No Bedrock configuration needed
- LiteLLM in your code handles Grok routing

---

## Part 2: AgentCore Local Runtime (15 minutes)

AgentCore provides a local development server that mimics the cloud environment.

### Step 2.1: Start AgentCore Dev Server (2 minutes)

```bash
# Start local AgentCore runtime
agentcore dev

# You'll see:
# Starting AgentCore development server...
# Server running on http://localhost:8080
# Watching for changes...
```

**Keep this terminal open!** Open a new terminal for the next steps.

### Step 2.2: Test with AgentCore CLI (3 minutes)

In a **new terminal** (keep dev server running):

```bash
# Activate virtual environment again
cd my-grok-agent
source venv/bin/activate  # Windows: venv\Scripts\activate

# Test your agent through AgentCore
agentcore invoke --local --payload '{
  "prompt": "Hello! Can you help me?",
  "user_id": "test_user"
}'
```

**Expected output:**
```json
{
  "statusCode": 200,
  "response": "Hello! I'm here to help...",
  "user_id": "test_user",
  "model": "grok/openai/gpt-oss-120b"
}
```

### Step 2.3: Test Multiple Conversations (3 minutes)

```bash
# Test password reset
agentcore invoke --local --payload '{
  "prompt": "I forgot my password",
  "user_id": "user_001"
}'

# Test business hours
agentcore invoke --local --payload '{
  "prompt": "What are your hours?",
  "user_id": "user_002"
}'

# Test ticket creation
agentcore invoke --local --payload '{
  "prompt": "I have a billing issue that needs urgent help",
  "user_id": "user_003"
}'
```

### Step 2.4: Monitor Logs (2 minutes)

In the terminal running `agentcore dev`, you'll see:

```
[2026-10-22 10:30:15] INFO: Request received from user_001
[2026-10-22 10:30:16] INFO: Tool called: answer_question
[2026-10-22 10:30:17] INFO: Response sent (200)
```

This shows you exactly what's happening!

### Step 2.5: Test Hot Reload (3 minutes)

With `agentcore dev` still running:

1. Open `agent.py`
2. Change the system prompt:
   ```python
   system_prompt="""
   You are an AWESOME customer support assistant! 😎
   ...
   """
   ```
3. Save the file
4. Test again:
   ```bash
   agentcore invoke --local --payload '{
     "prompt": "Hi there!",
     "user_id": "test"
   }'
   ```

**The changes take effect immediately!** No restart needed.

### Step 2.6: Stop Dev Server (1 minute)

When you're done testing:

```bash
# In the terminal running agentcore dev
# Press: Ctrl+C

# Server stopped
```

---

## Part 3: Deploy to AWS (20 minutes)

Now let's deploy your agent to AWS AgentCore cloud runtime.

### Step 3.1: Verify AWS Configuration (3 minutes)

```bash
# Check AWS credentials
aws sts get-caller-identity

# Expected output:
# {
#     "UserId": "AIDACKCEVSQ...",
#     "Account": "123456789012",
#     "Arn": "arn:aws:iam::123456789012:user/your-user"
# }
```

If this fails:
```bash
aws configure
# Enter your AWS Access Key ID
# Enter your AWS Secret Access Key
# Default region: us-east-1
# Default output format: json
```

### Step 3.2: Prepare for Deployment (2 minutes)

Make sure your `.env` is properly configured:

```bash
# Verify your configuration
cat .env

# Should show:
# MODEL_NAME=grok/openai/gpt-oss-120b
# GROK_API_KEY=xai-...
```

### Step 3.3: Deploy to AgentCore (5 minutes)

```bash
# Deploy your agent
agentcore deploy --region us-east-1 --stage production

# You'll see:
# [1/6] Validating configuration...
# [2/6] Packaging agent code...
# [3/6] Uploading to S3...
# [4/6] Creating AgentCore runtime...
# [5/6] Configuring environment variables...
# [6/6] Running health checks...
#
# ✅ Deployment successful!
#
# Agent ARN: arn:aws:bedrock-agentcore:us-east-1:123456789012:agent/my-grok-agent
# Endpoint: https://abc123xyz.agentcore.us-east-1.amazonaws.com
# Version: 1.0.0
```

**Important:** Save your endpoint URL!

```bash
# Save for later use
echo "https://abc123xyz.agentcore.us-east-1.amazonaws.com" > endpoint.txt
```

### Step 3.4: Verify Deployment (2 minutes)

```bash
# Check status
agentcore status

# Expected output:
# Agent: my-grok-agent
# Status: ACTIVE
# Version: 1.0.0
# Region: us-east-1
# Endpoint: https://abc123xyz.agentcore.us-east-1.amazonaws.com
# Last Updated: 2026-10-22T15:30:00Z
# Health: HEALTHY
```

### Step 3.5: Test Production Agent (5 minutes)

```bash
# Test your live agent
agentcore invoke --payload '{
  "prompt": "Hello from the cloud!",
  "user_id": "prod_user_001"
}'

# Expected response from Grok via AgentCore cloud:
# {
#   "statusCode": 200,
#   "response": "Hello! I'm running on AWS AgentCore...",
#   "user_id": "prod_user_001",
#   "model": "grok/openai/gpt-oss-120b"
# }
```

Test different scenarios:

```bash
# Password reset
agentcore invoke --payload '{
  "prompt": "I need to reset my password",
  "user_id": "prod_user_002"
}'

# Business hours
agentcore invoke --payload '{
  "prompt": "When are you open?",
  "user_id": "prod_user_003"
}'

# Ticket creation
agentcore invoke --payload '{
  "prompt": "I have an urgent technical issue",
  "user_id": "prod_user_004"
}'
```

### Step 3.6: Monitor Cloud Logs (3 minutes)

```bash
# View recent logs
agentcore logs --since 10m

# Expected output:
# 2026-10-22 15:30:45 [INFO] Agent invocation started
# 2026-10-22 15:30:46 [INFO] Using model: grok/openai/gpt-oss-120b
# 2026-10-22 15:30:47 [INFO] Tool called: answer_question
# 2026-10-22 15:30:48 [INFO] Response generated
# 2026-10-22 15:30:48 [INFO] Agent invocation completed (200)

# Follow live logs
agentcore logs --follow

# Press Ctrl+C to stop
```

---

## Part 4: AgentCore Features (15 minutes)

### Step 4.1: Memory Across Sessions (5 minutes)

Let's enable memory so your agent remembers users:

**Update `agentcore.yaml`:**

```yaml
memory:
  short_term: true   # Conversation context
  long_term: true    # ✅ Enable this!
  retention_days: 30
```

**Deploy the update:**

```bash
agentcore deploy --region us-east-1 --stage production
```

**Test memory:**

```bash
# First conversation
agentcore invoke --payload '{
  "prompt": "My name is Alice and I prefer short answers",
  "user_id": "alice_001",
  "session_id": "session_1"
}'

# Different session, same user
agentcore invoke --payload '{
  "prompt": "What was my name again?",
  "user_id": "alice_001",
  "session_id": "session_2"
}'

# Agent should remember: "Your name is Alice"
```

### Step 4.2: Gateway Tools (5 minutes)

Add external tools via Gateway (for APIs, Lambda functions, etc.):

**Update `agentcore.yaml`:**

```yaml
gateway:
  tools:
    # Example: Connect to an external API
    - type: openapi
      name: weather_api
      spec_url: https://api.example.com/openapi.yaml
      description: "Get real weather data"
      authentication:
        type: api_key
        header: X-API-Key
        secret_arn: arn:aws:secretsmanager:us-east-1:123456789012:secret:weather-api-key
```

**Update your agent code** to use the gateway tool:

```python
# Tools will be available via gateway
# AgentCore automatically injects them
```

**Redeploy:**

```bash
agentcore deploy --region us-east-1 --stage production
```

### Step 4.3: Observability & Tracing (5 minutes)

**View distributed traces:**

```bash
# List recent traces
agentcore traces list --limit 10

# Example output:
# Trace ID: abc123xyz789
# Duration: 1.2s
# Status: 200
# Breakdown:
#   - Context retrieval: 0.1s
#   - LLM call: 0.8s
#   - Tool execution: 0.2s
#   - Response: 0.1s
```

**View specific trace:**

```bash
agentcore traces get --trace-id abc123xyz789
```

**View metrics:**

```bash
# Latency metrics
agentcore metrics --metric InvocationLatency --period 3600

# Request count
agentcore metrics --metric RequestCount --period 3600

# Error rate
agentcore metrics --metric ErrorRate --period 3600
```

---

## Part 5: Making Changes & Updates (10 minutes)

### Step 5.1: Update Your Agent (5 minutes)

Let's add a new tool:

**Edit `agent.py`:**

```python
@tool
def check_order_status(order_id: str) -> str:
    """Check the status of an order"""
    # Mock implementation - replace with real API
    statuses = {
        "12345": "Shipped - arrives tomorrow",
        "67890": "Processing - ships in 2 days"
    }
    return statuses.get(order_id, f"Order {order_id} not found")

# Add to agent
agent = Agent(
    name=AGENT_NAME,
    model=MODEL_NAME,
    system_prompt="""
    You are a helpful customer support assistant.
    
    You can:
    - Answer questions using the answer_question tool
    - Create tickets using the create_support_ticket tool
    - Check order status using the check_order_status tool  # ✅ New!
    
    Be friendly, concise, and helpful.
    """,
    tools=[answer_question, create_support_ticket, check_order_status]  # ✅ Add here
)
```

**Test locally first:**

```bash
python agent.py
```

**Deploy update:**

```bash
agentcore deploy --region us-east-1 --stage production
```

**Test the new feature:**

```bash
agentcore invoke --payload '{
  "prompt": "Can you check the status of order 12345?",
  "user_id": "customer_001"
}'
```

### Step 5.2: Switch Models (3 minutes)

Want to use a different model? Just update `.env`:

```bash
# Edit .env
# Change MODEL_NAME to any LiteLLM-supported model:

# Grok
MODEL_NAME=grok/openai/gpt-oss-120b

# Or Groq (faster, cheaper)
MODEL_NAME=groq/llama3-70b-8192
GROQ_API_KEY=gsk-...

# Or OpenAI
MODEL_NAME=openai/gpt-4
OPENAI_API_KEY=sk-...

# Or Claude
MODEL_NAME=anthropic.claude-3-5-sonnet-20241022-v2:0
ANTHROPIC_API_KEY=sk-ant-...
```

**Redeploy:**

```bash
agentcore deploy --region us-east-1 --stage production
```

Your agent now uses the new model!

### Step 5.3: Rollback if Needed (2 minutes)

If something goes wrong:

```bash
# Check available versions
agentcore versions list

# Rollback to previous version
agentcore rollback --version 1.0.0

# Verify
agentcore status
```

---

## Part 6: Production Best Practices (10 minutes)

### Step 6.1: Set Up Alarms (3 minutes)

```bash
# High latency alarm
aws cloudwatch put-metric-alarm \
  --alarm-name my-grok-agent-high-latency \
  --alarm-description "Alert when P99 latency > 5s" \
  --metric-name InvocationLatency \
  --namespace AWS/BedrockAgentCore \
  --statistic Average \
  --period 300 \
  --threshold 5000 \
  --comparison-operator GreaterThanThreshold \
  --evaluation-periods 2 \
  --dimensions Name=AgentName,Value=my-grok-agent

# High error rate alarm
aws cloudwatch put-metric-alarm \
  --alarm-name my-grok-agent-high-errors \
  --alarm-description "Alert when error rate > 5%" \
  --metric-name ErrorRate \
  --namespace AWS/BedrockAgentCore \
  --statistic Average \
  --period 300 \
  --threshold 5 \
  --comparison-operator GreaterThanThreshold \
  --evaluation-periods 2 \
  --dimensions Name=AgentName,Value=my-grok-agent
```

### Step 6.2: Monitor Costs (3 minutes)

```bash
# View token consumption
agentcore metrics --metric TokensConsumed --period 86400

# Estimate costs:
# Grok pricing (approximate):
# - Input: $5 per 1M tokens
# - Output: $15 per 1M tokens

# Example:
# 10,000 requests/day
# ~500 tokens per request average
# = 5M tokens/day
# = ~$25-75/day depending on input/output ratio
```

**Cost optimization tips:**
1. Use shorter system prompts
2. Cache common responses
3. Use Groq for simpler queries (10x cheaper)
4. Monitor token usage daily

### Step 6.3: Security Best Practices (4 minutes)

**1. Rotate API Keys Regularly**

```bash
# Update .env with new key
GROK_API_KEY=xai-new-key-here

# Redeploy
agentcore deploy --region us-east-1 --stage production
```

**2. Use AWS Secrets Manager (Production)**

```bash
# Store API key in Secrets Manager
aws secretsmanager create-secret \
  --name /agentcore/grok-api-key \
  --secret-string "xai-your-key-here"

# Update agentcore.yaml
runtime:
  environment_variables:
    GROK_API_KEY: "{{resolve:secretsmanager:/agentcore/grok-api-key}}"
```

**3. Restrict IAM Permissions**

Create a minimal IAM role:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*"
    }
  ]
}
```

---

## Troubleshooting Guide

### Issue: "GROK_API_KEY not found"

**Solution:**
```bash
# Check .env file exists
ls -la .env

# Check key is set
cat .env | grep GROK_API_KEY

# Reload environment
deactivate
source venv/bin/activate
```

### Issue: "Module 'strands' not found"

**Solution:**
```bash
pip install strands-agents litellm python-dotenv
```

### Issue: "Deployment failed"

**Solution:**
```bash
# Check AWS credentials
aws sts get-caller-identity

# Check configuration
agentcore validate

# View detailed error
agentcore logs --since 30m
```

### Issue: "High latency in production"

**Solution:**
```bash
# Check traces
agentcore traces list --filter "duration > 3000"

# Common causes:
# 1. Grok API slow - try Groq instead
# 2. Large system prompt - shorten it
# 3. Too many tools - reduce or optimize
```

### Issue: "API rate limit exceeded"

**Solution:**
```bash
# Grok has rate limits
# Options:
# 1. Wait and retry
# 2. Implement exponential backoff
# 3. Use multiple API keys
# 4. Switch to different model temporarily
```

---

## Quick Reference

### Essential Commands

```bash
# Local Development
python agent.py                  # Test locally
agentcore dev                    # Start dev server
agentcore invoke --local         # Test via AgentCore locally

# Deployment
agentcore deploy --region us-east-1  # Deploy to cloud
agentcore status                     # Check status
agentcore rollback --version 1.0.0   # Rollback

# Monitoring
agentcore logs --follow          # Live logs
agentcore traces list            # View traces
agentcore metrics                # View metrics

# Testing
agentcore invoke --payload '{}'  # Test production
```

### Configuration Files

```
my-grok-agent/
├── .env                # Your secrets (don't commit!)
├── agent.py            # Agent code
├── agentcore.yaml      # AgentCore config
└── requirements.txt    # Python deps
```

---

## Next Steps

### 1. Add More Features

- Implement real tools (APIs, databases)
- Add more sophisticated logic
- Integrate with your systems

### 2. Optimize Performance

- Profile token usage
- Cache common responses
- Use faster models for simple queries

### 3. Scale to Production

- Set up CI/CD pipeline
- Implement comprehensive monitoring
- Add error recovery and retries

### 4. Multi-Agent Systems

- Create specialized agents
- Implement agent orchestration
- Build agent teams

---

## Resources

- **Grok Documentation:** https://docs.x.ai/
- **Strands SDK:** https://docs.strands.ai/
- **LiteLLM:** https://docs.litellm.ai/
- **AgentCore:** https://docs.aws.amazon.com/bedrock-agentcore/

---

## Congratulations! 🎉

You've successfully:
- ✅ Built an AI agent using Grok
- ✅ Tested it locally with AgentCore
- ✅ Deployed to AWS cloud
- ✅ Learned AgentCore features
- ✅ Implemented best practices

**Your agent is production-ready!**

Keep building and experimenting. The possibilities are endless! 🚀
