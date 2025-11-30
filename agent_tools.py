"""
Agent tools for BJJ Research application.
Contains tool functions that the AI agent can call during execution.
"""


async def declare_plan(plan: str) -> str:
    """
    Agent declares its plan before taking action.
    
    Args:
        plan: A brief description of the planned approach (2-3 sentences)
    
    Returns:
        Confirmation message
    """
    return "Plan recorded. Proceed with execution."


async def summarize_findings(summary: str) -> str:
    """
    Agent summarizes the key information gathered from tool calls before generating the final answer.
    
    Args:
        summary: A brief summary of the key findings (2-4 sentences)
    
    Returns:
        Confirmation message
    """
    return "Summary recorded. Proceed with final answer generation."

