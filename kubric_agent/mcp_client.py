# SPDX-FileCopyrightText: 2025 Kubric Contributors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""
MCP Client for Kubric Agent
"""

import socket
import json
from typing import Dict, Any, Optional


class MCPClient:
    def __init__(self, host="localhost", port=8765):
        self.host = host
        self.port = port
        self.socket = None
        self.connected = False

    def connect(self) -> bool:
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.connected = True
            return True
        except Exception as e:
            print(f"MCP connection error: {e}")
            self.connected = False
            return False

    def disconnect(self):
        if self.socket:
            self.socket.close()
            self.socket = None
        self.connected = False

    def call_tool(self, tool_name: str, params: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        if not self.connected:
            if not self.connect():
                return None

        try:
            message = {
                "method": "tools/call",
                "params": {
                    "name": tool_name,
                    "arguments": params or {},
                },
            }
            data = json.dumps(message).encode("utf-8")
            self.socket.sendall(data)

            response = self.socket.recv(4096).decode("utf-8")
            return json.loads(response)
        except Exception as e:
            print(f"MCP tool call error: {e}")
            self.connected = False
            return None

