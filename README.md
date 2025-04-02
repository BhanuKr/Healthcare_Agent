# 🩺 Healthcare Agent System - Triage Assistant (LangChain + FastAPI)

This project implements a minimal **AI-powered healthcare triage backend system** using **FastAPI** and **LangChain**. The system receives a user’s symptom description, reasons with an LLM to determine the most appropriate specialist from a predefined list, and returns a structured response.


---

## ✨ Features

- **Symptom Validation** using LLM-based prompt checking.
- **LangChain Agent** (ReAct-based) powered by OpenAI GPT.
- **Custom Tool**: `SpecialistInfoTool` that provides information on medical specialists.
- **Multi-step Reasoning**: ReAct-style prompting to think before acting.
- **Error Handling** for malformed inputs and agent failures.
- **Unit Testing** with Pytest and mock support.
- RESTful API exposed using **FastAPI**.
- Robust input validation using **Pydantic** models for clean and safe API requests.

---

## ⚙️ Setup Instructions

1. **Clone the Repository**:

```bash
git clone <repository_url>
cd Healthcare_Agent
```

2. **Install Dependencies**: Use the requirements.txt file to install all the necessary dependencies:
```bash
pip install -r requirements.txt
```

3. Configure Environment Variables:
Update the .env file in the root directory:
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

4. Run the FastAPI Server:
```bash
uvicorn main:app --reload
```
- **Interaction Instructions** :<br>
Swagger UI: http://127.0.0.1:8000/docs <br>
This URL can be used to test the API endpoints interactively(On the initial load, it may take a few minutes to load the UI). <br>
To give input, hit Try it out, enter the symptom description, and click Execute. <br>
All the logs from Agent steps and other API logs can be seen on console .<br>
Alternative - Postman or Curl: You can also use Postman or curl to test the API endpoints.


## API Usage
🔻 Endpoint: POST /triage
Request Body:


```json
{
  "symptom_description": "give description"
}
```


Success Response:
```json
{
  "specialist": "specialist",
  "explanation": "One Statement Reasoning Behind the Choice"
}
```
**Error Responses** :

400 Bad Request: For invalid symptom descriptions or malformed agent outputs.<br>
500 Internal Server Error: For agent or tool execution failures. <br>
Effort to keep the error handling robust.

## Agent & Prompt Design

**LLM Service Used**
LLM: gpt-3.5-turbo (OpenAI API)

Built using create_react_agent from LangChain.

```python
triage_template = '''You are a healthcare triage assistant. Your job is to analyze the user's symptoms and determine the most appropriate medical specialist they should consult.
You have access to the following tool which can be checked for the names of specialist to know more about what they do:
{tools}
You MUST choose only ONE of the following specialists:
- Cardiologist
- Neurologist
- Gastroenterologist
- Dermatologist
- Pulmonologist
- Orthopedist
- General Practitioner
Take note that If you are confused between more than one specialist , fallback to General Practitioner. 
Use the following format to think and act:
Question: the symptom description from the user
Thought: your reasoning about the symptoms and to which specialists it concerns .
Action: the action to take, You can check in the [{tool_names}] for specialists concerned that you have in mind .
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat at max 20 times) 
Thought: I now know the final answer
Final Answer: <Specialist>: <one-sentence explanation>
In one sentence explanation tell to what organs or aspects the symptoms are directing and connect it to why the specialist was chosen .
Simple Example : 
Question: I feel stiffness and pain in my knees after walking.
Thought: This may relate to bones or joints. Let me check what an Orthopedist does.
Action: SpecialistInfoTool
Action Input: Orthopedist
Observation: Orthopedist: Focuses on bones, joints, and muscles.
Thought: I now know the final answer
Final Answer: Orthopedist: The symptoms involve joint pain which is best addressed by an Orthopedist.

Begin!

Question: {input}
Thought: {agent_scratchpad}
Output: <Specialist>: <one-sentence explanation>'''
```


Agent is prompted with the structured ReAct template- triage_template to:

1. Think about the symptom.
2. Use SpecialistInfoTool when needed.
3. Pick a single best-fit specialist.
4. To give more professional responses.

The Thought Action and Observation loop is logged in console for debugging.

- **SpecialistInfoTool**
This tool accepts a string (specialist_name) and returns hardcoded descriptions from the list:
Used by the agent as a reference during reasoning.

## Testing
Run all unit tests along with code coverage by executing:
```bash
./test_run.ps1 
```
in PowerShell (Windows) . <br>
Mac/Linux users can run pytest directly with coverage options from the terminal.

## Project Structure

```bash
Healthcare_Agent/
├── agent.py            # LangChain agent logic + tools
├── main.py             # FastAPI app & endpoint
├── validation.py       # LLM-based symptom_description validation
├── models.py           # Pydantic models
├── requirements.txt    # Python dependencies
├── test_main.py        # API tests
├── test_agent.py       # Agent logic tests
├── .env                # (not committed) for API keys
└── README.md
```

## Bonus Tasks Implemented
- Symptom Validation using LLM instead of regex or heuristics.

- Comprehensive Error Handling with status-specific messages.

- Logging of Agent Steps via console (AgentExecutor chain).

- Unit Tests with full mocking and coverage tracking.




