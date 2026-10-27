# AWS AgentCore Project Overview

Complete guide and sample project for building production AI agents with AWS AgentCore.

## 📁 Project Structure

```
agentcore/
├── README.md                      # Comprehensive introduction and guide
├── DEPLOYMENT_GUIDE.md           # Step-by-step deployment instructions
├── PROJECT_OVERVIEW.md           # This file - project documentation
├── venv/                         # Python virtual environment
│
└── sample-project/               # Complete working example
    ├── agent.py                  # Main agent implementation (LangGraph)
    ├── agentcore.yaml           # AgentCore configuration
    ├── requirements.txt          # Python dependencies
    ├── .env.example             # Environment template
    ├── .gitignore              # Git ignore rules
    ├── QUICKSTART.md           # Quick start guide
    │
    ├── tests/
    │   ├── test_agent.py       # Unit tests
    │   └── eval_suite.json     # Evaluation test cases
    │
    └── cdk/                    # Infrastructure as Code (optional)
        ├── app.py              # CDK stack definition
        ├── cdk.json            # CDK configuration
        └── requirements.txt    # CDK dependencies
```

## 🎯 What You'll Learn

This project teaches you how to:

1. **Understand AgentCore Components**
   - Runtime, Memory, Gateway, Identity
   - Code Interpreter, Browser, Observability
   - Evaluations, Policy, Registry, Harness

2. **Build Agents Locally**
   - Set up development environment
   - Implement agent logic with LangGraph
   - Test with mock components
   - Run evaluations

3. **Deploy to AWS**
   - Configure AWS credentials
   - Deploy with AgentCore CLI
   - Alternative: Deploy with AWS CDK
   - Set up monitoring and alerts

4. **Production Operations**
   - Monitor performance with CloudWatch
   - Implement blue/green deployments
   - Handle errors and rollbacks
   - Optimize costs

## 🚀 Getting Started

### Option 1: Quick Start (Recommended for Beginners)

```bash
# 1. Read the README
cat README.md

# 2. Follow the Quick Start Guide
cd sample-project
cat QUICKSTART.md

# 3. Start coding!
python agent.py
```

### Option 2: Comprehensive Path (For Production)

```bash
# 1. Study core components in README
cat README.md | grep "Core Components" -A 50

# 2. Set up local environment
cd sample-project
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Test locally
python agent.py
pytest tests/

# 4. Deploy to AWS
cat ../DEPLOYMENT_GUIDE.md  # Read deployment guide
agentcore deploy --region us-east-1 --stage production
```

## 📚 Documentation Hierarchy

### 1. README.md (Start Here)
**Purpose:** Comprehensive introduction to AWS AgentCore  
**Audience:** Everyone  
**Content:**
- What is AgentCore?
- Core components explained
- Prerequisites
- Local development setup
- Sample project walkthrough
- Cost optimization
- Best practices

**When to read:** First time learning about AgentCore

### 2. QUICKSTART.md (In sample-project/)
**Purpose:** Get up and running in 15 minutes  
**Audience:** Developers who want to start coding quickly  
**Content:**
- 5-minute local setup
- 10-minute AWS deployment
- Common commands
- Basic troubleshooting

**When to read:** When you're ready to build your first agent

### 3. DEPLOYMENT_GUIDE.md
**Purpose:** Production deployment instructions  
**Audience:** DevOps engineers, Production deployments  
**Content:**
- Pre-deployment checklist
- Three deployment methods (CLI, CDK, Console)
- Post-deployment verification
- Monitoring setup
- CI/CD integration
- Advanced troubleshooting

**When to read:** Before deploying to production

### 4. PROJECT_OVERVIEW.md (This File)
**Purpose:** Navigate the project structure  
**Audience:** Anyone exploring the codebase  
**Content:**
- Project structure
- Documentation guide
- Learning paths
- File purposes

**When to read:** When you want to understand project organization

## 🎓 Learning Paths

### Path 1: "I Want to Understand AgentCore" (Study Mode)

1. Read **README.md** sections:
   - What is AWS AgentCore?
   - Core Components (all 12)
   - AgentCore vs Bedrock Agents comparison

2. Study the sample project:
   - Review `agentcore.yaml` configuration
   - Read through `agent.py` implementation
   - Examine `eval_suite.json` test cases

3. Explore deployment options:
   - Skim **DEPLOYMENT_GUIDE.md**
   - Review CDK infrastructure in `cdk/app.py`

**Time:** 2-3 hours  
**Outcome:** Deep understanding of AgentCore architecture

### Path 2: "I Want to Build Something Now" (Hands-On Mode)

1. Skim **README.md** (Prerequisites and Core Components sections)

2. Follow **sample-project/QUICKSTART.md** exactly:
   - Install dependencies (5 min)
   - Run local tests (5 min)
   - Deploy to AWS (10 min)

3. Customize the agent:
   - Modify system prompt in `agentcore.yaml`
   - Add your own tools
   - Test changes locally

**Time:** 30 minutes to first deployment  
**Outcome:** Working agent deployed to AWS

### Path 3: "I Need to Deploy to Production" (Production Mode)

1. Read **README.md**:
   - Prerequisites
   - Core Components
   - Best Practices section

2. Complete local development:
   - Set up per **QUICKSTART.md**
   - Write comprehensive tests
   - Run evaluations

3. Follow **DEPLOYMENT_GUIDE.md**:
   - Pre-deployment checklist
   - Choose deployment method
   - Set up monitoring
   - Configure CI/CD

4. Production operations:
   - Monitor metrics
   - Set up alarms
   - Plan rollback procedures

**Time:** 1-2 days for complete production setup  
**Outcome:** Production-ready deployment with full observability

## 🔍 Key Files Explained

### agent.py
**What it is:** Complete LangGraph implementation of a customer support agent

**Key sections:**
```python
# State definition - how data flows through the agent
class AgentState(TypedDict): ...

# Nodes - individual processing steps
async def retrieve_context(state): ...
async def process_request(state): ...
async def execute_tools(state): ...
async def save_memory(state): ...

# Graph - connects nodes into a workflow
workflow = StateGraph(AgentState)
```

**When to modify:**
- Change agent behavior
- Add new capabilities
- Implement custom tools
- Adjust conversation flow

### agentcore.yaml
**What it is:** Complete configuration for AgentCore services

**Key sections:**
```yaml
runtime:      # Container settings (timeout, memory)
harness:      # Model selection and system prompt
memory:       # Memory configuration (short/long/semantic)
gateway:      # Tool definitions (Lambda, REST API, MCP)
observability: # Logging and tracing
policy:       # Guardrails and content filters
```

**When to modify:**
- Change model or parameters
- Add/remove tools
- Adjust memory settings
- Configure deployment strategy

### tests/eval_suite.json
**What it is:** Comprehensive test scenarios for agent evaluation

**Structure:**
```json
{
  "test_cases": [      // Individual test scenarios
    {
      "input": {...},  // User prompt
      "expected_keywords": [...],  // Expected in response
      "evaluation_criteria": {...} // How to judge quality
    }
  ],
  "evaluation_criteria": {...},  // LLM-as-judge prompts
  "scoring": {...}               // Pass/fail thresholds
}
```

**When to modify:**
- Add new test scenarios
- Adjust quality thresholds
- Change evaluation criteria

### cdk/app.py
**What it is:** Infrastructure as Code for AgentCore resources

**Purpose:**
- Alternative to `agentcore deploy` CLI
- Version control for infrastructure
- Advanced customization (VPC, custom IAM, etc.)

**When to use:**
- Need custom networking
- Require specific IAM policies
- Want GitOps workflow
- Building complex multi-stack deployments

## 🎯 Common Tasks & Where to Look

### "I want to change what the agent says"
→ Edit `system_prompt` in `agentcore.yaml`

### "I want to add a new tool"
→ Edit `gateway.tools` in `agentcore.yaml`  
→ Implement tool logic in `agent.py`

### "I want to adjust memory retention"
→ Edit `memory.retention_days` in `agentcore.yaml`

### "I want to deploy to production"
→ Follow **DEPLOYMENT_GUIDE.md**

### "I want to monitor my agent"
→ See "Monitoring & Observability" in **DEPLOYMENT_GUIDE.md**

### "I want to write tests"
→ See `tests/test_agent.py` for examples  
→ Add scenarios to `tests/eval_suite.json`

### "I want to optimize costs"
→ See "Cost Optimization" in **README.md**

### "I want to use CDK instead of CLI"
→ See `cdk/app.py`  
→ Read CDK section in **DEPLOYMENT_GUIDE.md**

## 📊 Sample Project Features

The customer support agent demonstrates:

### ✅ Knowledge Base Integration
- Searches documentation for answers
- Mock implementation for local testing
- Production-ready Lambda function stub

### ✅ Ticket Creation
- Creates support tickets for complex issues
- Tool call example
- Error handling

### ✅ Memory Across Sessions
- Short-term: Conversation history
- Long-term: User preferences
- Semantic: Vector-based retrieval

### ✅ LangGraph Workflow
- Context retrieval
- LLM reasoning
- Tool execution
- Memory persistence

### ✅ Complete Testing
- Unit tests (pytest)
- Evaluation suite (10 test cases)
- Mock components for local dev

### ✅ Production Ready
- Observability (CloudWatch, X-Ray)
- Error handling
- Retry logic
- Guardrails

## 🛠️ Customization Guide

### 1. Change the Agent's Purpose

**File:** `agentcore.yaml`
```yaml
harness:
  system_prompt: |
    You are a [YOUR PURPOSE HERE].
    You can [LIST CAPABILITIES].
```

### 2. Add a New Tool

**File:** `agentcore.yaml`
```yaml
gateway:
  tools:
    - type: lambda
      name: your_tool_name
      arn: arn:aws:lambda:REGION:ACCOUNT:function:YOUR_FUNCTION
      description: "What your tool does"
```

**File:** `agent.py`
```python
# Add tool to available tools list
tools = [
    components.gateway.get_tool("search_knowledge_base"),
    components.gateway.get_tool("your_tool_name"),  # Add here
]
```

### 3. Use Different Model

**File:** `agentcore.yaml`
```yaml
harness:
  model: meta.llama3-70b-instruct-v1:0  # Or any Bedrock model
```

### 4. Adjust Memory Settings

**File:** `agentcore.yaml`
```yaml
memory:
  short_term: true       # Conversation history
  long_term: true        # User preferences
  semantic_search: false # Disable if not needed (saves cost)
  retention_days: 30     # Reduce from 90 to save cost
```

### 5. Add Custom Metrics

**File:** `agentcore.yaml`
```yaml
observability:
  custom_metrics:
    - name: your_metric_name
      unit: Count
```

**File:** `agent.py`
```python
# Emit custom metric
await components.observability.put_metric(
    "your_metric_name", 
    value=1, 
    unit="Count"
)
```

## 🔗 External Resources

### Official AWS Documentation
- [AgentCore Documentation](https://docs.aws.amazon.com/bedrock-agentcore/)
- [Bedrock User Guide](https://docs.aws.amazon.com/bedrock/)
- [CDK Python Reference](https://docs.aws.amazon.com/cdk/api/v2/python/)

### Frameworks
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [LangChain Documentation](https://python.langchain.com/)

### Community
- [AWS Samples Repository](https://github.com/aws-samples/)
- [AgentCore Examples](https://github.com/aws-samples/amazon-bedrock-agentcore-examples)

## 🎉 Next Steps

### For First-Time Users
1. ✅ Read **README.md** (Core Components section)
2. ✅ Follow **sample-project/QUICKSTART.md**
3. ✅ Deploy your first agent
4. ✅ Customize for your use case

### For Production Deployments
1. ✅ Complete local development and testing
2. ✅ Read **DEPLOYMENT_GUIDE.md** fully
3. ✅ Set up monitoring and alerts
4. ✅ Configure CI/CD pipeline
5. ✅ Deploy with blue/green strategy

### For Advanced Users
1. ✅ Explore CDK infrastructure in `cdk/`
2. ✅ Implement custom tools and integrations
3. ✅ Set up multi-region deployment
4. ✅ Integrate with existing systems

## 💡 Tips

- **Start small:** Deploy the sample project as-is first
- **Test locally:** Use `agentcore dev` for rapid iteration
- **Run evals:** Use evaluation suite before every deploy
- **Monitor costs:** Check AWS Cost Explorer regularly
- **Read logs:** `agentcore logs` is your friend
- **Use traces:** Distributed tracing shows bottlenecks

## 🆘 Getting Help

**Issue:** Can't find something?  
**Solution:** Use the table of contents in each .md file

**Issue:** Don't understand a concept?  
**Solution:** Start with README.md Core Components

**Issue:** Deployment failing?  
**Solution:** Check DEPLOYMENT_GUIDE.md Troubleshooting

**Issue:** Want production best practices?  
**Solution:** See Best Practices in README.md

**Issue:** Need cost estimates?  
**Solution:** See Cost Optimization in README.md

---

**Ready to build? Start with: `cd sample-project && cat QUICKSTART.md`**
