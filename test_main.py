from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# === 1. Success test ===
def test_triage_endpoint_success(monkeypatch):
    def mock_run_triage(_):
        return {"output": "Dermatologist: Skin rash and itching are skin-related."}

    def mock_validate(_):
        pass  # assume valid input

    monkeypatch.setattr("main.run_triage", mock_run_triage)
    monkeypatch.setattr("validation.validate_symptom_description", mock_validate)

    response = client.post("/triage", json={"symptom_description": "Rash and itching for 2 days"})
    assert response.status_code == 200
    assert response.json()["specialist"] == "Dermatologist"

# === 2. Invalid input rejected ===
def test_validation_rejects_invalid_input(monkeypatch):
    def mock_validate(_):
        raise ValueError("Unexpected input: not a valid symptom description.")

    monkeypatch.setattr("validation.validate_symptom_description", mock_validate)

    response = client.post("/triage", json={"symptom_description": "asdasd asd banana"})
    assert response.status_code == 400
    assert "Unexpected input" in response.json()["detail"]

# === 3. Agent returns malformed output ===
def test_agent_returns_bad_output(monkeypatch):
    def mock_run_triage(_):
        return {"output": "Invalid format output"}

    monkeypatch.setattr("main.run_triage", mock_run_triage)
    monkeypatch.setattr("validation.validate_symptom_description", lambda _: None)

    response = client.post("/triage", json={"symptom_description": "Headache and nausea"})
    assert response.status_code in [400, 500]
    assert "Unexpected response format" in response.json()["detail"]

# === 4. Agent crashes ===
def test_agent_raises_exception(monkeypatch):
    def mock_run_triage(_):
        raise Exception("Agent failed internally")

    monkeypatch.setattr("main.run_triage", mock_run_triage)
    monkeypatch.setattr("validation.validate_symptom_description", lambda _: None)

    response = client.post("/triage", json={"symptom_description": "Chest pain and breathlessness"})
    assert response.status_code == 500
    assert "Agent processing error" in response.json()["detail"]
