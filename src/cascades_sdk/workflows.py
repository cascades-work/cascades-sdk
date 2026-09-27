"""Workflow helper utilities for common operations.

Reduces boilerplate when submitting, tracking, and inspecting workflows.
"""


from typing import Any, Dict, Optional

from .client import CascadesClient
from .client.polling import wait_for_completion
from ._meta import SDK_WORKFLOWS_URL


def submit_and_wait(
    client: CascadesClient,
    workflow_id: str,
    context: Optional[Dict[str, Any]] = None,
    timeout: float = 3600.0,
    *,
    execution_mode: Optional[str] = None,
) -> Dict[str, Any]:
    """Submit a workflow and block until it reaches a terminal state.

    This is the most common workflow operation: submit, wait for completion,
    and return the terminal event. Combines ``submit_workflow_run()`` and
    ``wait_for_completion()`` into a single call.

    Args:
        client: An authenticated :class:`CascadesClient` instance.
        workflow_id: The ID of the workflow to execute (from the catalog
            or a previously saved workflow).
        context: Optional key-value pairs passed as workflow inputs.
        timeout: Maximum time in seconds to wait for completion
            (default 1 hour).
        execution_mode: Optional execution mode (``"inline"`` or
            ``"queued"``). When not set, the platform uses its default.

    Returns:
        The terminal SSE event dict with status and output data.

    Raises:
        AuthenticationError: If the session is invalid.
        NotFoundError: If the workflow_id doesn't exist.
        TimeoutError: If the run doesn't complete within ``timeout``.

    See Also:
        - :func:`submit_and_get_run` for just the submission step.
        - :func:`wait_for_completion` for the blocking step alone.
        - Workflow docs: {SDK_WORKFLOWS_URL}
    """
    body: Dict[str, Any] = {"workflowId": workflow_id}
    if context is not None:
        body["context"] = context
    if execution_mode is not None:
        body["executionMode"] = execution_mode

    accepted = client.submit_workflow_run(body)
    run_id = accepted["runId"]
    return wait_for_completion(client, run_id, timeout=timeout)


def submit_and_get_run(
    client: CascadesClient,
    workflow_id: str,
    context: Optional[Dict[str, Any]] = None,
    *,
    execution_mode: Optional[str] = None,
) -> Dict[str, Any]:
    """Submit a workflow and return the accepted response without waiting.

    Useful when you want to submit a workflow and check on it later,
    or when using webhook-based completion notifications.

    Args:
        client: An authenticated :class:`CascadesClient` instance.
        workflow_id: The ID of the workflow to execute.
        context: Optional key-value pairs passed as workflow inputs.
        execution_mode: Optional execution mode (``"inline"`` or
            ``"queued"``).

    Returns:
        The ``WorkflowRunAccepted`` dict with ``runId``, ``executionMode``,
        and status information.

    See Also:
        - :func:`submit_and_wait` for a blocking version.
        - :func:`iter_run_stream_events` for real-time event streaming.
    """
    body: Dict[str, Any] = {"workflowId": workflow_id}
    if context is not None:
        body["context"] = context
    if execution_mode is not None:
        body["executionMode"] = execution_mode
    return client.submit_workflow_run(body)


def list_workflows(client: CascadesClient) -> list[Dict[str, Any]]:
    """List all available workflow definitions from the catalog.

    Uses the Cascades API to fetch the workflow catalog. Returns both
    built-in workflows and any user-created workflows.

    Args:
        client: An authenticated :class:`CascadesClient` instance.

    Returns:
        A list of workflow definition dicts with ``id``, ``name``,
        ``version``, ``description``, ``collectors``, and ``schedule``.

    See Also:
        - :func:`submit_and_wait` to execute a workflow.
        - Workflow catalog docs: {SDK_WORKFLOWS_URL}/catalog
    """
    return client._http.request_json("GET", "/api/v1/workflows")
