import asyncio
from dataclasses import dataclass
from .context_config import user_context, available_dates_for_vacation, available_salary_increase_percentages

@dataclass
class UserContext:
    user_id: str
    first_name: str
    last_name: str
    position: str
    current_salary: float
    employee_rating: int
    
@dataclass
class AvailableDatesForVacation:
    dates: list[str]
    
@dataclass
class AvailableSalaryIncreasePercentages:
    percentages: list[int]

@dataclass
class ContextManager:
    user_context: UserContext
    available_dates_for_vacation: AvailableDatesForVacation
    available_salary_increase_percentages: AvailableSalaryIncreasePercentages
    
    def __init__(self):
        self.user_context = UserContext(**user_context)
        self.available_dates_for_vacation = AvailableDatesForVacation(dates=available_dates_for_vacation)
        self.available_salary_increase_percentages = AvailableSalaryIncreasePercentages(percentages=available_salary_increase_percentages)
        
        
        