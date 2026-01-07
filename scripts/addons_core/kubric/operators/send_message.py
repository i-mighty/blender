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

        self.report({"INFO"}, f"Message sent: {message}")

        context.scene.kubric_chat_input = ""

        return {"FINISHED"}


def register():
    bpy.utils.register_class(KUBRIC_OT_send_message)


def unregister():
    bpy.utils.unregister_class(KUBRIC_OT_send_message)

