# SPDX-FileCopyrightText: 2025 Kubric Contributors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""
Test script to verify Kubric add-on is properly loaded
Run this in Blender's Python console or as a script

Usage in Blender's Python console:
    import addon_utils
    import kubric
    kubric.test_addon()
    
Or directly:
    from kubric import test_addon
    test_addon()
"""

import bpy

def test_kubric_addon():
    """Test if Kubric add-on is loaded and enabled"""
    print("=" * 60)
    print("Kubric Add-on Diagnostic Test")
    print("=" * 60)
    
    # Check if add-on is in preferences
    if "kubric" in bpy.context.preferences.addons:
        print("✓ Add-on found in preferences")
        addon = bpy.context.preferences.addons["kubric"]
        if addon:
            print(f"  - Module: {addon.module}")
            print(f"  - Enabled: {hasattr(addon, 'preferences')}")
            if hasattr(addon, 'preferences'):
                prefs = addon.preferences
                print(f"  - Server URL: {prefs.agent_server_url}")
    else:
        print("✗ Add-on NOT found in preferences")
        print("  → Go to Edit > Preferences > Add-ons")
        print("  → Search for 'Kubric' and enable it")
        return False
    
    # Check if panel is registered
    if hasattr(bpy.types, "KUBRIC_PT_panel"):
        print("✓ Panel class registered")
    else:
        print("✗ Panel class NOT registered")
        return False
    
    # Check if operator is registered
    if hasattr(bpy.types, "KUBRIC_OT_send_message"):
        print("✓ Send message operator registered")
    else:
        print("✗ Send message operator NOT registered")
        return False
    
    # Check if properties are registered
    if hasattr(bpy.types.Scene, "kubric_chat_input"):
        print("✓ Chat input property registered")
    else:
        print("✗ Chat input property NOT registered")
        return False
    
    if hasattr(bpy.types.Scene, "kubric_chat_history"):
        print("✓ Chat history property registered")
    else:
        print("✗ Chat history property NOT registered")
        return False
    
    print("\n" + "=" * 60)
    print("How to access the Kubric panel:")
    print("1. Open the 3D Viewport")
    print("2. Press 'N' to toggle the sidebar (or View > Sidebar)")
    print("3. Look for the 'Kubric' tab in the sidebar")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    test_kubric_addon()
