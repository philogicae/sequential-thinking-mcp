import logging
from typing import Any

from fastmcp import FastMCP

logger = logging.getLogger("SequentialThinking")

mcp: FastMCP[Any] = FastMCP("Sequential Thinking Server")


@mcp.tool()
def think(
    thread_purpose: str,
    thought: str,
    thought_number: int,
    nb_remaining_steps: int,
    is_revision: bool = False,
    tool_recommendation: str | None = None,
    left_to_be_done: str | None = None,
) -> str:
    """Tool for dynamic, deep and reflective problem-solving via thought logging.
    Supports thread following, revisions, step-tracking, and tool recommendations.
    For each new user message, begin a new thought thread with this tool.
    Yield now thought after each step, and all threads must reach a final thought.

    # Use for:
    - Process user messages in a smarter step-by-step manner.
    - Breaking down complex problems.
    - Iterative planning & design.
    - Analysis requiring course correction.
    - Maintaining context over multiple steps.
    - Getting assistance with tool suggestions.

    # Key features:
    - Defined purpose for the current line of thinking (`thread_purpose`).
    - Log thoughts sequentially (`thought` and `thought_number`).
    - Revisions of failed thoughts (`thought_number=<original_num>` and `is_revision=True`).
    - Optional tool suggestion for the current thought (`tool_recommendation`).
    - Structured logging of multi-step plans (`left_to_be_done` defined ahead).
    - Flexible thought progression and estimation (adjust `nb_remaining_steps` up to 10).

    # Tool parameters (to be provided in order):
    - `thread_purpose`: (str) Purpose for the current line of thinking.
    - `thought`: (str) Current thinking step/content.
    - `thought_number`: (int) Sequence number for the current thought/revision.
    - `is_revision`: (bool, optional) True if this revises a previous thought. Default: False.
    - `tool_recommendation`: (str, optional) Recommended tool name for the current thought.
    - `left_to_be_done`: (str, optional) Descriptions of upcoming steps.
    - `nb_remaining_steps`: (int) Estimated number of thoughts/steps left (up to 10) for current line of thinking.

    # Example of thought process:
    -> Initial thought:
    think(thread_purpose="What is inflation?", thought="Must find information about inflation. Consider using 'websearch' tool.", thought_number=1, tool_recommendation="websearch", left_to_be_done="Summarize the findings to respond to the user", nb_remaining_steps=1)
    -> Action: call websearch
    -> Revised thought:
    think(thread_purpose="What is inflation?", thought="Results seem too poor. Refine the search query.", thought_number=1, is_revision=True, tool_recommendation="websearch", left_to_be_done="Summarize the findings to respond to the user", nb_remaining_steps=1)
    -> Action: retry websearch
    -> Final thought:
    think(thread_purpose="What is inflation?", thought="Summarize the findings to present an exhaustive insight to the user.", thought_number=2, nb_remaining_steps=0)
    -> Action: respond with summary
    """
    log = f"Thread purpose: {thread_purpose}\n"
    index = f"{thought_number}/{thought_number + nb_remaining_steps}"
    if is_revision:
        log += f"Thought {index} revised."
    elif nb_remaining_steps:
        log += f"Thought {index} logged."
    else:
        log += f"Final thought {index} logged. Process complete."
    if tool_recommendation:
        log += f" Recommended tool: {tool_recommendation}."

    logger.info(f"{log}\nThought: {thought}\nNext: {left_to_be_done}")
    return log
