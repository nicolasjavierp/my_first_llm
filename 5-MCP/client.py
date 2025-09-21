import asyncio
import json
import logging
from typing import Any, Dict, List, Optional
from dotenv import load_dotenv
from ollama import AsyncClient
from mcp.client.sse import sse_client
from mcp import ClientSession
from contextlib import AsyncExitStack

logging.basicConfig(level=logging.INFO)
my_logger = logging.getLogger(__name__)

model_name = "llama3.1:8b"
ollama_client = AsyncClient(host='http://localhost:11434')

load_dotenv(".env")

class MCPSSEClient:
    """Client for interacting with Ollama models using SSE MCP server."""

    def __init__(self, server_url: str = "http://localhost:8055/sse/"):
        """Initialize the SSE MCP client."""
        self.server_url = server_url
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()

    async def connect_to_server(self):
        """Connect to the SSE MCP server."""
        try:
            # Connect using SSE transport
            sse_transport = await self.exit_stack.enter_async_context(
                sse_client(self.server_url)
            )
            read_stream, write_stream = sse_transport
            self.session = await self.exit_stack.enter_async_context(
                ClientSession(read_stream, write_stream)
            )
            await self.session.initialize()
            # List available tools
            tools_result = await self.session.list_tools()
            print("\nConnected to SSE server with tools:")
            for tool in tools_result.tools:
                print(f"  - {tool.name}: {tool.description}")

        except Exception as e:
            print(f"Failed to connect to SSE server: {e}")
            raise

    async def get_mcp_tools(self) -> List[Dict[str, Any]]:
        """Get available tools from the MCP server in standard format."""
        if not self.session:
            raise RuntimeError("Not connected to server")
            
        tools_result = await self.session.list_tools()
        return [
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.inputSchema,
                },
            }
            for tool in tools_result.tools
        ]

    async def process_query(self, query: str) -> str:
        """Process a query using the LLM and available MCP tools."""
        if not self.session:
            raise RuntimeError("Not connected to server")

        # Get available tools
        tools = await self.get_mcp_tools()

        # Initial Ollama API call
        response = await ollama_client.chat(
            model=model_name,
            messages=[{"role": "user", "content": query}],
            tools=tools,
            #tool_choice="auto"
        )

        # Get assistant's response
        assistant_response = response['message']

        # Initialize conversation with user query and assistant response
        messages = [
            {"role": "user", "content": query},
            assistant_response,
        ]

        # Handle tool calls if present
        if assistant_response.get('tool_calls'):
            # Process each tool call
            for i, tool_call in enumerate(assistant_response.tool_calls):
                try:
                    if isinstance(tool_call.function.arguments, str):
                        arguments = json.loads(tool_call.function.arguments)
                    else:
                        arguments = tool_call.function.arguments
                    
                    print(f"Calling tool: {tool_call.function.name} with args: {arguments}")
                    
                    # Call the tool via MCP
                    result = await self.session.call_tool(
                        tool_call.function.name,
                        arguments=arguments,
                    )

                    # Extract text content from result
                    content = ""
                    if hasattr(result, 'content') and result.content:
                        if isinstance(result.content[0], dict):
                            content = result.content[0].get('text', str(result.content[0]))
                        elif hasattr(result.content[0], 'text'):
                            content = result.content[0].text
                        else:
                            content = str(result.content[0])
                    else:
                        content = str(result)

                    print(f"Tool result: {content}...")  # Just 200 chars {content[:200]}

                    # Adding a tool_call_id if it doesn't exist OpenAI vs Ollama compatibility
                    tool_call_id = getattr(tool_call, 'id', f"tool_call_{i}")

                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_call_id,
                            "content": content,
                        }
                    )
                    
                except Exception as e:
                    print(f"Error calling tool {tool_call.function.name}: {e}")
                    tool_call_id = getattr(tool_call, 'id', f"tool_call_{i}")
                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_call_id,
                            "content": f"Error: {str(e)}",
                        }
                    )

            # Get final response with tool results
            final_response = await ollama_client.chat(
                model=model_name,
                messages=messages,
                tools=tools,
                #tool_choice="none"  # No more tool calls
            )

            return final_response['message']['content']

        # No tool calls, just return the direct response
        return assistant_response.get('content', 'No response content')

    async def cleanup(self):
        """Clean up resources."""
        await self.exit_stack.aclose()


async def main():
    """Main entry point for the SSE client."""
    client = MCPSSEClient()
    
    try:
        await client.connect_to_server()
        query = "What is Nick's favorite movie?"
        print(f"\nQuery: {query}")
        response = await client.process_query(query)
        print(f"\nResponse: {response}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await client.cleanup()


if __name__ == "__main__":
    asyncio.run(main())