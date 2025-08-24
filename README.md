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

> **📖 First time setup?** See detailed instructions in [`INSTALLATION.md`](INSTALLATION.md)

### Prerequisites

- **Docker Desktop** installed and running
- **New Relic Account** with API access
- **Cursor IDE** with MCP support

### 1. Environment Setup

```bash
# Copy configuration template
cp config.env.example .env

# Edit with your New Relic credentials
# Add: NEW_RELIC_API_KEY, NEW_RELIC_ACCOUNT_ID, NEW_RELIC_REGION
```

### 2. Start the MCP Server

```bash
./run_mcp_docker.sh run
```

### 3. Configure Cursor

**Get your project path:**
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

### 1. **newrelic_query**
Execute custom NRQL queries for metrics, transactions, and analytics.

**Example Usage in Cursor:**
> "Execute this NRQL query: SELECT count(*) FROM Transaction SINCE 1 hour ago"

### 2. **newrelic_apps** 
List and search New Relic applications.

**Example Usage in Cursor:**
> "Show me all New Relic applications"

### 3. **newrelic_logs**
Search logs using NRQL queries.

**Example Usage in Cursor:**
> "Search New Relic logs: SELECT * FROM Log WHERE level = 'ERROR' SINCE 30 minutes ago LIMIT 10"

## 📊 Usage Examples

### Performance Analysis
- *"What's the average response time for my applications in the last hour?"*
- *"Show me the slowest transactions from the past 30 minutes"*
- *"Execute: SELECT percentile(duration, 95) FROM Transaction SINCE 1 day ago"*

### Error Investigation
- *"Find all errors in the last hour grouped by application"*
- *"Search for 500 errors: SELECT count(*) FROM TransactionError WHERE response.status = '500' SINCE 1 hour ago"*
- *"Show me recent critical log entries"*

### Application Monitoring
- *"List all applications with their transaction counts"*
- *"Find applications with high error rates"*
- *"Show me database query performance metrics"*

### Custom Analytics
- *"Execute: SELECT count(*) FROM PageView WHERE userAgentName = 'Chrome' SINCE 1 week ago"*
- *"Analyze user sessions by geography"*
- *"Monitor API endpoint performance trends"*

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

### Problem: "Container not running" Error
**Solution:**
```bash
./run_mcp_docker.sh run
```

### Problem: Cursor shows "No tools found"
**Solutions:**
1. Ensure container is running: `docker ps | grep newrelic-mcp`
2. Restart the container: `./run_mcp_docker.sh restart`
3. Restart Cursor completely
4. Verify configuration path is correct

### Problem: NRQL Queries Fail
**Solutions:**
1. Check credentials in `.env` file
2. Verify New Relic CLI authentication:
```bash
docker exec newrelic-mcp-server newrelic profile list
```
3. Test with simple query: `SELECT count(*) FROM Transaction SINCE 1 hour ago`

### Problem: Connection Issues
**Solutions:**
1. Check Docker is running: `docker info`
2. Rebuild container: `./run_mcp_docker.sh run`
3. View detailed logs: `./run_mcp_docker.sh logs`

## 📁 Project Structure

```
├── README.md                  # This documentation
├── mcp_docker_server.py       # Core MCP server implementation
├── Dockerfile.mcp             # Docker image definition
├── newrelic-mcp              # Cursor wrapper script
├── run_mcp_docker.sh         # Container management script
├── config.env.example        # Environment template
└── .env                      # Your credentials (create from template)
```

## 🔐 Security

- **Environment Variables**: Credentials stored in `.env` file, not in code
- **Docker Isolation**: Server runs in isolated container
- **No Local Dependencies**: New Relic CLI contained within Docker image
- **Non-root User**: Container runs with restricted privileges

## 🎯 Benefits

- **✅ Zero Local Setup** - Everything runs in Docker
- **✅ Persistent Container** - Always ready for connections
- **✅ Natural Language** - Ask questions in plain English
- **✅ Rich Responses** - Formatted JSON with insights
- **✅ Team Ready** - Easy to share and reproduce
- **✅ Production Ready** - Robust error handling and logging

## 🚀 Advanced Usage

### Custom NRQL Queries
You can execute any valid NRQL query:
```
"Execute: SELECT count(*) FROM Transaction WHERE response.status >= 400 SINCE 1 day ago FACET appName"
```

### Multi-step Analysis
Ask follow-up questions based on results:
```
1. "Show me error rates by application"
2. "Now drill down into the application with highest errors"
3. "What are the specific error messages for that app?"
```

### Performance Monitoring
```
"Create a performance dashboard query for my frontend app"
"Show me the P95 response time trends for the last week"
"Find slow database queries impacting user experience"
```

## 📞 Support

- **Container Issues**: Check Docker Desktop is running
- **Authentication Issues**: Verify New Relic API key and permissions
- **Query Issues**: Validate NRQL syntax in New Relic UI first
- **Cursor Issues**: Ensure MCP configuration path is absolute

## 🎉 Status

**✅ Production Ready** - Fully tested with real New Relic data  
**✅ Team Ready** - Comprehensive documentation included  
**✅ Cursor Integrated** - Native MCP protocol support  
**✅ Docker Isolated** - Zero impact on local development environment  

---

**🎯 Your New Relic data is now accessible directly from Cursor! Start asking questions about your application performance, errors, and user behavior using natural language.**