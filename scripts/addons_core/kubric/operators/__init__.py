# SPDX-FileCopyrightText: 2025 Kubric Contributors
#
# SPDX-License-Identifier: GPL-2.0-or-later

from . import send_message


def register():
    send_message.register()


def unregister():
    send_message.unregister()

