from __future__ import annotations

import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))

import validate_agent_map as vam  # noqa: E402

MAP = SCRIPTS.parent / "agent-map.yaml"


def test_real_map_passes() -> None:
    text = MAP.read_text(encoding="utf-8")
    assert vam.validate_agent_map(vam.parse_map(text)) == []
    assert vam.scan_vendor_ids(text) == []


def test_real_map_every_role_is_tiered() -> None:
    agents = vam.parse_map(MAP.read_text(encoding="utf-8"))["agents"]
    assert all(a.get("model_tier") in vam.MODEL_TIERS for a in agents.values())


def test_missing_and_invalid_tier_rejected() -> None:
    assert any("missing model_tier" in e for e in vam.validate_agent_map({"agents": {"x": {}}}))
    bad = vam.validate_agent_map({"agents": {"x": {"model_tier": "gpt-4o"}}})
    assert any("model_tier" in e for e in bad)


def test_unknown_execution_values_rejected() -> None:
    data = {"actions": {"a": {"min_orchestration": ["sequential"],
            "steps": [{"agent": "x", "execution": {"isolation": "bogus", "returns": "weird",
                                                    "parallel_group": 5}}]}}}
    errs = vam.validate_agent_map(data)
    assert any("isolation" in e for e in errs)
    assert any("returns" in e for e in errs)
    assert any("parallel_group" in e for e in errs)


def test_parallel_without_sequential_fallback_rejected() -> None:
    data = {"actions": {"a": {"steps": [{"parallel": ["x", "y"]}]}}}
    assert any("sequential" in e for e in vam.validate_agent_map(data))
    # declaring the fallback clears it
    data["actions"]["a"]["min_orchestration"] = ["sequential"]
    assert vam.validate_agent_map(data) == []


def test_unknown_orchestration_value_rejected() -> None:
    data = {"actions": {"a": {"min_orchestration": ["telepathy"], "steps": []}}}
    assert any("min_orchestration" in e for e in vam.validate_agent_map(data))


def test_vendor_id_scan() -> None:
    assert vam.scan_vendor_ids("    model_tier: claude-opus-4   # leaked\n")
    assert vam.scan_vendor_ids("    model_tier: balanced\n") == []
