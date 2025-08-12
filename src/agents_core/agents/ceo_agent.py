from agents import Agent, InputGuardrail, GuardrailFunctionOutput, Runner, set_default_openai_key, ModelSettings
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
    get_employee_profile,
    analyze_employee_eligibility
)
from agents_core.agents.payroll_agent import payroll_agent
from agents_core.agents.hr_agent import hr_agent
from agents_core.agents.hooks import agent_hooks




load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
model = os.getenv("MODEL_NAME")
if not api_key:
    raise EnvironmentError("OPENAI_API_KEY not found in environment variables. Check the .env file")
set_default_openai_key(api_key)

ceo_agent = Agent(
    name="CEO Agent",
    model=model,
    handoff_description="Specialist agent for CEO questions",
    instructions=f"""
    You are the CEO of the company, coordinating between different departments.
    
    When handling employee requests:
    - For salary/compensation matters: Use payroll consultation
    - For vacation/HR matters: Use HR consultation
    - You can consult both departments simultaneously when the request involves multiple areas
    - Use context functions to get employee information and assess eligibility before consultations
    
    Available context tools:
    - get_user_info: Get basic user information
    - get_employee_profile: Get comprehensive employee profile
    - analyze_employee_eligibility: Analyze employee eligibility for benefits
    
    Be natural, friendly, and speak on behalf of the company.
    Coordinate efficiently between departments to provide comprehensive responses.
    Start by understanding the employee's profile before making departmental consultations.
    """,
    tools=[
        get_user_info,
        get_user_basic_info,
        get_employee_profile,
        analyze_employee_eligibility,
        payroll_agent.as_tool(
            tool_name="payroll_consultation",
            tool_description="Consult with Payroll department about salary increases, bonuses, and compensation matters"
        ),
        hr_agent.as_tool(
            tool_name="hr_consultation",
            tool_description="Consult with HR department about vacation requests, leave policies, and HR-related matters"
        )
    ],
    # Enable parallel tool calls
    model_settings=ModelSettings(
        parallel_tool_calls=True
    ),
    hooks=agent_hooks
)

async def main():
    print("=== CEO Agent with parallel tool calls ===\n")
    
    context_manager = ContextManager()
    result = await Runner.run(ceo_agent, 
        "I need a salary increase by 10% and also want to schedule a vacation from 15 to 17 of August. "
        "Can you help me with both the compensation review and vacation planning?"
    ,context=context_manager)
    print(f"Result: {result.final_output}\n")   
  

if __name__ == "__main__":
    # Run main tests
    asyncio.run(main())
    
 