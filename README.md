# slideguard

A lightweight, open-source Python rate limiter.

- PyPI package name: `slideguard`
- Import path: `ratelimiter`

## Features

- Timestamp-window based rate limiting
- Simple `@rate_limit(calls=N, per=seconds)` decorator
- Custom `RateLimitExceeded` exception
- Thread-safe decorator implementation

## Installation

From PyPI (after publishing):

```bash
pip install slideguard
```

From source:

```bash
pip install -e .
```

## Usage

### 1) Use `is_allowed` directly

```python
import time
from ratelimiter import is_allowed

calls = []

allowed, calls = is_allowed(calls, max_calls=5, window=60)
if allowed:
    calls.append(time.time())
    print("Call accepted")
else:
    print("Call blocked")
```

### 2) Use the `@rate_limit` decorator

```python
from ratelimiter import RateLimitExceeded, rate_limit


@rate_limit(calls=5, per=60)
def send_event(payload: dict) -> str:
    return f"sent: {payload['id']}"


try:
    result = send_event({"id": "evt-1"})
    print(result)
except RateLimitExceeded as exc:
    print(f"Blocked by rate limiter: {exc}")
```

## Running tests

```bash
python -m pytest -q
```

## Open source

This project is open source and contributions are welcome.

Suggested contribution flow:

1. Fork the repository
2. Create a feature branch
3. Add or update tests
4. Open a pull request
