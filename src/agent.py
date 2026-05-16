# task-manager-api/src/agent.py

import os
from anthropic import Anthropic
from dotenv import load_dotenv
import httpx

load_dotenv()

API_URL = "http://localhost:8000"


def execute_tool(tool_name: str, tool_input: dict) -> str:
    if tool_name == "create_task":
        tool_input["owner_id"] = 1
        response = httpx.post(f"{API_URL}/tasks/", json=tool_input)
        if response.status_code == 200:
            task = response.json()
            return f"Задача создана. ID: {task['id']}, Тема: {task['subject']}"
        return f"Ошибка: {response.text}"

    if tool_name == "get_stats":
        quarter = tool_input.get("quarter", "")
        response = httpx.get(f"{API_URL}/stats/", params={"quarter": quarter})
        if response.status_code == 200:
            stats = response.json()
            return f"Квартал {stats['quarter']}: всего {stats['total']}, выполнено {stats['completed']}, процент выполнения {stats['completion_rate']}%"
        return f"Ошибка: {response.text}"

    if tool_name == "update_task":
        task_id = tool_input.pop("task_id")
        response = httpx.patch(f"{API_URL}/tasks/{task_id}", json=tool_input)
        if response.status_code == 200:
            task = response.json()
            return f"Задача #{task_id} обновлена. Статус: {task['status']}"
        return f"Ошибка: {response.text}"

    return "Unknown tool"


load_dotenv()

client = Anthropic()

tools = [
    {
        "name": "create_task",
        "description": "Create a new task in the task manager",
        "input_schema": {
            "type": "object",
            "properties": {
                "sender": {"type": "string", "description": "Who sent the request"},
                "subject": {"type": "string", "description": "Task subject"},
                "description": {"type": "string", "description": "Task description"},
                "priority": {
                    "type": "string",
                    "enum": ["Высокий", "Средний", "Низкий"],
                },
                "task_type": {"type": "string", "description": "Type of task"},
                "quarter_plan": {
                    "type": "string",
                    "description": "Planned quarter e.g. Q2 2026",
                },
            },
            "required": ["sender", "subject", "priority"],
        },
    },
    {
        "name": "get_stats",
        "description": "Get task statistics for a quarter",
        "input_schema": {
            "type": "object",
            "properties": {
                "quarter": {"type": "string", "description": "Quarter e.g. Q2 2026"}
            },
            "required": ["quarter"],
        },
    },
    {
        "name": "update_task",
        "description": "Update task status and add solution. Use when user wants to close, complete or update a task.",
        "input_schema": {
            "type": "object",
            "properties": {
                "task_id": {"type": "integer", "description": "Task ID to update"},
                "status": {
                    "type": "string",
                    "enum": ["Выполнена", "В работе", "В ожидании", "Отменена"],
                },
                "solution": {"type": "string", "description": "Solution or comment"},
                "quarter_fact": {
                    "type": "string",
                    "description": "Actual quarter e.g. Q2 2026",
                },
            },
            "required": ["task_id", "status"],
        },
    },
]

SYSTEM_PROMPT = """You are a task manager assistant for an IT support team at a bank.
You help create and track tasks based on user messages.
When a user describes a task or a request — use the create_task tool.
When a user asks for statistics — use the get_stats tool.
Always respond in Russian."""


def run_agent(user_message: str) -> str:
    messages = [{"role": "user", "content": user_message}]

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        tools=tools,
        messages=messages,
    )

    if response.stop_reason == "tool_use":
        tool_use = next(b for b in response.content if b.type == "tool_use")
        tool_name = tool_use.name
        tool_input = tool_use.input
        print(f"\n🔧 Agent uses tool: {tool_name}")
        print(f"📋 Parameters: {tool_input}")

        result = execute_tool(tool_name, tool_input)
        return f"✅ {result}"

    return response.content[0].text


if __name__ == "__main__":
    print("AI Task Agent started. Type 'exit' to quit.\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        response = run_agent(user_input)
        print(f"Agent: {response}\n")
