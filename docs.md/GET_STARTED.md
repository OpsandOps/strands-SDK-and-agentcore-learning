# 🚀 Get Started with AWS AgentCore

**Welcome!** Choose the path that's right for you:

---

## ⚡ QUICK PATHS

### 🆕 Complete Beginner? → [SIMPLE_START.md](SIMPLE_START.md)

**Perfect if:**
- This is your first AI agent
- You want something simple that works
- 30 minutes to deployed agent
- Uses Strands SDK (easiest framework)

**Start here:** [SIMPLE_START.md](SIMPLE_START.md)

---

### 🎓 Want Hands-On Learning? → [TUTORIAL.md](TUTORIAL.md)

**Perfect if:**
- You learn by doing
- Want step-by-step guidance
- 1 hour comprehensive tutorial
- Covers local dev → deployment → monitoring

**Start here:** [TUTORIAL.md](TUTORIAL.md)

---

### ⚡ Just Deploy Now? → [sample-project/QUICKSTART.md](sample-project/QUICKSTART.md)

**Perfect if:**
- You're experienced with AI/ML
- Want to deploy in 15 minutes
- Already know the concepts
- Need quick command reference

**Start here:** [sample-project/QUICKSTART.md](sample-project/QUICKSTART.md)

---

### 📖 Need Full Reference? → [README.md](README.md)

**Perfect if:**
- Want to understand all features
- Planning production deployment
- Need architectural details
- Reference for all 12 components

**Start here:** [README.md](README.md)

---

## 🎯 Not Sure Which Path?

**Answer these questions:**

1. **Is this your first AI agent project?**
   - Yes → Go to [SIMPLE_START.md](SIMPLE_START.md)
   - No → Continue to question 2

2. **Do you have 1+ hours to learn properly?**
   - Yes → Go to [TUTORIAL.md](TUTORIAL.md)
   - No → Go to [sample-project/QUICKSTART.md](sample-project/QUICKSTART.md)

3. **Are you deploying to production?**
   - Yes → Read [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) after getting started
   - No → Just pick any path above!

---

## ⚡ Absolute Fastest Start (5 Minutes)

**Want to see it work RIGHT NOW?**

```bash
# 1. Go to sample project
cd sample-project

# 2. Set up Python
python -m venv venv
venv\Scripts\activate              # Windows
# OR
source venv/bin/activate           # Mac/Linux

# 3. Install and run
pip install strands-agents boto3
python agent.py

# Done! You just ran an AI agent locally! ✨
```

**What just happened?**
- You ran a simple chatbot locally
- No AWS needed yet
- Check the output to see agent responses

**Next step:** Read [SIMPLE_START.md](SIMPLE_START.md) to understand what you did and deploy to AWS

---

## 📖 The 3-Step Learning Path

### Step 1: Understand the Basics (30 minutes)

**What to read:** [README.md](README.md) - Core Components section

**What you'll learn:**
- What is AWS AgentCore?
- The 12 core components
- How they work together

**Key takeaways:**
- AgentCore = Production AI agent platform
- No infrastructure management
- Works with any framework (LangGraph, CrewAI, etc.)

### Step 2: Build & Test Locally (30 minutes)

**What to follow:** [TUTORIAL.md](TUTORIAL.md) - Parts 1 & 2

**What you'll do:**
- Install prerequisites
- Set up development environment
- Run the sample agent locally
- Write and run tests

**Key takeaways:**
- Agent code uses LangGraph
- Configuration in `agentcore.yaml`
- Tests ensure quality before deployment

### Step 3: Deploy to AWS (30 minutes)

**What to follow:** [TUTORIAL.md](TUTORIAL.md) - Parts 3 & 4

**What you'll do:**
- Deploy to AWS with one command
- Test production endpoint
- Set up monitoring
- View logs and metrics

**Key takeaways:**
- Deployment is simple: `agentcore deploy`
- Full observability out of the box
- Production-ready from day one

---

## 🎯 Your First Hour Roadmap

```
Minutes 0-15: Setup
├─ Install Node.js, Python, AWS CLI
├─ Install AgentCore CLI
└─ Configure AWS credentials

Minutes 15-30: Local Testing
├─ Clone/explore sample project
├─ Run agent locally
└─ Review code structure

Minutes 30-45: Deployment
├─ Configure agentcore.yaml
├─ Deploy to AWS
└─ Verify deployment

Minutes 45-60: Monitoring
├─ View CloudWatch logs
├─ Check metrics
└─ Test production endpoint
```

Follow [TUTORIAL.md](TUTORIAL.md) for detailed instructions.

---

## 💼 For Different Roles

### 👨‍💻 Developers
**Your path:** QUICKSTART → TUTORIAL → Customize

**Start here:**
1. [sample-project/QUICKSTART.md](sample-project/QUICKSTART.md) - Get it running (15 min)
2. Review `agent.py` - Understand implementation
3. Modify `agentcore.yaml` - Customize behavior
4. Redeploy and test

**Key files for you:**
- `agent.py` - Agent logic
- `agentcore.yaml` - Configuration
- `tests/test_agent.py` - Unit tests

### 👷 DevOps Engineers
**Your path:** README → DEPLOYMENT_GUIDE → CI/CD

**Start here:**
1. [README.md](README.md) - Understand architecture (30 min)
2. [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - Production deployment (1 hour)
3. Set up monitoring and alarms
4. Implement CI/CD pipeline

**Key files for you:**
- `DEPLOYMENT_GUIDE.md` - All deployment options
- `sample-project/cdk/` - Infrastructure as code
- `.github/workflows/` - CI/CD examples (in DEPLOYMENT_GUIDE.md)

### 🏢 Architects
**Your path:** README → PROJECT_OVERVIEW → Architecture Decisions

**Start here:**
1. [README.md](README.md) - Complete overview (1 hour)
2. [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) - Project structure (20 min)
3. Review architecture diagrams
4. Understand cost models

**Key topics for you:**
- Component architecture
- Scaling strategies
- Cost optimization
- Security model

### 📊 Product Managers
**Your path:** README intro → TUTORIAL → Capabilities

**Start here:**
1. [README.md](README.md) - "What is AgentCore?" section (15 min)
2. [TUTORIAL.md](TUTORIAL.md) - See it in action (1 hour)
3. Understand capabilities and limitations
4. Review cost estimates

**Key sections for you:**
- Use cases
- Capabilities demo
- Cost breakdown
- Time to market

---

## 🎓 Learning Resources

### Official Documentation
- **AWS AgentCore Docs:** https://docs.aws.amazon.com/bedrock-agentcore/
- **Amazon Bedrock:** https://docs.aws.amazon.com/bedrock/
- **LangGraph:** https://langchain-ai.github.io/langgraph/

### This Repository
- **Complete Guide:** [README.md](README.md) - 12,000 words covering everything
- **Step-by-Step:** [TUTORIAL.md](TUTORIAL.md) - 1-hour hands-on tutorial
- **Quick Reference:** [sample-project/QUICKSTART.md](sample-project/QUICKSTART.md) - Command cheatsheet
- **Production Guide:** [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - Enterprise deployment
- **Project Structure:** [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) - Navigate the code
- **Documentation Map:** [INDEX.md](INDEX.md) - Find what you need

### Sample Code
- **Full Implementation:** `sample-project/agent.py` - 480 lines, fully commented
- **Configuration:** `sample-project/agentcore.yaml` - Production-ready config
- **Tests:** `sample-project/tests/` - Unit tests + evaluation suite
- **Infrastructure:** `sample-project/cdk/` - CDK stack (optional)

---

## ❓ Common Questions

### "What is AWS AgentCore?"
Amazon Bedrock AgentCore is AWS's platform for deploying production AI agents. Think of it as "serverless for AI agents" - you write agent code, AWS handles hosting, scaling, memory, tools, and monitoring.

→ Read more: [README.md](README.md) - Introduction section

### "Why should I use AgentCore vs. building my own?"
- No infrastructure management (no EC2, no load balancers)
- Built-in memory across sessions
- Tool connectivity out of the box
- Production observability included
- Pay only for active compute time

→ Read more: [README.md](README.md) - Core Components section

### "What frameworks does it support?"
All of them! AgentCore runs your code, so you can use:
- LangGraph (sample project uses this)
- CrewAI
- LlamaIndex
- Strands Agents
- Custom frameworks
- Plain Python/TypeScript

→ See sample: `sample-project/agent.py`

### "How much does it cost?"
For 10,000 conversations/month: ~$65
- Runtime: $30 (only pay for active compute)
- Memory: $2.50
- Gateway: $2
- Model inference: $30

→ Read more: [README.md](README.md) - Cost Optimization section

### "How long does deployment take?"
- Local testing: 5 minutes
- First AWS deployment: 3-5 minutes
- Subsequent deployments: 1-2 minutes

→ Try it: [sample-project/QUICKSTART.md](sample-project/QUICKSTART.md)

### "Can I use it with OpenAI/Anthropic/Google models?"
Yes! AgentCore supports:
- Amazon Bedrock models (Claude, Llama, etc.)
- OpenAI (GPT-4, GPT-3.5)
- Google Gemini
- Any OpenAI-compatible API

→ Configure: `agentcore.yaml` - harness.model section

### "Is it production-ready?"
Yes! AgentCore reached GA (General Availability) in 2026. It includes:
- Auto-scaling
- Blue/green deployments
- Full observability
- SLA guarantees
- Enterprise support

→ Read more: [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

---

## 🛠️ Prerequisites Checklist

Before you start, make sure you have:

### Required (Must Have)
- [ ] **AWS Account** - [Create one](https://aws.amazon.com/free/)
- [ ] **Node.js 20+** - [Download](https://nodejs.org/)
- [ ] **Python 3.10+** - [Download](https://www.python.org/downloads/)
- [ ] **AWS CLI** - [Install guide](https://aws.amazon.com/cli/)
- [ ] **AWS credentials configured** - Run `aws configure`

### Recommended (Nice to Have)
- [ ] **VS Code** or your preferred code editor
- [ ] **Git** for version control
- [ ] **Docker** (optional, for local testing)
- [ ] **Basic Python knowledge**
- [ ] **Basic AWS knowledge**

### AWS Permissions Needed
- [ ] `bedrock-agentcore:*`
- [ ] `bedrock:InvokeModel`
- [ ] `s3:*` (for artifact storage)
- [ ] `cloudwatch:*` (for monitoring)
- [ ] `iam:PassRole` (for execution roles)

→ Full setup guide: [TUTORIAL.md](TUTORIAL.md) - Part 1

---

## 🎯 What You'll Build

The sample project is a **Customer Support Agent** that can:

✅ **Answer questions** using a knowledge base  
✅ **Create tickets** for complex issues  
✅ **Remember users** across conversations  
✅ **Execute code** for data analysis  
✅ **Handle multi-turn** conversations intelligently

**Real-world use cases:**
- Customer support chatbots
- IT helpdesk assistants
- Sales qualification agents
- Documentation Q&A systems
- Internal knowledge base assistants

**Architecture:**
- LangGraph for workflow orchestration
- AgentCore Memory for context persistence
- AgentCore Gateway for tool integration
- Claude 3.5 Sonnet for language understanding
- CloudWatch for observability

---

## 🚀 Ready to Start?

### Option 1: I want to learn everything (Best for first-timers)
```
1. Read README.md (30 min)
2. Follow TUTORIAL.md (1 hour)
3. Explore sample-project/ (30 min)
4. Customize for your use case (1+ hours)
```

### Option 2: I want to deploy now (Best for experienced devs)
```
1. Follow sample-project/QUICKSTART.md (15 min)
2. Skim README.md core concepts (15 min)
3. Deploy and test (15 min)
4. Read DEPLOYMENT_GUIDE.md as needed
```

### Option 3: I'm evaluating AgentCore (Best for decision makers)
```
1. Read README.md introduction (15 min)
2. Review architecture diagrams
3. Check cost estimates (README.md)
4. Run sample-project locally (15 min)
```

---

## 📞 Need Help?

### While Learning
- Check [INDEX.md](INDEX.md) to find specific topics
- Review troubleshooting sections in each guide
- Search for error messages in documentation

### Technical Issues
- Check [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - Troubleshooting section
- Review CloudWatch logs: `agentcore logs --filter ERROR`
- Check AWS service health dashboard

### Best Practices
- See [README.md](README.md) - Best Practices section
- Review [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - Production Checklist
- Study the sample implementation in `sample-project/`

---

## 🎉 You're Ready!

Pick your starting point above and dive in. 

**Remember:**
- Start simple - deploy the sample first
- Test locally before deploying to AWS
- Use evaluation suite before production
- Monitor metrics from day one

**Most importantly:** Have fun building! AI agents are powerful, and AgentCore makes them production-ready.

---

**Quick Links:**
- 📖 [Full Guide](README.md)
- ⚡ [Quick Start](sample-project/QUICKSTART.md)
- 🎓 [Tutorial](TUTORIAL.md)
- 🏢 [Production Deployment](DEPLOYMENT_GUIDE.md)
- 🗺️ [Project Structure](PROJECT_OVERVIEW.md)
- 📚 [Documentation Index](INDEX.md)

**Let's build something amazing! 🚀**
