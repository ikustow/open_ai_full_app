import sys
import os
from pathlib import Path

# Add src directory to Python path for correct imports
current_file = Path(__file__).resolve()
src_dir = current_file.parent.parent.parent
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from agents import Agent, InputGuardrail, GuardrailFunctionOutput, Runner, set_default_openai_key, function_tool, RunContextWrapper
from agents.exceptions import InputGuardrailTripwireTriggered
from pydantic import BaseModel
import asyncio
from dotenv import load_dotenv
from agents_core.agents.context.context_manager import ContextManager
from agents_core.agents.context.functions import (
    get_user_info,
    get_user_basic_info,
    get_user_rating,
    get_available_vacation_dates,
    check_vacation_request,
    check_single_vacation_date,
    get_employee_profile,
    analyze_employee_eligibility
)
from agents_core.agents.hooks import agent_hooks


load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
model = os.getenv("MODEL_NAME")
if not api_key:
    raise EnvironmentError("OPENAI_API_KEY not found in environment variables. Check the .env file")
set_default_openai_key(api_key)

hr_agent = Agent[ContextManager](
    name="HR Agent",
    model=model,
    instructions="""
    Role: HR-manager.
    You are connected to evaluate employee vacation requests and provide HR support.
    
    Use your tools to:
    1. Get user information to personalize responses
    2. Check available vacation dates 
    3. Analyze vacation requests against available dates
    4. Provide employee profile information when needed
    5. Analyze employee eligibility for various benefits
    
    IMPORTANT: When calling check_vacation_request, pass dates as a list in YYYY-MM-DD format.    
    For example, if user asks for "vacation from 15 to 17 of September", pass ["2025-09-15", "2025-09-16", "2025-09-17"].
    
    Always check user info first, then available dates, then provide detailed analysis.
    Use get_employee_profile for comprehensive employee information.
    Use analyze_employee_eligibility to assess benefit eligibility.
    """,
    tools=[
        get_user_info,
        get_user_basic_info,
        get_user_rating,
        get_available_vacation_dates, 
        check_vacation_request,
        check_single_vacation_date,
        get_employee_profile,
        analyze_employee_eligibility
    ],
    hooks=agent_hooks
)

async def main():
    context_manager = ContextManager()
    result = await Runner.run(hr_agent, "I want to take a vacation from 15 to 30 of August. Can you check if I can take it?",context=context_manager)
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())