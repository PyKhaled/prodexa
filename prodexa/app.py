"""
Prodexa application entry point.

This module is responsible only for:
- Initializing the application
- Delegating execution to the UI layer
"""

from prodexa.ui.app_tk import run_app
from prodexa.__version__ import __version__


def main() -> None:
    """
    Application main entry.
    """
    try:
        run_app()
    except KeyboardInterrupt:
        # Graceful shutdown
        pass


def get_version() -> str:
    """
    Returns current application version.
    """
    return __version__
