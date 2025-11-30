"""
Agent setup utilities for BJJ Research application.
Contains functions for creating MCP server, agent, and building instructions.
"""

import asyncio
import logging
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStreamableHTTP
from pydantic_ai.models.openai import OpenAIResponsesModel
from agent_tools import declare_plan, summarize_findings

logger = logging.getLogger(__name__)


def create_mcp_server(token: str, url: str) -> MCPServerStreamableHTTP:
    """
    Create and configure MCP server instance.
    
    Args:
        token: MCP authentication token
        url: MCP server URL
        
    Returns:
        Configured MCPServerStreamableHTTP instance
    """
    logger.info("🔧 Creating MCP server connection...")
    mcp_server = MCPServerStreamableHTTP(
        url,
        headers={'Authorization': f'Bearer {token}'}
    )
    logger.info("✅ MCP server instance created")
    return mcp_server


async def initialize_mcp_server(mcp_server: MCPServerStreamableHTTP):
    """
    Initialize MCP server connection and wait for SSE to establish.
    
    Args:
        mcp_server: The MCP server instance to initialize
    """
    logger.info("✅ MCP server initialized")
    # Wait for SSE connection to fully establish
    logger.info("⏳ Waiting for SSE connection to establish...")
    await asyncio.sleep(0.5)  # Give SSE time to fully connect
    logger.info("✅ SSE connection ready")


def create_agent(mcp_server: MCPServerStreamableHTTP) -> Agent:
    """
    Create Pydantic AI agent with MCP toolset and planning tools.
    
    Args:
        mcp_server: Initialized MCP server instance
        
    Returns:
        Configured Agent instance
    """
    # Create OpenAI Responses API model with reasoning enabled
    model = OpenAIResponsesModel('gpt-5-nano')
    logger.info("✅ OpenAI Responses model created")
    
    # Create pydantic-ai agent with MCP server as toolset, planning tools, and Responses API model
    agent = Agent(
        model,
        toolsets=[mcp_server],
        tools=[declare_plan, summarize_findings]
    )
    logger.info("✅ Agent created with MCP toolset, planning tools, and Responses API")
    
    return agent


def build_instruction(position: str) -> str:
    """
    Generate the instruction prompt for the agent.
    
    Args:
        position: The BJJ position to analyze
        
    Returns:
        Formatted instruction string
    """
    instruction = f"""Analyze the BJJ position "{position}" and provide position chains with video recommendations.

IMPORTANT WORKFLOW - You MUST follow this exact sequence:

0. **Declare your plan**: Call declare_plan() with your 2-3 sentence approach
1. **Search for the position**: Use the search tool to find the position ID for "{position}"
2. **Get position metadata**: Retrieve detailed information including the chain of related positions (from/to positions). 
   Important: Always use the position ID instead of position name as argument
3. **Identify position chains**: Extract the chain of positions that connect to and from the main position
4. **Fetch videos**: Get instructional videos from YouTube:
   - 20 videos for the original position "{position}". Leave out 10 in final answer.
5. **Summarize findings**: Call summarize_findings() with a brief summary of what you learned (position chains found, number of videos retrieved, etc.)
6. **Create final recommendations**: Generate the structured output below

Output format (markdown):

# Position Analysis: [Position Name]

## Position Chains
- **From positions**: [list positions that lead to this one]
- **To positions**: [list positions this one leads to]

## Video Recommendations

### Original Position: [Position Name]
[only 10 relevant videos with drill notes and focus cues for each]

### Chain Positions
Don't fetch new videos per chain position. 
Look in the returned videos for the original position and identify videos for chain positions based on video information and analysed position chains. 
Only include videos that are related to the position chains. 
If there are no videos for a chain position omit this section.

"""
    
    logger.info(f"📝 Instruction length: {len(instruction)} characters")
    return instruction

