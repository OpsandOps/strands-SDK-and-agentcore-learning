# # ============================================
# #  Using MCP tools
# # ============================================
# from strands import Agent, tool
# from strands.models.litellm import LiteLLMModel
# import os
# from dotenv import load_dotenv
# from pprint import pprint
# from pathlib import Path
# from mcp import stdio_client, StdioServerParameters
# from strands.tools.mcp import MCPClient


# # load env
# load_dotenv()


# model = LiteLLMModel(
#     client_args={"api_key": os.getenv("POLLINATIONS_API_KEY"),  "api_base": "https://gen.pollinations.ai/v1"},
#     model_id=os.getenv("MODEL_NAME", "openai/community/YoannDev90/muse-glimmer-30b:free"),
#     params = {"temperature" :0.3,
#         "reasoning_effort": "low",
#         "max_tokens": 1000
#         }
# )

# # create an Mcp client
# mcp_client = MCPClient(lambda: stdio_client(
#     StdioServerParameters(
#         command="uvx",
#         args=["awslabs.aws-documentation-mcp-server@latest"]
#     )
# ))

# with mcp_client:
#     tools = mcp_client.list_tools_sync()
#     agent = Agent(model=model, tools=tools)
#     agent("give a short and brief definition of the lambda service on AWS")
#     pprint(f" ⚙ AGENT TOOLS: {agent.tool_names}\n")


# ================================
# GITHUB MCP Agent (streamable HTTP for remote servers )
# this transport mode is for remote servers:
# it uses Streamable HTTP, to connect mcp to agents
# ===================================
# from strands import Agent, tool
# from strands.models.litellm import LiteLLMModel
# import os
# from dotenv import load_dotenv
# from strands.tools.mcp import MCPClient
# from pprint import pprint

# load_dotenv()

# #model
# model = LiteLLMModel(
#     client_args={"api_key": os.getenv("POLLINATIONS_API_KEY"),  "api_base": "https://gen.pollinations.ai/v1"},
#     model_id=os.getenv("MODEL_NAME", "openai/community/YoannDev90/muse-glimmer-30b:free"),
#     params = {"temperature" :0.3,
#         "reasoning_effort": "low",
#         "max_tokens": 800
#         }
# )

# # tool(mcp)
# # from github mcp tools 
# READ_ONLY_TOOLS = [
#     # Core: browse and read the code
#     "get_file_contents",      # read files and list directory contents
#     "search_code",            # find where things are used or defined
#     "list_branches",
#     "list_commits",           # recent activity and who changes what
#     "get_commit",             # see what a specific commit changed

#     # Context: what the maintainers already know is wrong
#     "list_issues",
#     "issue_read",
#     "search_issues",
#     "list_pull_requests",
#     "pull_request_read",
#     "search_pull_requests",
# ]

# github_mcp = MCPClient(
#     url="https://api.githubcopilot.com/mcp/",
#     headers={"Authorization": f"Bearer {os.environ['GITHUB_PAT']}"},
#     tool_filters={"allowed": READ_ONLY_TOOLS},      
# )

# with github_mcp:
#     tools = github_mcp.list_tools_sync()
#     agent = Agent(model=model, tools=tools, system_prompt=(
#         "You are a code reviewer. Use the GitHub tools to explore repositories. "
#         "Look at the README and the top-level file structure first, then open "
#         "one or two key source files. Be concise and only state what you actually saw."
#     ),)
#     repo = input("Which repo? (owner/name): ").strip()
#     response = agent(
#     f"Explore the GitHub repo '{repo}'. Give me a short overview with:\n"
#     "1. What the project does (2-3 sentences)\n"
#     "2. Main language(s) and folder structure\n"
#     "3. The key files/modules and what each is for\n"
#     "4. How someone would get started using it"
#     )
#     print(response)
    
# =============================================
# CUSTOM MCP (use sse) fastmcp
# =============================================
# from strands import Agent, tool
# from strands.models.litellm import LiteLLMModel
# import os, sys
# from dotenv import load_dotenv
# from strands.tools.mcp import MCPClient
# from mcp import stdio_client, StdioServerParameters
# from pathlib import Path
# from pprint import pprint


# load_dotenv()

# calculator_mcp = MCPClient(
#     lambda: stdio_client(
#         StdioServerParameters(
#             command=sys.executable,
#             args=[str(Path(__file__).parent / "my_tools.py")],
#         )
#     )
# )

# model = LiteLLMModel(
#     client_args={"api_key": os.getenv("POLLINATIONS_API_KEY"),  "api_base": "https://gen.pollinations.ai/v1"},
#     model_id=os.getenv("MODEL_NAME", "openai/community/YoannDev90/muse-glimmer-30b:free"),
#     params = {"temperature" :0.3,
#         "reasoning_effort": "low",
#         "max_tokens": 800
#         }
# )

# with calculator_mcp:
#     tools = calculator_mcp.list_tools_sync()
#     agent = Agent(
#         model=model,
#         tools=tools,
#         system_prompt=(
#             """
#             you are a helpful mathematics assistant
#             when the user asks for arithemetic operations
#             1. use the calculator tool to perform the arithemetic operation
#             """),
#         callback_handler=None,
#         )
#     try:
#         a = int(input("Enter the first number: "))
#         b = int(input("Enter the second number: "))
#     except ValueError:
#         sys.exit("Please enter whole numbers only.")
#     response = agent(f"calculate the sum of {a} and {b}")
#     print(response)

# ========================================================
# MCP With elicitation
# ========================================================
from strands import Agent, tool
from strands.models.litellm import LiteLLMModel
import os, sys
from dotenv import load_dotenv
from strands.tools.mcp import MCPClient
from mcp import stdio_client, StdioServerParameters
from mcp.types import ElicitResult
from pathlib import Path
from pprint import pprint
import asyncio

load_dotenv()

# elicitation callback function

async def approval_callback(callback, params):
    print(f"\n [APPROVAL REQUSTED] {params.message}")
    result = await asyncio.to_thread(input, "Approve? (y/n): ")
    # normalise the answer
    if result.strip().lower() in ("y", "yes"):
        return ElicitResult(action="accept", context={"approve": False})
    return ElicitResult(action="decline")

# mcp client
calculator_mcp = MCPClient(
    lambda: stdio_client(
        StdioServerParameters(
            command=sys.executable,
            args=[str(Path(__file__).parent / "my_tools.py")],
        )
    ),
    elicitation_callback=approval_callback
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
with calculator_mcp:
    tools = calculator_mcp.list_tools_sync()
    agent = Agent(
        model=model,
        tools=tools,
        system_prompt=(
            "You are a helpful mathematics assistant. "
            "For ANY arithmetic, call the calculator tool immediately. "
            "Do NOT ask the user for permission or confirmation yourself: "
            "approval is handled automatically by the tool. "
            "If the tool says the user denied the calculation, do not retry; "
            "just tell the user it was not run."
        ),
        # callback_handler=None,
        )
    try:
        a = int(input("Enter the first number: "))
        b = int(input("Enter the second number: "))
    except ValueError:
        sys.exit("Please enter whole numbers only.")
    response = agent(f"calculate the sum of {a} and {b}")
    print(response)





