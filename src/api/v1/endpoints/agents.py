"""
Эндпоинты для работы с агентами
"""
from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()


class AgentInfo(BaseModel):
    name: str
    description: str
    capabilities: List[str]
    status: str


class AgentListResponse(BaseModel):
    agents: List[AgentInfo]


class AgentDetailResponse(BaseModel):
    agent: AgentInfo


@router.get("/", response_model=AgentListResponse)
async def get_agents():
    """Получить список доступных агентов"""
    agents_info = [
        AgentInfo(
            name="Route Agent",
            description="Маршрутизатор запросов между агентами. Определяет тип запроса и направляет к соответствующему агенту.",
            capabilities=["request_routing", "agent_selection", "context_analysis"],
            status="active"
        ),
        AgentInfo(
            name="Office Culture Agent", 
            description="Агент для вопросов о корпоративной культуре, офисной жизни и общих вопросов о компании.",
            capabilities=["office_culture", "company_info", "general_questions"],
            status="active"
        ),
        AgentInfo(
            name="CEO Agent",
            description="Руководитель для одобрения запросов на отпуска, повышения, командировки и других решений.",
            capabilities=["approval_requests", "vacation_approval", "salary_decisions", "business_trips"],
            status="active"
        ),
        AgentInfo(
            name="HR Agent",
            description="HR-менеджер для работы с кадровыми вопросами и информацией о сотрудниках.",
            capabilities=["employee_info", "hr_policies", "recruitment"],
            status="active"
        ),
        AgentInfo(
            name="Payroll Agent",
            description="Агент для работы с зарплатой, финансовыми расчетами и отчетами.",
            capabilities=["salary_calculations", "financial_reports", "payroll_management"],
            status="active"
        )
    ]
    
    return AgentListResponse(agents=agents_info)


@router.get("/{agent_name}", response_model=AgentDetailResponse)
async def get_agent(agent_name: str):
    """Получить информацию о конкретном агенте"""
    agents_map = {
        "route": AgentInfo(
            name="Route Agent",
            description="Маршрутизатор запросов между агентами. Определяет тип запроса и направляет к соответствующему агенту.",
            capabilities=["request_routing", "agent_selection", "context_analysis"],
            status="active"
        ),
        "office_culture": AgentInfo(
            name="Office Culture Agent",
            description="Агент для вопросов о корпоративной культуре, офисной жизни и общих вопросов о компании.",
            capabilities=["office_culture", "company_info", "general_questions"],
            status="active"
        ),
        "ceo": AgentInfo(
            name="CEO Agent",
            description="Руководитель для одобрения запросов на отпуска, повышения, командировки и других решений.",
            capabilities=["approval_requests", "vacation_approval", "salary_decisions", "business_trips"],
            status="active"
        ),
        "hr": AgentInfo(
            name="HR Agent",
            description="HR-менеджер для работы с кадровыми вопросами и информацией о сотрудниках.",
            capabilities=["employee_info", "hr_policies", "recruitment"],
            status="active"
        ),
        "payroll": AgentInfo(
            name="Payroll Agent",
            description="Агент для работы с зарплатой, финансовыми расчетами и отчетами.",
            capabilities=["salary_calculations", "financial_reports", "payroll_management"],
            status="active"
        )
    }
    
    agent_info = agents_map.get(agent_name.lower())
    if not agent_info:
        raise HTTPException(status_code=404, detail=f"Agent '{agent_name}' not found")
    
    return AgentDetailResponse(agent=agent_info)
