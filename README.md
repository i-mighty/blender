# Kubric - AI-Assisted Blender Extension

Kubric is an AI-assisted Blender extension that brings Cursor-like AI capabilities to 3D modeling. The MVP focuses on 3D modeling workflows with a dual-mode interface (Editor/Agent modes) and human-in-the-loop design.

## Architecture

Kubric uses a three-component architecture:

1. **Kubric Add-on** (Blender): UI panel, chat interface, communicates with agent
2. **Kubric Agent** (Backend): AI agent that processes messages and calls Blender MCP tools
3. **Blender MCP Server** (Blender): Exposes Blender operations via MCP protocol

**Communication Flow:**

```
User → Kubric Add-on → Kubric Agent → Blender MCP Server → Blender (bpy)
                                                                    ↓
User ← Kubric Add-on ← Kubric Agent ← Blender MCP Server ← Results
```

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed documentation.

## Project Structure

```
scripts/addons_core/kubric/  # Blender add-on
├── __init__.py           # Main add-on entry point
├── preferences.py        # Add-on preferences
├── ui/                   # UI components
│   ├── __init__.py
│   └── panel.py          # Main Kubric panel
├── operators/            # Blender operators
│   ├── __init__.py
│   └── send_message.py   # Send message operator
└── mcp/                  # MCP integration utilities
    ├── __init__.py
    └── client.py         # MCP status/utilities (not direct MCP client)

kubric_agent/             # AI Agent backend
├── __init__.py
├── main.py               # Agent server entry point
├── agent.py              # Core AI agent class
└── mcp_client.py        # MCP client (connects to Blender MCP Server)
```

## Installation

### Blender Add-on

The Kubric add-on is located in `scripts/addons_core/kubric/` and will be automatically included when building Blender locally.

**For local development builds:**

- The add-on is automatically installed in `scripts/addons_core/kubric/`
- After building Blender, enable the add-on:
  - Edit > Preferences > Add-ons
  - Search for "Kubric"
  - Enable the checkbox

**For testing without building:**

- Copy `scripts/addons_core/kubric/` to your Blender add-ons directory:
  - Linux: `~/.config/blender/[version]/scripts/addons/`
  - macOS: `~/Library/Application Support/Blender/[version]/scripts/addons/`
  - Windows: `%APPDATA%\Blender Foundation\Blender\[version]\scripts\addons\`

### Backend Agent

1. Install dependencies:

```bash
cd kubric_agent
pip install -r requirements.txt
```

2. Run the agent server:

```bash
python -m kubric_agent.main
```

## Development Status

**Week 1: Foundation & Basic Integration** (In Progress)

- [x] Project structure setup
- [ ] Blender MCP integration
- [ ] Basic UI panel
- [ ] Backend agent skeleton

## Requirements

- Blender 4.0 or later
- Python 3.10+ (for backend agent)
- Blender MCP add-on (separate add-on that runs MCP server in Blender)
  - See: https://github.com/ahujasid/blender-mcp

## How MCP Integration Works

**Blender MCP Server** runs **inside Blender** (as a separate add-on):

- Exposes Blender operations via MCP protocol
- Executes operations using `bpy` API
- Runs an HTTP server within Blender

**Kubric Agent** (backend) connects to Blender MCP Server **as an MCP client**:

- Processes user messages with LLM
- Decides what Blender operations to perform
- Calls Blender MCP tools via MCP protocol
- Returns results to Kubric Add-on

**Kubric Add-on** (Blender) does **NOT** communicate directly with Blender MCP:

- Only communicates with Kubric Agent (HTTP/WebSocket)
- Displays UI and user interactions

## License

GPL-2.0-or-later
