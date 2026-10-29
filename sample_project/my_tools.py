

# from strands import tool

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

# from typing import Annotated

# from pydantic import BaseModel, Field

# from mcp.server import MCPServer
# from mcp.server.mcpserver import (
#     AcceptedElicitation,
#     CancelledElicitation,
#     DeclinedElicitation,
#     Elicit,
#     ElicitationResult,
#     Resolve,
# )

# mcp = MCPServer("Calculator Server")


# # Flat fields only (str, int, float, bool)
# class Approval(BaseModel):
#     approval: bool = Field(description="Allow this calculation to run")


# # Resolver: reads the tool's own x and y arguments by name and asks the user
# async def ask_for_approval(x: int, y: int) -> Elicit[Approval]:
#     return Elicit(f"Approve running the calculation with {x} and {y}?", Approval)


# @mcp.tool(description="add two integers and return the sum")
# async def calculator(
#     x: int,
#     y: int,
#     answer: Annotated[ElicitationResult[Approval], Resolve(ask_for_approval)],
# ) -> str:
#     match answer:
#         case AcceptedElicitation(data=Approval(approval=True)):
#             return str(x + y)
#         case AcceptedElicitation():
#             return "the user denied the calculation, do not retry, tell the user it was not run"
#         case DeclinedElicitation() | CancelledElicitation():
#             return "the user declined the calculation, do not retry, tell the user it was not run"

# async def ask_to_multiply(x: int, y:int)-> Elicit[Approval]:
#     return Elicit(f"Approve running multiplication {x} and {y}", Approval)

# @mcp.tool(description="multiply two integers return the product")
# async def multiply(
#     x: int,
#     y: int, 
#     answer: Annotated[ElicitationResult[Approval], Resolve(ask_to_multiply)]
#     ) -> str:
#         match answer:
#             case AcceptedElicitation(data=Approval(approval=True)):
#                 return str(x * y)
#             case AcceptedElicitation():
#                 return "the user denied the calculation, do not retry, tell the user it was not run"
#             case DeclinedElicitation() | CancelledElictiation():
#                 return "the user declined the calculation, do not retry, tell the user it was not run"



# if __name__ == "__main__":
#     mcp.run(transport="stdio")

# ======================================================
#  ELICITATION FOR A DB EXAMPLE
# ======================================================
from typing import Annotated
import json, sys

from pydantic import BaseModel, Field

from mcp.server import MCPServer
from mcp.server.mcpserver import (
    AcceptedElicitation,
    CancelledElicitation,
    DeclinedElicitation,
    Elicit,
    ElicitationResult,
    Resolve,
)

mcp = MCPServer("Database Server")

# simulated database
DB: list[dict] = [
    {"id": 1, "name": "Ada Okafor", "email": "ada@example.com", "role": "admin"},
    {"id": 2, "name": "Bola Adeyemi", "email": "bola@example.com", "role": "editor"},
    {"id": 3, "name": "Chidi Eze", "email": "chidi@example.com", "role": "viewer"},
    {"id": 4, "name": "Dayo Bello", "email": "dayo@example.com", "role": "viewer"},
]

# tools for the db_Agent
def find(record_id: int) -> dict | None:
    return next((r for r in DB if r["id"] == record_id), None)


# Flat fields only (str, int, float, bool)
# Elictation schema
class Approval(BaseModel):
    approval: bool = Field(description="Allow this calculation to run")


# resolver
async def ask_to_delete(record_id: int) -> Approval | Elicit[Approval]:
    record = find(record_id)
    if record is None:
        return Approval(approval=True)
    return Elicit(
        f"Permanently delete record {record['id']}: "
        f"{record['name']} < {record['email']} > ({record['role']})?",
        Approval
    )


@mcp.tool(description="Read the database, Pass record_id for one record, or omit it to list all records")
async def read_db(record_id: int | None = None) -> str:
    if record_id is None:
        return json_dumps(DB)
    record = find(record_id)
    if record is None:
        return f"No record with id {record_id}."
    return json.dumps(record)


@mcp.tool(description="Delete one record with id. The user is asked to approve before anything is deleted.")
async def delete_record(
    record_id: int,
    answer: Annotated[ElicitationResult[Approval], Resolve(ask_to_delete)]
) -> str:
    record = find(record_id)
    if record is None:
        return f"NO record with id {record_id}; nothing to delete"
    
    match answer:
        case AcceptedElicitation(data=Approval(approval=True)):
            DB.remove(record)
            print(f"[SERVER] deleted record {record_id}", file=sys.stderr)
            return f"Deleted record {record_id} ({record['name']})."
        case _:
            return (
                f"The user did not approve deleting record {record_id}. "
                "it was NOT deleted. Do not retry; tell the user it was not deleted."
            )


if __name__ == "__main__":
    mcp.run(transport="stdio")

    