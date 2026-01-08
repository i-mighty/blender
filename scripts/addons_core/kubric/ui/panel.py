# SPDX-FileCopyrightText: 2025 Kubric Contributors
#
# SPDX-License-Identifier: GPL-2.0-or-later

import bpy
from bpy.types import Panel


class KUBRIC_PT_panel(Panel):
    bl_label = "Kubric"
    bl_idname = "KUBRIC_PT_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Kubric"

    def draw(self, context):
        layout = self.layout

        # Header
        row = layout.row()
        row.label(text="AI Assistant", icon="COMMENT")

        # Connection Status
        from ..http_client import get_client
        client = get_client()
        agent_connected = client.check_connection()

        box = layout.box()
        if agent_connected:
            row = box.row()
            row.label(text="Agent: Connected", icon="CHECKMARK")
        else:
            row = box.row()
            row.label(text="Agent: Disconnected", icon="ERROR")
            row = box.row()
            row.label(text="Check server URL in preferences")

        # MCP Status
        from ..mcp import client as mcp_client
        mcp_status = mcp_client.get_mcp_server_status()

        if not mcp_status["available"]:
            box = layout.box()
            box.label(text="MCP: Add-on not enabled", icon="INFO")
        elif not mcp_status["running"]:
            box = layout.box()
            box.label(text="MCP: Server not running", icon="INFO")
        else:
            row = layout.row()
            row.label(text="MCP: Connected", icon="CHECKMARK")

        layout.separator()

        # Chat History
        chat_history = getattr(context.scene, "kubric_chat_history", None)
        if chat_history and len(chat_history) > 0:
            box = layout.box()
            box.label(text="Chat History", icon="TEXT")
            
            # Show last 5 messages
            messages_to_show = min(5, len(chat_history))
            for i in range(len(chat_history) - messages_to_show, len(chat_history)):
                msg = chat_history[i]
                row = box.row()
                role = getattr(msg, "role", "unknown")
                message = getattr(msg, "message", "")
                if role == "user":
                    row.label(text=f"You: {message[:50]}{'...' if len(message) > 50 else ''}", icon="USER")
                else:
                    row.label(text=f"Agent: {message[:50]}{'...' if len(message) > 50 else ''}", icon="ASSET_MANAGER")

        layout.separator()

        # Input
        row = layout.row()
        row.prop(context.scene, "kubric_chat_input", text="")

        row = layout.row()
        op = row.operator("kubric.send_message", text="Send", icon="PLAY")
        op.enabled = agent_connected


class KUBRIC_PG_chat_message(bpy.types.PropertyGroup):
    """Chat message property group"""
    role: bpy.props.StringProperty(name="Role", default="")
    message: bpy.props.StringProperty(name="Message", default="")
    timestamp: bpy.props.StringProperty(name="Timestamp", default="")


def register():
    bpy.utils.register_class(KUBRIC_PG_chat_message)
    bpy.utils.register_class(KUBRIC_PT_panel)

    # Chat input property
    bpy.types.Scene.kubric_chat_input = bpy.props.StringProperty(
        name="Chat Input",
        description="Input for Kubric chat",
        default="",
    )

    # Chat history property
    bpy.types.Scene.kubric_chat_history = bpy.props.CollectionProperty(
        type=KUBRIC_PG_chat_message
    )


def unregister():
    bpy.utils.unregister_class(KUBRIC_PT_panel)
    bpy.utils.unregister_class(KUBRIC_PG_chat_message)
    
    del bpy.types.Scene.kubric_chat_input
    if hasattr(bpy.types.Scene, "kubric_chat_history"):
        del bpy.types.Scene.kubric_chat_history

