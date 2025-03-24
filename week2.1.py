1.from smolagents import CodeAgent, HfApiModel
from smolagents.tools import DuckDuckGoSearchTool

agent = CodeAgent(
    tools=[DuckDuckGoSearchTool()],  # Add the DuckDuckGo search tool.
    model=HfApiModel("Qwen/Qwen2.5-Coder-32B-Instruct")  # Properly configured HfApiModel.
)

2.import asyncio
from smolagents import Agent, Environment, Message

# Define the search tool that simulates a DuckDuckGo search.
class DuckDuckGoSearchTool:
    def search(self, query: str) -> str:
        # Simulate returning search results.
        return f"DuckDuckGo result for '{query}'"

# Helper function to simulate visiting a webpage.
def visit_webpage(url: str) -> str:
    return f"Visited webpage at {url}"

# Define the web agent as a ToolCallingAgent.
class ToolCallingAgent(Agent):
    def __init__(self, tools, model, max_steps, name, description):
        super().__init__(name)
        self.tools = tools              # Expected to include search tools.
        self.model = model              # Placeholder for an AI model.
        self.max_steps = max_steps      # Critical configuration parameter.
        self.description = description

    async def on_message(self, message: Message):
        # Process messages starting with "search:".
        if message.content.startswith("search:"):
            query = message.content.split("search:", 1)[1].strip()
            # Use the first tool (DuckDuckGoSearchTool) to perform the search.
            search_result = self.tools[0].search(query)
            # Simulate visiting a webpage.
            webpage_info = visit_webpage("https://example.com")
            result = f"{search_result} | {webpage_info}"
            print(f"[{self.name}] {result}")

# Define the manager agent as a CodeAgent.
class CodeAgent(Agent):
    def __init__(self, name, managed_agents=None):
        super().__init__(name)
        # List of agents that this manager oversees.
        self.managed_agents = managed_agents if managed_agents is not None else []

    async def on_message(self, message: Message):
        # For demonstration, simply print any incoming messages.
        print(f"[{self.name}] Received: {message.content}")

    async def instruct_agent(self, env: Environment, target_name: str, instruction: str):
        # Create and send a message instructing the target agent.
        msg = Message(sender=self.name, recipient=target_name, content=instruction)
        await env.send_message(msg)

async def main():
    # Create the multi-agent environment.
    env = Environment()

    # Instantiate the required search tool.
    search_tool = DuckDuckGoSearchTool()

    # Create the web agent with tools, a placeholder model, max_steps, name, and description.
    web_agent = ToolCallingAgent(
        tools=[search_tool],
        model="web-search-model",  # Placeholder model identifier.
        max_steps=5,
        name="WebAgent",
        description="Web agent with DuckDuckGoSearchTool and visit_webpage functionality."
    )

    # Create the manager agent and include the web agent in its managed_agents list.
    manager_agent = CodeAgent(name="ManagerAgent", managed_agents=[web_agent])

    # Add both agents to the environment.
    env.add_agent(web_agent)
    env.add_agent(manager_agent)

    # Manager instructs the web agent to perform a search for "Latest AI trends".
    await manager_agent.instruct_agent(env, "WebAgent", "search: Latest AI trends")

    # Allow some time for agents to process messages.
    await asyncio.sleep(1)
    await env.stop()

if __name__ == "__main__":
    asyncio.run(main())





3.from smolagents import CodeAgent, E2BSandbox

# Configure the E2B sandbox to allow only "numpy" as an authorized import.
sandbox = E2BSandbox(authorized_imports=["numpy"])

# Use the Qwen 2.5 model.
model = "Qwen/Qwen2.5-Coder-32B-Instruct"

# Set up the secure CodeAgent with the configured sandbox.
agent = CodeAgent(
    tools=[],
    model=model,
    sandbox=sandbox
)
4.from smolagents import ToolCallingAgent
from smolagents.models import HfApiModel

def custom_tool(query: str) -> str:
    return f"Simulated search results for: {query}"

agent = ToolCallingAgent(
    tools=[custom_tool],  # Pass the callable tool directly.
    model=HfApiModel("Qwen/Qwen2.5-Coder-32B-Instruct"),  # Actual model object.
    max_steps=5,  # Maximum steps allowed.
    name="ToolAgent",  # Agent's name.
    description="An agent that calls tools to perform search operations."  # Description.
)









5.from smolagents import HfApiModel

# Initialize the Hugging Face model integration with Qwen 2.5.
model = HfApiModel("Qwen/Qwen2.5-Coder-32B-Instruct")

from smolagents import LiteLLMModel

# Provide an alternative model integration using LiteLLMModel with the specified model ID.
alt_model = LiteLLMModel("anthropic/claude-3-sonnet")
