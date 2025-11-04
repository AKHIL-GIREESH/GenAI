from langchain_core.tools import tool,StructuredTool, BaseTool
from pydantic import BaseModel,Field
from typing import Type


# Method 1
@tool
def multiply(a:int,b:int) -> int:
    """ Multiply two numbers """
    return a*b

print(multiply.invoke({"a":10,"b":5}))
print(multiply.args_schema.model_json_schema()) # This is what LLM sees

# Method 2
class MultiplyInput(BaseModel):
    a:int = Field(required=True,description="First Number")
    b:int = Field(required=True,description="Second Number")

def multiply_func(a:int,b:int) -> int:
    return a*b

multiply_tool = StructuredTool.from_function(
    func=multiply_func,
    name="multiply",
    description="Multipling Tool",
    args_schema=MultiplyInput
)

print(multiply_tool.invoke({'a':10,'b':3}))

# Method 3

class MultiplyTool(BaseTool):
    name:str = "multiply"
    description:str="Multiplyng Tool"

    args_schema: Type[BaseModel] = MultiplyInput

    def _run(self,a:int,b:int) -> int:
        return a*b
    
new_multiply_tool = MultiplyTool()
print(new_multiply_tool.invoke({'a':10,'b':3}))