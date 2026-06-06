from mcp_servers.weather_server import (
    get_forecast
)

from mcp_servers.tavily_server import (
    search_web,
    search_hotels
)

from mcp_servers.memory_server import (
    get_prefs,
    save_prefs
)


# Unified MCP Tool Registry
TOOL_REGISTRY = {

    "tavily": {

        "search_web": search_web,

        "search_hotels": search_hotels
    },

    "weather": {

        "get_forecast": get_forecast
    },

    "memory": {

        "get_prefs": get_prefs,

        "save_prefs": save_prefs
    }
}


def call_tool(
    server_name: str,
    tool_name: str,
    arguments: dict
):
    """
    Unified MCP tool caller.

    Parameters:
        server_name: MCP server name
        tool_name: Tool function name
        arguments: Dictionary of tool arguments

    Returns:
        Tool response
    """

    # Validate server
    if server_name not in TOOL_REGISTRY:

        return (
            f"Unknown server: "
            f"{server_name}"
        )

    # Validate tool
    if tool_name not in TOOL_REGISTRY[server_name]:

        return (
            f"Unknown tool: "
            f"{tool_name}"
        )

    # Get tool function
    tool_function = TOOL_REGISTRY[
        server_name
    ][tool_name]

    try:

        # Execute tool dynamically
        result = tool_function(
            **arguments
        )

        return result

    except Exception as e:

        return (
            f"Tool execution error: "
            f"{str(e)}"
        )


if __name__ == "__main__":

    # Tavily Test
    print("\nTAVILY TEST:\n")

    tavily_result = call_tool(
        "tavily",
        "search_web",
        {
            "query": "Top things to do in Paris"
        }
    )

    print(tavily_result)

    # Weather Test
    print("\nWEATHER TEST:\n")

    weather_result = call_tool(
        "weather",
        "get_forecast",
        {
            "destination": "Paris",
            "dates": "Oct 10-15"
        }
    )

    print(weather_result)

    # Memory Save Test
    print("\nMEMORY SAVE TEST:\n")

    memory_save = call_tool(
        "memory",
        "save_prefs",
        {
            "user_id": "test_user",
            "new_data": "likes luxury resorts"
        }
    )

    print(memory_save)

    # Memory Get Test
    print("\nMEMORY GET TEST:\n")

    memory_get = call_tool(
        "memory",
        "get_prefs",
        {
            "user_id": "test_user"
        }
    )

    print(memory_get)