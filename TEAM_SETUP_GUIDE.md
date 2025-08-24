# 👥 Team Setup Guide - New Relic MCP Server

This guide helps your team members set up the New Relic MCP Server quickly and consistently.

## 🎯 Overview

The New Relic MCP Server allows anyone on your team to query New Relic data directly from Cursor IDE using natural language. No need to switch between tools or remember complex NRQL syntax.

## ⚡ 5-Minute Setup

### Step 1: Prerequisites Check

Ensure you have:
- [ ] **Docker Desktop** installed and running
- [ ] **Cursor IDE** installed  
- [ ] **New Relic Account** access (get credentials from your team lead)

### Step 2: Get the Code

```bash
# Clone or download the project
git clone <repository-url>
cd CursorProject

# Or download the ZIP and extract it
```

### Step 3: Configure New Relic Credentials

```bash
# Copy the environment template
cp config.env.example .env

# Edit .env with your team credentials
nano .env  # or use your preferred editor
```

**Required values:**
```env
NEW_RELIC_API_KEY=NRAK-XXXXXXXXXXXXXXXXXXXXXXXXXX
NEW_RELIC_ACCOUNT_ID=1234567
NEW_RELIC_REGION=US
```

> **🔑 Getting Credentials:** Ask your DevOps/SRE team for these values, or create them in [New Relic's API Keys page](https://one.newrelic.com/admin-portal/api-keys-ui/api-keys).

### Step 4: Start the Server

```bash
# Make the script executable and run
chmod +x run_mcp_docker.sh
./run_mcp_docker.sh run
```

**Expected output:**
```
🐳 New Relic MCP Server - Docker Runner
🔨 Building MCP Server Docker image...
✅ Image built successfully!
🚀 Starting MCP Server container (persistent mode)...
✅ MCP Server container started and running persistently!
📡 Server is ready to accept Cursor connections
```

### Step 5: Configure Cursor

1. **Open Cursor Settings:**
   - `Cursor → Settings → Features → Model Context Protocol`
   - Click **"Edit Configuration"**

2. **Add this configuration:**
   ```json
   {
     "mcpServers": {
       "newrelic": {
         "command": "/path/to/your/project/newrelic-mcp"
       }
     }
   }
   ```
   
   **To get your exact path:**
   ```bash
   # Navigate to your project directory and run:
   cd CursorProject  # or wherever you downloaded the project
   pwd
   # Use the output to replace "/path/to/your/project/" above
   ```

3. **Save and restart Cursor completely**

### Step 6: Test It Works

In Cursor, try asking:
> "Show me all New Relic applications"

or

> "Execute this NRQL query: SELECT count(*) FROM Transaction SINCE 1 hour ago"

## 🎯 Common Team Use Cases

### For Frontend Developers
- *"Show me browser performance metrics for the last hour"*
- *"Find JavaScript errors affecting users"*
- *"What's the page load time for our main application?"*

### For Backend Developers  
- *"Show me API endpoint response times"*
- *"Find database queries taking longer than 1 second"*
- *"List all 5xx errors from the last 30 minutes"*

### For DevOps/SRE
- *"Show me infrastructure alerts from the last hour"*
- *"What applications have the highest error rates?"*
- *"Monitor deployment impact on performance"*

### For Product Managers
- *"Show me user engagement metrics"*
- *"What are the most popular features being used?"*
- *"Analyze user journey completion rates"*

## 🔧 Team Best Practices

### Shared Credentials
- **Use team service account** for New Relic API key
- **Store credentials securely** (1Password, Vault, etc.)
- **Rotate keys regularly** following security policy

### Resource Management
```bash
# Check if your container is running
docker ps | grep newrelic-mcp

# Stop when not needed (saves resources)
./run_mcp_docker.sh stop

# Start when needed
./run_mcp_docker.sh start
```

### Query Guidelines
- **Start simple:** Use basic queries first
- **Be specific:** Include time ranges and limits
- **Ask follow-ups:** Build on previous results
- **Share queries:** Document useful queries in team wiki

## 🚨 Troubleshooting by Role

### **Developer Issues**

**❌ "No tools found in Cursor"**
```bash
# Check if container is running
docker ps | grep newrelic-mcp

# If not running, start it
./run_mcp_docker.sh run
```

**❌ "Queries return no data"**
- Check if your applications are sending data to New Relic
- Try broader time ranges: `SINCE 1 day ago`
- Verify application names: `SHOW EVENT TYPES`

### **DevOps Issues**

**❌ "Docker build fails"**
```bash
# Clean up and retry
docker system prune -f
./run_mcp_docker.sh run
```

**❌ "Permission denied"**
```bash
# Fix script permissions
chmod +x run_mcp_docker.sh newrelic-mcp
```

### **Manager Issues**

**❌ "Team not adopting the tool"**
- Share this guide and common use cases
- Schedule a 15-minute demo session
- Create team-specific query examples
- Add to onboarding checklist

## 📊 Team Monitoring

### Health Check Commands
```bash
# Verify everyone's setup
./run_mcp_docker.sh test

# Check resource usage
docker stats newrelic-mcp-server

# View activity logs
./run_mcp_docker.sh logs
```

### Usage Analytics
Track team adoption by asking:
- *"Show me query volume from our team applications"*
- *"What are the most monitored endpoints?"*
- *"Which team members are using New Relic most?"*

## 🎓 Learning Resources

### New to NRQL?
- [NRQL Tutorial](https://docs.newrelic.com/docs/query-your-data/nrql-new-relic-query-language/get-started/introduction-nrql-new-relics-query-language/)
- [NRQL Reference](https://docs.newrelic.com/docs/query-your-data/nrql-new-relic-query-language/get-started/nrql-syntax-clauses-functions/)

### Team Examples Repository
Create a shared document with your team's most useful queries:

**Common Queries:**
```sql
-- Application Health
SELECT count(*) FROM Transaction SINCE 1 hour ago FACET appName

-- Error Rates
SELECT percentage(count(*), WHERE error IS true) FROM Transaction SINCE 1 hour ago

-- Slow Transactions  
SELECT * FROM Transaction WHERE duration > 1 SINCE 1 hour ago LIMIT 10
```

## ✅ Success Checklist

- [ ] Docker container running successfully
- [ ] Cursor showing "Found 3 tools" in MCP logs
- [ ] Can execute basic NRQL queries
- [ ] Team credentials configured securely
- [ ] Bookmarked common queries
- [ ] Added to team onboarding process

## 🎉 You're Ready!

Your team can now analyze New Relic data directly from Cursor without context switching. Start with simple questions and build more complex analyses as you get comfortable.

**🚀 Pro Tip:** Create a team Slack channel to share interesting queries and findings!
