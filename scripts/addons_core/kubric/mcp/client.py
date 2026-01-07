# SPDX-FileCopyrightText: 2025 Kubric Contributors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""
Blender MCP Server Integration

This module handles integration with Blender MCP server.
Note: The Kubric add-on does NOT directly communicate with Blender MCP.
Instead, it communicates with the Kubric Agent, which then calls Blender MCP.

This module may be used for:
- Checking if Blender MCP server is running
- Utility functions for MCP-related operations
- Future: Direct MCP communication if needed (e.g., for local operations)
"""

import bpy


def is_blender_mcp_available():
    """
    Check if Blender MCP add-on is installed and available.
    Since Blender MCP is now a built-in add-on, it should be available.
    """
    try:
        import addon_utils
        addons = addon_utils.modules()
        blender_mcp_installed = any(
            'blender_mcp' in addon.__name__ or 'blendermcp' in addon.__name__.lower()
            for addon in addons
        )
        return blender_mcp_installed
    except Exception:
        return False


def is_blender_mcp_running():
    """
    Check if Blender MCP server is currently running.
    This checks if the socket server is listening on the default port.
    """
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.1)
        result = sock.connect_ex(('localhost', 9876))
        sock.close()
        return result == 0
    except Exception:
        return False


def get_mcp_server_status():
    """
    Get the status of Blender MCP server.
    Returns a dict with status information.
    """
    return {
        "available": is_blender_mcp_available(),
        "running": is_blender_mcp_running(),
        "port": 9876,
        "host": "localhost",
    }


def register():
    pass


def unregister():
    pass

