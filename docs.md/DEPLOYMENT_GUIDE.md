# AWS AgentCore Deployment Guide

Complete step-by-step guide for deploying your AgentCore agent to AWS production.

## Table of Contents
- [Pre-Deployment Checklist](#pre-deployment-checklist)
- [Deployment Methods](#deployment-methods)
- [Post-Deployment Verification](#post-deployment-verification)
- [Production Configuration](#production-configuration)
- [Monitoring & Observability](#monitoring--observability)
- [CI/CD Integration](#cicd-integration)
- [Troubleshooting](#troubleshooting)

---

## Pre-Deployment Checklist

### 1. AWS Account Readiness

```bash
# Verify AWS credentials
aws sts get-caller-identity

# Expected output:
# {
#     "UserId": "AIDACKCEVSQ6C2EXAMPLE",
#     "Account": "123456789012",
#     "Arn": "arn:aws:iam::123456789012:user/your-user"
# }

# Check region configuration
echo $AWS_DEFAULT_REGION
```

### 2. IAM Permissions

Ensure your IAM user/role has these permissions:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock-agentcore:*",
        "bedrock:InvokeModel",
        "bedrock:ListFoundationModels",
        "s3:CreateBucket",
        "s3:PutObject",
        "s3:GetObject",
        "cloudformation:*",
        "iam:PassRole",
        "iam:CreateRole",
        "iam:AttachRolePolicy",
        "lambda:CreateFunction",
        "lambda:InvokeFunction",
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents",
        "cloudwatch:PutMetricData"
      ],
      "Resource": "*"
    }
  ]
}
```

### 3. Model Access

```bash
# Request model access (if not already done)
aws bedrock list-foundation-models --region us-east-1

# If Claude is not available, request access in the AWS Console:
# Bedrock Console → Model access → Request access
```

### 4. Run Local Tests

```bash
cd sample-project

# Run unit tests
pytest tests/ -v

# Expected: All tests passing

# Run evaluations
agentcore eval --test-suite tests/eval_suite.json

# Expected: >80% pass rate
```

### 5. Update Configuration

Edit `agentcore.yaml`:

```yaml
# Replace placeholders
gateway:
  tools:
    - type: lambda
      arn: arn:aws:lambda:us-east-1:YOUR_ACCOUNT:function:kb-search  # ← Update this
```

---

## Deployment Methods

### Method 1: AgentCore CLI (Recommended)

**Best for:** Quick deployments, standard use cases

```bash
cd sample-project

# First-time deployment
agentcore deploy --region us-east-1 --stage production

# Output:
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
# Version: 1.0.0

# Save the endpoint URL for later use
export AGENT_ENDPOINT=https://xyz123.agentcore.us-east-1.amazonaws.com
```

**Deployment Options:**

```bash
# Deploy to specific region
agentcore deploy --region eu-west-1 --stage production

# Deploy with blue/green strategy
agentcore deploy --rollout-strategy blue_green --canary-percentage 10

# Deploy with custom timeout
agentcore deploy --timeout 7200  # 2 hours

# Deploy specific version
agentcore deploy --version 1.1.0
```

### Method 2: AWS CDK (For Advanced Use Cases)

**Best for:** Custom infrastructure, multi-stack deployments, complex networking

```bash
cd sample-project/cdk

# Install CDK dependencies
pip install -r requirements.txt

# Bootstrap CDK (one-time per account/region)
cdk bootstrap aws://123456789012/us-east-1

# Review changes
cdk diff

# Deploy the stack
cdk deploy CustomerSupportAgentStack

# You'll be prompted to approve IAM changes
# Type 'y' to proceed
```

### Method 3: AWS Console (Manual)

**Best for:** Learning, experimentation, visual configuration

1. Navigate to AWS Console → Bedrock → AgentCore
2. Click "Create Agent"
3. Upload your agent code (ZIP file)
4. Configure runtime, memory, and gateway settings
5. Deploy

---

## Post-Deployment Verification

### 1. Check Deployment Status

```bash
# Get agent status
agentcore status

# Expected output:
# Status: ACTIVE
# Version: 1.0.0
# Endpoint: https://xyz123.agentcore.us-east-1.amazonaws.com
# Last Updated: 2026-10-22T15:30:00Z
# Health: HEALTHY
```

### 2. Test the Production Endpoint

```bash
# Simple test
agentcore invoke --payload '{
  "prompt": "Hello, how can you help me?",
  "user_id": "test_user_production"
}'

# Expected: Valid response from agent

# Test knowledge base integration
agentcore invoke --payload '{
  "prompt": "How do I reset my password?",
  "user_id": "test_user_001"
}'

# Expected: Response from knowledge base
```

### 3. Verify Component Health

```bash
# Check memory
aws bedrock-agentcore describe-memory \
  --agent-name customer-support-agent \
  --region us-east-1

# Check gateway
aws bedrock-agentcore list-gateway-tools \
  --agent-name customer-support-agent \
  --region us-east-1
```

### 4. Review Initial Logs

```bash
# View recent logs
agentcore logs --since 10m

# Follow live logs
agentcore logs --follow

# Filter by error level
agentcore logs --filter ERROR --since 1h
```

---

## Production Configuration

### 1. Auto-Scaling Configuration

```yaml
# In agentcore.yaml
deployment:
  auto_scaling:
    min_capacity: 5      # Minimum instances
    max_capacity: 200    # Maximum instances
    target_utilization: 70  # CPU target %
    scale_in_cooldown: 300  # seconds
    scale_out_cooldown: 60  # seconds
```

Deploy the updated configuration:

```bash
agentcore deploy --update-config
```

### 2. Set Up Alarms

```bash
# High latency alarm
aws cloudwatch put-metric-alarm \
  --alarm-name customer-support-agent-high-latency \
  --alarm-description "Alert when P99 latency > 5s" \
  --metric-name InvocationLatency \
  --namespace AWS/BedrockAgentCore \
  --statistic Average \
  --period 300 \
  --threshold 5000 \
  --comparison-operator GreaterThanThreshold \
  --evaluation-periods 2 \
  --dimensions Name=AgentName,Value=customer-support-agent

# Error rate alarm
aws cloudwatch put-metric-alarm \
  --alarm-name customer-support-agent-high-errors \
  --alarm-description "Alert when error rate > 5%" \
  --metric-name ErrorRate \
  --namespace AWS/BedrockAgentCore \
  --statistic Average \
  --period 300 \
  --threshold 5 \
  --comparison-operator GreaterThanThreshold \
  --evaluation-periods 2 \
  --dimensions Name=AgentName,Value=customer-support-agent
```

### 3. Configure Memory Persistence

```bash
# Verify memory configuration
aws bedrock-agentcore describe-memory \
  --agent-name customer-support-agent \
  --region us-east-1

# Update retention if needed
aws bedrock-agentcore update-memory \
  --agent-name customer-support-agent \
  --retention-days 90 \
  --region us-east-1
```

---

## Monitoring & Observability

### 1. CloudWatch Dashboard

```bash
# Create dashboard using CLI
agentcore dashboard create --name customer-support-prod

# Or open in console
agentcore dashboard open
```

### 2. Key Metrics to Monitor

| Metric | Threshold | Action |
|--------|-----------|--------|
| InvocationLatency (P99) | > 5s | Investigate bottlenecks |
| ErrorRate | > 5% | Check logs for errors |
| ThrottlingRate | > 0.1% | Increase capacity |
| TokenConsumption | Trending up | Review prompt efficiency |
| MemoryUsage | > 85% | Scale up memory |

### 3. View Distributed Traces

```bash
# List recent traces
agentcore traces list --limit 20

# View specific trace
agentcore traces get --trace-id abc123xyz

# Filter slow traces
agentcore traces list --filter "duration > 3000" --limit 10
```

### 4. Set Up X-Ray Integration

```yaml
# In agentcore.yaml
observability:
  tracing: enabled
  export_traces_to:
    - cloudwatch
    - xray  # Enable X-Ray
  sampling_rate: 0.1  # Sample 10% of requests
```

---

## CI/CD Integration

### GitHub Actions Example

Create `.github/workflows/deploy-agent.yml`:

```yaml
name: Deploy AgentCore Agent

on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  test-and-deploy:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      
      - name: Install dependencies
        run: |
          pip install -r sample-project/requirements.txt
          npm install -g @aws/agentcore-cli
      
      - name: Run tests
        run: |
          cd sample-project
          pytest tests/ -v
      
      - name: Run evaluations
        run: |
          cd sample-project
          agentcore eval --test-suite tests/eval_suite.json
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          AWS_REGION: us-east-1
      
      - name: Deploy to production
        if: success()
        run: |
          cd sample-project
          agentcore deploy --region us-east-1 --stage production
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
```

### GitLab CI Example

Create `.gitlab-ci.yml`:

```yaml
stages:
  - test
  - deploy

variables:
  AWS_REGION: us-east-1

test:
  stage: test
  image: python:3.12
  script:
    - cd sample-project
    - pip install -r requirements.txt
    - pytest tests/ -v
    - npm install -g @aws/agentcore-cli
    - agentcore eval --test-suite tests/eval_suite.json

deploy:
  stage: deploy
  image: python:3.12
  script:
    - npm install -g @aws/agentcore-cli
    - cd sample-project
    - agentcore deploy --region $AWS_REGION --stage production
  only:
    - main
```

---

## Troubleshooting

### Issue 1: Deployment Fails with "AccessDeniedException"

**Cause:** Insufficient IAM permissions

**Solution:**
```bash
# Attach required policy
aws iam attach-user-policy \
  --user-name your-user \
  --policy-arn arn:aws:iam::aws:policy/AmazonBedrockFullAccess

# Or create custom policy (see IAM Permissions section above)
```

### Issue 2: Agent Returns 500 Errors

**Cause:** Runtime error in agent code or misconfigured tools

**Solution:**
```bash
# Check logs
agentcore logs --filter ERROR --since 1h

# Common fixes:
# 1. Verify Lambda function ARNs in agentcore.yaml
# 2. Check model ID is correct
# 3. Ensure agent code has no syntax errors
```

### Issue 3: High Latency (>5s)

**Cause:** Inefficient prompts, tool calls, or insufficient resources

**Solution:**
```bash
# View trace breakdown
agentcore traces list --filter "duration > 5000"

# Check component latency
agentcore metrics --metric ComponentLatency --dimensions Component=Gateway

# Optimize:
# 1. Reduce prompt size
# 2. Cache frequent tool responses
# 3. Use faster model for classification steps
# 4. Increase runtime memory in agentcore.yaml
```

### Issue 4: Memory Not Persisting

**Cause:** Memory component not properly configured

**Solution:**
```yaml
# In agentcore.yaml, ensure:
memory:
  long_term: true  # Must be enabled
  retention_days: 90

# Redeploy
agentcore deploy --update-config
```

### Issue 5: Tools Not Being Called

**Cause:** Tool definitions not properly registered with gateway

**Solution:**
```bash
# Verify tools are registered
aws bedrock-agentcore list-gateway-tools \
  --agent-name customer-support-agent

# Check tool definitions match expected format
# Ensure Lambda functions have correct permissions
```

---

## Blue/Green Deployment Strategy

### 1. Deploy Canary Version

```bash
# Deploy v1.1.0 with 10% traffic
agentcore deploy \
  --version 1.1.0 \
  --rollout-strategy blue_green \
  --canary-percentage 10 \
  --canary-duration-minutes 60
```

### 2. Monitor Canary Metrics

```bash
# Compare metrics between versions
agentcore metrics compare \
  --version-a 1.0.0 \
  --version-b 1.1.0 \
  --metric ErrorRate,Latency
```

### 3. Promote or Rollback

```bash
# If canary looks good, promote to 100%
agentcore promote --version 1.1.0

# If issues detected, rollback
agentcore rollback --version 1.0.0
```

---

## Production Checklist

Before going live:

- [ ] All tests passing (unit tests + evaluations)
- [ ] IAM permissions configured correctly
- [ ] Model access granted in Bedrock
- [ ] CloudWatch alarms configured
- [ ] Monitoring dashboard set up
- [ ] Auto-scaling configured
- [ ] CI/CD pipeline tested
- [ ] Load testing completed
- [ ] Rollback procedure documented
- [ ] On-call team trained

---

## Additional Resources

- [AgentCore CLI Reference](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/cli.html)
- [Production Best Practices](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/best-practices.html)
- [Cost Optimization Guide](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/cost-optimization.html)

**Ready for production? Start with: `agentcore deploy --region us-east-1 --stage production`**
