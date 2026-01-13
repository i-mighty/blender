# SPDX-FileCopyrightText: 2025 Kubric Contributors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""
HTTP Client for Kubric Add-on
Handles communication with Kubric Agent server
"""

import bpy
import json
import urllib.request
import urllib.error
import urllib.parse
import threading
from typing import Dict, Any, Optional, Callable
from datetime import datetime


class KubricHTTPClient:
    """HTTP client for communicating with Kubric Agent"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip("/")
        self.timeout = 30.0
        self._session_id: Optional[str] = None
        self._connected = False
        
    def check_connection(self) -> bool:
        """
        Check if agent server is reachable
        
        Returns:
            True if connected, False otherwise
        """
        try:
            url = f"{self.base_url}/health"
            request = urllib.request.Request(url, method="GET")
            
            with urllib.request.urlopen(request, timeout=5.0) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode())
                    self._connected = True
                    return True
        except Exception as e:
            print(f"Kubric: Connection check failed: {e}")
            self._connected = False
            return False
        
        self._connected = False
        return False
    
    def send_message(
        self,
        message: str,
        callback: Optional[Callable[[str, Optional[str]], None]] = None
    ) -> Optional[str]:
        """
        Send a message to the agent (synchronous)
        
        Args:
            message: Message to send
            callback: Optional callback for async processing
            
        Returns:
            Agent response or None if error
        """
        if callback:
            # Run in background thread
            thread = threading.Thread(
                target=self._send_message_async,
                args=(message, callback),
                daemon=True
            )
            thread.start()
            return None
        
        return self._send_message_sync(message)
    
    def _send_message_sync(self, message: str) -> Optional[str]:
        """Send message synchronously"""
        try:
            url = f"{self.base_url}/api/v1/message"
            
            data = {
                "message": message,
                "session_id": self._session_id,
            }
            
            json_data = json.dumps(data).encode("utf-8")
            request = urllib.request.Request(
                url,
                data=json_data,
                headers={
                    "Content-Type": "application/json",
                },
                method="POST"
            )
            
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                if response.status == 200:
                    result = json.loads(response.read().decode())
                    response_text = result.get("response", "")
                    
                    # Store session ID if provided
                    if "session_id" in result:
                        self._session_id = result["session_id"]
                    
                    return response_text
                else:
                    print(f"Kubric: Server returned status {response.status}")
                    return None
                    
        except urllib.error.HTTPError as e:
            print(f"Kubric: HTTP error: {e.code} - {e.reason}")
            try:
                error_body = e.read().decode()
                print(f"Kubric: Error details: {error_body}")
            except:
                pass
            return None
        except urllib.error.URLError as e:
            print(f"Kubric: URL error: {e.reason}")
            self._connected = False
            return None
        except Exception as e:
            print(f"Kubric: Unexpected error: {e}")
            return None
    
    def _send_message_async(
        self,
        message: str,
        callback: Callable[[str, Optional[str]], None]
    ):
        """Send message asynchronously in background thread"""
        response = self._send_message_sync(message)
        error = None if response else "Failed to get response from agent"
        callback(response, error)
    
    def get_status(self) -> Dict[str, Any]:
        """Get agent server status"""
        try:
            url = f"{self.base_url}/api/v1/status"
            request = urllib.request.Request(url, method="GET")
            
            with urllib.request.urlopen(request, timeout=5.0) as response:
                if response.status == 200:
                    return json.loads(response.read().decode())
        except Exception as e:
            print(f"Kubric: Status check failed: {e}")
        
        return {
            "agent_initialized": False,
            "mcp_connected": False,
        }
    
    @property
    def connected(self) -> bool:
        """Check if client is connected to agent"""
        return self._connected


# Global client instance
_http_client: Optional[KubricHTTPClient] = None


def get_client() -> KubricHTTPClient:
    """Get or create global HTTP client instance"""
    global _http_client
    
    try:
        prefs = bpy.context.preferences.addons["kubric"].preferences
        base_url = prefs.agent_server_url
    except (AttributeError, KeyError):
        # Fallback if preferences not loaded yet or add-on not enabled
        base_url = "http://localhost:8000"
    
    if _http_client is None or _http_client.base_url != base_url:
        _http_client = KubricHTTPClient(base_url=base_url)
    
    return _http_client


def reset_client():
    """Reset global client instance (e.g., when preferences change)"""
    global _http_client
    _http_client = None

