from agents import Agent, InputGuardrail, GuardrailFunctionOutput, Runner, set_default_openai_key
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
from agents_core.agents.context.functions import (
    get_user_basic_info,
    get_user_info
)
from agents_core.agents.hooks import agent_hooks

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
model = os.getenv("MODEL_NAME")
if not api_key:
    raise EnvironmentError("OPENAI_API_KEY not found in environment variables. Check the .env file")
set_default_openai_key(api_key)

office_culture_agent = Agent[ContextManager](
    name="Office Culture Agent",
    model=model,
    handoff_description="Specialist agent for office culture questions",
    instructions=f"""
    Office-culture manager answers questions about office culture and atmosphere in the office.
    Your task is to answer questions about office culture and atmosphere in the office.
    You are a representative of the company, answering questions about office life, company culture, and working atmosphere.
    
    You can personalize responses by getting user information when appropriate.
    Use get_user_basic_info to address employees by name and position for a more personal touch.
    
    Be natural, friendly, and speak on behalf of the company.
    Talk about office life, company culture, and working atmosphere.
    """,
    tools=[
        get_user_basic_info,
        get_user_info
    ],
    hooks=agent_hooks
)

async def main():
    context_manager = ContextManager()
    result = await Runner.run(office_culture_agent, "What is the office culture like?", context=context_manager)
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())