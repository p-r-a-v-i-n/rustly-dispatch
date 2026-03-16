from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional

from .client import TaskforgeClient, TaskHandle


@dataclass
class TaskDefinition:
    name: str
    client: TaskforgeClient
    default_queue: str = "default"

    def delay(self, *args: Any, **kwargs: Any) -> TaskHandle:
        return self.client.send_task(self.name, list(args), kwargs, queue=self.default_queue)

    def apply_async(
        self,
        args: Optional[list] = None,
        kwargs: Optional[dict] = None,
        **options: Any,
    ) -> TaskHandle:
        return self.client.send_task(
            self.name,
            args=args or [],
            kwargs=kwargs or {},
            queue=options.get("queue", self.default_queue),
            retry_policy=options.get("retry_policy"),
            eta=options.get("eta"),
            timeout_seconds=options.get("timeout_seconds"),
            idempotency_key=options.get("idempotency_key"),
        )


class TaskforgeApp:
    def __init__(self, broker_url: str, stream: str = "taskforge.tasks") -> None:
        self.client = TaskforgeClient(broker_url, stream=stream)

    def task(self, name: Optional[str] = None) -> Callable[[Callable[..., Any]], TaskDefinition]:
        def decorator(func: Callable[..., Any]) -> TaskDefinition:
            task_name = name or func.__name__
            return TaskDefinition(name=task_name, client=self.client)

        return decorator
