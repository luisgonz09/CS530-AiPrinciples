import json
from typing import Any


def load_completed_tasks(file_path: str):
    """
    Load a task list from a JSON file and return only completed tasks.

    Each task record must include:
      - id: int
      - title: str
      - completed: bool

    Invalid files and malformed records are handled safely by returning an empty
    list. Invalid tasks are skipped without exposing any sensitive detail.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (FileNotFoundError, OSError, json.JSONDecodeError):
        return []

    if not isinstance(data, list):
        return []

    completed_tasks = []

    for item in data:
        if not isinstance(item, dict):
            continue

        task_id = item.get("id")
        title = item.get("title")
        completed = item.get("completed")

        if (
            isinstance(task_id, int)
            and not isinstance(task_id, bool)
            and isinstance(title, str)
            and isinstance(completed, bool)
            and completed is True
        ):
            completed_tasks.append({
                "id": task_id,
                "title": title,
                "completed": True,
            })

    return completed_tasks
