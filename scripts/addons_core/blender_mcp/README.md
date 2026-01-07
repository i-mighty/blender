# Blender MCP Add-on

This is the Blender MCP add-on bundled with Blender.

## Overview

The Blender MCP add-on creates a socket server within Blender that allows external MCP clients (like Kubric Agent) to control Blender via the Model Context Protocol.

## Original Source

This add-on is based on [blender-mcp](https://github.com/ahujasid/blender-mcp) by Siddharth Ahuja.

## Integration with Kubric

This add-on works with Kubric:
1. **Blender MCP Add-on** (this add-on) runs in Blender and creates a socket server on port 9876
2. **Blender MCP Server** (separate process) connects to this socket server and implements the MCP protocol
3. **Kubric Agent** connects to the Blender MCP Server as an MCP client

## Usage

1. Enable the "Blender MCP" add-on in Blender preferences
2. Go to the 3D Viewport sidebar (press N)
3. Find the "BlenderMCP" tab
4. Click "Connect to Claude" or similar to start the server
5. The server will listen on localhost:9876

## Port Configuration

Default port: 9876 (configurable via environment variable `BLENDER_PORT`)

## License

MIT License (original source)

