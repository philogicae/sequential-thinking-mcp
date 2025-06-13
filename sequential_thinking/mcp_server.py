from typing import Any

from fastmcp import Context, FastMCP

mcp: FastMCP[Any] = FastMCP(
    name="Sequential Thinking Server",
    instructions=(
        "Always use this server to break down complex problems "
        "into manageable steps through a structured thinking process."
    ),
)

thought_history: list[dict[str, Any]] = []
thought_branches: dict[str, list[dict[str, Any]]] = {}


@mcp.tool()
def think(
    thought: str,
    thought_number: int,
    total_thoughts: int,
    next_thought_needed: bool,
    is_revision: bool | None = None,
    revises_thought: int | None = None,
    branch_from_thought: int | None = None,
    branch_id: str | None = None,
    needs_more_thoughts: bool | None = None,
    ctx: Context | None = None,
) -> str:
    """
    Facilitates a detailed, step-by-step thinking process for problem-solving and analysis.

    Args:
        thought: The current thinking step
        thought_number: Current thought number
        total_thoughts: Estimated total thoughts needed
        next_thought_needed: Whether another thought step is needed
        is_revision: Whether this revises previous thinking
        revises_thought: Which thought is being reconsidered
        branch_from_thought: Branching point thought number
        branch_id: Branch identifier
        needs_more_thoughts: If more thoughts are needed
        ctx: MCP context

    Returns:
        Response message about the recorded thought
    """
    thought_data = {
        "thought": thought,
        "thought_number": thought_number,
        "total_thoughts": total_thoughts,
        "next_thought_needed": next_thought_needed,
        "is_revision": is_revision,
        "revises_thought": revises_thought,
        "branch_from_thought": branch_from_thought,
        "branch_id": branch_id,
        "needs_more_thoughts": needs_more_thoughts,
    }

    if branch_id:
        if branch_from_thought:
            if branch_id not in thought_branches:
                branch_from_index = next(
                    (
                        i
                        for i, t in enumerate(thought_history)
                        if t["thought_number"] == branch_from_thought
                    ),
                    None,
                )

                if branch_from_index is not None:
                    thought_branches[branch_id] = thought_history[
                        : branch_from_index + 1
                    ].copy()
                else:
                    thought_branches[branch_id] = []

        if branch_id in thought_branches:
            if is_revision and revises_thought:
                revise_index = next(
                    (
                        i
                        for i, t in enumerate(thought_branches[branch_id])
                        if t["thought_number"] == revises_thought
                    ),
                    None,
                )
                if revise_index is not None:
                    thought_branches[branch_id][revise_index] = thought_data
            else:
                thought_branches[branch_id].append(thought_data)
    else:
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
            thought_history.append(thought_data)

    if is_revision:
        return f"Revised thought {revises_thought}."

    if branch_id:
        branch_text = f" (Branch: {branch_id})"
    else:
        branch_text = ""

    if next_thought_needed:
        if needs_more_thoughts:
            return (
                f"Recorded thought {thought_number}"
                f"/{total_thoughts}{branch_text}. More thoughts will be needed."
            )
        else:
            return (
                f"Recorded thought {thought_number}"
                f"/{total_thoughts}{branch_text}. Continue with the next thought."
            )
    else:
        return (
            f"Recorded final thought {thought_number}"
            f"/{total_thoughts}{branch_text}. The thinking process is complete."
        )


@mcp.resource("thoughts://history")
def get_thought_history() -> str:
    """
    Get the complete thought history as a formatted string.

    Returns:
        Formatted thought history
    """
    if not thought_history:
        return "No thoughts recorded yet."

    result = "# Thought History\n\n"
    for thought in thought_history:
        result += (
            f"## Thought {thought['thought_number']}/{thought['total_thoughts']}\n\n"
        )
        result += f"{thought['thought']}\n\n"

    return result


@mcp.resource("thoughts://branches/{branch_id}")
def get_branch_thoughts(branch_id: str) -> str:
    """
    Get the thoughts for a specific branch.

    Args:
        branch_id: The branch identifier

    Returns:
        Formatted branch thoughts
    """
    if branch_id not in thought_branches:
        return f"Branch '{branch_id}' not found."

    if not thought_branches[branch_id]:
        return f"No thoughts recorded for branch '{branch_id}'."

    result = f"# Branch: {branch_id}\n\n"
    for thought in thought_branches[branch_id]:
        result += (
            f"## Thought {thought['thought_number']}/{thought['total_thoughts']}\n\n"
        )
        result += f"{thought['thought']}\n\n"

    return result


@mcp.resource("thoughts://summary")
def get_thought_summary() -> str:
    """
    Get a summary of all thoughts and branches.

    Returns:
        Summary of thoughts and branches
    """
    result = "# Sequential Thinking Summary\n\n"

    result += "## Main Thought Line\n\n"
    result += f"- Total thoughts: {len(thought_history)}\n"
    if thought_history:
        result += (
            f"- Current progress: Thought "
            f"{thought_history[-1]['thought_number']}"
            f"/{thought_history[-1]['total_thoughts']}\n"
        )

    if thought_branches:
        result += "\n## Branches\n\n"
        for branch_id, branch in thought_branches.items():
            result += f"- Branch '{branch_id}': {len(branch)} thoughts\n"

    return result


@mcp.prompt()
def thinking_process_guide() -> str:
    """
    Guide for using the sequential thinking process.
    """
    return """
    # Sequential Thinking Process Guide
    
    This tool helps break down complex problems into manageable steps through a structured thinking process.
    
    ## How to Use
    
    1. Start with an initial thought (thought_number = 1)
    2. Continue adding thoughts sequentially
    3. You can revise previous thoughts if needed
    4. You can create branches to explore alternative paths
    
    ## Example
    
    ```python
    # First thought
    think(
        thought="First, we need to understand the problem requirements.",
        thought_number=1,
        total_thoughts=5,
        next_thought_needed=True
    )
    
    # Second thought
    think(
        thought="Now, let's analyze the key constraints.",
        thought_number=2,
        total_thoughts=5,
        next_thought_needed=True
    )
    
    # Revise a thought
    think(
        thought="Actually, we need to clarify the problem requirements first.",
        thought_number=1,
        total_thoughts=5,
        next_thought_needed=True,
        is_revision=True,
        revises_thought=1
    )
    
    # Branch from thought 2
    think(
        thought="Let's explore an alternative approach.",
        thought_number=3,
        total_thoughts=5,
        next_thought_needed=True,
        branch_from_thought=2,
        branch_id="alternative-approach"
    )
    ```
    """
