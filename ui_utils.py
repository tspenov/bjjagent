"""
UI utilities for BJJ Research application.
Contains functions for message formatting and input validation.
"""

from typing import Optional


def validate_position_input(position: str) -> tuple[bool, Optional[str]]:
    """
    Validate user input for BJJ position.
    
    Args:
        position: The position string to validate
        
    Returns:
        Tuple of (is_valid, error_message). error_message is None if valid.
    """
    if not position or position.strip() == "":
        return False, "❌ Please enter a BJJ position."
    return True, None


def create_error_message(error: Exception, error_type: str = "Error") -> dict:
    """
    Format an error message for the chat interface.
    
    Args:
        error: The exception that occurred
        error_type: Type of error (e.g., "Configuration Error", "Error")
        
    Returns:
        Chat message dictionary
    """
    if error_type == "Configuration Error":
        content = f"❌ Configuration Error: {str(error)}\n\nPlease check your .env file."
    else:
        content = f"❌ Error: {str(error)}\n\nPlease check:\n- Your MCP_TOKEN is valid\n- Your OPENAI_API_KEY is valid\n- The BJJ Coach MCP server is accessible\n- The position name is correct"
    
    return {"role": "assistant", "content": content}


def create_status_message(title: str, details: str, is_open: bool = True) -> dict:
    """
    Create a collapsible status message for the chat interface.
    
    Args:
        title: The title/summary of the status message
        details: The detailed content
        is_open: Whether the details should be open by default
        
    Returns:
        Chat message dictionary
    """
    open_attr = "open" if is_open else ""
    content = f"<details {open_attr}><summary><strong>{title}</strong></summary>\n\n{details}\n\n</details>"
    return {"role": "assistant", "content": content}


def create_tool_call_message(tool_count: int, tool_name: str, args: dict) -> str:
    """
    Create a formatted tool call message with collapsible details.
    
    Args:
        tool_count: The sequential number of this tool call
        tool_name: Name of the tool being called
        args: Arguments passed to the tool
        
    Returns:
        Formatted HTML string for the message
    """
    import json
    
    msg = f"<details><summary><strong>🔧 Tool Call #{tool_count}: `{tool_name}`</strong></summary>\n\n"
    
    if args:
        args_str = json.dumps(args, indent=2)
        msg += "**Arguments:**\n\n"
        msg += f"```json\n{args_str}\n```\n\n"
    
    msg += "*⏳ Running...*\n\n"
    msg += "</details>"
    
    return msg


def update_tool_call_with_result(base_message: str, result_content: str) -> str:
    """
    Update a tool call message with its result.
    
    Args:
        base_message: The original tool call message
        result_content: The result to append
        
    Returns:
        Updated message with result
    """
    # Remove the "Running..." text and closing tag
    base = base_message.replace("*⏳ Running...*\n\n</details>", "")
    
    # Add result section
    result_section = f"**✅ Result:**\n\n```\n{result_content}\n```\n\n</details>"
    
    return base + result_section


def create_plan_message(plan_text: str) -> dict:
    """
    Create a formatted message for the agent's initial plan.
    
    Args:
        plan_text: The plan text from the agent
        
    Returns:
        Chat message dictionary
    """
    content = f"<details><summary><strong>🧠 Initial Plan</strong></summary>\n\n{plan_text}\n\n</details>"
    return {"role": "assistant", "content": content}


def create_summary_message(summary_text: str) -> dict:
    """
    Create a formatted message for the agent's findings summary.
    
    Args:
        summary_text: The summary text from the agent
        
    Returns:
        Chat message dictionary
    """
    content = f"<details><summary><strong>📊 Summary of Findings</strong></summary>\n\n{summary_text}\n\n</details>"
    return {"role": "assistant", "content": content}


def create_loading_message() -> dict:
    """
    Create a loading/thinking message.
    
    Returns:
        Chat message dictionary
    """
    content = "<details open><summary><strong>🤔 Agent is thinking...</strong></summary>\n\nProcessing results and planning next step...\n\n</details>"
    return {"role": "assistant", "content": content}


def create_final_answer_header(position: str, text_content: str = "") -> dict:
    """
    Create the header for the final answer message.
    
    Args:
        position: The BJJ position being analyzed
        text_content: Optional initial text content
        
    Returns:
        Chat message dictionary
    """
    content = f"## 📋 Position Analysis: {position}\n\n{text_content}"
    return {"role": "assistant", "content": content}

