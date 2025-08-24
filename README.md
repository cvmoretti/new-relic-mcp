# 🚀 New Relic MCP Server

A **Model Context Protocol (MCP)** server that enables seamless New Relic integration directly within Cursor IDE. Execute NRQL queries, search logs, and monitor applications without leaving your development environment.

## ✨ Features

- **🔍 NRQL Query Execution** - Run custom New Relic queries directly from Cursor
- **📊 Application Monitoring** - List and search New Relic applications
- **📝 Log Analysis** - Search and analyze logs using NRQL
- **🐳 Docker Containerized** - Fully isolated with zero local dependencies
- **🔄 Persistent Container** - Runs continuously, ready for Cursor connections
- **🛡️ Secure** - Environment-based credential management

## 🏗️ Architecture

```
Cursor IDE ↔ MCP Protocol ↔ Docker Container ↔ New Relic CLI ↔ New Relic API
```

The server acts as a bridge between Cursor and New Relic, translating natural language requests into NRQL queries and returning formatted results.

## 🚀 Quick Start

### Prerequisites

- **Docker Desktop** installed and running
- **New Relic Account** with API access
- **Cursor IDE** with MCP support

### 1. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/cvmoretti/new-relic-mcp.git
cd new-relic-mcp

# Copy configuration template
cp config.env.example .env

# Edit .env with your New Relic credentials
# Required: NEW_RELIC_API_KEY, NEW_RELIC_ACCOUNT_ID, NEW_RELIC_REGION
```

### 2. Start the MCP Server

```bash
chmod +x run_mcp_docker.sh newrelic-mcp
./run_mcp_docker.sh run
```

### 3. Configure Cursor

Get your project path:
```bash
pwd  # Copy this output
```

**Cursor → Settings → Features → Model Context Protocol → Edit Configuration:**
```json
{
  "mcpServers": {
    "newrelic": {
      "command": "/YOUR/PROJECT/PATH/newrelic-mcp"
    }
  }
}
```

Replace `/YOUR/PROJECT/PATH/` with the output from `pwd`.

### 4. Restart Cursor

Completely restart Cursor IDE to activate the MCP integration.

## 🛠️ Available Tools

### 1. **newrelic_query** - Execute NRQL queries
**Example:** *"Execute this NRQL query: SELECT count(*) FROM Transaction SINCE 1 hour ago"*

### 2. **newrelic_apps** - List applications  
**Example:** *"Show me all New Relic applications"*

### 3. **newrelic_logs** - Search logs
**Example:** *"Search New Relic logs: SELECT * FROM Log WHERE level = 'ERROR' SINCE 30 minutes ago LIMIT 10"*

## 📊 Common NRQL Queries

### Performance Monitoring
```sql
-- Average response time by application
SELECT average(duration) FROM Transaction SINCE 1 hour ago FACET appName

-- 95th percentile response times
SELECT percentile(duration, 95) FROM Transaction SINCE 1 day ago FACET appName

-- Slowest transactions
SELECT * FROM Transaction WHERE duration > 1 SINCE 1 hour ago LIMIT 20
```

### Error Analysis
```sql
-- Error rate by application
SELECT percentage(count(*), WHERE error IS true) FROM Transaction SINCE 1 hour ago FACET appName

-- Most common errors
SELECT count(*) FROM TransactionError SINCE 1 day ago FACET error.message LIMIT 10

-- 4xx and 5xx errors
SELECT count(*) FROM Transaction WHERE response.status >= 400 SINCE 1 hour ago FACET response.status
```

### Infrastructure Metrics
```sql
-- CPU usage by host
SELECT average(cpuPercent) FROM SystemSample SINCE 1 hour ago FACET hostname

-- Memory usage trends
SELECT average(memoryUsedPercent) FROM SystemSample SINCE 1 day ago TIMESERIES 1 hour
```

## 💬 Usage Examples

### Performance Analysis
- *"What's the average response time for my applications in the last hour?"*
- *"Show me the slowest transactions from the past 30 minutes"*
- *"Find applications with high error rates"*

### Error Investigation
- *"Find all errors in the last hour grouped by application"*
- *"Search for 500 errors in the past day"*
- *"Show me recent critical log entries"*

### Business Intelligence
- *"What are the most popular API endpoints?"*
- *"Show me user session analysis for today"*
- *"Monitor deployment impact on performance"*

## 🔧 Management Commands

```bash
# Check container status
docker ps | grep newrelic-mcp

# View server logs
./run_mcp_docker.sh logs

# Restart the server
./run_mcp_docker.sh restart

# Stop the server
./run_mcp_docker.sh stop

# Show Cursor configuration
./run_mcp_docker.sh config
```

## 🚨 Troubleshooting

### Common Issues

**❌ "Container not running"**
```bash
./run_mcp_docker.sh run
```

**❌ "No tools found in Cursor"**
1. Check container: `docker ps | grep newrelic-mcp`
2. Restart container: `./run_mcp_docker.sh restart`
3. Restart Cursor completely
4. Verify configuration path is absolute

**❌ "NRQL Queries fail"**
1. Check credentials in `.env` file
2. Test with simple query: `SELECT count(*) FROM Transaction SINCE 1 hour ago`
3. Verify account access in New Relic UI

**❌ "Authentication failed"**
1. Verify `NEW_RELIC_API_KEY` is correct
2. Check `NEW_RELIC_ACCOUNT_ID` matches your account
3. Ensure API key has proper permissions

### Getting Your Credentials

1. **API Key**: [New Relic API Keys page](https://one.newrelic.com/admin-portal/api-keys-ui/api-keys)
2. **Account ID**: Found in New Relic URL or account dropdown
3. **Region**: `US` or `EU` depending on your New Relic region

## 📁 Project Structure

```
├── README.md                    # This documentation
├── mcp_docker_server.py         # Core MCP server implementation
├── Dockerfile.mcp               # Docker image definition
├── newrelic-mcp                 # Cursor wrapper script
├── run_mcp_docker.sh           # Container management script
├── config.env.example          # Environment template
└── cursor-mcp-config.json      # Cursor configuration template
```

## 🔐 Security

- **Environment Variables**: Credentials stored in `.env` file, not in code
- **Docker Isolation**: Server runs in isolated container
- **No Local Dependencies**: New Relic CLI contained within Docker image
- **Non-root User**: Container runs with restricted privileges

## 🎯 Benefits

- **✅ Zero Local Setup** - Everything runs in Docker
- **✅ Natural Language** - Ask questions in plain English
- **✅ Real-time Insights** - Immediate data access from Cursor
- **✅ Team Ready** - Easy setup and reproducible environment
- **✅ Production Ready** - Robust error handling and logging

## 📞 Support

1. **Check container status**: `./run_mcp_docker.sh test`
2. **View logs**: `./run_mcp_docker.sh logs`
3. **Restart everything**: `./run_mcp_docker.sh restart`
4. **Test NRQL in New Relic UI** before using in Cursor

## 🚀 Advanced Usage

### Team Deployment
- Share the repository URL
- Each team member follows Quick Start
- Use shared New Relic service account credentials

### Custom Queries
- Start with simple queries and build complexity
- Use `LIMIT` clauses to avoid large result sets  
- Include time ranges (`SINCE`) for better performance

---

**🎯 Your New Relic data is now accessible directly from Cursor! Start asking questions about your application performance, errors, and user behavior using natural language.**