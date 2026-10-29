#===============================================
# callback handlers
# """
# Intercept and process agent events as they happen, synchronously, with a callback function in Python. 
# Callback handlers drive real-time monitoring, custom output formatting, and integration with external systems.
# To use a callback handler, pass the callback function to the agent
# -- Strands calls your handler once per streaming event, and **kwargs holds everything in that event.
# -- see example
# -- use callback_handler=None (if you do not want to stream the events)
# -- use default callback handler  PrintingCallbackHandler() (formats the output to the console), remeber to pass in ()
# When implementing callback handlers:

# Keep Them Fast: Callback handlers run in the critical path of agent execution
# Handle All Event Types: Be prepared for different event types
# Graceful Errors: Handle exceptions within your handler
# State Management: Store accumulated state in the request_state
# """
# ==============================================
from strands import Agent, tool
from strands.models.litellm import LiteLLMModel
from strands.vended_tools import http_request, notebook
import os, json
from dotenv import load_dotenv
from pprint import pprint
# default callback handler
from strands.handlers.callback_handler import PrintingCallbackHandler

load_dotenv()

# def custom_handler(**kwargs)-> str:
#     """
#     format the response as required if it exist
#     """
#     if "data" in kwargs:
#         print(f"\n [MODEL OUTPUT]: {kwargs["data"]}")
#     elif "current_tool_use" in kwargs and kwargs['current_tool_use'].get('name'):
#         print(f"\n [MODEL TOOL NAME]: {kwargs["current_tool_use"]["name"]}")

# to see the full event object that is streamed
# def custom_handler(**kwargs):
    
#     # skip the huge/noisy entries
#     skip = {"agent", "event_loop_parent_span", "event_loop_cycle_span"}
#     slim = {k: v for k, v in kwargs.items() if k not in skip}
#     pprint(slim, width=100, depth=3)
#     print("-" * 60)

# =================EXAMPLE FOR CUSTOM CALLBACK HANDLER
# to output only a new message when it is added to that agent memory
# def message_buffer_handler(**kwargs):
#     # When a new message is created from the assistant, print its content
#     if "message" in kwargs and kwargs["message"].get("role") == "assistant":
#         print(json.dumps(kwargs["message"], indent=2))

# ==================ANOTHER EXAMPLE TO TRACK THE EVENT LOOP
def event_loop_tracker(**kwargs):
    # Track event loop lifecycle
    if kwargs.get("init_event_loop", False):
        print("Event loop initialized")
    elif kwargs.get("start_event_loop", False):
        print("Event loop cycle starting")
    elif "message" in kwargs:
        print(f"New message created: {kwargs['message']['role']}")
    elif "result" in kwargs:
        print("Agent completed with result")
    elif kwargs.get("force_stop", False):
        print(f"Event loop force-stopped: {kwargs.get('force_stop_reason', 'unknown reason')}")

    # Track tool usage
    if "current_tool_use" in kwargs and kwargs["current_tool_use"].get("name"):
        tool_name = kwargs["current_tool_use"]["name"]
        print(f"Using tool: {tool_name}")

    # Show the first 20 characters of each text chunk to keep output readable
    # tuple comprehension
    if "data" in kwargs:
        data_snippet = kwargs["data"][:20] + ("..." if len(kwargs["data"]) > 20 else "")
        print(f"Text: {data_snippet}")


model = LiteLLMModel(
    client_args={"api_key": os.getenv("POLLINATIONS_API_KEY"),  "api_base": os.getenv("API_URL")},
    model_id=os.getenv("MODEL_NAME", "openai/glyph-cluster"),
    params = {"temperature" :0.3,
        "reasoning_effort": "low",
        "max_tokens": 800,
        "allowed_openai_params": ["reasoning_effort"],
        },  
   
)
agent = Agent(
    tools=[http_request, notebook],
    model=model,
    callback_handler=event_loop_tracker
    
)

url = "https://www.example.com"

response = agent(f"add a new idea for the webpage in the {url} to the summary notebook created")
print(response)

#======================
# """
# the output of this looks chunk, because the model streams responses in chuncks
#  [MODEL TOOL NAME]: http_request

#  [MODEL OUTPUT]: This

#  [MODEL OUTPUT]:  domain is for

#  [MODEL OUTPUT]:  use in documentation

#  [MODEL OUTPUT]:  examples without needing

#  [MODEL OUTPUT]:  permission.
# This domain is for use in documentation examples without needing permission.
# """
#========================================

