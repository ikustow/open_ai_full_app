from agents import Agent, InputGuardrail, GuardrailFunctionOutput, Runner, SQLiteSession, set_default_openai_key
from agents.exceptions import InputGuardrailTripwireTriggered
from pydantic import BaseModel
import asyncio
from dotenv import load_dotenv
import os
import sys
from pathlib import Path

# Add src directory to Python path for correct imports
current_file = Path(__file__).resolve()
src_dir = current_file.parent.parent.parent
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from agents_core.agents.context.context_manager import ContextManager
from agents_core.agents.context.functions import get_user_basic_info
from agents_core.agents.office_culture import office_culture_agent
from agents_core.agents.ceo_agent import ceo_agent

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
model = os.getenv("MODEL_NAME")
if not api_key:
    raise EnvironmentError("OPENAI_API_KEY not found in environment variables. Check the .env file")
set_default_openai_key(api_key)


route_agent = Agent[ContextManager](
    name="Route Agent",
    model=model,
    instructions=f"""Your task is to determine what type of dialog is going on and route it to the appropriate agent.

   If this is a small talk about office life, questions about the company culture, or general office-related topics, then return path: 'office_culture'.
   If this is a request for vacation, salary increase, business trip, schedule change, or any approval request, then return path: 'approval_request'.
   
   You can optionally use get_user_basic_info to personalize the routing response.
   
   Route to office_culture_agent for office culture topics.
   Route to ceo_agent for approval requests.
   """,
    tools=[get_user_basic_info],
    handoffs=[office_culture_agent, ceo_agent]   
)

async def main():
    # same session for the entire dialog
    session = SQLiteSession("thread_1", "src/database/conversation_history.db")
    context_manager = ContextManager()

    result = await Runner.run(
        route_agent,
        "What is the office culture like?",
        session=session,
        context=context_manager
    )
    print(result.final_output)

    result = await Runner.run(
        route_agent,
         "I need a salary increase by 10% and also want to schedule a vacation from 15 to 17 of August. "
        "Can you help me with both the compensation review and vacation planning?",
        session=session,
        context=context_manager
    )
    print(result.final_output)
    

if __name__ == "__main__":
    asyncio.run(main())