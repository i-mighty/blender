# SPDX-FileCopyrightText: 2025 Kubric Contributors
#
# SPDX-License-Identifier: GPL-2.0-or-later

from . import client


def register():
    client.register()


def unregister():
    client.unregister()

