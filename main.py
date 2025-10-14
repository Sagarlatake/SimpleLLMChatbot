import getpass
import os
from dotenv import load_dotenv
try:
    # load environment variables from .env file (requires `python-dotenv`)
    from dotenv import load_dotenv

    load_dotenv()
    print('env variable loaded...')
except ImportError:
    pass

os.environ["LANGSMITH_TRACING"] = "true"
if "LANGSMITH_API_KEY" not in os.environ:
    os.environ["LANGSMITH_API_KEY"] = getpass.getpass(
        prompt="Enter your LangSmith API key (optional): "
    )
if "LANGSMITH_PROJECT" not in os.environ:
    os.environ["LANGSMITH_PROJECT"] = getpass.getpass(
        prompt='Enter your LangSmith Project Name (default = "default"): '
    )
    if not os.environ.get("LANGSMITH_PROJECT"):
        os.environ["LANGSMITH_PROJECT"] = "default"



if not os.environ.get("GROQ_API_KEY"):
  os.environ["GROQ_API_KEY"] = getpass.getpass("Enter API key for Groq: ")

from langchain.chat_models import init_chat_model

model = init_chat_model("Llama-3.3-70B-Versatile", model_provider="groq")

from langchain_core.messages import HumanMessage, SystemMessage

messages = [
    SystemMessage(content="Translate the following from English into Italian"),
    HumanMessage(content="hi!"),
]

response = model.invoke(messages)
print(response.content)

# open AI format
# print("Open AI formatted calls:")
# response = model.invoke("Hello")
# print(response.content)
# response = model.invoke([{"role": "user", "content": "Hello"}])
# print(response.content)
# response = model.invoke([HumanMessage("Hello")])
# print(response.content)


# streaming

for token in model.stream(messages):
    print(token.content, end="|")


# using Prompt Template

from langchain_core.prompts import ChatPromptTemplate

system_template = "Translate the following from English into {language}"

prompt_template = ChatPromptTemplate.from_messages(
    [("system", system_template), ("user", "{text}")]
)

prompt = prompt_template.invoke({"language": "Italian", "text": "hi!"})
print('Prompt created using prompt template')
print(prompt)
print(prompt.to_messages())
print('Model Response:')
response = model.invoke(prompt)
print(response.content)