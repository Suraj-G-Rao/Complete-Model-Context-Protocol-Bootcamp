"""
client_sse.py

This file implements an MCP client that connects to an MCP server using SSE (Server-Sent Events) transport.
SSE is a technology that allows a server to push real-time updates to a client over a single, persistent HTTP connection.
Unlike websockets, SSE provides one-way communication from the server to the client, which is useful for streaming updates.

This client also uses Google's Gemini SDK for AI model integration. The Gemini API can perform natural language processing
tasks and, when needed, call external tools (in this case, MCP tools) to perform specific functions.

A stream manager (or stream context) in this code is responsible for managing the lifecycle of the SSE connection,
ensuring that the connection is properly opened and closed. We use asynchronous context managers to handle these resources safely.
"""

import asyncio            # For asynchronous programming
import os                 # For accessing environment variables
import sys                # For command-line argument handling
import json               # For JSON processing
from typing import Optional  # For type annotations, e.g., indicating that a variable may be None

# Import ClientSession from the MCP package. This object manages communication with the MCP server.
from mcp import ClientSession

# Import the SSE client helper. This is assumed to be an asynchronous context manager that provides the connection streams.
# These streams represent the channels over which data is sent and received via SSE.
from mcp.client.sse import sse_client

# Import components from the Gemini SDK for AI-based function calling and natural language processing.
from google import genai
from google.genai import types
from google.genai.types import Tool, FunctionDeclaration
from google.genai.types import GenerateContentConfig

# Import dotenv to load environment variables from a .env file (e.g., API keys).
from dotenv import load_dotenv

# Load environment variables from the .env file so that our API keys and other settings are available.
load_dotenv()


class MCPClient:
    def __init__(self):
        """
        Initialize the MCP client.
        
        This constructor sets up:
         - The Gemini AI client using an API key from the environment variables.
         - Placeholders for the client session and the stream context (which manages the SSE connection).
        
        The Gemini client is used to generate content (e.g., processing user queries) and can request to call tools.
        """
        # Placeholder for the MCP session that will manage communication with the MCP server.
        self.session: Optional[ClientSession] = None
        
        # These will hold our context managers for the SSE connection.
        self._streams_context = None  # Manages the SSE stream lifecycle
        self._session_context = None  # Manages the MCP session lifecycle

        # Retrieve the Gemini API key from environment variables.
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        if not gemini_api_key:
            raise ValueError("GEMINI_API_KEY not found. Please add it to your .env file.")

        # Initialize the Gemini client with the API key. This client is used to communicate with the Gemini AI models.
        self.genai_client = genai.Client(api_key=gemini_api_key)

    async def connect_to_sse_server(self, server_url: str):
        """
        Connect to an MCP server that uses SSE transport.
        
        Steps performed in this function:
         1. Open an SSE connection using the provided server URL.
         2. Use the connection streams to create an MCP ClientSession.
         3. Initialize the MCP session, which sets up the protocol for communication.
         4. Retrieve and display the list of available tools from the MCP server.
        
        Args:
            server_url (str): The URL of the MCP server that supports SSE.
        """
        # 1. Open an SSE connection to the server.
        #    The sse_client function returns an async context manager that yields the streams (data channels) for communication.
        self._streams_context = sse_client(url=server_url)
        # Enter the asynchronous context to get the streams. This ensures proper resource management.
        streams = await self._streams_context.__aenter__()
        # 'streams' is expected to be a tuple (like (reader, writer)) that the ClientSession can use.

        # 2. Create an MCP ClientSession using the streams provided by the SSE connection.
        #    The ClientSession object handles sending and receiving messages following the MCP protocol.
        self._session_context = ClientSession(*streams)
        self.session: ClientSession = await self._session_context.__aenter__()

        # 3. Initialize the MCP session.
        #    This step typically sends an initialization message to the server to negotiate capabilities and start the protocol.
        await self.session.initialize()

        # 4. Retrieve and list available tools from the MCP server.
        #    This helps confirm that the connection is working and shows what functions or tools are available.
        print("Initialized SSE client...")
        print("Listing tools...")
        response = await self.session.list_tools()
        tools = response.tools
        print("\nConnected to server with tools:", [tool.name for tool in tools])

        # Convert the MCP tool definitions to a format compatible with the Gemini API for function calling.
        self.function_declarations = convert_mcp_tools_to_gemini(tools)

    async def cleanup(self):
        """
        Clean up resources by properly closing the SSE session and stream contexts.
        
        As we used asynchronous context managers (which are like 'with' blocks for async code), we need to manually call their exit methods.
        This ensures that all network connections and resources are gracefully closed when the client is finished.
        """
        # If the MCP session context was created, exit it to close the session.
        if self._session_context:
            await self._session_context.__aexit__(None, None, None)
        # If the SSE stream context was created, exit it to close the underlying SSE connection.
        if self._streams_context:
            await self._streams_context.__aexit__(None, None, None)

    async def process_query(self, query: str) -> str:
        """
        Process a user query using the Gemini API. If Gemini requests a tool call (via function calling),
        this function will call the tool on the MCP server and send the result back to Gemini for a final response.
        
        Steps:
         1. Format the user's query as a structured content object.
         2. Send the query to Gemini and include available MCP tool declarations.
         3. Check if Gemini's response contains a function call; if so, execute the tool and send back the response.
         4. Return the final processed text from Gemini.
        
        Args:
            query (str): The input query from the user.
        
        Returns:
            str: The final text response generated by the Gemini model.
        """
        # 1. Create a Gemini Content object representing the user's query.
        #    This object includes a role (user) and the query text wrapped in a part.
        user_prompt_content = types.Content(
            role='user',
            parts=[types.Part.from_text(text=query)]
        )

        # 2. Send the query to the Gemini model.
        #    We include available tool declarations so Gemini knows it can request function calls.
        response = self.genai_client.models.generate_content(
            model='gemini-2.0-flash-001',  # Name of the Gemini model to use.
            contents=[user_prompt_content],
            config=types.GenerateContentConfig(
                tools=self.function_declarations,  # Pass in the list of MCP tools formatted for Gemini.
            ),
        )

        # Prepare a list to accumulate the final response text.
        final_text = []

        # 3. Process each candidate response from Gemini.
        for candidate in response.candidates:
            if candidate.content.parts:  # Ensure that the response has parts (sections).
                for part in candidate.content.parts:
                    # If the part includes a function call, Gemini is asking us to run an MCP tool.
                    if part.function_call:
                        # Extract the name of the tool and its arguments from the function call.
                        tool_name = part.function_call.name
                        tool_args = part.function_call.args
                        print(f"\n[Gemini requested tool call: {tool_name} with args {tool_args}]")

                        # Attempt to call the specified tool on the MCP server.
                        try:
                            result = await self.session.call_tool(tool_name, tool_args)
                            # Wrap the result in a dictionary under the key "result".
                            function_response = {"result": result.content}
                        except Exception as e:
                            # If an error occurs, capture the error message.
                            function_response = {"error": str(e)}

                        # Create a Gemini function response part using the result of the tool call.
                        function_response_part = types.Part.from_function_response(
                            name=tool_name,
                            response=function_response
                        )

                        # Wrap the function response part in a Content object marked as coming from a tool.
                        function_response_content = types.Content(
                            role='tool',
                            parts=[function_response_part]
                        )

                        # 4. Send the original query, the function call, and the tool response back to Gemini.
                        #    Gemini will process this combined input to generate the final answer.
                        response = self.genai_client.models.generate_content(
                            model='gemini-2.0-flash-001',
                            contents=[
                                user_prompt_content,       # Original user query.
                                part,                      # The function call that was requested.
                                function_response_content, # The response from executing the tool.
                            ],
                            config=types.GenerateContentConfig(
                                tools=self.function_declarations,
                            ),
                        )

                        # Append the text from the first part of Gemini's new candidate response.
                        final_text.append(response.candidates[0].content.parts[0].text)
                    else:
                        # If there is no function call, just use the text provided by Gemini.
                        final_text.append(part.text)

        # 5. Combine all parts of the response into a single string to be returned.
        return "\n".join(final_text)

    async def chat_loop(self):
        """
        Run an interactive chat loop in the terminal.
        
        This function allows the user to type queries one after the other. The loop continues until the user types 'quit'.
        Each query is processed using the process_query method, and the response is printed to the console.
        """
        print("\nMCP Client Started! Type 'quit' to exit.")

        while True:
            # Prompt the user to enter a query.
            query = input("\nQuery: ").strip()
            if query.lower() == 'quit':
                break  # Exit the loop if the user types 'quit'

            # Process the query through the Gemini model and MCP server tool calls.
            response = await self.process_query(query)
            # Print the final response.
            print("\n" + response)


def clean_schema(schema):
    """
    Recursively remove 'title' fields from a JSON schema.
    
    Some JSON schemas include a 'title' field that is not needed for our tool function calls.
    This function goes through the schema and removes any 'title' entries, including nested ones.
    
    Args:
        schema (dict): A dictionary representing a JSON schema.
    
    Returns:
        dict: The cleaned JSON schema without any 'title' fields.
    """
    if isinstance(schema, dict):
        # Remove the 'title' key if it exists.
        schema.pop("title", None)
        # If the schema has a "properties" key (common in JSON schemas) and it's a dict, process each property.
        if "properties" in schema and isinstance(schema["properties"], dict):
            for key in schema["properties"]:
                schema["properties"][key] = clean_schema(schema["properties"][key])
    return schema


def convert_mcp_tools_to_gemini(mcp_tools):
    """
    Convert MCP tool definitions into Gemini-compatible function declarations.
    
    Each MCP tool contains information such as its name, description, and an input JSON schema.
    This function cleans the JSON schema (by removing unnecessary fields) and then creates a Gemini FunctionDeclaration.
    The function declarations are then wrapped in Gemini Tool objects.
    
    Args:
        mcp_tools (list): A list of MCP tool objects with attributes 'name', 'description', and 'inputSchema'.
    
    Returns:
        list: A list of Gemini Tool objects ready for function calling.
    """
    gemini_tools = []

    for tool in mcp_tools:
        # Clean the input schema to remove extraneous fields like 'title'
        parameters = clean_schema(tool.inputSchema)

        # Create a function declaration that describes how Gemini should call this tool.
        function_declaration = FunctionDeclaration(
            name=tool.name,
            description=tool.description,
            parameters=parameters
        )

        # Wrap the function declaration in a Gemini Tool object.
        gemini_tool = Tool(function_declarations=[function_declaration])
        gemini_tools.append(gemini_tool)

    return gemini_tools


async def main():
    """
    Main entry point for the client.
    
    This function:
     - Checks that a server URL is provided as a command-line argument.
     - Creates an instance of MCPClient.
     - Connects to the MCP server via SSE.
     - Enters an interactive chat loop to process user queries.
     - Cleans up all resources (like the SSE connection) when finished.
    
    Usage:
        python client_sse.py <server_url>
    """
    if len(sys.argv) < 2:
        print("Usage: python client_sse.py <server_url>")
        sys.exit(1)

    client = MCPClient()
    try:
        # Connect to the MCP server using the provided SSE URL.
        await client.connect_to_sse_server(sys.argv[1])
        # Start the interactive chat loop for user queries.
        await client.chat_loop()
    finally:
        # Ensure that all resources and network connections are properly closed.
        await client.cleanup()

if __name__ == "__main__":
    # Run the main function using the asyncio event loop.
    asyncio.run(main())
