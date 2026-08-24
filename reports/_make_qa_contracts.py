import json
from pathlib import Path

base = Path("D:/CapoHornLab/contracts")
tasks = [
    (
        "chl-20260824-0015",
        "cratos",
        "Read-only structural QA: inspect canonical root pages, pages redirect stubs, local static links/assets and authenticated-client wiring. Return concise issue list with file+line/evidence. Do not edit or deploy.",
    ),
    (
        "chl-20260824-0016",
        "midas",
        "Read-only research QA: inspect research.html and research-detail.html data/rendering logic, all public research entries and local chart references. Confirm mandatory sections/metrics/charts; return concrete defects only. Do not edit or deploy.",
    ),
]
for task_id, recipient, objective in tasks:
    task_path = base / "tasks" / f"{task_id}_task.json"
    result_path = base / "envelopes" / f"{task_id}_result.json"
    if task_path.exists() or result_path.exists():
        raise RuntimeError(f"Duplicate task id: {task_id}")
    envelope = {
        "schema_version": "1.0",
        "task_id": task_id,
        "from": "camilla",
        "to": recipient,
        "objective": objective,
        "allowed_data": ["D:/CapoHornLab/projects/capohornlab-website"],
        "allowed_tools": ["read_file", "search_files", "terminal"],
        "forbidden_actions": ["edit", "deploy", "send", "delete", "order_live"],
        "risk": "read",
        "budget": {"minutes": 20, "tool_calls": 30, "delegation_depth": 0},
        "acceptance": [
            "Evidence contains exact paths/commands or reproducible observations",
            "No external or write actions",
            "Concise status completed|failed",
        ],
    }
    task_path.write_text(json.dumps(envelope, indent=2), encoding="utf-8")
    print(task_path)
