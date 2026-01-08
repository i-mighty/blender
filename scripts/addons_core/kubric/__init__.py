# SPDX-FileCopyrightText: 2025 Kubric Contributors
#
# SPDX-License-Identifier: GPL-2.0-or-later

bl_info = {
    "name": "Kubric",
    "author": "Kubric Team",
    "version": (0, 1, 0),
    "blender": (4, 0, 0),
    "location": "3D Viewport > Sidebar > Kubric",
    "description": "AI-assisted 3D modeling with natural language interface",
    "warning": "Development version",
    "doc_url": "",
    "support": "COMMUNITY",
    "category": "3D View",
}

import bpy

from . import preferences
from . import ui
from . import operators
from . import mcp
from . import http_client


def register():
    preferences.register()
    operators.register()
    ui.register()
    mcp.register()


def unregister():
    ui.unregister()
    operators.unregister()
    mcp.unregister()
    preferences.unregister()
    
    # Reset HTTP client when unregistering
    http_client.reset_client()


if __name__ == "__main__":
    register()

