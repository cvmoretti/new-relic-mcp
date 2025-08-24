#!/usr/bin/env python3

import asyncio
import json
import logging
import subprocess
import sys
import os
from typing import Any, Dict, List, Optional

# Configure logging to stderr (MCP uses stdout for protocol communication)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger(__name__)

class NewRelicMCPServer:
    """
    Model Context Protocol Server for New Relic integration
    Optimized for Docker container communication
    """
    
    def __init__(self):
        self.server_info = {
            "name": "newrelic-mcp-server",
            "version": "1.0.0"
        }
        logger.info(f"Initializing {self.server_info['name']} v{self.server_info['version']}")

    def execute_newrelic_command(self, command: List[str]) -> Dict[str, Any]:
        """Execute New Relic CLI command safely"""
        try:
            # Add environment variables for New Relic CLI
            env = os.environ.copy()
            if "NEW_RELIC_API_KEY" in env and "NEW_RELIC_ACCOUNT_ID" in env:
                command.extend(["--accountId", env["NEW_RELIC_ACCOUNT_ID"]])
            
            logger.info(f"Executing command: {' '.join(command)}")
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=30,
                check=True,
                env=env
            )
            
            # Try to parse as JSON, otherwise return as text
            try:
                data = json.loads(result.stdout.strip()) if result.stdout.strip() else {}
                return {
                    "success": True,
                    "data": data,
                    "raw_output": result.stdout.strip()
                }
            except json.JSONDecodeError:
                return {
                    "success": True,
                    "data": {"message": result.stdout.strip()},
                    "raw_output": result.stdout.strip()
                }
                
        except subprocess.CalledProcessError as e:
            logger.error(f"Command failed with exit code {e.returncode}: {e.stderr}")
            return {
                "success": False,
                "error": f"New Relic CLI error: {e.stderr}",
                "details": e.stderr
            }
        except subprocess.TimeoutExpired:
            error_msg = "New Relic CLI command timed out"
            logger.error(error_msg)
            return {
                "success": False,
                "error": error_msg
            }
        except Exception as e:
            error_msg = f"Command execution failed: {str(e)}"
            logger.error(error_msg)
            return {
                "success": False,
                "error": error_msg
            }

    async def run(self):
        """Main MCP server loop - keeps running continuously"""
        logger.info("🚀 New Relic MCP Server ready for Cursor connections...")
        logger.info("📡 Listening on stdin for MCP protocol messages...")
        
        try:
            while True:
                try:
                    # Read JSON-RPC request from stdin (blocking)
                    line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
                    
                    # If stdin is closed, keep the server running
                    if not line:
                        logger.info("📭 No input received, continuing to listen...")
                        await asyncio.sleep(1)
                        continue
                        
                    line = line.strip()
                    if not line:
                        continue
                    
                    logger.info(f"📨 Received request: {line[:100]}...")
                    
                    try:
                        request = json.loads(line)
                    except json.JSONDecodeError as e:
                        logger.error(f"❌ Failed to parse JSON: {e}")
                        continue
                    
                    # Handle the request
                    response = await self.handle_request(request)
                    
                    # Skip response for notifications
                    if response is None:
                        continue
                    
                    # Add request ID to response
                    if "id" in request:
                        response["id"] = request["id"]
                    
                    # Send JSON-RPC response to stdout
                    response_json = json.dumps(response)
                    print(response_json, flush=True)
                    logger.info(f"📤 Sent response: {response_json[:100]}...")
                    
                except EOFError:
                    logger.info("📭 EOF received, but keeping server alive...")
                    await asyncio.sleep(1)
                    continue
                except Exception as e:
                    logger.error(f"❌ Error in main loop: {e}")
                    error_response = {
                        "jsonrpc": "2.0",
                        "error": {
                            "code": -32603,
                            "message": f"Internal error: {str(e)}"
                        }
                    }
                    if "request" in locals() and "id" in request:
                        error_response["id"] = request["id"]
                    print(json.dumps(error_response), flush=True)
                    
        except KeyboardInterrupt:
            logger.info("🛑 Server stopped by user")
        except Exception as e:
            logger.error(f"❌ Critical server error: {e}")
            raise

    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming MCP request with proper JSON-RPC format"""
        method = request.get("method")
        params = request.get("params", {})
        
        response = {
            "jsonrpc": "2.0"
        }
        
        # Handle notifications (no response needed)
        if method == "notifications/initialized":
            logger.info("Received initialized notification")
            return None  # No response for notifications
            
        elif method == "initialize":
            response["result"] = {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": self.server_info
            }
            logger.info("Sent initialize response")
            
        elif method == "tools/list":
            response["result"] = {
                "tools": [
                    {
                        "name": "newrelic_query",
                        "description": "Execute NRQL queries in New Relic to get metrics, logs, and application data",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "nrql": {
                                    "type": "string",
                                    "description": "NRQL query to execute (e.g., 'SELECT count(*) FROM Transaction SINCE 1 hour ago')"
                                }
                            },
                            "required": ["nrql"]
                        }
                    },
                    {
                        "name": "newrelic_apps",
                        "description": "Search for New Relic applications",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "name": {
                                    "type": "string", 
                                    "description": "Application name to search for (optional)"
                                }
                            },
                            "required": []
                        }
                    },
                    {
                        "name": "newrelic_logs",
                        "description": "Search logs in New Relic using NRQL",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "query": {
                                    "type": "string",
                                    "description": "NRQL query for log search"
                                }
                            },
                            "required": ["query"]
                        }
                    }
                ]
            }
            logger.info("Sent tools list")
            
        elif method == "tools/call":
            tool_name = params.get("name")
            arguments = params.get("arguments", {})
            
            logger.info(f"Tool call: {tool_name}")
            
            if tool_name == "newrelic_query":
                nrql = arguments.get("nrql")
                if nrql:
                    result = self.execute_newrelic_command(["newrelic", "nrql", "query", "--query", nrql])
                    if result["success"]:
                        response["result"] = {
                            "content": [
                                {
                                    "type": "text", 
                                    "text": f"📊 **NRQL Query Result**\n\n**Query:** `{nrql}`\n\n```json\n{json.dumps(result['data'], indent=2)}\n```"
                                }
                            ]
                        }
                    else:
                        response["result"] = {
                            "content": [
                                {
                                    "type": "text",
                                    "text": f"❌ **Query Failed**\n\n**Error:** {result['error']}\n\n**Query:** `{nrql}`"
                                }
                            ],
                            "isError": True
                        }
                else:
                    response["error"] = {"code": -32602, "message": "NRQL query is required"}
                    
            elif tool_name == "newrelic_apps":
                result = self.execute_newrelic_command(["newrelic", "apm", "application", "search"])
                if result["success"]:
                    response["result"] = {
                        "content": [
                            {
                                "type": "text",
                                "text": f"🚀 **New Relic Applications**\n\n```json\n{json.dumps(result['data'], indent=2)}\n```"
                            }
                        ]
                    }
                else:
                    response["result"] = {
                        "content": [
                            {
                                "type": "text", 
                                "text": f"❌ **Application Search Failed**\n\n**Error:** {result['error']}"
                            }
                        ],
                        "isError": True
                    }
                    
            elif tool_name == "newrelic_logs":
                query = arguments.get("query")
                if query:
                    result = self.execute_newrelic_command(["newrelic", "nrql", "query", "--query", query])
                    if result["success"]:
                        response["result"] = {
                            "content": [
                                {
                                    "type": "text",
                                    "text": f"🔍 **New Relic Logs**\n\n**Query:** `{query}`\n\n```json\n{json.dumps(result['data'], indent=2)}\n```"
                                }
                            ]
                        }
                    else:
                        response["result"] = {
                            "content": [
                                {
                                    "type": "text",
                                    "text": f"❌ **Log Search Failed**\n\n**Error:** {result['error']}\n\n**Query:** `{query}`"
                                }
                            ],
                            "isError": True
                        }
                else:
                    response["error"] = {"code": -32602, "message": "Log query is required"}
                    
            else:
                response["error"] = {"code": -32601, "message": f"Unknown tool: {tool_name}"}
                
        else:
            response["error"] = {"code": -32601, "message": f"Method not found: {method}"}
        
        return response

def main():
    """Main entry point"""
    server = NewRelicMCPServer()
    
    try:
        asyncio.run(server.run())
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
