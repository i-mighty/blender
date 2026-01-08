# SPDX-FileCopyrightText: 2025 Kubric Contributors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""
Kubric AI Agent - Main entry point
"""

import os
from .server import run_server


def main():
    """Main entry point for Kubric Agent"""
    host = os.getenv("AGENT_HOST", "0.0.0.0")
    port = int(os.getenv("AGENT_PORT", "8000"))
    
    run_server(host=host, port=port)


if __name__ == "__main__":
    main()

