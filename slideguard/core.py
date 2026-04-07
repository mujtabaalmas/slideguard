from time import time


def is_allowed(calls: list[float], max_calls: int, window: float) -> tuple[bool, list[float]]:
	"""Return whether a new call is allowed and the cleaned list of calls.

	Expired timestamps are those older than `window` seconds from now.
	"""
	now = time()
	calls[:] = [timestamp for timestamp in calls if now - timestamp <= window]
	allowed = len(calls) < max_calls
	return allowed, calls
