import os
import json
import pytest
import shutil
import tempfile
import sys
from datetime import datetime
from unittest.mock import patch, MagicMock

# Add the directory containing the hook to sys.path
hook_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, hook_dir)

from security_reminder_hook import cleanup_old_state_files

@pytest.fixture
def temp_home():
    with tempfile.TemporaryDirectory() as tmpdir:
        # Patch os.path.expanduser to return a directory within our temp dir
        mock_expand = lambda p: p.replace('~', tmpdir)
        with patch('os.path.expanduser', side_effect=mock_expand):
            yield tmpdir

def test_cleanup_old_state_files(temp_home):
    claude_dir = os.path.join(temp_home, ".claude")
    os.makedirs(claude_dir)

    current_time = datetime.now().timestamp()
    old_time = current_time - (31 * 24 * 60 * 60)
    recent_time = current_time - (1 * 24 * 60 * 60)

    # Create an old file
    old_file = os.path.join(claude_dir, "security_warnings_state_old.json")
    with open(old_file, 'w') as f:
        f.write('[]')
    os.utime(old_file, (old_time, old_time))

    # Create a recent file
    recent_file = os.path.join(claude_dir, "security_warnings_state_recent.json")
    with open(recent_file, 'w') as f:
        f.write('[]')
    os.utime(recent_file, (recent_time, recent_time))

    # Create a file with different name pattern
    other_file = os.path.join(claude_dir, "other_file.json")
    with open(other_file, 'w') as f:
        f.write('[]')
    os.utime(other_file, (old_time, old_time))

    cleanup_old_state_files()

    assert not os.path.exists(old_file), "Old state file should have been deleted"
    assert os.path.exists(recent_file), "Recent state file should not have been deleted"
    assert os.path.exists(other_file), "File with different pattern should not have been deleted"
