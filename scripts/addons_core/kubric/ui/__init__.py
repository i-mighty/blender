# SPDX-FileCopyrightText: 2025 Kubric Contributors
#
# SPDX-License-Identifier: GPL-2.0-or-later

import bpy
from . import panel


def register():
    panel.register()
    
    # Register pending message property
    bpy.types.WindowManager.kubric_message_pending = bpy.props.BoolProperty(
        name="Message Pending",
        description="Whether a message is currently being processed",
        default=False
    )


def unregister():
    panel.unregister()
    
    if hasattr(bpy.types.WindowManager, "kubric_message_pending"):
        del bpy.types.WindowManager.kubric_message_pending

