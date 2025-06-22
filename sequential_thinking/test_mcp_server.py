from typing import Any

import pytest
from fastmcp import Client

from .mcp_server import mcp


@pytest.fixture(scope="session")
def mcp_client() -> Client[Any]:
    """Create a FastMCP client for testing."""
    return Client(mcp)


@pytest.mark.asyncio
async def test_think(mcp_client: Client[Any]) -> None:
    """Test the 'think' tool."""
    async with mcp_client as client:
        result = await client.call_tool(
            "think",
            {
                "thread_purpose": "What is berserk?",
                "thought": "Must find information about berserk. Consider using 'websearch' tool.",
                "thought_index": 1,
                "tool_recommendation": "websearch",
                "left_to_be_done": "Summarize the findings to respond to the user",
            },
        )
        assert result is not None and len(result[0].text) > 32
