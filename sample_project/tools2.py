
## using custom tools(tools created by you)
## ensure that the fucntions in your tools, work properly. so that the agent dosent fail in its task

# from strands import Agent, tool
# # we can use built in tools like file_editor and web_fetch and others from strands.vended_tools
# from strands.vended_tools import file_editor
# from strands.vended_tools.web_fetch import web_fetch
# from strands import Agent
# from strands.models.litellm import LiteLLMModel
# import os


# from dotenv import load_dotenv

# load_dotenv()


# @tool
# def report_weather(longitude: float, latitude: float) -> dict:
#     """
#     report the weather for a given city within the limits of a given number of days
#     Args:
#         city: name of the city
#         days: number of days for the forecast

#     Returns:
#         a dictionary of the weather report

#     """
#     import openmeteo_requests

#     import pandas as pd
#     import requests_cache
#     from retry_requests import retry

#     # Setup the Open-Meteo API client with cache and retry on error
#     cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
#     retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
#     openmeteo = openmeteo_requests.Client(session = retry_session)

#     url = "https://api.open-meteo.com/v1/forecast"
#     params = {
# 	    "latitude": {longitude},
# 	    "longitude": {latitude},
# 	    "daily": "weather_code",
# 	    "hourly": "temperature_2m",
#     }
#     responses = openmeteo.weather_api(url, params = params)

#     # Process first location. Add a for-loop for multiple locations or weather models
#     response = responses[0]

#     # daily data
#     daily = response.Daily()
#     daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy()
#     daily_temperature_2m_min = daily.Variables(1).ValuesAsNumpy()
#     daily_apparent_temperature_max = daily.Variables(2).ValuesAsNumpy()
#     daily_apparent_temperature_min = daily.Variables(3).ValuesAsNumpy()
#     return {
#         "daily_temperature_max": {daily_temperature_2m_max},
#         "daily_temperature_min": {daily_temperaure_2m_min}
#     }


# @tool
# def get_location():
#     """
#     fetch the given location using https://www.ipapi.co accurately
#     using the request library
#     """
#     import requests 

#     base_url = "https://ipapi.co/json/"
#     try:
#         with requests.Session() as session:
#             response = session.get(base_url, headers={"User-agent": "weather-bot 1.0"})
#             data = response.json()

#         return {
#             "ip": data.get("ip"),
#             "city": data.get("city"),
#             "country_name": data.get("country_name")
#         }
#     except requests.RequestException as error:
#         print(f"Error fetching IP location: {error}")
#         return None

# @tool
# def write_report(filename: str, report: str) -> str:
#     """
#     write the weather report to the file given
#     Args:
#         filename: name of the report file
#     """
#     weather_report = {
#         "city": "...",
#         "country": "...",
#         "ip_address": "...",
#         "weather": "...",

#     }
#     return f"\n SUCCESS ✅ filed saved in {filename}, here is the weather report {weather_report}"

    
# SYSTEM_PROMPT = """You are a weather analyst. You help the team understand
# weather for the some given number of days .

# When given a research task:
# 1. use get_location to get the location of the user, the ip, city and country information, determine the longitudes and latitudes for the city
# 2. Use report_weather to return the weather forecast for the city
# 3. Write a brief and short analysis using write_report and display it in the format and save it to the given file."""


# model = LiteLLMModel(
#         client_args={"api_key": os.getenv("POLLINATIONS_API_KEY"),  "api_base": "https://gen.pollinations.ai/v1"},
#         model_id=os.getenv("MODEL_NAME", "openai/community/YoannDev90/muse-glimmer-30b:free"),
#         params = {"temperature" :0.3,
#         "reasoning_effort": "low",
#         "max_tokens": 800
#         }
# )

# agent = Agent(
#     model=model,
#     tools=[get_location, report_weather, write_report],
#     system_prompt=SYSTEM_PROMPT,
# )

# result = agent("Research what the weather forecast is in my city today, Write a short summary and save it to report.md")

### ATTACHING AND INVOKING TOOLS ===========================
from strands import Agent, tool
from strands.models.litellm import LiteLLMModel
from strands.vended_tools import http_request, notebook
import os
from dotenv import load_dotenv
from pprint import pprint
from pathlib import Path
# from my_tools import randNum

# load env
load_dotenv()


model = LiteLLMModel(
    client_args={"api_key": os.getenv("POLLINATIONS_API_KEY"),  "api_base": "https://gen.pollinations.ai/v1"},
    model_id=os.getenv("MODEL_NAME", "openai/community/YoannDev90/muse-glimmer-30b:free"),
    params = {"temperature" :0.3,
        "reasoning_effort": "low",
        "max_tokens": 800
        }
)

# tools can be called via direct method call
# @tool
# def randomNum(a: int, b: int):
#     """ generate a random number between two given numbers"""
#     from random import randint
#     result =  round(randint(a, b))
#     return result 


# we can load tools from a file by adding the absolute path to the file
# tools = ["path/to/the/tools.py"]
# - Automatic loading and reloading of tools in the ./tools/ directory is disabled by default.
#  To enable this behavior, set load_tools_from_directory=True during Agent initialization:
# - ensure that tool have been tested for safety because the agent auto picks them up
# agents decide when to use tools based on natural language requests, it read the user prompts and determines
# tool invocation 
agent = Agent(
    model=model,
    tools=[str(Path(__file__).parent / 'my_tools.py')],    
)

# when calling via direct call, always use default arguments instead of positional arguments
result = agent.tool.randNum(a=10, b=30, record_direct_tool_call=False)
pprint(result)

print("="*20)
print(result["content"][0])


# agent("create a notebook called ideas with three simple agent project ideas")
# print("\n\n")
# agent("Get https://example.com and summarize the response status.")

# to see the tools loaded in your agent
pprint(f" ⚙ AGENT TOOLS: {agent.tool_names}")
# pprint(f"\n    AGENT TOOLS REGISTRY: {agent.tool_registry.get_all_tools_config()}")