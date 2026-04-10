import unittest
import sys
import os

# Ensure we can import from the same directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from config_loader import extract_frontmatter

class TestConfigLoader(unittest.TestCase):
    def test_basic_frontmatter(self):
        content = """---
name: test
enabled: true
---
body"""
        fm, msg = extract_frontmatter(content)
        self.assertEqual(fm, {'name': 'test', 'enabled': True})
        self.assertEqual(msg, "body")

    def test_inline_dict(self):
        content = """---
conditions:
  - field: command, operator: regex_match, pattern: "rm -rf"
---"""
        fm, msg = extract_frontmatter(content)
        self.assertEqual(len(fm['conditions']), 1)
        self.assertEqual(fm['conditions'][0], {
            'field': 'command',
            'operator': 'regex_match',
            'pattern': 'rm -rf'
        })

    def test_multiline_dict(self):
        content = """---
conditions:
  - field: command
    operator: regex_match
    pattern: "rm -rf"
---"""
        fm, msg = extract_frontmatter(content)
        self.assertEqual(len(fm['conditions']), 1)
        self.assertEqual(fm['conditions'][0], {
            'field': 'command',
            'operator': 'regex_match',
            'pattern': 'rm -rf'
        })

    def test_mixed_list(self):
        content = """---
tags:
  - simple
  - key: value
  - k1: v1, k2: v2
---"""
        fm, msg = extract_frontmatter(content)
        self.assertEqual(fm['tags'], [
            'simple',
            {'key': 'value'},
            {'k1': 'v1', 'k2': 'v2'}
        ])

    def test_edge_cases(self):
        content = """---
key_with_colon: "value: with colon"
empty_val:
next_key: value
---"""
        fm, msg = extract_frontmatter(content)
        self.assertEqual(fm['key_with_colon'], "value: with colon")
        self.assertEqual(fm['next_key'], "value")
        # The parser's current behavior for empty_val followed by another top-level key:
        # It treats empty_val as the start of a list (in_list = True), but next_key is indent 0,
        # so it saves the previous (empty) list and starts next_key.
        self.assertEqual(fm.get('empty_val'), [])

    def test_nested_colons_in_inline(self):
        content = """---
conditions:
  - pattern: "regex: with: colons", field: command
---"""
        fm, msg = extract_frontmatter(content)
        self.assertEqual(fm['conditions'][0]['pattern'], "regex: with: colons")
        self.assertEqual(fm['conditions'][0]['field'], "command")

if __name__ == '__main__':
    unittest.main()
