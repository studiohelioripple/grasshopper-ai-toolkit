"""
tests/test_live_bridge.py - Unit tests for live Rhino 8 Grasshopper bridge.
"""

import os
import pytest
from gh_toolkit.live import (
    find_rhinocode,
    get_rhino_env,
    get_bridge_tmp_dir,
    is_rhino_running,
    get_rhino_instances,
    live_status,
)


def test_rhinocode_detection():
    """Verify rhinocode path detection logic."""
    rhinocode_path = find_rhinocode()
    # On macOS with Rhino 8 installed, this should find /Applications/Rhino 8.app/...
    if os.path.exists("/Applications/Rhino 8.app"):
        assert rhinocode_path is not None
        assert "rhinocode" in rhinocode_path.lower()


def test_rhino_env_roll_forward():
    """Verify environment variables configure .NET roll forward properly."""
    env = get_rhino_env()
    assert env.get("DOTNET_ROLL_FORWARD") == "LatestMajor"


def test_bridge_tmp_dir_creation():
    """Verify bridge exchange directory is created in user space."""
    tmp_dir = get_bridge_tmp_dir()
    assert os.path.exists(tmp_dir)
    assert os.path.isdir(tmp_dir)
    assert ".gh_toolkit" in tmp_dir


def test_get_rhino_instances_structure():
    """Verify get_rhino_instances returns a list of dictionaries with expected keys."""
    instances = get_rhino_instances()
    assert isinstance(instances, list)
    for inst in instances:
        assert "pid" in inst
        assert "pipe_id" in inst


def test_live_status_structure():
    """Verify live_status produces valid dictionary output."""
    status = live_status()
    assert isinstance(status, dict)
    assert "rhino_running" in status
