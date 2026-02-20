import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool
import httpx
import asyncio

load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY not found in environment variables.")

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


# Manual tool definition — you control the schema, behavior, and error handling
@tool
async def fetch_url(url: str) -> str:
    """Fetch the contents of a URL and return the response body as text."""
    async with httpx.AsyncClient() as client:
        response = await client.get(url, follow_redirects=True)
        response.raise_for_status()
        return response.text


async def main():
    # Step 1: Tools are defined manually — no discovery needed
    tools = [fetch_url]
    print(f"Registered {len(tools)} tool(s) manually:")
    for t in tools:
        print(f"  - {t.name}: {t.description}")

    # Step 2: Create agent with the same LLM
    agent = create_react_agent(llm, tools, prompt="You are a helpful web fetching assistant.")

    # Step 3: Run the agent with the same query
    print("\n--- Direct Approach: Running agent ---\n")
    response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "Fetch https://jsonplaceholder.typicode.com/posts/1 and summarize it."}]}
    )

    for msg in response["messages"]:
        print(f"[{msg.type}] {msg.content}")


asyncio.run(main())
