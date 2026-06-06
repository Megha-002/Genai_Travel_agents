import os
import requests

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP


load_dotenv()


# Create MCP server
mcp = FastMCP("weather")


OPENWEATHER_API_KEY = os.getenv(
    "OPENWEATHER_API_KEY"
)


@mcp.tool()
def get_forecast(
    destination: str,
    dates: str
) -> str:
    """
    Get weather forecast for a destination.
    """

    url = "http://api.openweathermap.org/data/2.5/forecast"

    params = {
        "q": destination,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
    }

    response = requests.get(
        url,
        params=params
    )

    data = response.json()

    # Basic validation
    if response.status_code != 200:

        return (
            f"ERROR:\n"
            f"Status Code: {response.status_code}\n"
            f"Response: {data}"
    )

    forecasts = data.get("list", [])

    if not forecasts:
        return f"No forecast available for {destination}"

    # Use first forecast entry
    first_forecast = forecasts[0]

    temperature = first_forecast["main"]["temp"]

    weather_description = first_forecast[
        "weather"
    ][0]["description"]

    result = (
        f"Weather in {destination} "
        f"for {dates}: "
        f"{temperature}°C, "
        f"{weather_description}"
    )

    return result
print(
    get_forecast(
        "Paris",
        "Oct 10-15"
    )
)
if __name__ == "__main__":

    mcp.run(
        transport="stdio"
    )