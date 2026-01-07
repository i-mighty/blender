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
    Check if Blender MCP server is available and running.
    This can be done by checking if the Blender MCP add-on is installed,
    or by attempting to connect to the MCP server.
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


def get_mcp_server_status():
    """
    Get the status of Blender MCP server.
    Returns a dict with status information.
    """
    return {
        "available": is_blender_mcp_available(),
        "running": False,  # TODO: Implement actual check
    }


def register():
    pass


def unregister():
    pass

