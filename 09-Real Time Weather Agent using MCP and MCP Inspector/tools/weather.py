import urllib.request


def get_weather(location: str) -> str:
    """
    Fetches the weather for a given location.

    Args:
        location (str): The city of location name (e.g., "New York", "London").

    Returns:
        str: Concise weather information for the location.
    """

    try:
        url = f"https://wttr.in/{location}?format=3"
        with urllib.request.urlopen(url) as response:
            result = response.read().decode('utf-8').strip()
            return result
    except Exception as e:
        return f"Error: {e}"
    


