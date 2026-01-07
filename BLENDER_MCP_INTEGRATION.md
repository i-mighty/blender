# Blender MCP Integration

## Overview

Blender MCP has been integrated as a built-in dependency for Kubric. This document explains how the components work together.

## Components

### 1. Blender MCP Add-on
**Location**: `scripts/addons_core/blender_mcp/`
**Source**: [blender-mcp](https://github.com/ahujasid/blender-mcp) by Siddharth Ahuja

This add-on runs within Blender and:
- Creates a TCP socket server on port 9876 (default)
- Receives JSON commands via the socket
- Executes Blender operations using `bpy` API
- Returns results as JSON responses

**Installation**: Automatically included when building Blender locally

### 2. Blender MCP Server (MCP Protocol Server)
**Location**: `extern/blender_mcp/`
**Purpose**: Implements the Model Context Protocol

This server runs as a separate Python process and:
- Connects to the Blender MCP add-on's socket server (port 9876)
- Implements the MCP protocol (JSON-RPC-like)
- Exposes Blender operations as MCP tools
- Can be connected to by MCP clients (like Kubric Agent)

**Note**: Requires external dependencies (`mcp.server.fastmcp`), which need to be installed separately:
```bash
pip install mcp
```

### 3. Kubric Agent
**Location**: `kubric_agent/`
**Purpose**: AI agent that uses Blender MCP

The Kubric Agent:
- Connects to Blender MCP Server as an MCP client
- Processes user messages with LLM
- Calls Blender MCP tools to perform operations
- Returns results to Kubric Add-on

## Communication Flow

```
User (Kubric Add-on)
    ↓
    │ Types message: "Add a cube"
    ▼
Kubric Add-on (Blender)
    ↓ HTTP/WebSocket
    │ Sends to Kubric Agent
    ▼
Kubric Agent (Backend)
    ↓
    │ Processes with LLM
    │ Decides: call "create_cube" tool
    │
    │ MCP Protocol (HTTP/JSON)
    ▼
Blender MCP Server (Separate Process)
    ↓
    │ Connects to Blender MCP Add-on
    │ TCP Socket (port 9876)
    │ JSON command: {"type": "create_cube"}
    ▼
Blender MCP Add-on (Blender)
    ↓
    │ Executes: bpy.ops.mesh.primitive_cube_add()
    ▼
Blender Scene
    ↓
    │ Cube created
    │ Results flow back
    ▼
Kubric Agent
    ↓
    │ Returns response
    ▼
Kubric Add-on
    ↓
    │ Shows preview
    ▼
User (Reviews & Approves)
```

## Setup Instructions

### 1. Enable Blender MCP Add-on

1. Build Blender locally (add-on is automatically included)
2. Open Blender
3. Go to Edit > Preferences > Add-ons
4. Search for "Blender MCP"
5. Enable the checkbox

### 2. Start Blender MCP Server

The Blender MCP server needs to be started separately:

```bash
# Install dependencies
pip install mcp

# Run the MCP server
python -m extern.blender_mcp.server
# Or if using the original structure:
python -m blender_mcp.server
```

**Note**: The server will automatically connect to the Blender MCP add-on's socket server on localhost:9876

### 3. Configure Kubric Agent

The Kubric Agent needs to be configured to connect to the Blender MCP Server. This will be implemented in Week 1-2.

## Port Configuration

- **Blender MCP Add-on socket server**: Port 9876 (default, configurable via `BLENDER_PORT` environment variable)
- **Blender MCP Server (MCP protocol)**: HTTP server (port TBD, typically 8000-9000)
- **Kubric Agent**: HTTP server for Kubric Add-on (port 8000, configurable)

## Development Notes

### External Dependencies

The Blender MCP server requires:
- `mcp` package (MCP SDK)
- Other dependencies as specified in the original blender-mcp repository

These are not bundled with Blender and need to be installed separately for the MCP server to run.

### Integration Status

- ✅ Blender MCP add-on bundled in `scripts/addons_core/blender_mcp/`
- ✅ Blender MCP server code bundled in `extern/blender_mcp/`
- ✅ Kubric detects Blender MCP availability
- 🚧 Kubric Agent MCP client integration (Week 1-2)
- 🚧 Full end-to-end communication (Week 1-2)

## References

- Original Blender MCP: https://github.com/ahujasid/blender-mcp
- Model Context Protocol: https://modelcontextprotocol.io/

