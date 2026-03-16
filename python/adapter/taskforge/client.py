import json
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import redis


@dataclass(frozen=True)
class TaskHandle:
    id: str


class TaskforgeClient:
    def __init__(self, broker_url: str, stream: str = "taskforge.tasks") -> None:
        self._redis = redis.Redis.from_url(broker_url, decode_responses=True)
        self._stream = stream

    def send_task(
        self,
        name: str,
        args: Optional[List[Any]] = None,
        kwargs: Optional[Dict[str, Any]] = None,
        queue: str = "default",
        retry_policy: Optional[Dict[str, Any]] = None,
        eta: Optional[datetime] = None,
        timeout_seconds: Optional[int] = None,
        idempotency_key: Optional[str] = None,
    ) -> TaskHandle:
        args = args or []
        kwargs = kwargs or {}
        retry_policy = retry_policy or {
            "max_attempts": 3,
            "attempt": 0,
            "backoff_seconds": 5,
        }

        if not isinstance(args, list):
            raise TypeError("args must be a list")
        if not isinstance(kwargs, dict):
            raise TypeError("kwargs must be a dict")

        payload = {
            "id": str(uuid.uuid4()),
            "name": name,
            "args": args,
            "kwargs": kwargs,
            "queue": queue,
            "retry": retry_policy,
            "eta": eta.astimezone(timezone.utc).isoformat() if eta else None,
            "timeout_seconds": timeout_seconds,
            "idempotency_key": idempotency_key,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }

        self._redis.xadd(self._stream, {"payload": json.dumps(payload)})
        return TaskHandle(id=payload["id"])
