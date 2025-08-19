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
    session_id: str = "default"
    tenant_id: str = "default"
    
    def __init__(self, session_id: str = "default", tenant_id: str = "default", user_id: str = None):
        # Создаем копию user_context и обновляем user_id если передан
        user_data = user_context.copy()
        if user_id:
            user_data["user_id"] = user_id
            
        self.user_context = UserContext(**user_data)
        self.available_dates_for_vacation = AvailableDatesForVacation(dates=available_dates_for_vacation)
        self.available_salary_increase_percentages = AvailableSalaryIncreasePercentages(percentages=available_salary_increase_percentages)
        self.session_id = session_id
        self.tenant_id = tenant_id
        
        
        