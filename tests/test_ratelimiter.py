import threading
from unittest.mock import patch

import pytest

from slideguard import RateLimitExceeded, rate_limit


def test_calls_within_limit_pass() -> None:
    @rate_limit(calls=3, per=60)
    def multiply_by_two(value: int) -> int:
        return value * 2

    with patch("slideguard.core.time", return_value=1000.0), patch(
        "slideguard.decorator.time", return_value=1000.0
    ):
        assert multiply_by_two(1) == 2
        assert multiply_by_two(2) == 4
        assert multiply_by_two(3) == 6


def test_call_exceeding_limit_raises() -> None:
    @rate_limit(calls=2, per=60)
    def ping() -> str:
        return "pong"

    with patch("slideguard.core.time", return_value=1000.0), patch(
        "slideguard.decorator.time", return_value=1000.0
    ):
        assert ping() == "pong"
        assert ping() == "pong"
        with pytest.raises(RateLimitExceeded):
            ping()


def test_calls_allowed_again_after_window_expires() -> None:
    @rate_limit(calls=2, per=10)
    def ping() -> str:
        return "pong"

    with patch("slideguard.core.time", side_effect=[1000.0, 1001.0, 1002.0, 1012.0]), patch(
        "slideguard.decorator.time", side_effect=[1000.0, 1001.0, 1012.0]
    ):
        assert ping() == "pong"
        assert ping() == "pong"

        with pytest.raises(RateLimitExceeded):
            ping()

        assert ping() == "pong"


def test_thread_safety_only_n_succeed() -> None:
    limit = 4
    total_threads = 10

    @rate_limit(calls=limit, per=60)
    def guarded() -> str:
        return "ok"

    barrier = threading.Barrier(total_threads)
    results: list[str] = []

    def worker() -> None:
        barrier.wait()
        try:
            guarded()
            results.append("ok")
        except RateLimitExceeded:
            results.append("blocked")

    threads = [threading.Thread(target=worker) for _ in range(total_threads)]

    with patch("slideguard.core.time", return_value=1000.0), patch(
        "slideguard.decorator.time", return_value=1000.0
    ):
        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join(timeout=3)

    assert all(not thread.is_alive() for thread in threads)
    assert results.count("ok") == limit
    assert results.count("blocked") == total_threads - limit
