# 🚀 Installation Guide - New Relic MCP Server

**Complete step-by-step installation for team members**

## 📋 Prerequisites

Before starting, ensure you have:

- ✅ **Docker Desktop** installed and running
- ✅ **Cursor IDE** installed
- ✅ **New Relic account** with API access

## ⚡ Installation Steps

### Step 1: Download the Project

```bash
# Option A: Clone from repository
git clone <repository-url>
cd <project-directory>

# Option B: Download ZIP file
# Extract the ZIP file to your desired location
cd /path/to/extracted/project
```

### Step 2: Get Your Project Path

```bash
# Navigate to your project directory
cd <your-project-directory>

# Get the absolute path (copy this output)
pwd
```

**Example output:** `/Users/john/Downloads/CursorProject`

### Step 3: Configure New Relic Credentials

```bash
# Copy the template
cp config.env.example .env

# Edit with your credentials
nano .env
# or
code .env
# or use any text editor
```

**Add your team's New Relic credentials:**
```env
NEW_RELIC_API_KEY=NRAK-XXXXXXXXXXXXXXXXXXXXXXXXXX
NEW_RELIC_ACCOUNT_ID=1234567
NEW_RELIC_REGION=US
```

> **🔑 Need credentials?** Ask your DevOps/SRE team or create them at [New Relic API Keys](https://one.newrelic.com/admin-portal/api-keys-ui/api-keys)

### Step 4: Start the MCP Server

```bash
# Make scripts executable
chmod +x run_mcp_docker.sh newrelic-mcp

# Build and start the server
./run_mcp_docker.sh run
```

**Expected output:**
```
🐳 New Relic MCP Server - Docker Runner
🔨 Building MCP Server Docker image...
✅ Image built successfully!
🚀 Starting MCP Server container (persistent mode)...
✅ MCP Server container started and running persistently!
```

### Step 5: Configure Cursor

1. **Open Cursor MCP Settings:**
   ```
   Cursor → Settings → Features → Model Context Protocol → Edit Configuration
   ```

2. **Use your project path from Step 2:**
   ```json
   {
     "mcpServers": {
       "newrelic": {
         "command": "/Users/john/Downloads/CursorProject/newrelic-mcp"
       }
     }
   }
   ```
   
   **⚠️ Important:** Replace `/Users/john/Downloads/CursorProject` with YOUR actual path from Step 2!

3. **Save the configuration**

4. **Completely restart Cursor**

### Step 6: Test the Integration

In Cursor, try asking:

> "Show me all New Relic applications"

or

> "Execute this NRQL query: SELECT count(*) FROM Transaction SINCE 1 hour ago"

You should see formatted New Relic data returned directly in Cursor!

## 🎯 Verification Checklist

After installation, verify everything works:

- [ ] Docker container is running: `docker ps | grep newrelic-mcp`
- [ ] MCP server responds: `./run_mcp_docker.sh test`
- [ ] Cursor shows "Found 3 tools" in MCP logs
- [ ] Can execute simple queries in Cursor
- [ ] Queries return real New Relic data

## 🚨 Common Installation Issues

### Issue: "Command not found: docker"
**Solution:** Install Docker Desktop from [docker.com](https://www.docker.com/products/docker-desktop/)

### Issue: "Permission denied" on scripts
**Solution:** 
```bash
chmod +x run_mcp_docker.sh newrelic-mcp
```

### Issue: "Container fails to start"
**Solution:**
```bash
# Check Docker is running
docker info

# View detailed error
./run_mcp_docker.sh logs
```

### Issue: "API authentication failed"
**Solution:** Verify credentials in `.env` file match your New Relic account

### Issue: "Cursor doesn't find tools"
**Solutions:**
1. Check the path in Cursor configuration is absolute and correct
2. Restart Cursor completely
3. Verify container is running: `docker ps | grep newrelic-mcp`

## 🎉 Success Indicators

✅ **Container Status:** `Up X minutes (healthy)`  
✅ **Cursor Logs:** `Found 3 tools and 0 prompts`  
✅ **Query Test:** Returns formatted New Relic data  
✅ **No Errors:** Clean logs in container and Cursor  

## 📞 Need Help?

1. **Check the logs:** `./run_mcp_docker.sh logs`
2. **Review troubleshooting guide:** `TROUBLESHOOTING.md`
3. **Test individual components:** Use provided test commands
4. **Ask your team:** Share error messages for faster resolution

---

**🎯 After successful installation, you'll be able to query New Relic data using natural language directly from Cursor!**
