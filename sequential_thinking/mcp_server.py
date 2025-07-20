import logging
from typing import Any

from fastmcp import FastMCP

logger = logging.getLogger("SequentialThinking")

mcp: FastMCP[Any] = FastMCP("Sequential Thinking")


@mcp.tool()
def think(
    thread_purpose: str,
    thought: str,
    thought_index: int,
    tool_recommendation: str | None = "None",
    left_to_be_done: str | None = "None",
) -> str:
    """Logs a single step in a thought process for agentic problem-solving.
    Supports thread following, step-tracking, self-correction, and tool recommendations.
    For each new user message, begin a new thought thread and log each thought after each completed step.

    # Key functionalities
        Agentic Workflow Orchestration: Guides through complex tasks by breaking them into precise, manageable, traceable steps.
        Automatic smart thinking process: Avoids over-questionning users about their intention and just figures it out how to proceed.
        Iterative Refinement: Assesses success of each step and self-corrects if necessary, adapting to new information or errors (failure, empty results, etc).
        Tool Recommendation: Suggests relevantly specific available tools (`tool_recommendation`) to execute planned actions or gather necessary information.
        Proactive Planning: Utilizes `left_to_be_done` for explicit future state management and task estimation.

    Args:
        thread_purpose: A concise, high-level objective or thematic identifier for the current thought thread. Essential for organizing complex problem-solving trajectories.
        thought: The detailed, atomic unit of reasoning or action taken by the AI agent at the current step. This forms the core of the agent's internal monologue.
        thought_index: A monotonically increasing integer representing the sequence of thoughts within a specific thread_purpose. Crucial for chronological tracking and revision targeting.
        tool_recommendation: A precise actionable suggestion for the next tool to be invoked, omitted if no tool is needed, directly following the current thought.
        left_to_be_done: A flexible forward-looking statement outlining the next steps or sub-goals to be completed within the current thread_purpose. Supports multi-step planning and progress tracking. Omitted if no further action is needed.

    Returns: A confirmation that the thought has been logged.

    # Example of thought process
    1) user: "I keep hearing about central banks, but I don't understand what they are and how they work."
    2) think(thread_purpose="Central banks explained", thought="Requires information about central banks and how they work. Consider using <named_tool> tool.", thought_index=1, tool_recommendation="<named_tool>", left_to_be_done="Summarize the findings and create an exhaustive graph representation")
    3) call <named_tool>
    4) think(thread_purpose="Central banks explained", thought="Summary of the findings is clear and exhaustive, I have enough information. Must create the graph with <named_tool>.", thought_index=2, tool_recommendation="<named_tool>", left_to_be_done="Send summary and graph to the user")
    5) call <named_tool>
    6) final: respond with summary and graph (no need to call think since left_to_be_done is a simple final step)
    """
    log = f"Thread purpose: {thread_purpose}\nThought {thought_index} logged."
    if tool_recommendation and tool_recommendation.lower() != "none":
        log += f" Recommended tool: {tool_recommendation}."
    extra_log = f"{log}\nThought: {thought}"
    if left_to_be_done and left_to_be_done.lower() != "none":
        extra_log += f"\nNext: {left_to_be_done}"
    logger.info(extra_log)
    return log
