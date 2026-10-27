from strands import tool

# @tool
# def randNum(a: int, b: int):
#     """
#     returns a random number between two numbers"""
#     from random import randint
#     result = round(randint(a, b))
#     return result

#=====================================
# NORMAL MCP CALLL
#======================================
# from mcp.server.mcpserver import MCPServer
# # mcp toool
# mcp = MCPServer("Calculator Server")

# @mcp.tool(description="Add two integers and return the sum")
# def calculator(x: int, y: int) -> int:
#     return x + y


# if __name__ == "__main__":
#     # run() blocks forever, so this file does nothing else.
#     # stdio = Strands starts this script itself, no ports needed.
#     # never print() in this file; stdout is the MCP channel.
#     mcp.run(transport="stdio")

#=====================================
# ELICITATION WITH MCP CALLL
#======================================
from mcp.server.mcpserver import Context, MCPServer
from pydantic import BaseModel, Field

# create mcp server
mcp = MCPServer("Calculator Server")

# what we want from the human approver
# elicitation schema must be flat (int, float, str, Bool)
class Approval(BaseModel):
    approval: float = Field(description="Allow this calculation to run")

# tools, --must be async because now we wait for user approval, passed as contxt
@mcp.tool(description="add two integers and return a sum")
async def calculator(x: int, y: int, ctx: Context) -> str:
    result = await ctx.elicit(
        message=f"approve running calculation with {x} and {y}",
        schema=Approval
    )
    print(f"this is the result of the elicitation: {result.action}")
    print(f"this is the data returned: {result.data.approve}")

    if result.action != "accept" or not result.data.approve:
        return "the user denied the calculation, do not retry, tell the user it was not run"
    return str({x + y})

if __name__ == "__main__":
    mcp.run(transport="stdio")




    