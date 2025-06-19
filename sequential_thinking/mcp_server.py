from typing import Any

from fastmcp import FastMCP

mcp: FastMCP[Any] = FastMCP("Sequential Thinking Server")

thought_history: list[dict[str, Any]] = []


@mcp.tool()
def think(
    thought: str,
    thought_number: int,
    total_thoughts: int,
    next_thought_needed: bool,
    is_revision: bool = False,
    revises_thought: int | None = None,
    available_tools: list[str] | None = None,
    request_tool_recommendation: bool = False,
    current_step: dict[str, Any] | None = None,
    previous_steps: list[dict[str, Any]] | None = None,
    remaining_steps: list[str | dict[str, Any]] | None = None,
) -> str:
    """Tool for dynamic, reflective problem-solving via logged thoughts. Supports revisions, step-tracking, and tool recommendations.

    Use for:
    - Breaking down complex problems.
    - Iterative planning & design.
    - Analysis requiring course correction.
    - Maintaining context over multiple steps.
    - Getting assistance with tool suggestions.

    Key features:
    - Flexible thought progression (adjust total_thoughts).
    - Revisions of thoughts.
    - Structured logging of multi-step plans (current, previous, remaining steps).
    - Optional tool recommendations based on `available_tools`.

    Parameters (`think` tool):
    - `thought`: (str) Current thinking step/content.
    - `next_thought_needed`: (bool) True if more thinking is required; False for final thought.
    - `thought_number`: (int) Sequence number for the current thought/revision.
    - `total_thoughts`: (int) Estimated total thoughts for current line of thinking.
    - `is_revision`: (bool, optional) True if this revises a previous thought. Default: False.
    - `revises_thought`: (int, optional) If `is_revision`, the `thought_number` of the thought to revise.
    - `available_tools`: (list[str], optional) User-provided tool names for recommendation.
    - `request_tool_recommendation`: (bool, optional) True to request tool suggestions. Default: False.
    - `current_step`: (dict, optional) User-defined dict for the current operational step.
    - `previous_steps`: (list[dict], optional) User-defined list of dicts for completed steps.
    - `remaining_steps`: (list[str|dict], optional) User-defined list for upcoming steps.

    Basic Usage:
    1. Log thoughts sequentially using `thought_number`.
    2. To revise: `is_revision=True`, `revises_thought=<original_num>`, `thought_number=<original_num>`.
    3. For tool suggestions: `request_tool_recommendation=True` (optionally pass `available_tools`).

    Example:
    # Initial thought
    think(thought="Analyze requirements.", thought_number=1, total_thoughts=3, next_thought_needed=True)
    # Thought with tool recommendation request
    think(thought="Consider using 'websearch' tool.", thought_number=2, total_thoughts=3, next_thought_needed=True, request_tool_recommendation=True, available_tools=["websearch", "list_files", "read_file", "summarize_text"])
    # Final thought
    think(thought="Solution defined.", thought_number=3, total_thoughts=3, next_thought_needed=False)
    """

    if is_revision and revises_thought is None:
        return "Error: `revises_thought` must be provided when `is_revision` is true."

    thought_data = {
        "thought": thought,
        "thought_number": thought_number,
        "total_thoughts": total_thoughts,
        "next_thought_needed": next_thought_needed,
        "is_revision": is_revision,
        "revises_thought": revises_thought,
        "available_tools": available_tools,
        "request_tool_recommendation": request_tool_recommendation,
        "recommended_tools_for_thought": [],
        "current_step": current_step,
        "previous_steps": previous_steps,
        "remaining_steps": remaining_steps,
    }

    if is_revision and revises_thought:
        revise_index = next(
            (
                i
                for i, t in enumerate(thought_history)
                if t["thought_number"] == revises_thought
            ),
            None,
        )
        if revise_index is not None:
            thought_history[revise_index] = thought_data
        else:
            return (
                f"Error: Thought {revises_thought} not found in history for revision."
            )
    else:
        thought_history.append(thought_data)

    recommendation_text = ""
    all_tools_for_recommendation = set(available_tools or [])

    if request_tool_recommendation and all_tools_for_recommendation:
        suggested = []
        for tool_name in sorted(list(all_tools_for_recommendation)):
            if tool_name.lower() in thought.lower():
                suggested.append(tool_name)

        if suggested:
            thought_data["recommended_tools_for_thought"] = suggested
            recommendation_text = (
                f"\nRecommended tools for this thought: {', '.join(suggested)}."
            )
        else:
            recommendation_text = "\nNo tool keywords matched in thought."
    elif request_tool_recommendation:
        recommendation_text = "\nTool recommendation requested, but no tools were provided in `available_tools`."

    if is_revision:
        return f"Thought {revises_thought} revised.{recommendation_text}"

    if next_thought_needed:
        return f"Thought {thought_number}/{total_thoughts} logged.{recommendation_text}"
    else:
        return f"Final thought {thought_number}/{total_thoughts} logged. Process complete.{recommendation_text}"


@mcp.tool()
def get_thought_history() -> str:
    """Get the complete thought history as a formatted string."""
    if not thought_history:
        return "No thoughts recorded yet."
    result = "# Thought History\n\n"
    for thought in thought_history:
        result += (
            f"## Thought {thought['thought_number']}/{thought['total_thoughts']}:\n"
        )
        result += f"{thought['thought']}\n\n"
    return result.strip()


@mcp.tool()
def clear_thoughts() -> str:
    """Clears all recorded thoughts."""
    global thought_history
    thought_history = []
    return "All thoughts have been cleared."
