"""
Context functions for agents.
Shared functions for accessing and manipulating context data across all agents.
"""

import sys
import os
from pathlib import Path
from agents import function_tool, RunContextWrapper

# Add src directory to Python path for correct imports
current_file = Path(__file__).resolve()
src_dir = current_file.parent.parent.parent.parent
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from agents_core.agents.context.context_manager import ContextManager


# ===============================
# USER INFORMATION FUNCTIONS
# ===============================

@function_tool
async def get_user_info(wrapper: RunContextWrapper[ContextManager]) -> str:
    """Get comprehensive user information (name, position, salary, rating)."""
    user = wrapper.context.user_context
    return f"User: {user.first_name} {user.last_name}, Position: {user.position}, Current salary: ${user.current_salary:,}, Rating: {user.employee_rating}/100"

@function_tool
async def get_user_basic_info(wrapper: RunContextWrapper[ContextManager]) -> str:
    """Get basic user information (name and position only)."""
    user = wrapper.context.user_context
    return f"User: {user.first_name} {user.last_name}, Position: {user.position}"

@function_tool
async def get_user_rating(wrapper: RunContextWrapper[ContextManager]) -> str:
    """Get user employee rating."""
    user = wrapper.context.user_context
    return f"Employee rating: {user.employee_rating}/100"


# ===============================
# VACATION FUNCTIONS
# ===============================

@function_tool  
async def get_available_vacation_dates(wrapper: RunContextWrapper[ContextManager]) -> str:
    """Get all available vacation dates."""
    dates = wrapper.context.available_dates_for_vacation.dates
    return f"Available vacation dates: {', '.join(dates)}"

@function_tool
async def check_vacation_request(wrapper: RunContextWrapper[ContextManager], requested_dates: list[str]) -> str:
    """
    Check vacation request for specified dates. 
    Accepts a list of dates in YYYY-MM-DD format.
    Returns detailed analysis with approved/unavailable dates and alternatives.
    """
    available_dates = wrapper.context.available_dates_for_vacation.dates
    user = wrapper.context.user_context
    
    conflicts = []
    approved = []
    
    for date in requested_dates:
        if date in available_dates:
            approved.append(date)
        else:
            conflicts.append(date)
    
    result = f"🔍 Vacation request analysis for {user.first_name} {user.last_name}:\n"
    result += f"📅 Requested dates: {', '.join(requested_dates)}\n"
    
    if approved:
        result += f"✅ Approved dates: {', '.join(approved)}\n"
    if conflicts:
        result += f"❌ Unavailable dates: {', '.join(conflicts)}\n"
        # Suggest alternatives from available dates
        available_alternatives = [d for d in available_dates if d not in requested_dates][:3]
        if available_alternatives:
            result += f"💡 Alternative available dates: {', '.join(available_alternatives)}"
        else:
            result += f"💡 All available dates: {', '.join(available_dates)}"
    
    return result

@function_tool
async def check_single_vacation_date(wrapper: RunContextWrapper[ContextManager], date: str) -> str:
    """Check if a single vacation date is available. Accepts date in YYYY-MM-DD format."""
    available_dates = wrapper.context.available_dates_for_vacation.dates
    user = wrapper.context.user_context
    
    if date in available_dates:
        return f"✅ Date {date} is available for {user.first_name} {user.last_name}"
    else:
        return f"❌ Date {date} is not available for {user.first_name} {user.last_name}"


# ===============================
# SALARY FUNCTIONS
# ===============================

@function_tool
async def get_employee_salary_info(wrapper: RunContextWrapper[ContextManager]) -> str:
    """Get employee salary and rating information."""
    user = wrapper.context.user_context
    return f"Employee: {user.first_name} {user.last_name}, Current salary: ${user.current_salary:,}, Rating: {user.employee_rating}/100"

@function_tool
async def get_available_salary_increases(wrapper: RunContextWrapper[ContextManager]) -> str:
    """Get available salary increase percentages."""
    percentages = wrapper.context.available_salary_increase_percentages.percentages
    return f"Available salary increase percentages: {', '.join(map(str, percentages))}%"

@function_tool
async def calculate_salary_increase(wrapper: RunContextWrapper[ContextManager], percentage: int) -> str:
    """
    Calculate salary increase by specified percentage.
    Returns detailed analysis including eligibility based on employee rating.
    """
    user = wrapper.context.user_context
    available_percentages = wrapper.context.available_salary_increase_percentages.percentages
    
    current_salary = user.current_salary
    employee_rating = user.employee_rating
    
    # Check percentage availability
    if percentage not in available_percentages:
        return f"❌ Percentage {percentage}% is not available. Available percentages: {', '.join(map(str, available_percentages))}%"
    
    # Check employee rating
    min_rating_required = 70  # Minimum rating for salary increase
    if employee_rating < min_rating_required:
        return f"❌ Salary increase unavailable. Minimum rating required: {min_rating_required}, current rating: {employee_rating}"
    
    new_salary = current_salary * (1 + percentage / 100)
    increase_amount = new_salary - current_salary
    
    # Additional rating-based checks
    max_allowed_percentage = min(percentage, employee_rating // 10 * 5)  # Higher rating allows bigger increase
    if max_allowed_percentage < percentage:
        adjusted_salary = current_salary * (1 + max_allowed_percentage / 100)
        return f"⚠️ Requested increase {percentage}% exceeds allowed amount for your rating.\n" \
               f"Recommended increase: {max_allowed_percentage}%\n" \
               f"New salary: ${adjusted_salary:,.2f} (increase of ${adjusted_salary - current_salary:,.2f})"
    
    return f"✅ Salary increase analysis for {user.first_name} {user.last_name}:\n" \
           f"Current salary: ${current_salary:,}\n" \
           f"Increase: {percentage}%\n" \
           f"New salary: ${new_salary:,.2f}\n" \
           f"Increase amount: ${increase_amount:,.2f}\n" \
           f"Employee rating: {employee_rating}/100 ✅"

@function_tool
async def get_max_allowed_salary_increase(wrapper: RunContextWrapper[ContextManager]) -> str:
    """Get maximum allowed salary increase based on employee rating."""
    user = wrapper.context.user_context
    employee_rating = user.employee_rating
    
    if employee_rating < 70:
        return f"❌ No salary increase allowed. Minimum rating required: 70, current rating: {employee_rating}"
    
    max_percentage = employee_rating // 10 * 5  # Higher rating allows bigger increase
    available_percentages = wrapper.context.available_salary_increase_percentages.percentages
    
    # Find the highest available percentage that doesn't exceed max_percentage
    allowed_percentages = [p for p in available_percentages if p <= max_percentage]
    
    if allowed_percentages:
        max_allowed = max(allowed_percentages)
        return f"Maximum allowed salary increase for rating {employee_rating}: {max_allowed}%"
    else:
        return f"No salary increase percentages available for rating {employee_rating}"


# ===============================
# COMPREHENSIVE ANALYSIS FUNCTIONS
# ===============================

@function_tool
async def get_employee_profile(wrapper: RunContextWrapper[ContextManager]) -> str:
    """Get complete employee profile including all context information."""
    user = wrapper.context.user_context
    available_dates = wrapper.context.available_dates_for_vacation.dates
    available_percentages = wrapper.context.available_salary_increase_percentages.percentages
    
    profile = f"👤 Employee Profile:\n"
    profile += f"Name: {user.first_name} {user.last_name}\n"
    profile += f"Position: {user.position}\n"
    profile += f"Current Salary: ${user.current_salary:,}\n"
    profile += f"Employee Rating: {user.employee_rating}/100\n\n"
    
    profile += f"📅 Available Vacation Dates: {', '.join(available_dates)}\n\n"
    profile += f"💰 Available Salary Increase Percentages: {', '.join(map(str, available_percentages))}%"
    
    return profile

@function_tool
async def analyze_employee_eligibility(wrapper: RunContextWrapper[ContextManager]) -> str:
    """Analyze employee eligibility for various benefits based on rating."""
    user = wrapper.context.user_context
    rating = user.employee_rating
    
    analysis = f"🔍 Eligibility Analysis for {user.first_name} {user.last_name} (Rating: {rating}/100):\n\n"
    
    # Salary increase eligibility
    if rating >= 70:
        max_percentage = rating // 10 * 5
        analysis += f"✅ Eligible for salary increases up to {max_percentage}%\n"
    else:
        analysis += f"❌ Not eligible for salary increases (minimum rating: 70)\n"
    
    # Vacation eligibility (assuming all employees can take vacation)
    analysis += f"✅ Eligible for vacation requests\n"
    
    # Additional benefits based on rating
    if rating >= 90:
        analysis += f"⭐ Excellent performance - eligible for all benefits\n"
    elif rating >= 80:
        analysis += f"👍 Good performance - eligible for most benefits\n"
    elif rating >= 70:
        analysis += f"📈 Satisfactory performance - eligible for basic benefits\n"
    else:
        analysis += f"📉 Below expectations - limited benefits available\n"
    
    return analysis
