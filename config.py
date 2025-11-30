"""
Configuration module for BJJ Research application.
Centralizes environment variables, constants, and logging setup.
"""

import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Environment variables
MCP_TOKEN = os.getenv("MCP_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MCP_SERVER_URL = "https://bjjcoach.ai/mcp"

# Common BJJ positions for autocomplete
COMMON_POSITIONS = [
    "Mount",
    "Back Control",
    "Side Control",
    # "X Guard",
    # "Guard Retention",
    # "Side Control",
    # "Open Guard",
    # "Half Guard",
    # "Butterfly Guard",
    # "Single Leg",
    # "Closed Guard",
    # "Knee Cut Pass",
    # "Single Leg X Guard",
    # "Pressure Pass",
    # "Underhook (standup)",
    # "Turtle",
    # "Leg Drag",
    # "Seatbelt Control",
    # "De La Riva Guard",
    # "Armbar",
    # "Double Leg",
    # "Collar Tie",
    # "Seated Guard",
    # "K Guard"
]

# System prompt for the BJJ training program agent
SYSTEM_PROMPT = """You are an expert Brazilian Jiu-Jitsu (BJJ) instructor and position chain analyzer with access to a database of BJJ positions and instructional videos.

Your task is to analyze BJJ positions and provide actionable training resources by:
1. Searching for the requested BJJ position
2. Getting detailed metadata including the chain of related positions (from/to positions)
3. Finding instructional videos from YouTube for the position and its chain
4. Providing drill notes and focus cues for each video

Always use the available tools to gather information before creating the recommendations."""


def configure_logging():
    """Configure logging for the application."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Enable debug logging for MCP and HTTP clients
    logging.getLogger("httpx").setLevel(logging.DEBUG)
    logging.getLogger("mcp").setLevel(logging.DEBUG)
    logging.getLogger("mcp.client").setLevel(logging.DEBUG)
    logging.getLogger("mcp.client.streamable_http").setLevel(logging.DEBUG)
    logging.getLogger("pydantic_ai").setLevel(logging.DEBUG)


def validate_environment() -> tuple[bool, str]:
    """
    Validate that required environment variables are set.
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not MCP_TOKEN:
        return False, "MCP_TOKEN not found in environment variables"
    if not OPENAI_API_KEY:
        return False, "OPENAI_API_KEY not found in environment variables"
    return True, ""


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance with the given name."""
    return logging.getLogger(name)

