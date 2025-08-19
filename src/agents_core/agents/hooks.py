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
import json
import os
from google.cloud import pubsub_v1

TContext = TypeVar('TContext')

class UnifiedAgentHooks(AgentHooksBase[TContext, Agent]):
    """
    Unified hooks for agent lifecycle events.
    
    Provides consistent logging for:
    - Agent start events
    - Agent completion events with final output
    """
    
    async def _send_pubsub_message(self, context, agent: Agent, message_type: str, message: str) -> None:
        """
        Sends message to PubSub topic.
        
        Args:
            context: Agent execution context
            agent: Agent
            message_type: Message type (e.g., 'think', 'chat')
            message: Message text
        """
        try:
            # Get configuration from environment variables
            project_id = os.getenv("PUBSUB_PROJECT_ID")
            topic_id = os.getenv("PUBSUB_TOPIC_ID")
            
            # Check if PubSub is disabled
            if project_id.lower() == "disabled":
                print(f"🔇 PubSub disabled for agent {agent.name}")
                return
            
            # Create PubSub client
            publisher = pubsub_v1.PublisherClient()
            topic_path = publisher.topic_path(project_id, topic_id)
            
            # Form message data
            data = {
                "agent_name": agent.name,
                "message_ts": datetime.datetime.now().isoformat() + "Z",
                "message_type": message_type,
                "message": message
            }
            
            # Get real IDs from context
            user_id = getattr(context, 'user_context', {})
            if hasattr(user_id, 'user_id'):
                user_id = user_id.user_id
            else:
                user_id = "system"  # fallback
            
            session_id = getattr(context, 'session_id', 'default')
            tenant_id = getattr(context, 'tenant_id', 'default')
            
            # Send message
            future = publisher.publish(
                topic_path,
                json.dumps(data).encode("utf-8"),
                user_id=user_id,
                session_id=session_id,
                tenant=tenant_id
            )
            
            # Wait for send result
            future.result()
            print(f"✓ Message sent to PubSub: {agent.name} - {message_type}")
            
        except Exception as e:
            print(f"⚠️ Error sending message to PubSub: {e}")
            print(f"   Using project: {project_id}, topic: {topic_id}")
            print(f"   To disable PubSub set PUBSUB_PROJECT_ID=disabled")
    
    async def on_start(self, context, agent: Agent) -> None:
        """
        Called when an agent starts execution.
        
        Args:
            context: The run context wrapper
            agent: The agent that is starting
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] 🚀 Agent '{agent.name}' started execution")
        
        # Send message to PubSub when agent starts
        await self._send_pubsub_message(context, agent, "think", f"Agent '{agent.name}' started execution")
    
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
        
        # Send message to PubSub when agent completes
        await self._send_pubsub_message(context, agent, "completion", f"Agent '{agent.name}' completed execution with output: {str(output)[:200]}...")

# Create a shared instance that can be used across all agents
agent_hooks = UnifiedAgentHooks()
