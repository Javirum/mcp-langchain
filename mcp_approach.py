import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
import asyncio

load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY not found in environment variables.")

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

mcp_client = MultiServerMCPClient({
    "fetch": {
        "transport": "stdio",
        "command": "uvx",
        "args": ["mcp-server-fetch"],
    }
})


async def main():
    # Step 1: Tool discovery — MCP exposes tools automatically
    mcp_tools = await mcp_client.get_tools()
    print(f"Discovered {len(mcp_tools)} tool(s) from MCP server:")
    for tool in mcp_tools:
        print(f"  - {tool.name}: {tool.description[:80]}...")

    # Step 2: Resource loading (if supported)
    resource_context = ""
    try:
        resources = await mcp_client.get_resources()
        print(f"\nLoaded {len(resources)} resource(s)")
        for blob in resources:
            uri = blob.metadata.get("uri", "unknown")
            content = blob.as_string() if blob.mimetype and "text" in blob.mimetype else str(blob.data)
            resource_context += f"\n--- Resource: {uri} ---\n{content}\n"
    except Exception:
        print("\nServer does not support resources, skipping.")

    # Step 3: Create agent with discovered tools
    system_message = "You are a helpful web fetching assistant."
    if resource_context:
        system_message += f"\n\nBackground context:\n{resource_context}"

    agent = create_react_agent(llm, mcp_tools, prompt=system_message)

    # Step 4: Run the agent
    print("\n--- MCP Approach: Running agent ---\n")
    response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "Fetch https://jsonplaceholder.typicode.com/posts/1 and summarize it."}]}
    )

    for msg in response["messages"]:
        print(f"[{msg.type}] {msg.content}")


asyncio.run(main())
