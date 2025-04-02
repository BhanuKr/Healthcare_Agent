import os
from dotenv import load_dotenv
from langchain_openai import OpenAI
from langchain.agents import AgentExecutor, create_react_agent
from tools import SpecialistInfoTool
from langchain_core.exceptions import OutputParserException
from langchain.schema.output_parser import OutputParserException as SchemaOutputParserException
from langchain.agents import AgentExecutor
from langchain_core.prompts import PromptTemplate

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

tools = [SpecialistInfoTool()]
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

prompt = PromptTemplate.from_template(triage_template)
llm = OpenAI(temperature=0)
tools = [SpecialistInfoTool()]

# Create ReAct agent
agent = create_react_agent(llm, tools, prompt)

# Wrap in an executor
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

class AgentExecutionError(Exception):
    """Raised when the agent fails to produce a valid result."""
    pass

def run_triage(symptom_description: str) -> dict:
    try:
        return agent_executor.invoke({"input": symptom_description})
    except OutputParserException as pe:
        print("[AGENT ERROR] Output parsing error:", pe)
        raise RuntimeError("LLM returned an output the agent couldn't understand.") from pe
    except SchemaOutputParserException as se:
        print("[AGENT ERROR] Schema parsing error:", se)
        raise RuntimeError("Agent failed to parse the output format.") from se
    except ValueError as ve:
        print("[AGENT ERROR] ValueError during agent execution:", ve)
        raise RuntimeError("The agent encountered a value error. Possibly tool misuse.") from ve
    except Exception as e:
        print("[AGENT ERROR] Unexpected failure:", e)
        raise RuntimeError("Unexpected agent execution error.") from e
