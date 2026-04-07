from functools import wraps
from threading import Lock
from time import time
from typing import Callable, ParamSpec, TypeVar

from .core import is_allowed
from .exceptions import RateLimitExceeded

P = ParamSpec("P")
R = TypeVar("R")


def rate_limit(calls: int, per: float) -> Callable[[Callable[P, R]], Callable[P, R]]:
	"""Limit function execution to `calls` within `per` seconds."""

	def decorator(func: Callable[P, R]) -> Callable[P, R]:
		timestamps: list[float] = []
		lock = Lock()

		@wraps(func)
		def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
			with lock:
				allowed, _ = is_allowed(timestamps, calls, per)
				if not allowed:
					raise RateLimitExceeded(
						f"Rate limit exceeded: max {calls} calls per {per} seconds"
					)

				timestamps.append(time())
			return func(*args, **kwargs)

		return wrapper

	return decorator

