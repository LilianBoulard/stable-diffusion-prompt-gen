from pathlib import Path

import jsonschema
import pytest
from prompt_forge import Generator, Candidate, Block


def test_config_parsing():
    # Test that provided example config is valid
    Generator.from_file(Path(__file__).parent.parent / "example-config.toml")

    with pytest.raises(jsonschema.exceptions.ValidationError, match="required property"):
        # Empty config
        Generator.from_string("")
        # Not a config
        Generator.from_string("Invalid configuration")
        Generator.from_string('{"props": [1, 2, 3]}')
        # Malformed config
        Generator.from_string('[bloks.invalid]\ncandidates=[]')  # No `blocks`, but something else
        Generator.from_string('[blocks.test]')  # No candidates in block


def test_parse_candidate():
    """
    Tests that parsing a candidate returns the expected keywords.
    """
    test_candidates: list[tuple[str, tuple]] = [
        ("[[large | small] | [beautiful | ugly]] car | van", ("large car", "small car", "beautiful car", "ugly car", "van")),
    ]
    for candidate, expected_keywords in test_candidates:
        # Dump the weights, we'll test that in another unit
        keywords, _ = zip(*Candidate.parse(candidate).expand(weighting="keyword"))
        assert keywords == expected_keywords
