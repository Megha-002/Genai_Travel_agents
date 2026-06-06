from mcp.server.fastmcp import FastMCP

from tools.tavily_search import tavily_search
from tools.hotels_search import (
    search_hotels as _search_hotels
)


# Create MCP server
mcp = FastMCP("tavily")


@mcp.tool()
def search_web(query: str) -> str:
    """
    Search the web using Tavily.
    """

    result = tavily_search(query)

    return str(result)


@mcp.tool()
def search_hotels(
    destination: str,
    budget: int,
    dates: str
) -> str:
    """
    Search hotels using existing hotel search tool.
    """

    result = _search_hotels(
        destination,
        budget
    )

    return str(result)
print(
    search_web(
        "Top tourist attractions in Paris"
    )
)

if __name__ == "__main__":

    mcp.run(
        transport="stdio"
    )