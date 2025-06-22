import logging
from typing import Any

from fastmcp import FastMCP

logger = logging.getLogger("SequentialThinking")

mcp: FastMCP[Any] = FastMCP("Sequential Thinking Server")


@mcp.tool()
def think(
    thread_purpose: str,
    thought: str,
    thought_index: int,
    tool_recommendation: str | None = None,
    left_to_be_done: str | None = None,
) -> str:
    """Tool for advanced meta-cognition and dynamic reflective problem-solving via thought logging.
    Supports thread following, step-tracking, self-correction, and tool recommendations.
    For each new user message, begin a new thought thread with this tool.
    You must log a thought after each step and all threads must reach a final thought.

    Key functionalities:
    - Agentic Workflow Orchestration: Guides through complex tasks by breaking them into smart, manageable, traceable steps.
    - Iterative Refinement: Enables thought revision for self-correction and adaptation to new information or errors.
    - Tool Recommendation: Suggests specific tools (`tool_recommendation`) to execute planned actions or gather necessary information.
    - Proactive Planning: Utilizes `left_to_be_done` for explicit future state management and task estimation.

    Args:
    - `thread_purpose` (str): A concise, high-level objective or thematic identifier for the current thought thread. Essential for organizing complex problem-solving trajectories.
    - `thought` (str): The detailed, atomic unit of reasoning or action taken by the AI agent at the current step. This forms the core of the agent's internal monologue.
    - `thought_index` (int): A monotonically increasing integer representing the sequence of thoughts within a specific `thread_purpose`. Crucial for chronological tracking and revision targeting.
    - `tool_recommendation` (str, optional): A precise, actionable suggestion for the next tool to be invoked, directly following the current thought.
    - `left_to_be_done` (str, optional): A flexible forward-looking statement outlining the next steps or sub-goals within the current `thread_purpose`. Supports multi-step planning and progress tracking.

    Example of thought process:
    -> think(thread_purpose="What is inflation?", thought="Must find information about inflation. Consider using 'websearch' tool.", thought_index=1, tool_recommendation="websearch", left_to_be_done="Summarize the findings to respond to the user")
    -> call websearch
    -> think(thread_purpose="What is inflation?", thought="Results seem quite poor. Must retry with a more specific query.", thought_index=2, tool_recommendation="websearch", left_to_be_done="Summarize the findings to respond to the user")
    -> call websearch
    -> think(thread_purpose="What is inflation?", thought="Summarize the findings to present an exhaustive insight to the user.", thought_index=3)
    -> respond with summary
    """
    log = f"Thread purpose: {thread_purpose}\nThought {thought_index} logged."
    if tool_recommendation:
        log += f" Recommended tool: {tool_recommendation}."
    logger.info(f"{log}\nThought: {thought}\nNext: {left_to_be_done}")
    return log


# TODO: Add test_mcp_server.py
