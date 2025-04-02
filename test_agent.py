from unittest.mock import MagicMock
from agent import run_triage

# === 1. Agent returns expected format ===
def test_run_triage_returns_expected_format(monkeypatch):
    mock_response = {
        "output": "Pulmonologist: Shortness of breath suggests lung involvement."
    }

    mock_executor = MagicMock()
    mock_executor.invoke.return_value = mock_response
    monkeypatch.setattr("agent.agent_executor", mock_executor)

    result = run_triage("I have shortness of breath.")
    assert isinstance(result, dict)
    assert "output" in result
    assert "Pulmonologist" in result["output"]
