from fastapi import FastAPI, HTTPException
from models import SymptomRequest, TriageResponse
from agent import run_triage
from validation import validate_symptom_description

app = FastAPI()

@app.post("/triage", response_model=TriageResponse)
def triage(symptom: SymptomRequest):
    try:
        symptom_text = symptom.symptom_description.strip()
        print("[INFO] Received symptom:", symptom_text)

        # Validation from an healthcare assistant if the input is a valid symptom description.
        validate_symptom_description(symptom_text)

        result = run_triage(symptom_text)

        # If result is a dict (ReAct output), access "output"
        if isinstance(result, dict) and "output" in result:
            result = result["output"]

        print("[INFO] Model output:", result)

        if ":" not in result:
            raise ValueError("Unexpected response format. Colon ':' not found.")

        specialist, explanation = result.split(":", 1)
        return TriageResponse(
            specialist=specialist.strip(),
            explanation=explanation.strip()
        )


    except ValueError as ve:
        message = str(ve)
        if "not a valid symptom" in message:
            print("[ERROR] Unexpected input:", message)
            raise HTTPException(status_code=400, detail=message) from ve
        if "Colon ':' not found" in message:
            print("[ERROR] Malformed agent output:", message)
            raise HTTPException(status_code=400, detail=message) from ve
        raise HTTPException(
            status_code=500, detail="Unhandled validation error."
        ) from ve

    except RuntimeError as re:
        print("[ERROR] Agent failed:", re)
        raise HTTPException(status_code=500, detail=str(re)) from re

    except Exception as e:
        print("[ERROR]", e)
        raise HTTPException(
            status_code=500,
            detail=f"Agent processing error: {str(e)}"
        ) from e

