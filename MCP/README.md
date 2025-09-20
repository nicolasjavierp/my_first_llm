# MCP (Model Control Protocol) Directory

Core infrastructure for LLM tool integration and orchestration:

## Key Components
- **client.py**: SSE client for MCP server communication
  - Tool discovery/execution
  - Async query processing pipeline
  - Ollama model integration
- **server.py**: MCP server implementation
  - Tool registration/management
  - SSE transport handling
- **Docker Support**: 
  - Dockerfile for containerized deployment
  - docker-compose.yaml for local development

## Dependencies
- AsyncIO
- Ollama Python client
- SSE client library
- Python-dotenv

## Usage
```python
from MCP.client import MCPSSEClient

async def main():
    client = MCPSSEClient()
    await client.connect_to_server()
    response = await client.process_query("Your query here")
