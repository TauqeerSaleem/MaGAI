import json
import ollama
import asyncio

class ToolCall():
    def __init__(self, 
                 tools = "default", 
                 available_functions = "default"):

        if tools == "default":
            self.tools = [
                {
                    "type": "function",
                    "function": {
                        "name": "add_3d_axis",
                        "description": "returns the code for adding a 3d/ three dimensional axes in a manim scene",
                        "parameters": {}
                        }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "add_circle",
                        "description": "returns the code for adding a circle in the manim scene",
                        "parameters": {
                            "type": "array",
                            "properties": {
                                "center" : {
                                    "type" : "array",
                                    "description" : "An array of shape (3,) describing the center of the sphere"
                                },
                                "radius" : {
                                    "type" : "float",
                                    "description" : "A number (float) describing the size/ radius of the sphere"
                                }
                            }
                        }
                        }
                }
            ]
        
        if available_functions == "default":
            self.available_functions = {
                "add_3d_axis": self.add_3d_axis
            }

    #### TOOLS ####

    def add_3d_axis(self) -> str:
        return "add(ThreeDAxes())"
    
    def no_tool(self, response):
        return response["message"]["content"]

    #### END OF TOOLS ####

    async def get_code(self,
                       prompt: str,
                       model = "llama3.2:1b"):
        
        client = ollama.AsyncClient()

        # Initialize conversation with a user query
        messages = [
            {
                "role": "user",
                "content": prompt,
            }
        ]

        # First API call: Send the query and function description to the model
        response = await client.chat(
            model = model,
            messages = messages,
            tools = self.tools,
        )

        # Add the model's response to the conversation history
        messages.append(response["message"])

        # Check if the model decided to use the provided function
        if not response["message"].get("tool_calls"):
            return self.no_tool(response)

        else: #elif response["message"].get("tool_calls"):
            # print(f"\nThe model used some tools")
            
            # print(f"\navailable_function: {available_functions}")
            for tool in response["message"]["tool_calls"]:
                function_to_call = self.available_functions[tool["function"]["name"]]

                if function_to_call == self.add_3d_axis:
                    function_response = function_to_call()
                else:
                    return "wait(1)"

                messages.append(
                    {
                        "role": "tool",
                        "content": function_response,
                    }
                )
            return function_response

## Example
# async def main():
#     tool = ToolCall()
#     result = await tool.get_code(prompt="add three dimensional axes")
#     print(result)

# asyncio.run(main())
