# Customer Support Agent - Quick Start Guide

This is a complete, production-ready customer support agent built with AWS AgentCore.

## Prerequisites

Before you begin, ensure you have:

1. **AWS Account** with appropriate permissions
2. **Node.js 20+** installed
3. **Python 3.10+** installed
4. **AWS CLI** configured
5. **AWS CDK v2** installed

## Local Setup (5 Minutes)

### 1. Install AgentCore CLI

```bash
npm install -g @aws/agentcore-cli
agentcore --version
```

### 2. Set Up Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your AWS account details
# Update AWS_REGION and AWS_ACCOUNT_ID
```

### 4. Test Locally

```bash
# Run the agent locally
python agent.py

# You should see test cases running with responses
```

## Deploy to AWS (10 Minutes)

### 1. Bootstrap CDK (One-Time)

```bash
# Replace with your account ID and region
cdk bootstrap aws://123456789012/us-east-1
```

### 2. Deploy the Agent

```bash
# Deploy to production
agentcore deploy --region us-east-1 --stage production

# Wait for deployment (~3-5 minutes)
# You'll get an endpoint URL when complete
```

### 3. Test Production Endpoint

```bash
# Invoke the production agent
agentcore invoke --payload '{
  "prompt": "How do I reset my password?",
  "user_id": "test_user"
}'
```

## Project Structure

```
customer-support-agent/
├── agent.py              # Main agent implementation
├── agentcore.yaml        # AgentCore configuration
├── requirements.txt      # Python dependencies
├── .env.example         # Environment template
├── tests/
│   ├── test_agent.py    # Unit tests
│   └── eval_suite.json  # Evaluation scenarios
└── QUICKSTART.md        # This file
```

## Key Features

✅ **Knowledge Base Search** - Searches documentation automatically  
✅ **Ticket Creation** - Creates support tickets for complex issues  
✅ **Memory Persistence** - Remembers user preferences across sessions  
✅ **Code Execution** - Can analyze data using Python  
✅ **Production Ready** - Includes observability, evaluations, and testing

## Next Steps

1. **Customize the Agent**
   - Edit the `system_prompt` in `agentcore.yaml`
   - Add custom tools in the `gateway` section
   - Adjust memory settings

2. **Add Real Knowledge Base**
   - Replace mock KB in `agent.py` with actual data source
   - Configure Lambda function or API endpoint
   - Update ARN in `agentcore.yaml`

3. **Set Up Monitoring**
   ```bash
   # View live logs
   agentcore logs --follow
   
   # View traces
   agentcore traces list
   
   # Open CloudWatch dashboard
   agentcore dashboard
   ```

4. **Run Evaluations**
   ```bash
   # Test agent accuracy before deployment
   agentcore eval --test-suite tests/eval_suite.json
   ```

## Common Commands

```bash
# Local development
agentcore dev                    # Start local dev server
python agent.py                  # Run local tests

# Testing
pytest tests/                    # Run unit tests
agentcore eval --test-suite tests/eval_suite.json  # Run evaluations

# Deployment
agentcore deploy --stage production  # Deploy to AWS
agentcore status                     # Check deployment status
agentcore rollback --version 1.0.0   # Rollback if needed

# Monitoring
agentcore logs --follow              # Live logs
agentcore traces list                # View traces
agentcore metrics --metric InvocationLatency
```

## Troubleshooting

**Error: AccessDeniedException**
```bash
# Add required IAM permissions
aws iam attach-user-policy \
  --user-name your-user \
  --policy-arn arn:aws:iam::aws:policy/AmazonBedrockFullAccess
```

**Error: Module not found**
```bash
# Ensure virtual environment is activated and dependencies installed
pip install -r requirements.txt
```

**High latency in production**
```bash
# Check CloudWatch metrics
agentcore metrics --metric InvocationLatency --period 3600
```

## Cost Estimate

For 10,000 conversations/month:
- Runtime: ~$30/month
- Memory: ~$2.50/month
- Gateway: ~$2/month
- Model Inference: ~$30/month

**Total: ~$65/month**

## Support

- [AWS AgentCore Documentation](https://docs.aws.amazon.com/bedrock-agentcore/)
- [Sample Projects](https://github.com/aws-samples/amazon-bedrock-agentcore-examples)
- [Community Slack](https://aws-agentcore.slack.com)

---

**Ready to deploy? Run `agentcore deploy --region us-east-1 --stage production`**
