import os
import sys
import pytest
from unittest.mock import patch

# Add the directory to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__)))
import security_reminder_hook

def test_get_state_file_normal():
    session_id = "test-session-123"
    path = security_reminder_hook.get_state_file(session_id)
    assert "security_warnings_state_test-session-123.json" in path
    assert path.startswith(os.path.expanduser("~/.claude/"))

def test_get_state_file_traversal():
    session_id = "../../../tmp/malicious"
    path = security_reminder_hook.get_state_file(session_id)
    # Should be sanitized to just 'malicious'
    assert "security_warnings_state_malicious.json" in path
    assert ".." not in path[len(os.path.expanduser("~/.claude/")):]

def test_get_state_file_sanitization():
    session_id = "session!@#$%^&*()_+"
    path = security_reminder_hook.get_state_file(session_id)
    # Only alphanumeric and _- are kept. Note: _ is kept, + is removed.
    assert "security_warnings_state_session_.json" in path

def test_get_state_file_empty_or_invalid():
    assert "security_warnings_state_default.json" in security_reminder_hook.get_state_file("")
    assert "security_warnings_state_default.json" in security_reminder_hook.get_state_file("   ")
    assert "security_warnings_state_default.json" in security_reminder_hook.get_state_file(".")
    assert "security_warnings_state_default.json" in security_reminder_hook.get_state_file("..")

def test_check_patterns():
    # Test path check
    rule, reminder = security_reminder_hook.check_patterns(".github/workflows/deploy.yml", "")
    assert rule == "github_actions_workflow"
    assert "GitHub Actions" in reminder

    # Test content check
    rule, reminder = security_reminder_hook.check_patterns("test.js", "child_process.exec('ls')")
    assert rule == "child_process_exec"
    assert "command injection" in reminder

    # Test no match
    rule, reminder = security_reminder_hook.check_patterns("test.js", "console.log('hello')")
    assert rule is None
    assert reminder is None
