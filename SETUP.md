# Kubric Setup Guide

## Week 1: Foundation Setup

This guide covers the initial setup for the Kubric add-on and backend agent.

## Prerequisites

- Blender 4.0 or later
- Python 3.10+ (for backend agent)
- Git (for cloning Blender MCP if needed)

## Blender Add-on Installation

### Automatic Installation (Local Build)

The Kubric add-on is located in `scripts/addons_core/kubric/` and will be automatically included when building Blender locally.

1. **Build Blender:**
   ```bash
   # Follow Blender's build instructions
   # The add-on will be automatically included in the build
   ```

2. **Enable the add-on in Blender:**
   - Open your locally built Blender
   - Go to Edit > Preferences > Add-ons
   - Search for "Kubric"
   - Enable the checkbox

3. **Verify installation:**
   - Open a 3D Viewport
   - Press `N` to open the sidebar (or View > Sidebar)
   - Look for the "Kubric" tab in the sidebar

### Manual Installation (Testing Without Build)

For testing without building Blender:

1. **Locate Blender's add-ons directory:**
   - Linux: `~/.config/blender/[version]/scripts/addons/`
   - macOS: `~/Library/Application Support/Blender/[version]/scripts/addons/`
   - Windows: `%APPDATA%\Blender Foundation\Blender\[version]\scripts\addons\`

2. **Copy the kubric directory:**
   ```bash
   cp -r scripts/addons_core/kubric ~/.config/blender/[version]/scripts/addons/
   ```

3. **Enable the add-on in Blender** (same as above)

## Backend Agent Setup

### Initial Setup

1. **Navigate to the agent directory:**
   ```bash
   cd kubric_agent
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the agent server:**
   ```bash
   python -m kubric_agent.main
   ```

   Note: Full HTTP server implementation will be added in Week 2.

## Blender MCP Integration

### Installing Blender MCP

1. **Clone the Blender MCP repository:**
   ```bash
   git clone https://github.com/ahujasid/blender-mcp.git
   cd blender-mcp
   ```

2. **Follow Blender MCP installation instructions:**
   - Install the Blender add-on component
   - Set up the MCP server
   - Configure connection settings

3. **Test MCP connection:**
   - Start Blender MCP server
   - Verify it's listening on the expected port (default: 8765)

### Integration with Kubric

The Kubric add-on includes a basic MCP client in `kubric/mcp/client.py`. This will be extended in Week 1-2 to:

- Connect to Blender MCP server
- Call MCP tools (create_cube, scene_inspection, etc.)
- Handle responses and errors

## Testing Week 1 Features

### Test 1: Add-on Registration

1. Enable the Kubric add-on in Blender preferences
2. Verify no errors in the Blender console
3. Check that the Kubric panel appears in the 3D Viewport sidebar

### Test 2: Basic UI Panel

1. Open 3D Viewport
2. Open sidebar (N key)
3. Click on "Kubric" tab
4. Verify you see:
   - "AI Assistant" label
   - Chat input field
   - Send button

### Test 3: Send Message Operator

1. Type a message in the chat input
2. Click "Send" button
3. Check Blender console for "Message sent: [your message]"
4. Verify input field clears after sending

### Test 4: MCP Connection (After MCP Setup)

1. Start Blender MCP server
2. The MCP client will attempt to connect automatically
3. Check console for connection status

## Development Workflow

### Reloading the Add-on

During development, you can reload the add-on without restarting Blender:

1. In Blender, go to Edit > Preferences > Add-ons
2. Find "Kubric" add-on
3. Click the refresh/reload button (circular arrow icon)
4. Or disable and re-enable the add-on

### Debugging

- Check Blender's console for Python errors
- Use `print()` statements for debugging (visible in console)
- Enable Python error reporting in Blender preferences

## Next Steps (Week 2)

- Implement full HTTP communication between add-on and agent
- Add LLM integration to the agent
- Implement first end-to-end command ("Add a cube")
- Create chat message history display

## Troubleshooting

### Add-on doesn't appear

- For local builds: Ensure Blender was built after adding the add-on
- For manual installation: Check that the `kubric` directory is in the correct add-ons location
- Verify `scripts/addons_core/kubric/__init__.py` contains valid `bl_info`
- Check Blender console for import errors

### Panel doesn't show

- Ensure you're in 3D Viewport (not other editors)
- Press `N` to toggle sidebar if hidden
- Check that panel is registered correctly

### MCP connection fails

- Verify Blender MCP server is running
- Check port numbers match (default: 8765)
- Review firewall settings

