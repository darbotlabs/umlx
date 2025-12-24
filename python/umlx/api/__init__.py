# Copyright © 2025 UMLX Contributors

"""
UMLX FastAPI Integration

This module provides REST API access to UMLX functionality.
"""

from .server import app, start_server

__all__ = ["app", "start_server"]
