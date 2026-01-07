# Kubric Architecture

## Overview

Kubric uses a three-component architecture:
1. **Kubric Add-on** (Blender): UI and communication with agent
2. **Kubric Agent** (Backend): AI agent that processes messages and calls Blender MCP
3. **Blender MCP Server** (Blender): Exposes Blender operations via MCP protocol

## Component Responsibilities

### 1. Kubric Add-on (Blender App)
**Location**: `scripts/addons_core/kubric/`
**Purpose**: User interface and communication with the agent

**Responsibilities**:
- Display UI panel in 3D Viewport sidebar
- Chat interface for user input
- Display agent responses and action history
- Show previews and review/approve UI
- Communicate with Kubric Agent (HTTP/WebSocket)
- **Does NOT** communicate directly with Blender MCP

### 2. Kubric Agent (Backend Process)
**Location**: `kubric_agent/`
**Purpose**: AI agent that processes user requests and executes Blender operations

**Responsibilities**:
- Receive user messages from Kubric Add-on
- Process messages with LLM (Claude/DeepSeek)
- Plan actions and decide what Blender operations to perform
- **Call Blender MCP Server** as an MCP client
- Return results to Kubric Add-on

### 3. Blender MCP Server (Blender App)
**Location**: Separate add-on (e.g., `blender-mcp` from GitHub)
**Purpose**: Expose Blender operations via MCP protocol

**Responsibilities**:
- Run as an MCP server within Blender
- Expose Blender operations as MCP tools (create_cube, scene_inspection, etc.)
- Execute operations using `bpy` API
- Return results to MCP clients (like Kubric Agent)

## Communication Flow

```
User (Blender UI)
    │
    │ Types message
    ▼
Kubric Add-on (Blender)
    │
    │ HTTP/WebSocket
    ▼
Kubric Agent (Backend)
    │
    │ Processes with LLM
    │ Decides: "create a cube"
    │
    │ MCP Protocol (HTTP/JSON-RPC)
    ▼
Blender MCP Server (Blender)
    │
    │ Executes via bpy
    │ bpy.ops.mesh.primitive_cube_add()
    ▼
Blender Scene (Object created)
    │
    │ Results flow back
    ▼
Kubric Agent
    │
    │ Returns result
    ▼
Kubric Add-on
    │
    │ Shows preview
    ▼
User (Review & Approve)
```

## Detailed Flow Example

**User Request**: "Add a cube"

1. **User** types "Add a cube" in Kubric panel
2. **Kubric Add-on** sends HTTP request to Kubric Agent:
   ```json
   {
     "message": "Add a cube",
     "user_id": "...",
     "session_id": "..."
   }
   ```

3. **Kubric Agent** receives message:
   - Processes with LLM: understands "add a cube"
   - Decides to call Blender MCP tool: `create_cube`
   - Connects to Blender MCP Server (MCP client)

4. **Kubric Agent** calls Blender MCP Server:
   ```json
   {
     "method": "tools/call",
     "params": {
       "name": "create_cube",
       "arguments": {}
     }
   }
   ```

5. **Blender MCP Server** (running in Blender):
   - Receives MCP call
   - Executes: `bpy.ops.mesh.primitive_cube_add()`
   - Returns result: `{"success": true, "object_name": "Cube"}`

6. **Kubric Agent** receives result:
   - Formats response for user
   - Returns to Kubric Add-on

7. **Kubric Add-on**:
   - Shows preview of created cube
   - Displays message: "I've created a cube for you"
   - Shows review/approve UI

8. **User** reviews and approves

## Why This Architecture?

### Separation of Concerns

- **Kubric Add-on**: UI and user interaction only
- **Kubric Agent**: AI reasoning and planning
- **Blender MCP**: Blender operation execution

### Benefits

1. **Reusability**: Blender MCP can be used by other tools/agents
2. **Security**: Blender MCP handles all Blender operations, agent doesn't need direct Blender access
3. **Flexibility**: Agent can call multiple Blender MCP tools in sequence
4. **Maintainability**: Each component has a clear responsibility

## Implementation Notes

### Blender MCP Server
- Should be installed as a separate add-on (or we can bundle it)
- Runs an HTTP server within Blender
- Uses MCP protocol (JSON-RPC-like) to expose tools
- Examples: `create_cube`, `scene_inspection`, `apply_material`, etc.

### Kubric Agent MCP Client
- Connects to Blender MCP Server as an MCP client
- Uses MCP SDK (or custom implementation) to call tools
- Handles tool discovery, execution, and error handling

### Communication Protocols

1. **Add-on ↔ Agent**: HTTP REST or WebSocket
   - Simple request/response initially
   - WebSocket for real-time updates later

2. **Agent ↔ Blender MCP**: MCP Protocol
   - Standard MCP JSON-RPC-like protocol
   - Tool calls, results, errors

## Current Implementation Status

### ✅ Implemented
- Kubric Add-on basic structure
- Kubric Agent skeleton
- Basic UI panel

### 🚧 In Progress (Week 1)
- Blender MCP integration
- Communication between add-on and agent

### 📋 Planned
- LLM integration in agent
- MCP tool discovery and calling
- Preview and review UI

