# SPDX-FileCopyrightText: 2025 Kubric Contributors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""
Kubric AI Agent - Main entry point
"""

import asyncio
import json
from typing import Dict, Any
from .agent import KubricAgent
from .mcp_client import MCPClient


class AgentServer:
    def __init__(self, host="localhost", port=8000):
        self.host = host
        self.port = port
        self.agent = KubricAgent()
        self.mcp_client = MCPClient()

    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        message = request.get("message", "")
        if not message:
            return {"error": "No message provided"}

        try:
            response = await self.agent.process_message(message)
            return {"response": response}
        except Exception as e:
            return {"error": str(e)}

    def run(self):
        print(f"Kubric Agent Server starting on {self.host}:{self.port}")
        print("Note: Full HTTP server implementation will be added in Week 2")


if __name__ == "__main__":
    server = AgentServer()
    server.run()

