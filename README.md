# MCP vs Direct API Integration with LangChain

A side-by-side comparison of two approaches to building LLM-powered tool-calling agents with LangChain and LangGraph: **MCP (Model Context Protocol)** vs **direct API calls**.

Both scripts fetch the same URL, use the same LLM (`gpt-4o-mini`), and produce the same result — the only difference is how the tool is provided to the agent.

## Files

| File | Description |
|---|---|
| `mcp_approach.py` | Uses `mcp-server-fetch` via MCP for automatic tool discovery |
| `direct_approach.py` | Uses `httpx` with a custom `@tool` decorator |
| `comparison.md` | Detailed trade-offs between the two approaches |

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install langchain-openai langchain-mcp-adapters langgraph python-dotenv
```

Create a `.env` file:

```
OPENAI_API_KEY=your-key-here
```

The MCP approach also requires [`uvx`](https://docs.astral.sh/uv/) to run `mcp-server-fetch`.

## Usage

```bash
# MCP approach — tools discovered automatically from the server
python3 mcp_approach.py

# Direct approach — tools defined manually with httpx
python3 direct_approach.py
```

Both scripts fetch `https://jsonplaceholder.typicode.com/posts/1` and ask the agent to summarize it.

## Key Takeaways

- **MCP**: Zero tool code — the server declares tools automatically. Great for composing multiple integrations.
- **Direct**: Full control over HTTP behavior, parsing, and error handling. No subprocess overhead.
- **Hybrid**: You can mix both in the same agent — LangGraph accepts tools from any source.

See [comparison.md](comparison.md) for the full breakdown.
