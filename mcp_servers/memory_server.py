import os

from dotenv import load_dotenv

from mem0 import MemoryClient

from mcp.server.fastmcp import FastMCP


# Load environment variables
load_dotenv()


# Create MCP server
mcp = FastMCP("memory")


# Initialize Mem0 client
client = MemoryClient(
    api_key=os.getenv("MEM0_API_KEY")
)


@mcp.tool()
def get_prefs(user_id: str) -> str:
    """
    Retrieve saved travel preferences.
    """

    try:

        memories = client.search(
            "preferences",
            filters={"AND": [{"user_id": user_id}]}
)

        if not memories:
            return "No preferences saved yet"

        results = []

        for memory in memories:

            # Mem0 returns dict objects
            if isinstance(memory, dict):

                text = memory.get("memory")

                if text:
                    results.append(text)

        if not results:
            return "No preferences saved yet"

        return "\n".join(results)

    except Exception as e:

        return (
            f"Error retrieving preferences: "
            f"{str(e)}"
        )


@mcp.tool()
def save_prefs(
    user_id: str,
    new_data: str
) -> str:
    """
    Save travel preferences.
    """

    try:

        client.add(
            new_data,
            user_id=user_id
        )

        return "Preferences saved successfully"

    except Exception as e:

        return (
            f"Error saving preferences: "
            f"{str(e)}"
        )


if __name__ == "__main__":

    # TEMP TESTS
    print(
        save_prefs(
            "test_user",
            "likes expensive hotels"
        )
    )

    print(
        get_prefs(
            "test_user"
        )
    )

    # Start MCP server
    mcp.run(
        transport="stdio"
    ) 