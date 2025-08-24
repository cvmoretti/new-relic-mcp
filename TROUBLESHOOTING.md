# 🔧 Troubleshooting Guide

Complete troubleshooting guide for the New Relic MCP Server.

## 🚨 Quick Diagnostics

Run these commands first to identify the issue:

```bash
# Check container status
docker ps | grep newrelic-mcp

# Test MCP server
./run_mcp_docker.sh test

# View recent logs
./run_mcp_docker.sh logs
```

## 🐳 Docker Issues

### Container Not Running
**Symptoms:** `Container is not running` errors
```bash
# Check if Docker is running
docker info

# Start the container
./run_mcp_docker.sh run

# If build fails, clean up first
docker system prune -f
./run_mcp_docker.sh run
```

### Port Conflicts
**Symptoms:** Port binding errors during startup
```bash
# Find conflicting processes
lsof -i :8080

# Kill conflicting processes
sudo kill -9 <PID>

# Restart container
./run_mcp_docker.sh restart
```

### Out of Disk Space
**Symptoms:** `No space left on device` errors
```bash
# Clean up Docker resources
docker system prune -a -f

# Remove unused images
docker image prune -a -f

# Check available space
df -h
```

## 🔌 Cursor Integration Issues

### MCP Server Not Found
**Symptoms:** Cursor shows "No MCP servers" or tools not available

**Check configuration path:**
```bash
# Verify wrapper script exists and is executable
ls -la newrelic-mcp
chmod +x newrelic-mcp

# Test wrapper script directly
echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}}' | ./newrelic-mcp
```

**Cursor configuration:**
1. Ensure path is absolute: `/path/to/your/project/newrelic-mcp` (run `pwd` to get exact path)
2. Restart Cursor completely after config changes
3. Check Cursor MCP logs: View → Output → Model Context Protocol

### Tools Not Loading
**Symptoms:** "Found 0 tools" in Cursor MCP logs

```bash
# Verify container responds to tools/list
./run_mcp_docker.sh test

# Check container logs for errors
docker logs newrelic-mcp-server --tail 50

# Restart with fresh container
./run_mcp_docker.sh restart
```

### Connection Timeouts
**Symptoms:** Queries timeout or connection drops

```bash
# Increase container resources (if needed)
docker update --memory=1g --cpus=1.0 newrelic-mcp-server

# Check system resources
docker stats newrelic-mcp-server

# Restart container
./run_mcp_docker.sh restart
```

## 🔑 Authentication Issues

### New Relic API Key Invalid
**Symptoms:** "Unauthorized" or "Forbidden" errors

```bash
# Verify credentials in .env
cat .env

# Test API key manually
curl -H "Api-Key: YOUR_API_KEY" \
     "https://api.newrelic.com/v2/applications.json"

# Check CLI authentication inside container
docker exec newrelic-mcp-server newrelic profile list
```

### Account ID Mismatch
**Symptoms:** "Account not found" errors

```bash
# Verify account ID
docker exec newrelic-mcp-server newrelic account list

# Update .env with correct account ID
# Then restart container
./run_mcp_docker.sh restart
```

### Region Configuration
**Symptoms:** API connection issues, wrong region errors

```bash
# Check current region setting
grep NEW_RELIC_REGION .env

# Valid values: US, EU
# Update .env and restart if needed
```

## 📊 Query Issues

### NRQL Syntax Errors
**Symptoms:** "Syntax error" in query responses

**Common fixes:**
- Ensure proper quote escaping: `'single quotes'` not `"double quotes"`
- Use proper time format: `SINCE 1 hour ago` not `SINCE 1h`
- Verify attribute names: `appName` not `app_name`
- Include LIMIT clause for large datasets

**Test query in New Relic UI first:**
1. Go to New Relic Query Builder
2. Test your NRQL query
3. Copy working query to Cursor

### No Data Returned
**Symptoms:** Empty results or "No data available"

```bash
# Check data availability
echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "newrelic_query", "arguments": {"nrql": "SHOW EVENT TYPES SINCE 1 day ago"}}}' | ./newrelic-mcp

# Verify time range
SELECT count(*) FROM Transaction SINCE 1 week ago

# Check application names
SELECT uniques(appName) FROM Transaction SINCE 1 day ago
```

### Timeout Errors
**Symptoms:** Queries taking too long or timing out

**Optimization strategies:**
- Add time limits: `SINCE 1 hour ago` instead of `SINCE 1 week ago`
- Use LIMIT clause: `LIMIT 100`
- Avoid expensive operations on large datasets
- Use specific WHERE clauses to filter early

## 🔍 Performance Issues

### Slow Response Times
**Monitoring:**
```bash
# Check container performance
docker stats newrelic-mcp-server

# Monitor query execution time
time echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "newrelic_query", "arguments": {"nrql": "SELECT count(*) FROM Transaction SINCE 1 hour ago"}}}' | ./newrelic-mcp
```

**Optimization:**
```bash
# Restart container to clear any memory issues
./run_mcp_docker.sh restart

# Increase container resources if needed
docker update --memory=2g newrelic-mcp-server
```

### High Memory Usage
```bash
# Check memory usage
docker exec newrelic-mcp-server free -h

# Restart if memory usage is high
./run_mcp_docker.sh restart
```

## 📝 Logging and Debugging

### Enable Detailed Logging
```bash
# View live logs
./run_mcp_docker.sh logs

# Enable debug mode (edit mcp_docker_server.py)
# Change: logging.basicConfig(level=logging.INFO)
# To: logging.basicConfig(level=logging.DEBUG)
# Then rebuild: ./run_mcp_docker.sh run
```

### Common Log Messages

**✅ Normal Operation:**
```
INFO - Initializing newrelic-mcp-server v1.0.0
INFO - 🚀 New Relic MCP Server ready for Cursor connections
INFO - 📨 Received request: {"method":"tools/list"...
INFO - Sent tools list
```

**⚠️ Warning Signs:**
```
ERROR - Failed to parse JSON
ERROR - Command execution failed
ERROR - New Relic CLI error
```

**🚨 Critical Issues:**
```
ERROR - Container process died
ERROR - Cannot connect to New Relic API
ERROR - Authentication failed
```

## 🔄 Recovery Procedures

### Complete Reset
```bash
# Stop everything
./run_mcp_docker.sh stop

# Clean up Docker
docker system prune -f

# Remove old images
docker rmi newrelic-mcp:latest

# Fresh start
./run_mcp_docker.sh run
```

### Backup Configuration
```bash
# Backup working configuration
cp .env .env.backup
cp newrelic-mcp newrelic-mcp.backup

# Restore if needed
cp .env.backup .env
cp newrelic-mcp.backup newrelic-mcp
```

### Update to Latest Version
```bash
# Pull latest code
git pull origin main

# Rebuild with latest changes
./run_mcp_docker.sh run
```

## 🛠️ Advanced Debugging

### Container Shell Access
```bash
# Access container shell for debugging
docker exec -it newrelic-mcp-server /bin/bash

# Test New Relic CLI directly
newrelic nrql query --query "SELECT count(*) FROM Transaction SINCE 1 hour ago"

# Check environment variables
env | grep NEW_RELIC
```

### Network Issues
```bash
# Test network connectivity from container
docker exec newrelic-mcp-server ping google.com

# Check DNS resolution
docker exec newrelic-mcp-server nslookup api.newrelic.com

# Test API connectivity
docker exec newrelic-mcp-server curl -I https://api.newrelic.com
```

### MCP Protocol Debugging
```bash
# Test MCP protocol manually
echo '{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {}}}' | ./newrelic-mcp

# Validate JSON responses
echo '{"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}' | ./newrelic-mcp | jq '.'
```

## 📞 Getting Help

### Information to Gather
Before seeking help, collect:
1. **System info:** `uname -a` and Docker version
2. **Container logs:** `./run_mcp_docker.sh logs`
3. **Configuration:** `.env` file (redact sensitive data)
4. **Error messages:** Complete error text
5. **Steps to reproduce:** What you were doing when it failed

### Self-Diagnosis Checklist
- [ ] Docker is running
- [ ] Container starts successfully
- [ ] New Relic credentials are valid
- [ ] Cursor configuration path is correct
- [ ] No port conflicts
- [ ] Sufficient disk space
- [ ] Network connectivity works
- [ ] NRQL query syntax is valid

### Quick Fix Summary
```bash
# The "turn it off and on again" approach
./run_mcp_docker.sh stop
docker system prune -f
./run_mcp_docker.sh run

# Test everything works
./run_mcp_docker.sh test
```

**90% of issues are resolved by container restart and credential verification.**
