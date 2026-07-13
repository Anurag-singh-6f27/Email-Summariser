from __future__ import annotations

from pathlib import Path


LOG_FILE = Path("logs/application.log")


def get_log_page(
    page: int,
    page_size: int = 100,
) -> tuple[list[str], int]:
    """
    Return one page of log lines (newest first).
    """

    if not LOG_FILE.exists():
        return [], 0

    with LOG_FILE.open(
        "r",
        encoding="utf-8",
    ) as file:

        lines = file.readlines()

    lines.reverse()

    total_lines = len(lines)

    start = (page - 1) * page_size
    end = start + page_size

    return (
        lines[start:end],
        total_lines,
    )