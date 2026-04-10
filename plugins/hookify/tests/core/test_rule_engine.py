import re
import pytest
from hookify.core.rule_engine import compile_regex

def test_compile_regex_caching():
    """Test that compile_regex correctly caches compiled patterns."""
    pattern = r"test\d+"

    # First call compiles and caches
    regex1 = compile_regex(pattern)

    # Second call should return the exact same object from cache
    regex2 = compile_regex(pattern)

    assert regex1 is regex2
    assert regex1.pattern == pattern

def test_compile_regex_different_patterns():
    """Test that different patterns return different compiled objects."""
    pattern1 = r"test1"
    pattern2 = r"test2"

    regex1 = compile_regex(pattern1)
    regex2 = compile_regex(pattern2)

    assert regex1 is not regex2
    assert regex1.pattern == pattern1
    assert regex2.pattern == pattern2

def test_compile_regex_ignorecase():
    """Test that compile_regex uses re.IGNORECASE by default."""
    pattern = r"test"
    regex = compile_regex(pattern)

    assert regex.flags & re.IGNORECASE

    # Verify it actually matches case-insensitively
    assert regex.search("TEST")
    assert regex.search("test")
    assert regex.search("TeSt")

def test_compile_regex_valid_regex():
    """Test that it correctly compiles a valid regex."""
    pattern = r"^start.*end$"
    regex = compile_regex(pattern)

    assert regex.search("start middle end")
    assert not regex.search("middle end")
    assert not regex.search("start middle")

def test_compile_regex_invalid_regex():
    """Test behavior with invalid regex patterns.
    Note: compile_regex itself doesn't catch re.error,
    it's caught in RuleEngine._regex_match.
    Direct call to compile_regex with invalid pattern should raise re.error.
    """
    invalid_pattern = r"["
    with pytest.raises(re.error):
        compile_regex(invalid_pattern)
