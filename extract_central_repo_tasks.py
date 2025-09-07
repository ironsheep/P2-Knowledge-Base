#!/usr/bin/env python3
"""
Extract only central_repo_build tasks from project dump and create a new dump file.
"""

import json
import sys
from datetime import datetime

def extract_central_repo_tasks(input_file, output_file):
    """Extract central_repo_build tasks and create new dump file."""
    
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    # Extract only tasks with central_repo_build tag
    central_repo_tasks = []
    for task in data.get('tasks', []):
        tags_str = task.get('tags', '[]')
        if 'central_repo_build' in tags_str:
            central_repo_tasks.append(task)
    
    print(f"Found {len(central_repo_tasks)} central_repo_build tasks")
    
    # Create new dump structure with only central_repo_build tasks (match original format)
    new_dump = {
        "schema_version": data.get("schema_version", "0.6.8"),
        "created_at": datetime.now().isoformat() + "-06:00",  # Match timezone format
        "tasks": central_repo_tasks,
        "context_storage": {},  # Empty context for clean start
        "metadata": data.get("metadata", {
            "compressed": False,
            "generator": "todo-mcp v0.6.8",
            "project_id": 4
        }),
        "checksum": "extracted_central_repo_build"
    }
    
    # Write new dump file
    with open(output_file, 'w') as f:
        json.dump(new_dump, f, indent=2)
    
    print(f"Created new dump file: {output_file}")
    print(f"Contains {len(central_repo_tasks)} central_repo_build tasks")
    
    # Show task summary
    completed = sum(1 for t in central_repo_tasks if t.get('status') == 'completed')
    in_progress = sum(1 for t in central_repo_tasks if t.get('status') == 'in_progress') 
    paused = sum(1 for t in central_repo_tasks if t.get('status') == 'paused')
    created = sum(1 for t in central_repo_tasks if t.get('status') == 'created')
    
    print(f"Task Status Summary:")
    print(f"  Completed: {completed}")
    print(f"  In Progress: {in_progress}")
    print(f"  Paused: {paused}")
    print(f"  Created: {created}")

if __name__ == "__main__":
    input_file = "tasks/backups/project_dump_20250906_150402.json"
    output_file = "tasks/backups/central_repo_build_only.json"
    
    extract_central_repo_tasks(input_file, output_file)