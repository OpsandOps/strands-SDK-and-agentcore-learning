# import os
# from strands import Agent
# from strands.models.litellm import LiteLLMModel
# from dotenv import load_dotenv

# # load the env variables
# load_dotenv()

# SYSTEM_PROMPT = """
# you are a helpful pre-school teacher,

# when the user asks about pre-school games, recommend safe games to play
# that are fun and engaging, provide a short description and what it teaches.
# """

# model = LiteLLMModel(
#     client_args={"api_key": os.getenv("GROQ_API_KEY")},
#     model_id=os.getenv("MODEL_NAME", "groq/openai/gpt-oss-120b"),
#     params={
#         "temperature": 0.3,
#         "max_tokens": 500,
#         "reasoning_effort": "low"
        
#     }

# )

# # instantiate the agents from strands
# agent = Agent(model=model, system_prompt=SYSTEM_PROMPT)

# # send a message to the agent
# response = agent("i want to play a pre-school game")

# # print the response of the agent
# print(response)


