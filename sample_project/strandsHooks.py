# ===========================================================
# A hook is a callback registered against a lifecycle event,
#  and the agent loop runs it when that event fires.
# ==========================================================
from strands import Agent, tool
from strands.models.litellm import LiteLLMModel
from strands.vended_tools import http_request, notebook
import os, json
from dotenv import load_dotenv
from pprint import pprint
from pathlib import Path
from typing import Any, Callable
# from my_tools import randNum
# imports for strands Hooks based on the relevant event in this examples
from strands.hooks import ( 
    AfterToolCallEvent,
    BeforeToolCallEvent,
    HookProvider,
    HookRegistry,
)


# load env
load_dotenv()


# # in-memory db
# DB: dict[str, dict] = {
#     "u1": {"name": "Ada", "email": "ada@example.com"},
#     "u2": {"name": "Tunde", "email": "tunde@example.com"},
#     "u3": {"name": "Ngozi", "email": "ngozi@example.com"},
# }

# # tools,
# @tool
# def list_records() -> dict:
#     """List all records currently in the database."""
#     return DB


# @tool
# def get_record(key: str) -> dict:
#     """
#     Look up a record by the key
#     Args:
#         key: The record key, e.g. "ul".
#     """
#     return DB.get(key, {"error": f"No record with the key, '{key}'"})

# @tool
# def delete_record(key: str) -> dict:
#     """
#     Delete a record from the database by key
#     Args:
#         key: The record key, used to delete its value, e.g "u2".
#     """
#     if key not in DB:
#         return {"error": f"No record with the key: '{key}'"}
#     removed = DB.pop(key)
#     return {"deleted": key, "record": removed}


# # Elicitation callback, Schema for the callback function
# ElicitCallback = Callable[[str, dict], dict]

# # elicitation callback function
# # HOLD THIS -> The elicitation callback (elicit_cli) is the “how we ask”:
# # it prints a prompt and returns [accept, decline or cancel.] 
# def elicit_cli(message: str, schema: dict) -> dict:
#     print(f"\n [approval needed] {message}")
#     try:
#         answer = input("Proceed? [y/n]: ").strip().lower()
#     except (EOFError, KeyboardInterrupt):
#         return {"action": "cancel"}
#     if answer in ("y", "yes"):
#         return {"action": "accept", "content": {"approval": True}}
#     return {"action": "decline"}

# # define the elicitation action here

# # Hool callback registered to the lifecylce events via a HookProvider
# class DeleteApprovalHook(HookProvider):
#     """
#     Before delete_record runs, ask the human, Declined => cancel the call
#     """
#     def __init__(self, elicit: ElicitCallback) -> None:
#         self.elicit = elicit

#     def register_hooks(self, registry: HookRegistry, **kwargs: Any) -> None:
#         registry.add_callback(BeforeToolCallEvent, self.approve)
#         registry.add_callback(AfterToolCallEvent, self.audit)

#     def approve(self, event: BeforeToolCallEvent) -> None:
#         if event.tool_use["name"] != "delete_record":
#             return 

#         key = event.tool_use["input"]["key"]
#         record = DB.get(key)
#         message = (
#             f"The agent wants to DELETE record '{key}': {json.dumps(record)}"
#             if record
#             else f"The agent wants to delete '{key}', which does not exist."
#         )
#         schema = {
#             "type": "object",
#             "properties": {"approved": {"type": "boolean"}},
#             "required": ["approval"]
#         }
#         response = self.elicit(message, schema)
#         if response['action'] != "accept":
#             # this is here like an error tool result the model reads
#             event.cancel_tool = f"User {response['action']}d the deletion of '{key}'"

#     def audit(self, event: AfterToolCallEvent) -> None:
#         print(f"[audit] {event.tool_use['name']} ({event.tool_use['input']}) -> {event.result['status']}")


        
# model = LiteLLMModel(
#     client_args={
#         "api_key": os.getenv("GROQ_API_KEY"),
#         "api_base": os.getenv("API_URL")
#         },
#     model_id=os.getenv("MODEL_NAME", "groq/openai/gpt-oss-120b"),
#     params = {"temperature" :0.3,
#         "reasoning_effort": "low",
#         "max_tokens": 800
#         }
# )

# # tools can be called via direct method call

# # we can load tools from a file by adding the absolute path to the file
# # tools = ["path/to/the/tools.py"]
# # - Automatic loading and reloading of tools in the ./tools/ directory is disabled by default.
# #  To enable this behavior, set load_tools_from_directory=True during Agent initialization:
# # - ensure that tool have been tested for safety because the agent auto picks them up
# # agents decide when to use tools based on natural language requests, it read the user prompts and determines
# # tool invocation 
# SYSTEM_PROMPT = "You manage a small user database. Use the tools to answer."

# agent = Agent(
#     model=model,
#     tools=[list_records, get_record, delete_record],
#     hooks=[DeleteApprovalHook(elicit_cli)],
#     system_prompt=SYSTEM_PROMPT,   
# )

# if __name__ == "__main__":
#     result = agent("Delete the recordd for key u2, then tell me what's left in the database")
#     print("\n", result)
#     print("\nFINAL DB:", DB)
# when calling via direct call, always use default arguments instead of positional arguments

# agent("create a notebook called ideas with three simple agent project ideas")
# print("\n\n")
# agent("Get https://example.com and summarize the response status.")

# to see the tools loaded in your agent
# pprint(f" ⚙ AGENT TOOLS: {agent.tool_names}")
# pprint(f"\n    AGENT TOOLS REGISTRY: {agent.tool_registry.get_all_tools_config()}")

# ==========================================
# another example for hooks with file operation
# =========================================
# we have to bypass the tool consent so that our approval step becomes the only one
os.environ["BYPASS_TOOL_CONSENT"] = "true"
from strands_tools import file_read, file_write, editor

# All file work is confined to this folder
WORKSPACE = Path("workspace").resolve()
WORKSPACE.mkdir(exist_ok=True)
os.chdir(WORKSPACE)

# ensure that our work if done inside the workspace folder
def _safe_path(name: str) -> Path:
    """Resolve a name inside WORKSPACE, rejecting anything that escapes it."""
    path = (WORKSPACE / name).resolve()
    if path != WORKSPACE and WORKSPACE not in path.parents:
        raise ValueError(f"'{name}' is outside workspace")
    return path


# the elicitation callback
ElicitCallback = Callable[[str, dict], dict]

def elicitation_cli(message: str, schema: dict) -> str:
    """ show a step to the user and ask for approval """
    print(f"\n [APPROVAL NEEDED] -> {message}")

    try:
        answer = input("Proceed? [y/N]: ").strip().lower()
    except (EOFError, KeyboardInerrupt):
        return {"action": "cancel"}
    if answer in ("y", "yes"):
        return {"action": "accept", "content": {"approval": True}}
    return {"action": "decline"}

# changes the returned dictionary that the model outputs to readable output
def describe_step(tool_use: dict) -> str:
    """Turn a tool call into a human-readable step"""
    tool_name = tool_use["name"]
    tool_input = tool_use.get("input", {})
    path = tool_input.get('path') or tool_input.get("filename")

    if tool_name == "list_files":
        return "LIST the files in the workspace"
    if tool_name == "file_read":
        return f"READ the file '{path}'"
    if tool_name == "file_write":
        content = str(tool_input.get("content", ""))
        preview = content if len(content) <= 60 else content[:60] + "..."
        try:
            exists = (WORKSPACE / str(path)).exists()
        except(TypeError, ValueError, OSError):
            exists = False
        action = "OVERWRITE" if exists else "CREATE"
        return f"{action} the file '{path}' with content: {preview!r}"

    if tool_name == "editor":
        command = tool_input.get("command", "edit")
        return f"EDIT the file '{path}' (editor command: {command})"

    if tool_name == "delete_file":
        return f"DELETE the file '{path}' permanently"

    return f"Run tool '{tool_name}' with {tool_input}"


@tool(description="list all files if exist in the folder")
def list_files() -> list[str]:
    """
    List the names of all files in the workspace folder
    """
    return sorted(p.name for p in WORKSPACE.iterdir() if p.is_file())

@tool(description="delete a named file from the workspace folder")
def delete_file(filename: str) -> dict:
    """
    Permanently delete a file from the workspace folder
    Args:
        filename: name of the file to be deleted, e.g "notes.txt"
    """
    path = _safe_path(filename)
    if not path.is_file():
        return {"error": f"No file named '{filename}'"}
    path.unlink()
    return {"deleted": filename}


GUARDED_TOOLS = {
    "file_read",
    "file_write",
    "editor"
}

APPROVAL_TOOLS = {
    "list_files",
    "file_read",
    "file_write",
    "editor",
    "delete_file"
}

class StepApprovalHook(HookProvider):
    """Before each file action, show the step and ask the user to approve it."""
    def __init__(self, elicit: ElicitCallback) -> None:
        self.elicit = elicit

    def register_hooks(self, registry: HookRegistry, **kwargs) -> None:
        registry.add_callback(BeforeToolCallEvent, self.approve)

    def approve(self, event: BeforeToolCallEvent) -> None:
        if event.tool_use["name"] not in APPROVAL_TOOLS:
            return

            #another hook (the workspace guard) already blocked this call
        if event.cancel_tool:
            return

        step = descricbe_step(event.tool_use)
        schema = {
            "type": "object",
            "properties": {"approved": {"type": "boolean"}},
            "required": ["approval"],
        }
        response = self.elicit(step, schema)

        if response['action'] != "accept":
            event.cancel_tool = (
                f"The user {response['action']}d this step: {step}."
                "Do not retry it. Tell the user it was not done"
            )
            

# hook class
class WorkspaceGuardHook(HookProvider):
    """
    Cancel vended file-tool calls that point outside WORKSPACE.
    """
    def register_hooks(self, registry: HookRegistry, **kwargs)-> None:
        registry.add_callback(BeforeToolCallEvent, self.check_path)

    def check_path(self, event: BeforeToolCallEvent) -> None:
        if event.tool_use['name'] not in GUARDED_TOOLS:
            return 

        raw_path = event.tool_use['input'].get("path")
        if not raw_path:
            event.cancel_tool = "Refused: no path given."
            return 

        try:
            _safe_path(os.path.expanduser(str(raw_path)))
        except ValueError:
            event.cancel_tool = (
                f"Refused: '{raw_path}' is outside the workspace"
                "use a relative filename like 'notes.txt"
            )


model = LiteLLMModel(
    client_args={
        "api_key": os.getenv("GROQ_API_KEY"),
        "api_base": os.getenv("API_URL")
        },
    model_id=os.getenv("MODEL_NAME", "groq/openai/gpt-oss-120b"),
    params = {"temperature" :0.3,
        "reasoning_effort": "low",
        "max_tokens": 800
        }
)

SYSTEM_PROMPT = """You are a file management assistant working inside one workspace folder.

Rules for files:
- Use relative filenames only, like "notes.txt". Never use absolute paths, "..", or "~".
- Use list_files to see what exists before reading, writing or deleting.
- Use file_write to create a file or write to it, file_read to read it, and editor for targeted edits.
- Use delete_file to delete a file.

Approvals:
- Every action (listing, reading, creating, writing, editing, deleting) needs the user's approval before it runs.
- If a step is declined or cancelled, do not retry it, and do not try to reach the same result another way.
- Never say an action was done unless a tool result confirms it. If a step was declined, tell the user plainly that it was not done.

Errors:
- If a tool returns an error or a refusal, explain it to the user instead of repeating the same call."""

agent = Agent(
    model=model,
    tools=[file_read, file_write, editor, list_files, delete_file],
    hooks=[
        WorkspaceGuardHook(),
        StepApprovalHook(elicitation_cli),
    ],
    system_prompt=SYSTEM_PROMPT,
)


if __name__ == "__main__":
    print(agent("Create a file called hello.txt containing 'hi there', then list the files then read hello.txt"))

