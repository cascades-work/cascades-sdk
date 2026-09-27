"""
Practical code examples for common Cascades SDK use cases.

These examples are designed to be copy-pasted and adapted.
Each example includes the necessary imports, authentication setup,
and step-by-step comments.
"""

# ────────────────────────────────────────────────────────────
# Example 1: Submit and Run a Workflow
# ────────────────────────────────────────────────────────────
SUBMIT_WORKFLOW_EXAMPLE = """
from cascades_sdk import CascadesClient, SessionCookieAuth
from cascades_sdk.workflows import submit_and_wait

# Initialize the client
client = CascadesClient(
    "https://your-cascades-instance.example.com",
    SessionCookieAuth("your-session-cookie"),
)

# Submit a workflow and wait for it to reach a terminal state
result = submit_and_wait(client, "your-workflow-id", {
    "input": "value",
})

print(f"Run completed with status: {result.get('status', '?')}")
"""

# ────────────────────────────────────────────────────────────
# Example 2: DAG Compilation with @task and @flow
# ────────────────────────────────────────────────────────────
DAG_COMPILATION_EXAMPLE = """
from cascades_sdk import task, flow
from cascades_sdk.compiler import build_dag_from_flow, canonical_json

@task
def fetch(value: str) -> str:
    # In capture mode, this function is NOT executed.
    # Return type hints help document the data flow.
    return f"fetched {value}"

@task
def transform(value: str) -> str:
    return f"transformed {value}"

@task
def merge(value: str, a: str, b: str) -> dict:
    return {"input": value, "a": a, "b": b}

@flow
def pipeline(value: str) -> dict:
    a = fetch(value)
    b = transform(value)
    return merge(value, a, b)

# Compile the DAG — note: no real API calls are made
dag = build_dag_from_flow(pipeline, {"value": "example"})

# dag = {
#     "nodes": [
#         {"id": "node-0", "task_name": "fetch", "dependencies": []},
#         {"id": "node-1", "task_name": "transform", "dependencies": []},
#         {"id": "node-2", "task_name": "merge", "dependencies": ["node-0", "node-1"]},
#     ],
#     "edges": [
#         {"from": "node-0", "to": "node-2"},
#         {"from": "node-1", "to": "node-2"},
#     ],
#     "return_node": "node-2",
#     "entrypoints": {"default": {"node": "node-0"}},
# }

# fetch and transform run in parallel (no dependency)
# merge runs after both complete
# Canonical JSON for deterministic comparison
print(canonical_json(dag))
"""

# ────────────────────────────────────────────────────────────
# Example 3: Scheduled Cron Workflow
# ────────────────────────────────────────────────────────────
SCHEDULED_WORKFLOW_EXAMPLE = """
import requests

# Create a trigger for a recurring workflow
response = requests.post(
    "https://your-cascades-instance.example.com/api/v1/triggers",
    json={
        "workflowId": "your-workflow-id",
        "schedule": "0 * * * *",  # every hour
        "inputs": {
            "input": "value",
        },
    },
    cookies={"__session": "your-session-cookie"},
)
print(response.json())
"""

# ────────────────────────────────────────────────────────────
# Example 4: Error Handling
# ────────────────────────────────────────────────────────────
ERROR_HANDLING_EXAMPLE = """
from cascades_sdk import CascadesClient, SessionCookieAuth
from cascades_sdk.errors import (
    AuthenticationError,
    NotFoundError,
    RateLimitError,
    TimeoutError,
)
from cascades_sdk.workflows import submit_and_wait

client = CascadesClient(
    "https://your-cascades-instance.example.com",
    SessionCookieAuth("your-session-cookie"),
)

try:
    result = submit_and_wait(client, "your-workflow-id", {"input": "value"})
except AuthenticationError as e:
    print(f"Auth failed: {e}")
    print("→ Re-login and get a fresh session cookie")
except NotFoundError as e:
    print(f"Workflow not found: {e}")
except RateLimitError as e:
    print(f"Rate limited, waiting...")
except TimeoutError as e:
    print(f"Workflow timed out: {e}")
"""
