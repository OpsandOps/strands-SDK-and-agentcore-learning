# AWS AgentCore: Getting Started Guide

**Last Updated:** October 2026

---

## ⚡ Start Here (Choose Your Path)

### 🆕 **New to AgentCore? → [SIMPLE_START.md](SIMPLE_START.md)**

**Best for:** Beginners, first-time users  
**Time:** 30 minutes  
**Framework:** Strands SDK (simple!)  
**Result:** Working agent deployed to AWS

### 🎓 **Want Step-by-Step Tutorial? → [TUTORIAL.md](TUTORIAL.md)**

**Best for:** Learning by doing  
**Time:** 1 hour  
**Framework:** Your choice (includes LangGraph example)  
**Result:** Full understanding + deployed agent

### 📖 **Want Complete Reference? → Keep reading below**

**Best for:** Deep dive into all features  
**Time:** 2-3 hours  
**Content:** All 12 components, configuration, best practices  
**Result:** Comprehensive knowledge

---

## 🚨 Important: Complexity Notice

This README contains **comprehensive documentation** about all AgentCore features. It can be overwhelming for beginners.

**If you're just starting out:** Please use [SIMPLE_START.md](SIMPLE_START.md) instead. You can always come back to this README later when you need advanced features.

**This README is best for:**
- Understanding all 12 AgentCore components
- Learning advanced configuration options
- Production deployment planning
- Architecture decisions

---

## Quick Navigation

| I want to... | Go to... | Time |
|--------------|----------|------|
| ⚡ **Get started fast (beginner)** | [SIMPLE_START.md](SIMPLE_START.md) | 30 min |
| 📖 **Learn what AgentCore is** | [What is AWS AgentCore?](#what-is-aws-agentcore) below | 10 min |
| 🎓 **Step-by-step tutorial** | [TUTORIAL.md](TUTORIAL.md) | 1 hour |
| 🏢 **Deploy to production** | [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) | 2 hours |
| 🗺️ **Explore the project** | [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) | 20 min |

---

## Table of Contents

- [What is AWS AgentCore?](#what-is-aws-agentcore)
- [Core Components (All 12)](#core-components)
- [Prerequisites](#prerequisites)
- [Sample Project Walkthrough](#sample-project-walkthrough)
- [Deployment to AWS](#deployment-to-aws)
- [Cost Optimization](#cost-optimization)
- [Best Practices](#best-practices)

---

## What is AWS AgentCore?

Amazon Bedrock AgentCore is AWS's production-ready platform for building, deploying, and operating AI agents at scale.

**Think of it as "Serverless for AI Agents":**
- You write agent code
- AWS handles hosting, scaling, memory, tools, and monitoring
- You only pay for what you use

**Key Benefits:**
- 🚀 **Framework Agnostic** - Works with LangGraph, CrewAI, LlamaIndex, Strands Agents, or custom frameworks
- 🔒 **Secure by Default** - Built-in identity management, session isolation, and guardrails
- 💰 **Cost-Effective** - Pay only for active compute time (near-zero during I/O wait)
- 📊 **Production Ready** - Integrated observability, evaluation frameworks, and monitoring

**Use Cases:**
- Customer support chatbots
- IT helpdesk assistants
- Sales qualification agents
- Documentation Q&A systems
- Workflow automation

---

### AgentCore vs Bedrock Agents (Classic)

| Feature | AgentCore | Bedrock Agents |
|---------|-----------|----------------|
| Agent Code | Custom Python/TypeScript | Declarative (no code) |
| Frameworks | **Any** (LangGraph, Strands, etc.) | AWS-native only |
| Session Length | Up to 8 hours | Per-request |
| Memory | Short-term + Long-term + Semantic | Session-level only |
| Best For | Complex agents, custom logic | Quick prototypes, simple agents |

### Quick Example

```python
# Simple agent with Strands SDK
from strands import Agent, Tool

def search_docs(query: str) -> str:
    return "Documentation result..."

agent = Agent(
    name="Helper",
    instructions="You're a helpful assistant",
    tools=[Tool(name="search", function=search_docs)]
)

# That's it! Deploy with: agentcore deploy
```

**Want to try this?** → Go to [SIMPLE_START.md](SIMPLE_START.md)

---

## Core Components

### 1. **AgentCore Runtime** ✅ GA
Serverless container execution environment for your agent code.
- Supports Python 3.10+ and TypeScript/Node.js 20+
- Sessions up to 8 hours with automatic scaling
- No infrastructure management required

### 2. **AgentCore Harness** ✅ GA
Configuration layer that wires together models, prompts, and tools.
- Works with Amazon Bedrock, OpenAI, Google Gemini, and any OpenAI-compatible provider
- Centralized system prompt and model parameter management

### 3. **AgentCore Memory** ✅ GA
Managed memory system enabling context retention across conversations.

**Three Memory Types:**
- **Short-Term (Session):** Conversation history within a single session
- **Long-Term (Cross-Session):** Persistent facts and preferences per user
- **Semantic Memory:** Vector-backed retrieval of relevant past interactions

### 4. **AgentCore Gateway** ✅ GA
Unified tool connectivity hub that simplifies integration.
- Converts REST APIs, Lambda functions, and MCP servers into agent-ready tools
- Handles authentication, retries, and response formatting automatically

### 5. **AgentCore Identity** ✅ GA
OAuth2-based identity and access management for agents.
- Assigns unique, verifiable identities to agents
- Enables secure agent-powered interactions with enterprise systems

### 6. **AgentCore Code Interpreter** ✅ GA
Sandboxed Python code execution environment.
- Agents can write and run code safely without external infrastructure
- Isolated execution prevents security risks

### 7. **AgentCore Browser** ✅ GA
Managed browser tool for web navigation and interaction.
- Agents can browse, click, and extract information from websites
- No Playwright or Selenium setup required

### 8. **AgentCore Observability** ✅ GA
Integrated tracing and monitoring via CloudWatch and OpenTelemetry.
- Captures every agent step, tool call, and LLM invocation
- Real-time dashboards for performance metrics

### 9. **AgentCore Evaluations** ✅ GA
Built-in framework for testing agent accuracy, safety, and performance.
- LLM-as-judge evaluation patterns
- Automated regression testing before deployment

### 10. **AgentCore Policy** ✅ GA
Agent-level guardrails and policy enforcement.
- Integrates with AWS Bedrock Guardrails
- Define what agents can and cannot do

### 11. **AgentCore Registry** ✅ GA
Central registry for agent discovery and versioning.
- Semantic versioning with rollback support
- Share agents across teams

### 12. **AgentCore Payments** ✅ GA
Consumption-based billing with optimized pricing.
- Charges only for active compute time
- Near-zero cost during I/O wait (LLM processing, tool calls)

---

## Prerequisites

### For Beginners

If you're just getting started, you only need:

1. **Python 3.10+** - [Download](https://www.python.org/downloads/)
2. **AWS Account** - [Sign up](https://aws.amazon.com/free/)
3. **AWS CLI configured** - Run `aws configure`

**That's it!** Go to [SIMPLE_START.md](SIMPLE_START.md) to begin.

---

### For Advanced Users

If you're planning production deployment, you'll also want:

**Required Software**

1. **Node.js 20+**
   ```bash
   node --version  # Should show v20.0.0 or higher
   ```

2. **Python 3.10+**
   ```bash
   python --version  # Should show 3.10.0 or higher
   ```

3. **AWS CLI**
   ```bash
   aws --version
   aws configure  # Configure your AWS credentials
   ```

4. **AWS CDK v2** (optional, for Infrastructure as Code)
   ```bash
   npm install -g aws-cdk
   cdk --version
   ```

### AWS Account Setup

1. **IAM Permissions Required:**
   - `bedrock-agentcore:*` (for AgentCore operations)
   - `bedrock:InvokeModel` (for foundation model access)
   - `s3:*` (for artifact storage)
   - `cloudwatch:*` (for observability)
   - `iam:PassRole` (for execution roles)

2. **Service Quotas:**
   - Ensure Bedrock model access is enabled in your region
   - Request quota increases for Claude models if needed

3. **Supported Regions (as of Oct 2026):**
   - us-east-1 (N. Virginia)
   - us-west-2 (Oregon)
   - eu-west-1 (Ireland)
   - ap-southeast-1 (Singapore)
   - And 10 more regions

---

## Local Development Setup

### Step 1: Install AgentCore CLI

```bash
# Install globally
npm install -g @aws/agentcore-cli

# Verify installation
agentcore --version  # Expected: 0.4.0+
```

### Step 2: Bootstrap CDK (One-Time Setup)

```bash
# Bootstrap CDK in your AWS account/region
cdk bootstrap aws://YOUR_ACCOUNT_ID/us-east-1

# Example:
# cdk bootstrap aws://123456789012/us-east-1
```

### Step 3: Verify Permissions

```bash
# Test AgentCore access
aws bedrock-agentcore list-agents --region us-east-1

# If you get AccessDeniedException, add the required IAM policy
```

### Step 4: Configure AWS Profile (Optional)

```bash
# If using named profiles
export AWS_PROFILE=your-profile-name

# Or set default region
export AWS_DEFAULT_REGION=us-east-1
```

---

## Sample Project Walkthrough

**Note:** This section describes an advanced example using LangGraph.

**For a simpler starting point**, see [SIMPLE_START.md](SIMPLE_START.md) which uses Strands SDK.

---

### Project Overview

The sample project demonstrates a **Customer Support Agent** that can:
- Answer questions using a knowledge base
- Create support tickets
- Remember customer preferences across conversations
- Execute code for data analysis

### Project Initialization

```bash
# Create new AgentCore project
agentcore init customer-support-agent

# You'll be prompted to select:
# 1. Language: Python
# 2. Framework: LangGraph
# 3. Template: Production

cd customer-support-agent
```

### Project Structure

After initialization, you'll see:

```
customer-support-agent/
├── agent.py              # Main agent logic
├── requirements.txt      # Python dependencies
├── agentcore.yaml       # AgentCore configuration
├── tests/
│   ├── test_agent.py    # Unit tests
│   └── eval_suite.json  # Evaluation scenarios
├── tools/
│   └── search_kb.py     # Custom tool implementations
└── .env                 # Local environment variables
```

### Add Required Components

```bash
# Add memory for conversation context
agentcore add memory

# Add gateway for tool connectivity
agentcore add gateway

# Add code interpreter for data analysis
agentcore add code-interpreter

# Add observability for monitoring
agentcore add observability
```

### Configure agentcore.yaml

Content was rephrased for compliance with licensing restrictions. The configuration structure organizes essential agent settings including runtime parameters (timeout and memory allocation), model selection through the harness component, memory capabilities spanning short-term sessions and long-term semantic storage, gateway tool definitions connecting Lambda functions and REST APIs, and observability settings enabling comprehensive tracing and logging.

```yaml
name: customer-support-agent
version: "1.0.0"

runtime:
  timeout: 3600        # 1 hour max session (up to 8h supported)
  memory: 2048         # MB
  python_version: "3.12"

harness:
  model: anthropic.claude-3-5-sonnet-20241022-v2:0
  system_prompt: |
    You are a helpful customer support agent for TechCorp.
    You can search our knowledge base, create support tickets,
    and analyze customer data. Always be polite and professional.
  temperature: 0.7
  max_tokens: 2048

memory:
  short_term: true      # Session conversation history
  long_term: true       # Cross-session user preferences
  semantic_search: true # Vector-based memory retrieval
  retention_days: 90

gateway:
  tools:
    # Lambda function for knowledge base search
    - type: lambda
      name: search_knowledge_base
      arn: arn:aws:lambda:us-east-1:ACCOUNT:function:kb-search
      description: "Search TechCorp knowledge base for answers"
    
    # REST API for ticket creation
    - type: openapi
      name: create_ticket
      spec_url: https://api.techcorp.com/openapi.yaml
      description: "Create a support ticket in our system"

code_interpreter:
  enabled: true
  timeout: 300  # 5 minutes max per code execution

observability:
  tracing: enabled
  log_level: INFO
  custom_metrics:
    - ticket_creation_count
    - avg_resolution_time

policy:
  guardrail_id: "your-guardrail-id"  # Optional: Bedrock Guardrails
  blocked_topics:
    - competitor_pricing
    - unreleased_features
```

### Implement Agent Logic (agent.py)

```python
"""
Customer Support Agent implementation using LangGraph
"""
import os
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from bedrock_agentcore import Memory, Gateway, CodeInterpreter
from langchain_aws import ChatBedrock

# Define conversation state
class AgentState(TypedDict):
    messages: list
    user_id: str
    context: dict
    next_action: str

# Initialize components
memory = Memory()
gateway = Gateway()
code_interpreter = CodeInterpreter()

# Initialize LLM
llm = ChatBedrock(
    model_id="anthropic.claude-3-5-sonnet-20241022-v2:0",
    model_kwargs={"temperature": 0.7}
)

async def retrieve_context(state: AgentState) -> AgentState:
    """Retrieve relevant context from memory"""
    user_id = state["user_id"]
    current_message = state["messages"][-1]
    
    # Get semantic context from past conversations
    relevant_context = await memory.semantic_search(
        user_id=user_id,
        query=current_message,
        top_k=5
    )
    
    # Get user preferences
    preferences = await memory.get(user_id, "preferences") or {}
    
    state["context"] = {
        "past_interactions": relevant_context,
        "preferences": preferences
    }
    return state

async def process_request(state: AgentState) -> AgentState:
    """Main agent processing logic"""
    messages = state["messages"]
    context = state["context"]
    
    # Enhance prompt with context
    enhanced_prompt = f"""
    User Message: {messages[-1]}
    
    Context from past interactions:
    {context.get('past_interactions', 'None')}
    
    User Preferences:
    {context.get('preferences', 'None')}
    
    Please respond helpfully. You have access to:
    - search_knowledge_base: Search our documentation
    - create_ticket: Create support tickets
    - Code execution: Analyze data when needed
    """
    
    # Get LLM response with tool calling
    response = await llm.ainvoke(
        enhanced_prompt,
        tools=[
            gateway.get_tool("search_knowledge_base"),
            gateway.get_tool("create_ticket"),
            code_interpreter.as_tool()
        ]
    )
    
    state["messages"].append(response)
    state["next_action"] = determine_next_action(response)
    
    return state

async def execute_tools(state: AgentState) -> AgentState:
    """Execute any tool calls from the LLM"""
    last_message = state["messages"][-1]
    
    if hasattr(last_message, "tool_calls"):
        for tool_call in last_message.tool_calls:
            if tool_call["name"] == "search_knowledge_base":
                result = await gateway.invoke(
                    "search_knowledge_base",
                    tool_call["args"]
                )
            elif tool_call["name"] == "create_ticket":
                result = await gateway.invoke(
                    "create_ticket",
                    tool_call["args"]
                )
            elif tool_call["name"] == "execute_code":
                result = await code_interpreter.execute(
                    tool_call["args"]["code"]
                )
            
            state["messages"].append({"role": "tool", "content": result})
    
    return state

async def save_memory(state: AgentState) -> AgentState:
    """Save important information to memory"""
    user_id = state["user_id"]
    
    # Extract and save preferences if mentioned
    # (In production, use NER or LLM to extract structured info)
    
    # Save conversation summary
    await memory.put(
        user_id,
        "last_interaction",
        {
            "timestamp": "2026-10-22",
            "summary": state["messages"][-1]
        }
    )
    
    return state

def determine_next_action(message) -> str:
    """Decide whether to continue or end conversation"""
    if hasattr(message, "tool_calls") and message.tool_calls:
        return "execute_tools"
    return "end"

# Build the LangGraph workflow
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("retrieve_context", retrieve_context)
workflow.add_node("process_request", process_request)
workflow.add_node("execute_tools", execute_tools)
workflow.add_node("save_memory", save_memory)

# Define edges
workflow.set_entry_point("retrieve_context")
workflow.add_edge("retrieve_context", "process_request")
workflow.add_conditional_edges(
    "process_request",
    lambda state: state["next_action"],
    {
        "execute_tools": "execute_tools",
        "end": "save_memory"
    }
)
workflow.add_edge("execute_tools", "process_request")
workflow.add_edge("save_memory", END)

# Compile the agent
agent = workflow.compile()

# Handler function for AgentCore Runtime
async def handler(event, context):
    """
    Main entry point called by AgentCore Runtime
    """
    user_message = event.get("prompt", "")
    user_id = event.get("user_id", "anonymous")
    session_id = event.get("session_id")
    
    # Initialize state
    initial_state = {
        "messages": [user_message],
        "user_id": user_id,
        "context": {},
        "next_action": ""
    }
    
    # Run the agent
    result = await agent.ainvoke(initial_state)
    
    # Return response
    return {
        "statusCode": 200,
        "response": result["messages"][-1],
        "session_id": session_id
    }
```

### Create Supporting Tools (tools/search_kb.py)

```python
"""
Mock knowledge base search tool
In production, this would connect to your actual KB
"""

async def search_knowledge_base(query: str) -> dict:
    """
    Search the knowledge base for relevant information
    """
    # Mock implementation - replace with actual KB search
    mock_results = {
        "password reset": "To reset password, go to Settings > Security > Reset Password",
        "billing": "Billing issues can be resolved by contacting billing@techcorp.com",
        "default": "I'll need to look that up for you."
    }
    
    for keyword, answer in mock_results.items():
        if keyword.lower() in query.lower():
            return {
                "success": True,
                "answer": answer,
                "confidence": 0.95
            }
    
    return {
        "success": False,
        "answer": mock_results["default"],
        "confidence": 0.3
    }
```

### Add Dependencies (requirements.txt)

```txt
# Core dependencies
boto3>=1.34.0
langgraph>=0.2.0
langchain-aws>=0.1.0
langchain>=0.2.0

# AgentCore SDK
bedrock-agentcore>=0.4.0

# Utilities
pydantic>=2.5.0
python-dotenv>=1.0.0
```

### Local Testing

```bash
# Start local development server with hot reload
agentcore dev

# The agent is now running on http://localhost:8080

# Test with CLI
agentcore invoke --local --payload '{
  "prompt": "How do I reset my password?",
  "user_id": "user123"
}'

# Expected response:
# {
#   "response": "To reset password, go to Settings > Security > Reset Password",
#   "session_id": "local-session-xyz"
# }
```

### Run Evaluations

Create an evaluation suite (tests/eval_suite.json):

```json
{
  "test_cases": [
    {
      "name": "password_reset_query",
      "input": {
        "prompt": "I forgot my password",
        "user_id": "test_user_1"
      },
      "expected_keywords": ["reset", "password", "settings"],
      "max_latency_ms": 3000
    },
    {
      "name": "billing_question",
      "input": {
        "prompt": "I have a billing issue",
        "user_id": "test_user_2"
      },
      "expected_keywords": ["billing", "contact"],
      "max_latency_ms": 3000
    }
  ],
  "evaluation_criteria": {
    "accuracy": "llm-as-judge",
    "safety": "guardrails",
    "latency": "measured"
  }
}
```

Run evaluations:

```bash
# Run the evaluation suite
agentcore eval --test-suite tests/eval_suite.json

# Output:
# ✅ password_reset_query: PASS (accuracy: 95%, latency: 1240ms)
# ✅ billing_question: PASS (accuracy: 92%, latency: 1580ms)
# 
# Overall: 2/2 passed (100%)
```

---

## Deployment to AWS

### Simple Deployment (Recommended for Beginners)

```bash
# After building your agent, deploy with one command:
agentcore deploy --region us-east-1 --stage production
```

**Full guide:** [SIMPLE_START.md](SIMPLE_START.md) - Steps 6-8

---

### Advanced Deployment Options

For production deployments with auto-scaling, monitoring, and CI/CD:

**See:** [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

---

### Step 1: Pre-Deployment Checklist

```bash
# 1. Ensure all tests pass
agentcore eval --test-suite tests/eval_suite.json

# 2. Review configuration
cat agentcore.yaml

# 3. Check AWS credentials
aws sts get-caller-identity

# 4. Verify region
echo $AWS_DEFAULT_REGION
```

### Step 2: Deploy to Production

```bash
# Deploy to AWS (CodeZip packaging - no Docker required)
agentcore deploy --region us-east-1 --stage production

# Deployment process:
# [1/5] Packaging agent code...
# [2/5] Uploading to S3...
# [3/5] Provisioning AgentCore Runtime...
# [4/5] Configuring Memory and Gateway...
# [5/5] Running health checks...
# 
# ✅ Deployment successful!
# 
# Agent ARN: arn:aws:bedrock-agentcore:us-east-1:123456789012:agent/customer-support-agent
# Endpoint: https://xyz123.agentcore.us-east-1.amazonaws.com
```

### Step 3: Verify Deployment

```bash
# Check deployment status
agentcore status

# Expected output:
# Status: ACTIVE
# Version: 1.0.0
# Endpoint: https://xyz123.agentcore.us-east-1.amazonaws.com
# Last Updated: 2026-10-22T10:30:00Z

# Test production endpoint
agentcore invoke --payload '{
  "prompt": "Hello, how can you help me?",
  "user_id": "prod_user_001"
}'
```

### Step 4: Monitor Deployment

```bash
# View live logs
agentcore logs --follow

# View traces
agentcore traces list --limit 10

# Open CloudWatch dashboard
agentcore dashboard
```

### Step 5: Configure Auto-Scaling (Optional)

Create a CloudWatch alarm for auto-scaling:

```bash
aws cloudwatch put-metric-alarm \
  --alarm-name customer-support-agent-high-latency \
  --alarm-description "Alert when p99 latency exceeds 5 seconds" \
  --metric-name InvocationLatency \
  --namespace AWS/BedrockAgentCore \
  --statistic Average \
  --period 300 \
  --threshold 5000 \
  --comparison-operator GreaterThanThreshold \
  --evaluation-periods 2
```

### Step 6: Set Up Blue/Green Deployments

```bash
# Deploy new version as canary
agentcore deploy --stage production --version 1.1.0 --traffic-split 10

# Monitor canary for 24 hours, then promote
agentcore promote --version 1.1.0

# Or rollback if issues detected
agentcore rollback --version 1.0.0
```

---

## Cost Optimization

### Understanding AgentCore Pricing

AgentCore has a unique pricing model optimized for AI workloads:

**Pay only for active compute time** - Near-zero charges during:
- LLM processing (waiting for model response)
- Tool execution (waiting for external API calls)
- I/O operations

**Pricing Components:**
1. **Runtime Compute:** $0.0001 per second of active execution
2. **Memory Storage:** $0.25 per GB-month (long-term memory only)
3. **Gateway Requests:** $0.0001 per tool invocation
4. **Model Inference:** Separate Bedrock charges apply

### Cost Optimization Strategies

#### 1. Use Streaming Responses
```python
# Reduces perceived latency and compute time
response = await llm.ainvoke(prompt, stream=True)
```

#### 2. Minimize Unnecessary Tool Calls
```python
# Bad: Always call tools
result = await gateway.invoke("search_kb", query)

# Good: Only call when needed
if requires_knowledge_base(query):
    result = await gateway.invoke("search_kb", query)
```

#### 3. Use Cheaper Models for Classification
```python
# Use Claude Haiku for intent classification
intent = await classify_with_haiku(user_message)

# Use Claude Sonnet only for complex generation
if intent.requires_complex_reasoning:
    response = await generate_with_sonnet(user_message)
```

#### 4. Cache Gateway Responses
```yaml
# In agentcore.yaml
gateway:
  tools:
    - type: lambda
      name: search_knowledge_base
      cache_ttl: 3600  # Cache results for 1 hour
```

#### 5. Optimize Memory Retention
```yaml
memory:
  retention_days: 30  # Instead of 90 - reduces storage costs
  semantic_search: false  # Disable if not needed - saves vector storage
```

### Sample Cost Estimate

For a customer support agent handling 10,000 conversations/month:

```
Runtime Compute:
  - Avg session: 3 minutes
  - Active compute: 30 seconds/session
  - Cost: 10,000 × 30 × $0.0001 = $30/month

Memory Storage:
  - 1,000 active users
  - 10 MB per user long-term memory
  - Cost: 10 GB × $0.25 = $2.50/month

Gateway Requests:
  - 2 tool calls per session average
  - Cost: 20,000 × $0.0001 = $2/month

Model Inference (Claude Sonnet):
  - 1,000 input tokens + 500 output tokens per session
  - Cost: ~$30/month (varies by model)

Total: ~$65/month for 10,000 conversations
```

---

## Best Practices

### Security

1. **Use IAM Least Privilege**
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [{
       "Effect": "Allow",
       "Action": [
         "bedrock:InvokeModel"
       ],
       "Resource": "arn:aws:bedrock:*:*:foundation-model/anthropic.claude-3-5-sonnet*"
     }]
   }
   ```

2. **Enable Guardrails**
   - Configure Bedrock Guardrails for content filtering
   - Set up topic blocking for sensitive subjects

3. **Rotate Credentials Regularly**
   - Use AWS Secrets Manager for API keys
   - Implement automatic rotation

### Performance

1. **Set Appropriate Timeouts**
   ```yaml
   runtime:
     timeout: 1800  # 30 minutes for complex tasks
   ```

2. **Monitor Key Metrics**
   - P99 latency
   - Token consumption
   - Error rates
   - Session duration

3. **Use Async Operations**
   ```python
   # Parallel tool execution
   results = await asyncio.gather(
       gateway.invoke("tool1", args1),
       gateway.invoke("tool2", args2)
   )
   ```

### Reliability

1. **Implement Error Handling**
   ```python
   try:
       result = await gateway.invoke("search_kb", query)
   except GatewayTimeoutError:
       result = {"answer": "Service temporarily unavailable"}
   ```

2. **Add Retry Logic**
   ```python
   from tenacity import retry, stop_after_attempt, wait_exponential
   
   @retry(stop=stop_after_attempt(3), wait=wait_exponential())
   async def call_external_api():
       return await gateway.invoke("external_api", params)
   ```

3. **Set Up Health Checks**
   ```python
   async def health_check():
       # Verify critical dependencies
       memory_ok = await memory.ping()
       gateway_ok = await gateway.ping()
       return memory_ok and gateway_ok
   ```

### Testing

1. **Write Unit Tests**
   ```python
   # tests/test_agent.py
   import pytest
   from agent import retrieve_context
   
   @pytest.mark.asyncio
   async def test_retrieve_context():
       state = {
           "user_id": "test_user",
           "messages": ["Hello"],
           "context": {}
       }
       result = await retrieve_context(state)
       assert "context" in result
   ```

2. **Run Evaluations Before Every Deploy**
   ```bash
   # Add to CI/CD pipeline
   agentcore eval --test-suite tests/eval_suite.json || exit 1
   agentcore deploy --region us-east-1 --stage production
   ```

3. **Load Testing**
   ```bash
   # Use artillery or k6 for load testing
   artillery quick --count 100 --num 10 https://your-agent-endpoint.com
   ```

---

## Additional Resources

- [AWS AgentCore Official Documentation](https://docs.aws.amazon.com/bedrock-agentcore/)
- [AgentCore CLI Reference](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/cli-reference.html)
- [Sample Projects Repository](https://github.com/aws-samples/amazon-bedrock-agentcore-examples)
- [Pricing Calculator](https://calculator.aws/#/addService/BedrockAgentCore)
- [AWS Architecture Center - Agentic AI Patterns](https://aws.amazon.com/architecture/agentic-ai/)

---

## Troubleshooting

### Common Issues

**Issue:** `AccessDeniedException` when deploying
```bash
# Solution: Add required IAM permissions
aws iam attach-user-policy \
  --user-name your-user \
  --policy-arn arn:aws:iam::aws:policy/AmazonBedrockFullAccess
```

**Issue:** Local development server won't start
```bash
# Solution: Check port availability
netstat -an | grep 8080
# Kill process using port 8080 if needed
```

**Issue:** High latency in production
```bash
# Solution: Review CloudWatch metrics
agentcore metrics --metric InvocationLatency --period 3600

# Check if tools are the bottleneck
agentcore traces list --filter "duration > 3000"
```

**Issue:** Memory not persisting across sessions
```yaml
# Solution: Verify memory configuration
memory:
  long_term: true  # Must be enabled
  retention_days: 90
```

---

## Next Steps

1. ✅ Complete prerequisites setup
2. ✅ Create your first agent locally
3. ✅ Test with sample data
4. ✅ Deploy to AWS
5. 📊 Set up monitoring dashboards
6. 🔄 Implement CI/CD pipeline
7. 🚀 Scale to production traffic

**Happy building with AWS AgentCore! 🎉**

---

*This guide reflects AgentCore capabilities as of October 2026. Check the official AWS documentation for the latest updates.*
