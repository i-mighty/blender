# SPDX-FileCopyrightText: 2025 Kubric Contributors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""
Kubric AI Agent - Core agent class
"""

from typing import Dict, Any, Optional
from .mcp_client import MCPClient


class KubricAgent:
    def __init__(self):
        self.mcp_client = MCPClient()
        self.conversation_history = []

    async def process_message(self, message: str) -> str:
        self.conversation_history.append({"role": "user", "content": message})

        response = "Hello! I'm the Kubric AI agent. LLM integration will be added in Week 1-2."

        self.conversation_history.append({"role": "assistant", "content": response})
        return response

    def get_context(self) -> Dict[str, Any]:
        return {
            "history": self.conversation_history[-10:],
        }

