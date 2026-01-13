# Kubric Add-on

AI-assisted 3D modeling with natural language interface for Blender.

## Installation

The Kubric add-on is automatically included when building Blender from source (located in `scripts/addons_core/kubric`).

## Enabling the Add-on

1. Open Blender
2. Go to **Edit > Preferences > Add-ons**
3. Search for "Kubric" in the search box
4. Check the checkbox next to "Kubric" to enable it

## Accessing the Chat Interface

1. Open the **3D Viewport** (default view when Blender starts)
2. Press **N** to toggle the sidebar (or go to **View > Sidebar**)
3. Look for the **"Kubric"** tab in the sidebar
4. The chat interface should be visible in that panel

## Configuration

1. Go to **Edit > Preferences > Add-ons**
2. Find "Kubric" and click on it to expand
3. Configure:
   - **Agent Server URL**: Default is `http://localhost:8000`
   - **API Key**: Your LLM API key (if required)
   - **Default Mode**: Editor or Agent mode
   - **Auto-approve Simple Actions**: Enable to skip review for simple actions

## Troubleshooting

### Can't see the panel?

1. **Check if add-on is enabled**: Go to Preferences > Add-ons and verify "Kubric" is checked
2. **Check the 3D Viewport**: The panel only appears in the 3D Viewport sidebar
3. **Check the sidebar**: Press **N** to toggle the sidebar if it's hidden
4. **Look for the "Kubric" tab**: It should be in the sidebar tabs (alongside Item, Tool, View, etc.)

### Test the add-on

Run this in Blender's Python console (Window > Toggle System Console, then Scripting workspace):

```python
import kubric
kubric.test_addon()
```

This will check if the add-on is properly loaded and registered, and show you how to access the panel.

### Connection Issues

- Make sure the Kubric Agent server is running (see `kubric_agent/README.md`)
- Check the server URL in preferences matches your agent server
- The panel will show connection status (Connected/Disconnected)

## Development

See the main project README for development setup and testing instructions.
