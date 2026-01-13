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
        row.label(text="AI Assistant", icon="CONSOLE")

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
        
        # Check if there's a pending message
        wm = context.window_manager
        is_pending = getattr(wm, "kubric_message_pending", False)
        
        if chat_history and len(chat_history) > 0:
            box = layout.box()
            header_row = box.row()
            header_row.label(text="Chat History", icon="TEXTURE")
            
            # Show pending indicator if message is being processed
            if is_pending:
                header_row.label(text="Processing...", icon="INFO")
            
            # Show messages (last 10 messages for better visibility)
            messages_to_show = min(10, len(chat_history))
            start_idx = max(0, len(chat_history) - messages_to_show)
            
            for i in range(start_idx, len(chat_history)):
                msg = chat_history[i]
                role = getattr(msg, "role", "unknown")
                message = getattr(msg, "message", "")
                
                if not message:
                    continue
                
                # Create message row with better formatting
                msg_row = box.row()
                msg_row.scale_y = 0.85
                
                if role == "user":
                    # User message - right side
                    msg_box = msg_row.box()
                    msg_box.scale_x = 0.92
                    split = msg_box.split(factor=0.95)
                    col = split.column()
                    col.alignment = 'RIGHT'
                    # Split long messages into multiple lines
                    for line in message.split('\n')[:3]:  # Max 3 lines per message
                        if line.strip():
                            col.label(text=line.strip(), icon="USER")
                else:
                    # Agent message - left side
                    split = msg_row.split(factor=0.08)
                    split.label(text="", icon="ASSET_MANAGER")
                    msg_box = split.box()
                    msg_box.scale_x = 0.95
                    col = msg_box.column()
                    col.alignment = 'LEFT'
                    # Split long messages into multiple lines
                    for line in message.split('\n')[:5]:  # Max 5 lines per message
                        if line.strip():
                            col.label(text=line.strip())
        else:
            box = layout.box()
            if is_pending:
                box.label(text="Sending message...", icon="INFO")
            else:
                box.label(text="No messages yet", icon="CONSOLE")
                box.label(text="Start a conversation below", icon="INFO")

        layout.separator()

        # Input Section
        box = layout.box()
        row = box.row()
        row.prop(context.scene, "kubric_chat_input", text="", icon="TEXTURE")
        
        row = box.row()
        row.scale_y = 1.2
        # Disable send button if not connected
        if not agent_connected:
            row.enabled = False
        op = row.operator("kubric.send_message", text="Send", icon="PLAY")
            
        # Helper text
        if not agent_connected:
            row = box.row()
            row.scale_y = 0.8
            row.label(text="Connect to agent to send messages", icon="INFO")


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

