import os
import json
import sys

# Add plugin root to Python path
PLUGIN_ROOT = os.getcwd() + "/plugins/hookify"
sys.path.insert(0, PLUGIN_ROOT)
sys.path.insert(0, os.path.dirname(PLUGIN_ROOT))

from hookify.core.config_loader import Rule, Condition
from hookify.core.rule_engine import RuleEngine

def test_transcript_matching():
    transcript_path = "test_transcript.txt"
    content = "Hello world!\nThis is a test transcript with a SECRET_KEY inside.\nGoodbye!"
    with open(transcript_path, "w") as f:
        f.write(content)

    rule = Rule(
        name="test-secret",
        enabled=True,
        event="stop",
        conditions=[
            Condition(field="transcript", operator="contains", pattern="SECRET_KEY")
        ],
        message="Found a secret!"
    )

    input_data = {
        "hook_event_name": "Stop",
        "transcript_path": transcript_path
    }

    engine = RuleEngine()
    result = engine.evaluate_rules([rule], input_data)

    assert "Found a secret!" in result.get("systemMessage", ""), f"Expected match not found. Result: {result}"
    print("Match test passed!")

    # Test non-match
    rule2 = Rule(
        name="test-missing",
        enabled=True,
        event="stop",
        conditions=[
            Condition(field="transcript", operator="contains", pattern="MISSING_KEY")
        ],
        message="Found missing!"
    )

    result2 = engine.evaluate_rules([rule2], input_data)
    assert result2 == {}, f"Expected no match, but got: {result2}"
    print("Non-match test passed!")

    os.remove(transcript_path)

if __name__ == "__main__":
    try:
        test_transcript_matching()
        print("All tests passed!")
    except Exception as e:
        print(f"Test failed: {e}")
        sys.exit(1)
