# SPDX-FileCopyrightText: 2025 Kubric Contributors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""
Kubric Agent HTTP Server
FastAPI-based server for communication with Kubric Add-on
"""

import asyncio
import logging
from contextlib import asynccontextmanager
from typing import Dict, Any, Optional

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn

from .agent import KubricAgent
from .mcp_client import MCPClient


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Request/Response Models
class MessageRequest(BaseModel):
    """Request model for user messages"""
    message: str = Field(..., description="User message to process")
    session_id: Optional[str] = Field(None, description="Session ID for conversation context")
    user_id: Optional[str] = Field(None, description="User ID")


class MessageResponse(BaseModel):
    """Response model for agent messages"""
    response: str = Field(..., description="Agent response")
    session_id: Optional[str] = Field(None, description="Session ID")
    status: str = Field("success", description="Response status")


class HealthResponse(BaseModel):
    """Health check response"""
    status: str = Field("healthy", description="Service status")
    version: str = Field("0.1.0", description="Agent version")
    mcp_connected: bool = Field(False, description="MCP connection status")


# Global agent instance
_agent: Optional[KubricAgent] = None
_mcp_client: Optional[MCPClient] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown"""
    global _agent, _mcp_client
    
    logger.info("Starting Kubric Agent server...")
    
    # Initialize agent
    _agent = KubricAgent()
    _mcp_client = MCPClient()
    
    # Try to connect to MCP (non-blocking)
    # MCP connection will be established when first used
    logger.info("MCP client will connect on first use")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Kubric Agent server...")
    if _mcp_client:
        _mcp_client.disconnect()
    _agent = None
    _mcp_client = None


# Create FastAPI app
app = FastAPI(
    title="Kubric Agent API",
    description="AI agent for Kubric Blender extension",
    version="0.1.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    global _mcp_client
    
    mcp_connected = False
    if _mcp_client:
        mcp_connected = _mcp_client.connected
    
    return HealthResponse(
        status="healthy",
        version="0.1.0",
        mcp_connected=mcp_connected
    )


@app.post("/api/v1/message", response_model=MessageResponse)
async def process_message(request: MessageRequest):
    """
    Process a user message and return agent response
    
    Args:
        request: Message request with user message and optional session/user IDs
        
    Returns:
        Message response with agent reply
    """
    global _agent
    
    if not _agent:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Agent not initialized"
        )
    
    try:
        logger.info(f"Processing message: {request.message[:50]}...")
        
        # Process message with agent
        response = await _agent.process_message(request.message)
        
        return MessageResponse(
            response=response,
            session_id=request.session_id,
            status="success"
        )
    except Exception as e:
        logger.error(f"Error processing message: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing message: {str(e)}"
        )


@app.get("/api/v1/status")
async def get_status():
    """Get agent status"""
    global _agent, _mcp_client
    
    status_info = {
        "agent_initialized": _agent is not None,
        "mcp_connected": _mcp_client.connected if _mcp_client else False,
        "mcp_host": _mcp_client.host if _mcp_client else None,
        "mcp_port": _mcp_client.port if _mcp_client else None,
    }
    
    return status_info


def run_server(host: str = "0.0.0.0", port: int = 8000):
    """
    Run the FastAPI server
    
    Args:
        host: Host to bind to
        port: Port to bind to
    """
    logger.info(f"Starting Kubric Agent server on {host}:{port}")
    
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info",
        access_log=True
    )


if __name__ == "__main__":
    import os
    
    host = os.getenv("AGENT_HOST", "0.0.0.0")
    port = int(os.getenv("AGENT_PORT", "8000"))
    
    run_server(host=host, port=port)

