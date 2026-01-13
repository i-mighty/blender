# SPDX-FileCopyrightText: 2025 Kubric Contributors
#
# SPDX-License-Identifier: GPL-2.0-or-later

import bpy
from bpy.types import AddonPreferences
from bpy.props import StringProperty, IntProperty, BoolProperty, EnumProperty


class KubricPreferences(AddonPreferences):
    bl_idname = "kubric"

    agent_server_url: StringProperty(
        name="Agent Server URL",
        description="URL of the Kubric AI Agent server",
        default="http://localhost:8000",
    )

    agent_api_key: StringProperty(
        name="API Key",
        description="API key for LLM service",
        default="",
        subtype="PASSWORD",
    )

    default_mode: EnumProperty(
        name="Default Mode",
        description="Default mode when Kubric is enabled",
        items=[
            ("EDITOR", "Editor", "Editor mode: workspace primary, agent in sidebar"),
            ("AGENT", "Agent", "Agent mode: chat primary, workspace optional"),
        ],
        default="EDITOR",
    )

    auto_approve_simple: BoolProperty(
        name="Auto-approve Simple Actions",
        description="Automatically approve simple actions without review",
        default=False,
    )

    def draw(self, context):
        layout = self.layout

        layout.label(text="Agent Configuration")
        layout.prop(self, "agent_server_url")
        layout.prop(self, "agent_api_key")

        layout.separator()

        layout.label(text="User Preferences")
        layout.prop(self, "default_mode")
        layout.prop(self, "auto_approve_simple")


def register():
    bpy.utils.register_class(KubricPreferences)


def unregister():
    bpy.utils.unregister_class(KubricPreferences)

