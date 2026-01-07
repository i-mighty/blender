# SPDX-FileCopyrightText: 2025 Kubric Contributors
#
# SPDX-License-Identifier: GPL-2.0-or-later

import bpy
from bpy.types import Operator


class KUBRIC_OT_send_message(Operator):
    bl_idname = "kubric.send_message"
    bl_label = "Send Message"
    bl_description = "Send message to Kubric AI agent"

    def execute(self, context):
        message = context.scene.kubric_chat_input

        if not message.strip():
            self.report({"WARNING"}, "Message is empty")
            return {"CANCELLED"}

        from ..mcp import client as mcp_client
        mcp_status = mcp_client.get_mcp_server_status()

        if not mcp_status["available"]:
            self.report({"ERROR"}, "Blender MCP add-on not found. Please enable it.")
            return {"CANCELLED"}

        if not mcp_status["running"]:
            self.report({"ERROR"}, "Blender MCP server not running. Start it in BlenderMCP panel.")
            return {"CANCELLED"}

        self.report({"INFO"}, f"Message sent: {message}")

        context.scene.kubric_chat_input = ""

        return {"FINISHED"}


def register():
    bpy.utils.register_class(KUBRIC_OT_send_message)


def unregister():
    bpy.utils.unregister_class(KUBRIC_OT_send_message)

