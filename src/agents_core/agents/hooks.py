"""
Agent lifecycle hooks for logging and monitoring agent execution.

This module provides unified hooks for all agents to track their lifecycle events:
- Agent start: When an agent begins execution
- Agent end: When an agent completes execution with final output

These hooks can be applied to any agent to provide consistent logging across the system.
"""

from agents.lifecycle import AgentHooksBase
from agents import Agent
from typing import Any, TypeVar
import datetime

TContext = TypeVar('TContext')

class UnifiedAgentHooks(AgentHooksBase[TContext, Agent]):
    """
    Unified hooks for agent lifecycle events.
    
    Provides consistent logging for:
    - Agent start events
    - Agent completion events with final output
    """
    
    async def on_start(self, context, agent: Agent) -> None:
        """
        Called when an agent starts execution.
        
        Args:
            context: The run context wrapper
            agent: The agent that is starting
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] 🚀 Agent '{agent.name}' started execution")
    
    async def on_end(self, context, agent: Agent, output: Any) -> None:
        """
        Called when an agent completes execution.
        
        Args:
            context: The run context wrapper  
            agent: The agent that completed
            output: The final output from the agent
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] ✅ Agent '{agent.name}' completed execution")
        print(f"[{timestamp}] 📋 Final result from '{agent.name}': {output}")
        print("-" * 80)

# Create a shared instance that can be used across all agents
agent_hooks = UnifiedAgentHooks()
