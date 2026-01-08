# SPDX-FileCopyrightText: 2025 Kubric Contributors
#
# SPDX-License-Identifier: GPL-2.0-or-later

# SPDX-FileCopyrightText: 2025 Kubric Contributors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""
Kubric AI Agent - Core agent class
"""

import logging
from typing import Dict, Any, Optional, List

from .mcp_client import MCPClient


logger = logging.getLogger(__name__)


class KubricAgent:
    def __init__(self):
        self.mcp_client = MCPClient()
        self.conversation_history: List[Dict[str, str]] = []
        self.session_context: Dict[str, Any] = {}

    async def process_message(self, message: str, session_id: Optional[str] = None) -> str:
        """
        Process a user message and return agent response
        
        Args:
            message: User message to process
            session_id: Optional session ID for context
            
        Returns:
            Agent response string
        """
        # Store conversation history
        self.conversation_history.append({"role": "user", "content": message})
        
        try:
            # For now, return a simple response
            # TODO: Integrate LLM in Week 1-2
            response = self._generate_response(message)
            
            self.conversation_history.append({"role": "assistant", "content": response})
            logger.info(f"Generated response: {response[:50]}...")
            
            return response
        except Exception as e:
            logger.error(f"Error processing message: {e}", exc_info=True)
            return f"I encountered an error: {str(e)}"

    def _generate_response(self, message: str) -> str:
        """
        Generate a response to the user message
        This is a placeholder until LLM integration is complete
        """
        message_lower = message.lower()
        
        # Simple keyword-based responses for testing
        if any(word in message_lower for word in ["hello", "hi", "hey"]):
            return "Hello! I'm the Kubric AI agent. I'm ready to help you with 3D modeling tasks."
        elif any(word in message_lower for word in ["cube", "create"]):
            return "I understand you want to create something. LLM integration will allow me to execute this through Blender MCP."
        else:
            return "I'm the Kubric AI agent. I can help you with 3D modeling tasks in Blender. Full LLM integration will be added in Week 1-2."

    def get_context(self) -> Dict[str, Any]:
        """Get current conversation context"""
        return {
            "history": self.conversation_history[-10:],
            "session": self.session_context,
            "mcp_connected": self.mcp_client.connected if self.mcp_client else False,
        }

