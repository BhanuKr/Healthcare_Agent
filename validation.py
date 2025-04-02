from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

def validate_symptom_description(symptom_description: str) -> None:
    prompt = f"""
You are a medical assistant. Determine whether the following input is a valid medical symptom description or just random/gibberish text.

Input: "{symptom_description}"

Respond ONLY with "Valid" or "Invalid".
"""
    response = llm.invoke(prompt).content.strip().lower()

    if response == "invalid":
        raise ValueError("Unexpected input: not a valid symptom description.")
