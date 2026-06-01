import pytest
from hookify.core.config_loader import extract_frontmatter

def test_extract_frontmatter_basic():
    content = """---
name: test-rule
enabled: true
event: bash
pattern: "rm -rf"
---
Message body here."""
    fm, msg = extract_frontmatter(content)
    assert fm == {
        "name": "test-rule",
        "enabled": True,
        "event": "bash",
        "pattern": "rm -rf"
    }
    assert msg == "Message body here."

def test_extract_frontmatter_no_frontmatter():
    content = "Just plain text."
    fm, msg = extract_frontmatter(content)
    assert fm == {}
    assert msg == "Just plain text."

def test_extract_frontmatter_malformed_delimiters():
    content = """---
name: test-rule
No closing delimiter"""
    fm, msg = extract_frontmatter(content)
    assert fm == {}
    assert msg == content

def test_extract_frontmatter_booleans():
    content = """---
active: true
inactive: false
---"""
    fm, _ = extract_frontmatter(content)
    assert fm["active"] is True
    assert fm["inactive"] is False

def test_extract_frontmatter_simple_list():
    content = """---
items:
  - item1
  - "item2"
  - 'item3'
---"""
    fm, _ = extract_frontmatter(content)
    assert fm["items"] == ["item1", "item2", "item3"]

def test_extract_frontmatter_complex_list():
    content = """---
conditions:
  - field: command
    operator: regex_match
    pattern: "rm -rf"
  - field: tool_name, operator: equals, pattern: Bash
---"""
    fm, _ = extract_frontmatter(content)
    assert fm["conditions"] == [
        {"field": "command", "operator": "regex_match", "pattern": "rm -rf"},
        {"field": "tool_name", "operator": "equals", "pattern": "Bash"}
    ]

def test_extract_frontmatter_comments_and_empty_lines():
    content = """---
# This is a comment
name: test-rule

  # Indented comment
enabled: true
---"""
    fm, _ = extract_frontmatter(content)
    assert fm == {"name": "test-rule", "enabled": True}

def test_extract_frontmatter_nested_dict_in_list_last():
    content = """---
conditions:
  - field: command
    operator: contains
---"""
    fm, _ = extract_frontmatter(content)
    assert fm["conditions"] == [{"field": "command", "operator": "contains"}]

def test_extract_frontmatter_mixed_types():
    content = """---
name: "Mixed Rule"
count: 123
tags:
  - security
  - critical
enabled: false
---"""
    fm, _ = extract_frontmatter(content)
    # Note: current implementation seems to keep everything as strings except top-level booleans
    # Let's check the code: value = value.strip('"').strip("'")
    assert fm["name"] == "Mixed Rule"
    assert fm["count"] == "123" # Current parser doesn't cast to int
    assert fm["tags"] == ["security", "critical"]
    assert fm["enabled"] is False
