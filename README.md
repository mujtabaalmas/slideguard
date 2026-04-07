# SLIDEGUARD

A small, open-source Python rate limiter.

`slideguard` provides a thread-safe decorator for limiting function calls in a rolling time window, plus a low-level helper for custom workflows.

## Features

- Simple `@rate_limit(calls=N, per=seconds)` decorator
- Per-function in-memory timestamp tracking
- Thread-safe enforcement using `threading.Lock`
- Custom `RateLimitExceeded` exception
- Low-level `is_allowed(...)` helper

## Requirements

- Python 3.9+

## Installation

Install from PyPI:

```bash
pip install slideguard
```

Install locally from source:

```bash
git clone https://github.com/mujtabaalmas/slideguard.git
cd slideguard
pip install .
```

For development (editable install):

```bash
pip install -r requirements.txt
pip install -e .
```

## Quick Start

```python
from slideguard import RateLimitExceeded, rate_limit


@rate_limit(calls=5, per=60)
def send_event(payload: dict) -> str:
    return f"sent {payload['id']}"


for i in range(6):
    try:
        print(send_event({"id": i}))
    except RateLimitExceeded as exc:
        print(f"blocked: {exc}")
```

## Usage

### Decorator API

```python
from slideguard import rate_limit


@rate_limit(calls=10, per=60)
def process_job(job_id: str) -> str:
    return f"processed {job_id}"
```

If the call limit is exceeded in the current window, `RateLimitExceeded` is raised.

### Exception Handling

```python
from slideguard import RateLimitExceeded, rate_limit


@rate_limit(calls=2, per=5)
def ping() -> str:
    return "pong"


try:
    print(ping())
except RateLimitExceeded:
    print("Too many requests. Try again soon.")
```

### Low-Level Helper (`is_allowed`)

Use this when you need custom control outside the decorator.

```python
import time
from slideguard import is_allowed

calls: list[float] = []

allowed, calls = is_allowed(calls, max_calls=3, window=10)
if allowed:
    calls.append(time.time())
    print("accepted")
else:
    print("blocked")
```

`is_allowed` removes expired timestamps from the provided list and returns `(allowed, cleaned_calls)`.

## Behavior Notes

- Limits are per decorated function (closure-based state).
- Storage is in-memory and process-local.
- The decorator is thread-safe for concurrent calls in one process.

## Development

Run tests:

```bash
python -m pytest -q
```

## Contributing

Contributions are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Add or update tests.
4. Open a pull request.

## License

MIT. See the [LICENSE](LICENSE).
