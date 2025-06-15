from typing import Callable, Dict, Any

class MCPServer():
    """
    Represents a custom function that can be invoked by the OpenAI API.

    Attributes:
        label (str): The label of the MCP Server.
        url (str): The URL of the remote MCP server.
    """
    def __init__(
            self,
            label: str,
            url: str,
    ) -> None:
        self.label = label
        self.url = url

    def __repr__(self) -> str:
        return f"MCPServer(label='{self.label}')"
        
class CustomFunction():
    """
    Represents a custom function that can be invoked by the OpenAI API.

    Attributes:
        name (str): The name of the function.
        description (str): A brief description of what the function does.
        parameters (Dict[str, Any]): The parameters required by the function.
        handler (Callable): The actual function to be executed.
    """
    def __init__(
            self,
            name: str,
            description: str,
            parameters: Dict[str, Any],
            handler: Callable,
    ) -> None:
        self.name = name
        self.description = description
        self.parameters = parameters
        self.handler = handler

    def __repr__(self) -> str:
        return f"CustomFunction(name='{self.name}')"
