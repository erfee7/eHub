# src/main.py

from fastapi import FastAPI
from starlette.requests import Request
from mcp.server import Server
from mcp.server.sse import SseServerTransport
from typing import Any
import mcp.types as types

from src.tools.image_gen import IMAGE_GEN_TOOL, handle_image_gen

# Initialize FastAPI and the MCP Server
app = FastAPI(title="Unified MCP Hub")
mcp = Server("unified-mcp-hub")

# Registry: Expose tools to the LLM
@mcp.list_tools()
async def list_tools() -> list[types.Tool]:
    return [IMAGE_GEN_TOOL]

# Router: Direct tool calls to their respective handlers
@mcp.call_tool()
async def call_tool(name: str, arguments: dict) -> list[Any]:
    if name == "generate_image":
        return await handle_image_gen(arguments)
    raise ValueError(f"Unknown tool: {name}")

# Standard MCP SSE Setup
sse_transport = SseServerTransport("/messages")

@app.get("/sse")
async def endpoint_sse(request: Request):
    """Initial connection endpoint for LibreChat"""
    async with sse_transport.connect_sse(request.scope, request.receive, request._send) as streams:
        await mcp.run(*streams, mcp.create_initialization_options())

@app.post("/messages")
async def endpoint_messages(request: Request):
    """Subsequent endpoint for transmitting MCP data"""
    # Simply forward the POST request logic to the established transport
    await sse_transport.handle_post_message(request.scope, request.receive, request._send)