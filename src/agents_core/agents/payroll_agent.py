from agents import Agent, InputGuardrail, GuardrailFunctionOutput, Runner, set_default_openai_key, function_tool, RunContextWrapper
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
    get_user_info,
    get_user_basic_info,
    get_user_rating,
    get_employee_salary_info,
    get_available_salary_increases,
    calculate_salary_increase,
    get_max_allowed_salary_increase,
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


payroll_agent = Agent[ContextManager](
    name="Payroll Agent",
    model=model,
    instructions="""
    Role: Payroll-manager.
    You are connected to evaluate employee salary increase requests and provide compensation analysis.
    
    Use your tools to:
    1. Get employee salary and rating information
    2. Check available salary increase percentages
    3. Calculate and analyze salary increase requests
    4. Determine maximum allowed salary increases based on rating
    5. Provide employee profile information when needed
    6. Analyze employee eligibility for various benefits
    
    Always check employee info first, then available percentages, then provide detailed analysis.
    Consider employee rating when making recommendations.
    Use get_max_allowed_salary_increase to understand rating-based limits.
    Use get_employee_profile for comprehensive employee information.
    Use analyze_employee_eligibility to assess benefit eligibility.
    """,
    tools=[
        get_user_info,
        get_user_basic_info,
        get_user_rating,
        get_employee_salary_info,
        get_available_salary_increases,
        calculate_salary_increase,
        get_max_allowed_salary_increase,
        get_employee_profile,
        analyze_employee_eligibility
    ],
    hooks=agent_hooks
)

async def main():
    context_manager = ContextManager()
    result = await Runner.run(payroll_agent, "I want to increase my salary by 10%.", context=context_manager)
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())