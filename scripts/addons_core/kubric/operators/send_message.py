# SPDX-FileCopyrightText: 2025 Kubric Contributors
#
# SPDX-License-Identifier: GPL-2.0-or-later

import bpy
from bpy.types import Operator
import threading


class KUBRIC_OT_send_message(Operator):
    bl_idname = "kubric.send_message"
    bl_label = "Send Message"
    bl_description = "Send message to Kubric AI agent"

    def execute(self, context):
        message = context.scene.kubric_chat_input

        if not message.strip():
            self.report({"WARNING"}, "Message is empty")
            return {"CANCELLED"}

        from ..http_client import get_client
        
        # Check agent connection
        client = get_client()
        if not client.check_connection():
            self.report({"ERROR"}, "Cannot connect to Kubric Agent. Check server URL in preferences.")
            return {"CANCELLED"}

        # Check MCP status (optional - we can still send messages even if MCP isn't ready)
        from ..mcp import client as mcp_client
        mcp_status = mcp_client.get_mcp_server_status()
        if not mcp_status["available"]:
            self.report({"WARNING"}, "Blender MCP add-on not enabled. Some features may not work.")

        # Add user message to chat history
        chat_history = getattr(bpy.context.scene, "kubric_chat_history", None)
        if chat_history is not None:
            user_msg = chat_history.add()
            user_msg.role = "user"
            user_msg.message = message
            user_msg.timestamp = bpy.utils.smpte_from_frame(bpy.context.scene.frame_current)

        # Clear input
        context.scene.kubric_chat_input = ""

        # Send message asynchronously
        def on_response(response, error):
            """Callback for when response is received"""
            if error:
                self.report({"ERROR"}, f"Agent error: {error}")
                return

            if response:
                # Add agent response to chat history
                chat_history = getattr(bpy.context.scene, "kubric_chat_history", None)
                if chat_history is not None:
                    agent_msg = chat_history.add()
                    agent_msg.role = "assistant"
                    agent_msg.message = response
                    agent_msg.timestamp = bpy.utils.smpte_from_frame(bpy.context.scene.frame_current)
                
                # Trigger UI update
                for area in bpy.context.screen.areas:
                    if area.type == 'VIEW_3D':
                        area.tag_redraw()

        # Send in background thread
        client.send_message(message, callback=on_response)
        self.report({"INFO"}, "Message sent to agent...")

        return {"FINISHED"}


def register():
    bpy.utils.register_class(KUBRIC_OT_send_message)


def unregister():
    bpy.utils.unregister_class(KUBRIC_OT_send_message)

