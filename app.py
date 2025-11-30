"""
BJJ Research - Gradio 6 App with MCP Integration
Analyzes BJJ positions, discovers position chains, and provides YouTube video recommendations
with drill notes and focus cues using Pydantic AI agents and MCP tools.
"""

import logfire
import gradio as gr
from config import (
    MCP_TOKEN,
    MCP_SERVER_URL,
    COMMON_POSITIONS,
    configure_logging,
    validate_environment,
    get_logger,
)
from ui_utils import (
    validate_position_input,
    create_error_message,
    create_status_message,
)
from agent_setup import (
    create_mcp_server,
    initialize_mcp_server,
    create_agent,
    build_instruction,
)
from event_handler import ChatEventHandler

# Configure Logfire
logfire.configure()
logfire.instrument_pydantic_ai()
logfire.instrument_httpx()
logfire.instrument_openai()

# Configure logging
configure_logging()
logger = get_logger(__name__)


async def generate_program(position: str):
    """
    Generate position chain analysis and video recommendations for the given BJJ position.
    Streams all agent activity in real-time.
    
    Args:
        position: The BJJ position to analyze
        
    Yields:
        List of message dictionaries for unified chat interface
    """
    # Initialize event handler
    event_handler = ChatEventHandler(position)
    
    try:
        # Validate input
        is_valid, error_msg = validate_position_input(position)
        if not is_valid:
            event_handler.add_message({"role": "assistant", "content": error_msg})
            yield event_handler.get_chat_history()
            return
        
        logger.info(f"🎯 Starting program generation for: {position}")
        
        # Add initial status message
        event_handler.add_message(create_status_message(
            "🎯 Analyzing Position: " + position,
            "Starting analysis...",
            is_open=True
        ))
        yield event_handler.get_chat_history()
        
        # Validate environment variables
        is_valid, error_msg = validate_environment()
        if not is_valid:
            raise ValueError(error_msg)
        
        # Initialize MCP server and agent
        event_handler.add_message(create_status_message(
            "🔧 Initialization",
            "- Creating MCP server connection...",
            is_open=True
        ))
        yield event_handler.get_chat_history()
        
        mcp_server = create_mcp_server(MCP_TOKEN, MCP_SERVER_URL)
        
        event_handler.update_message(-1, create_status_message(
            "🔧 Initialization",
            "- Creating MCP server connection...\n- ✅ MCP server connected",
            is_open=True
        ))
        yield event_handler.get_chat_history()
        
        # Use context manager for MCP connection
        async with mcp_server:
            await initialize_mcp_server(mcp_server)
            
            event_handler.update_message(-1, create_status_message(
                "🔧 Initialization",
                "- Creating MCP server connection...\n- ✅ MCP server connected\n- ✅ MCP server initialized",
                is_open=True
            ))
            yield event_handler.get_chat_history()
            
            # Create agent
            agent = create_agent(mcp_server)
            
            event_handler.update_message(-1, create_status_message(
                "🔧 Initialization",
                "- Creating MCP server connection...\n- ✅ MCP server connected\n- ✅ MCP server initialized\n- ✅ AI Agent created with Responses API (gpt-5), MCP toolset, and planning tools",
                is_open=False
            ))
            yield event_handler.get_chat_history()
            
            # Add agent execution message
            event_handler.add_message(create_status_message(
                "🤖 Agent Execution",
                "*Agent is analyzing the position and calling tools...*",
                is_open=True
            ))
            yield event_handler.get_chat_history()
            
            # Build instruction and run agent
            instruction = build_instruction(position)
            
            logger.info("🚀 Running agent with streaming and reasoning enabled...")
            logger.info("🤖 Starting agent execution...")
            
            # Stream agent execution
            async for event in agent.run_stream_events(instruction):
                if event_handler.process_event(event):
                    yield event_handler.get_chat_history()
    
    except ValueError as e:
        logger.error(f"❌ Configuration Error: {e}")
        error_history = [create_error_message(e, "Configuration Error")]
        yield error_history
    except Exception as e:
        logger.error(f"❌ Unexpected Error: {e}", exc_info=True)
        error_history = [create_error_message(e)]
        yield error_history


def create_interface() -> gr.Blocks:
    """Create the Gradio 6 interface."""
    
    with gr.Blocks(title="BJJ Position Chain Analyzer") as demo:
        gr.Markdown("""
        # 🥋 BJJ Position Chain Analyzer
        
        Analyze BJJ positions, discover position chains, and get curated YouTube videos with instructions how to practice the position.
        
        *Powered by [BJJ Coach AI](https://bjjcoach.ai) - Your intelligent BJJ training companion*
        """)
        
        with gr.Row():
            with gr.Column(scale=3):
                position_input = gr.Dropdown(
                    choices=COMMON_POSITIONS,
                    label="BJJ Position",
                    info="Select a position or type your own",
                    allow_custom_value=True,
                    value="Mount"
                )
            with gr.Column(scale=1):
                generate_btn = gr.Button("Analyze Position", variant="primary", size="lg")
        
        with gr.Row():
            with gr.Column():
                chat_output = gr.Chatbot(
                    label="Position Analysis (Debug info is collapsible)",
                    value=[],
                    height=800,
                    autoscroll=True
                )
        
        # Event handler
        generate_btn.click(
            fn=generate_program,
            inputs=[position_input],
            outputs=[chat_output]
        )
    
    return demo


def main():
    """Main entry point for the application."""
    
    # Check environment variables
    is_valid, error_msg = validate_environment()
    if not is_valid:
        print(f"⚠️  Warning: {error_msg}")
    
    # Create and launch the interface
    demo = create_interface()
    
    # Launch with Gradio 6 syntax
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )


if __name__ == "__main__":
    main()
