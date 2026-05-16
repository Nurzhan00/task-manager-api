# import_tasks.py
import pandas as pd
import httpx

API_URL = "http://localhost:8000"

df = pd.read_excel("Task Tracker fixed.xlsx", sheet_name="📋 Задачи", skiprows=1)
df = df.dropna(subset=["ID"])

for _, row in df.iterrows():
    task = {
        "sender": str(row.get("Отправитель", "")) or "Неизвестен",
        "subject": str(row.get("Тема письма", "")) or "Без темы",
        "description": str(row.get("Описание задачи\n(своими словами)", ""))
        if pd.notna(row.get("Описание задачи\n(своими словами)"))
        else None,
        "priority": str(row.get("Приоритет", "Средний"))
        if pd.notna(row.get("Приоритет"))
        else "Средний",
        "assignee": str(row.get("Исполнитель", ""))
        if pd.notna(row.get("Исполнитель"))
        else None,
        "quarter_plan": str(row.get("Квартал\n(план)", ""))
        if pd.notna(row.get("Квартал\n(план)"))
        else None,
        "quarter_fact": str(row.get("Квартал\n(факт)", ""))
        if pd.notna(row.get("Квартал\n(факт)"))
        else None,
        "solution": str(row.get("Решение / ответ", ""))
        if pd.notna(row.get("Решение / ответ"))
        else None,
        "department": str(row.get("Управление /\nОтдел", ""))
        if pd.notna(row.get("Управление /\nОтдел"))
        else None,
        "task_type": str(row.get("Тип задачи", ""))
        if pd.notna(row.get("Тип задачи"))
        else None,
        "owner_id": 1,
    }

    response = httpx.post(f"{API_URL}/tasks/", json=task)
    if response.status_code == 200:
        print(f"✅ Imported: {task['subject']}")
    else:
        print(f"❌ Error: {response.text}")
