from google.adk.agents import Agent 
from google.adk.runners import Runner
from google.adk.sessions import Session
from google.adk.memory import InMemoryMemoryService
from dotenv import load_dotenv

load_dotenv()

root_agent_model = "gemini-2.0-flash-exp"
sub_agent_model = "gemini-2.0-flash"


session_service = InMemoryMemoryService()

APP_NAME = "First Application to Test"
USER_ID = "user_1"
SESSION_ID = "session_001"

session = Session(
    app_name=APP_NAME,
    user_id=USER_ID,
    id =SESSION_ID
)

session = session_service.add_session_to_memory(session = session)



def say_hello(name: str = "there") -> str:
    """Provides a simple greeting, optionally addressing the user by name.

    Args:
        name (str, optional): The name of the person to greet. Defaults to "there".

    Returns:
        str: A friendly greeting message.
    """
    print(f"--- Tool: say_hello called with name: {name} ---")
    return f"Hello, {name}!"


def say_goodbye() -> str:
    """Provides a simple farewell message to conclude the conversation."""
    print(f"--- Tool: say_goodbye called ---")
    return "Goodbye! Have a great day."



def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city.

    Args:
        city (str): The name of the city for which to retrieve the weather report.

    Returns:
        dict: status and result or error msg.
    """
    if city.lower() == "new york":
        return {
            "status": "success",
            "report": (
                "The weather in New York is sunny with a temperature of 25 degrees "
                "Celsius (41 degrees Fahrenheit)."
            ),
        }
    
    else:
        return {
            "status": "error",
            "error_message": f"Weather information for '{city}' is not available."
        }
    



greeting_agent = Agent(
    # Using a potentially different/cheaper model for a simple task
    model=sub_agent_model,
    name="greeting_agent",
    instruction="You are the Greeting Agent. Your ONLY task is to provide a friendly greeting.\n"
                "Use the 'say_hello' tool to generate the greeting.\n"
                "If the user provides their name, make sure to pass it to the tool.\n"
                "Do not engage in any other conversation or tasks.",
    description="Handles simple greetings and hellos using the 'say_hello' tool.",
    tools=[say_hello],
)




farewell_agent = Agent(
    # Can use the same or a different model
    model=sub_agent_model,
    name="farewell_agent",
    instruction="You are the Farewell Agent. Your ONLY task is to provide a polite farewell message.\n"
                "Use the 'say_goodbye' tool when the user indicates they are leaving\n"
                "(e.g., using words like 'bye', 'goodbye', 'thanks bye', 'see you').\n"
                "Do not perform any other actions.",
    description="Handles simple farewells and goodbyes using the 'say_goodbye' tool.",
    tools=[say_goodbye],
)



root_agent = Agent(
    name="Root_Agent",
    model=root_agent_model,
    description="The main coordinator agent. Handles weather requests and delegates greetings/farewells to specialists.",
    instruction="You are the main Weather Agent coordinating a team. Your primary responsibility is to provide weather information.\n"
                "Use the 'get_weather' tool ONLY for specific weather requests (e.g., 'weather in London').\n"
                "You have specialized sub-agents:\n"
                "1. 'greeting_agent': Handles simple greetings like 'Hi', 'Hello'. Delegate to it for these.\n"
                "2. 'farewell_agent': Handles simple farewells like 'Bye', 'See you'. Delegate to it for these.\n"
                "Analyze the user's query. If it's a greeting, delegate to 'greeting_agent'. If it's a farewell, delegate to 'farewell_agent'.\n"
                "If it's a weather request, handle it yourself using 'get_weather'.\n"
                "For anything else, respond appropriately or state you cannot handle it.",

    tools=[get_weather],
    sub_agents=[greeting_agent, farewell_agent]
)


runner_root = Runner(
    app_name=APP_NAME,
    session_service=session,
    agent=root_agent
)