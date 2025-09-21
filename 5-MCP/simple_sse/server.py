from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

load_dotenv(".env")

# Create an MCP server
mcp = FastMCP(
    name="Math Calculator",
    host="0.0.0.0",
    port=8055,
    stateless_http=True,
)


@mcp.tool()
def x_elevated_to_y(x: int, y: int) -> int:
    """Get the output of x^y"""
    return x ** y


# Run the server
if __name__ == "__main__":
    mcp.run(transport="sse")
