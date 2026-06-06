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

        # 1. Use get_all() instead of search() to fetch the full profile

        # 2. Use the correct v3 filter syntax

        memories = client.get_all(

            filters={"user_id": user_id}

        )
 
        if not memories:

            return "No preferences saved yet"
 
        # 3. Extract the list from the 'results' dictionary key

        if isinstance(memories, dict):

            memory_list = memories.get("results", [])

        else:

            memory_list = memories  # Fallback
 
        results = []

        for memory in memory_list:

            if isinstance(memory, dict):

                text = memory.get("memory")

                if text:

                    results.append(text)
 
        if not results:

            return "No preferences saved yet"
 
        return "\n".join(results)
 
    except Exception as e:

        return f"Error retrieving preferences: {str(e)}"
 
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

        return f"Error saving preferences: {str(e)}"
 
if __name__ == "__main__":

    # TEMP TESTS

    print(
        save_prefs(
        "test_user_1",
        "likes beach resorts at bay"
    )
)

 
 
    print(

        get_prefs(

            "test_user_1"

        )

    )
 
    # Start MCP server

    mcp.run(

        transport="stdio"

    )
 