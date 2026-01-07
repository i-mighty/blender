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

        row = layout.row()
        row.label(text="AI Assistant", icon="COMMENT")

        from ..mcp import client as mcp_client
        mcp_status = mcp_client.get_mcp_server_status()

        if not mcp_status["available"]:
            box = layout.box()
            box.label(text="Blender MCP add-on not found", icon="ERROR")
            box.label(text="Please enable Blender MCP add-on")
        elif not mcp_status["running"]:
            box = layout.box()
            box.label(text="Blender MCP server not running", icon="INFO")
            box.label(text="Start it in BlenderMCP panel")

        row = layout.row()
        row.prop(context.scene, "kubric_chat_input", text="")

        row = layout.row()
        op = row.operator("kubric.send_message", text="Send", icon="PLAY")
        # The operator will check if MCP is running internally


def register():
    bpy.utils.register_class(KUBRIC_PT_panel)

    bpy.types.Scene.kubric_chat_input = bpy.props.StringProperty(
        name="Chat Input",
        description="Input for Kubric chat",
        default="",
    )


def unregister():
    bpy.utils.unregister_class(KUBRIC_PT_panel)
    del bpy.types.Scene.kubric_chat_input

