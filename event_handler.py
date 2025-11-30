"""
Event handler for BJJ Research application.
Manages chat history and processes agent stream events.
"""

import json
import logging
from typing import Optional
from pydantic_ai import (
    AgentRunResultEvent,
    FunctionToolCallEvent,
    FunctionToolResultEvent,
)
from ui_utils import (
    create_tool_call_message,
    update_tool_call_with_result,
    create_plan_message,
    create_summary_message,
    create_loading_message,
    create_final_answer_header,
)

logger = logging.getLogger(__name__)


class ChatEventHandler:
    """Handles streaming events from the AI agent and manages chat history."""
    
    def __init__(self, position: str):
        """
        Initialize the event handler.
        
        Args:
            position: The BJJ position being analyzed
        """
        self.position = position
        self.chat_history = []
        self.tool_call_count = 0
        self.pending_tool_calls = {}
        self.final_generation_started = False
        self.final_answer_index: Optional[int] = None
        self.loading_message_index: Optional[int] = None
    
    def get_chat_history(self) -> list:
        """Get a copy of the current chat history."""
        return self.chat_history.copy()
    
    def add_message(self, message: dict):
        """Add a message to chat history."""
        self.chat_history.append(message)
    
    def update_message(self, index: int, message: dict):
        """Update a message at a specific index."""
        self.chat_history[index] = message
    
    def remove_loading_message(self):
        """Remove the loading message if it exists."""
        if self.loading_message_index is not None:
            self.chat_history.pop(self.loading_message_index)
            self.loading_message_index = None
    
    def extract_text_from_args(self, args, key: str, default: str = "") -> str:
        """
        Extract text from tool arguments (handles dict, JSON string, and plain string formats).
        
        Args:
            args: The arguments object (dict, string, or other)
            key: The key to extract from dict/JSON
            default: Default value if extraction fails
            
        Returns:
            Extracted text or default
        """
        if isinstance(args, dict):
            return args.get(key, default)
        elif isinstance(args, str):
            try:
                args_dict = json.loads(args)
                return args_dict.get(key, args)
            except (json.JSONDecodeError, AttributeError):
                return args
        else:
            return str(args) if args else default
    
    def handle_text_delta(self, text_content: str) -> bool:
        """
        Handle text delta events (streaming final answer).
        
        Args:
            text_content: The text content delta
            
        Returns:
            True if chat history was modified
        """
        # First text delta means we're starting final generation
        if not self.final_generation_started:
            self.remove_loading_message()
            
            # Only add "Generating Final Answer" if it wasn't already added with summary
            if not (self.chat_history and "Generating Final Answer" in self.chat_history[-1]["content"]):
                self.add_message({
                    "role": "assistant",
                    "content": "<details><summary><strong>✍️ Generating Final Answer</strong></summary>\n\n*Compiling position analysis and video recommendations...*\n\n</details>"
                })
            self.final_generation_started = True
        
        # Stream the final output
        if self.final_answer_index is not None:
            # Append to existing final answer message
            self.chat_history[self.final_answer_index]["content"] += text_content
        else:
            # Start new final answer message
            msg = create_final_answer_header(self.position, text_content)
            self.add_message(msg)
            self.final_answer_index = len(self.chat_history) - 1
        
        return True
    
    def handle_declare_plan(self, event: FunctionToolCallEvent) -> bool:
        """
        Handle declare_plan tool call event.
        
        Args:
            event: The function tool call event
            
        Returns:
            True if this was a declare_plan event
        """
        if event.part.tool_name != "declare_plan":
            return False
        
        plan_text = self.extract_text_from_args(event.part.args, "plan", "No plan provided")
        self.add_message(create_plan_message(plan_text))
        return True
    
    def handle_summarize_findings(self, event: FunctionToolCallEvent) -> bool:
        """
        Handle summarize_findings tool call event.
        
        Args:
            event: The function tool call event
            
        Returns:
            True if this was a summarize_findings event
        """
        if event.part.tool_name != "summarize_findings":
            return False
        
        summary_text = self.extract_text_from_args(event.part.args, "summary", "No summary provided")
        
        # Add Summary of Findings
        self.add_message(create_summary_message(summary_text))
        
        # Immediately add "Generating Final Answer" message
        self.add_message({
            "role": "assistant",
            "content": "<details><summary><strong>✍️ Generating Final Answer</strong></summary>\n\n*Compiling position analysis and video recommendations...*\n\n</details>"
        })
        self.final_generation_started = True
        
        return True
    
    def handle_tool_call(self, event: FunctionToolCallEvent) -> bool:
        """
        Handle regular tool call events.
        
        Args:
            event: The function tool call event
            
        Returns:
            True if chat history was modified
        """
        # Remove any existing loading message
        self.remove_loading_message()
        
        # Check for special tool handlers
        if self.handle_declare_plan(event):
            return True
        
        if self.handle_summarize_findings(event):
            return True
        
        # Handle regular tool call
        self.tool_call_count += 1
        
        # Create tool call message
        tool_msg = create_tool_call_message(
            self.tool_call_count,
            event.part.tool_name,
            event.part.args
        )
        
        # Add tool call to chat history
        tool_call_id = event.part.tool_call_id
        self.add_message({"role": "assistant", "content": tool_msg})
        
        # Store the index for later update
        self.pending_tool_calls[tool_call_id] = {
            "count": self.tool_call_count,
            "index": len(self.chat_history) - 1,
            "message": tool_msg
        }
        
        logger.info(f"🔧 Tool call #{self.tool_call_count} ({tool_call_id}): {event.part.tool_name}")
        return True
    
    def handle_tool_result(self, event: FunctionToolResultEvent) -> bool:
        """
        Handle tool result events.
        
        Args:
            event: The function tool result event
            
        Returns:
            True if chat history was modified
        """
        # Remove any existing loading message first
        self.remove_loading_message()
        
        result_content = str(event.result.content)
        tool_call_id = event.tool_call_id
        
        # Update the existing tool call message with the result
        if tool_call_id in self.pending_tool_calls:
            tool_data = self.pending_tool_calls[tool_call_id]
            
            # Update message with result
            complete_message = update_tool_call_with_result(
                tool_data["message"],
                result_content
            )
            
            # Update at original index
            self.update_message(
                tool_data["index"],
                {"role": "assistant", "content": complete_message}
            )
            del self.pending_tool_calls[tool_call_id]
            
            # Add loading message after tool completes
            self.add_message(create_loading_message())
            self.loading_message_index = len(self.chat_history) - 1
            
            return True
        else:
            logger.warning(f"Received result for unknown tool call: {tool_call_id}")
            return False
    
    def handle_final_result(self, event: AgentRunResultEvent) -> bool:
        """
        Handle final result event.
        
        Args:
            event: The agent run result event
            
        Returns:
            True if chat history was modified
        """
        final_output = event.result.output
        logger.info("✅ Agent completed successfully")
        
        if not final_output:
            logger.error("❌ Agent returned empty output")
            self.add_message({
                "role": "assistant",
                "content": "❌ Agent did not return any output. Please try again."
            })
            return True
        
        logger.info(f"✅ Position analysis generated successfully ({len(final_output)} characters)")
        
        # If we haven't streamed any output yet, add it now
        if self.final_answer_index is None:
            msg = create_final_answer_header(self.position, final_output)
            self.add_message(msg)
            return True
        
        return False
    
    def process_event(self, event) -> bool:
        """
        Process a single event from the agent stream.
        
        Args:
            event: The event to process
            
        Returns:
            True if chat history was modified
        """
        event_type = type(event).__name__
        
        # Handle text output delta events
        if event_type == "PartDeltaEvent" and hasattr(event, 'delta'):
            delta_type = type(event.delta).__name__
            
            if delta_type == "TextPartDelta" and hasattr(event.delta, "content_delta"):
                return self.handle_text_delta(event.delta.content_delta)
        
        # Handle tool call start
        elif isinstance(event, FunctionToolCallEvent):
            return self.handle_tool_call(event)
        
        # Handle tool result
        elif isinstance(event, FunctionToolResultEvent):
            return self.handle_tool_result(event)
        
        # Handle final result
        elif isinstance(event, AgentRunResultEvent):
            return self.handle_final_result(event)
        
        return False

