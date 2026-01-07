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

        row = layout.row()
        row.prop(context.scene, "kubric_chat_input", text="")

        row = layout.row()
        row.operator("kubric.send_message", text="Send", icon="PLAY")


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

