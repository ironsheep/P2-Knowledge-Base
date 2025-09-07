#!/usr/bin/env python3
"""
Create central_repo_build tasks directly using Todo MCP batch create.
"""

import json

def create_tasks_directly():
    """Extract task data and format for batch creation."""
    
    with open("tasks/backups/project_dump_20250906_150402.json", 'r') as f:
        data = json.load(f)
    
    # Extract central_repo_build tasks
    tasks_to_create = []
    
    for task in data.get('tasks', []):
        tags_str = task.get('tags', '[]')
        if 'central_repo_build' in tags_str:
            task_data = {
                "content": task["content"],
                "estimate_minutes": task["estimate_minutes"],
                "priority": "critical"  # All central_repo_build are critical priority
            }
            tasks_to_create.append(task_data)
    
    # Sort by sequence if available
    def get_sequence(task_dict):
        # Find original task in data to get sequence
        for orig_task in data.get('tasks', []):
            if orig_task["content"] == task_dict["content"]:
                return orig_task.get("sequence", 999)
        return 999
    
    tasks_to_create.sort(key=get_sequence)
    
    print(f"Found {len(tasks_to_create)} central_repo_build tasks")
    print("Tasks to create:")
    for i, task in enumerate(tasks_to_create[:5]):  # Show first 5
        print(f"{i+1}. {task['content'][:80]}... (est: {task['estimate_minutes']}m)")
    
    if len(tasks_to_create) > 5:
        print(f"... and {len(tasks_to_create) - 5} more")
    
    return tasks_to_create

if __name__ == "__main__":
    create_tasks_directly()