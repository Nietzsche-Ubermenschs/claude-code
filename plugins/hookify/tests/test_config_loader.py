import pytest
from hookify.core.config_loader import extract_frontmatter

def test_extract_frontmatter_basic():
    content = """---
name: test-rule
enabled: true
event: bash
---
Message body here."""
    fm, msg = extract_frontmatter(content)
    assert fm == {
        "name": "test-rule",
        "enabled": True,
        "event": "bash"
    }
    assert msg == "Message body here."

def test_extract_frontmatter_no_frontmatter():
    content = "Just plain markdown content."
    fm, msg = extract_frontmatter(content)
    assert fm == {}
    assert msg == content

def test_extract_frontmatter_malformed():
    content = """---
name: test-rule
no closing marker
Message body here."""
    fm, msg = extract_frontmatter(content)
    assert fm == {}
    assert msg == content

def test_extract_frontmatter_simple_list():
    content = """---
tags:
  - one
  - two
  - three
---
Body"""
    fm, msg = extract_frontmatter(content)
    assert fm == {
        "tags": ["one", "two", "three"]
    }

def test_extract_frontmatter_multi_line_dict_list():
    content = """---
conditions:
  - field: command
    operator: regex_match
    pattern: rm -rf
  - field: file_path
    operator: contains
    pattern: secrets
---
Warning message"""
    fm, msg = extract_frontmatter(content)
    assert fm == {
        "conditions": [
            {"field": "command", "operator": "regex_match", "pattern": "rm -rf"},
            {"field": "file_path", "operator": "contains", "pattern": "secrets"}
        ]
    }

def test_extract_frontmatter_inline_dict_list():
    content = """---
conditions:
  - field: command, operator: regex_match, pattern: rm -rf
  - field: file_path, operator: contains, pattern: secrets
---
Warning message"""
    fm, msg = extract_frontmatter(content)
    assert fm == {
        "conditions": [
            {"field": "command", "operator": "regex_match", "pattern": "rm -rf"},
            {"field": "file_path", "operator": "contains", "pattern": "secrets"}
        ]
    }

def test_extract_frontmatter_comments_and_empty_lines():
    content = """---
# This is a comment
name: test-rule

enabled: false
---
Body"""
    fm, msg = extract_frontmatter(content)
    # The parser skips lines starting with # and empty lines
    assert fm == {
        "name": "test-rule",
        "enabled": False
    }

def test_extract_frontmatter_quoted_values():
    content = """---
name: "quoted name"
pattern: 'quoted pattern'
---
Body"""
    fm, msg = extract_frontmatter(content)
    assert fm == {
        "name": "quoted name",
        "pattern": "quoted pattern"
    }

def test_extract_frontmatter_mixed_types():
    content = """---
name: mixed
enabled: true
tags:
  - a
  - b
conditions:
  - field: f1
    val: v1
  - field: f2
    val: v2
---
Body"""
    fm, msg = extract_frontmatter(content)
    assert fm == {
        "name": "mixed",
        "enabled": True,
        "tags": ["a", "b"],
        "conditions": [
            {"field": "f1", "val": "v1"},
            {"field": "f2", "val": "v2"}
        ]
    }

def test_extract_frontmatter_boolean_in_list():
    content = """---
items:
  - name: one
    valid: true
  - name: two
    valid: false
---
Body"""
    fm, msg = extract_frontmatter(content)
    # The current parser does NOT convert booleans inside lists/dicts
    assert fm == {
        "items": [
            {"name": "one", "valid": "true"},
            {"name": "two", "valid": "false"}
        ]
    }
