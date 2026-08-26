#!/usr/bin/env python3
"""Preview the backend-logging Pretty Terminal visual contract.

This script is a dependency-free visual reference. It is not intended to be
copied as the production logger implementation.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
import unicodedata
from dataclasses import dataclass
from typing import Iterable

ANSI_RE = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")
RESET = "\x1b[0m"

STYLES = {
    "time": "\x1b[2;90m",
    "trace": "\x1b[2;90m",
    "debug": "\x1b[96m",
    "info": "\x1b[92m",
    "warn": "\x1b[1;93m",
    "error": "\x1b[1;91m",
    "fatal": "\x1b[1;91m",
    "scope": "\x1b[94m",
    "key": "\x1b[2;90m",
    "error_type": "\x1b[1;91m",
    "stack": "\x1b[2;90m",
    "status_ok": "\x1b[92m",
    "status_redirect": "\x1b[96m",
    "status_warn": "\x1b[93m",
    "status_error": "\x1b[91m",
    "duration_slow": "\x1b[93m",
    "duration_critical": "\x1b[91m",
}


@dataclass(frozen=True)
class Row:
    time: str
    level: str
    scope: str
    message: str
    context: tuple[tuple[str, object], ...]
    error: str | None = None
    stack: tuple[str, ...] = ()


def strip_ansi(text: str) -> str:
    return ANSI_RE.sub("", text)


def char_width(char: str) -> int:
    if not char or unicodedata.combining(char):
        return 0
    if unicodedata.category(char) in {"Cf", "Cc"}:
        return 0
    return 2 if unicodedata.east_asian_width(char) in {"W", "F"} else 1


def display_width(text: str) -> int:
    return sum(char_width(char) for char in strip_ansi(text))


def truncate_display(text: str, width: int, ellipsis: str = "…") -> str:
    if width <= 0:
        return ""
    if display_width(text) <= width:
        return text

    target = max(0, width - display_width(ellipsis))
    result: list[str] = []
    used = 0
    for char in text:
        char_cells = char_width(char)
        if used + char_cells > target:
            break
        result.append(char)
        used += char_cells
    return "".join(result) + ellipsis


def pad_display(text: str, width: int) -> str:
    clipped = truncate_display(text, width)
    return clipped + " " * max(0, width - display_width(clipped))


def style(text: str, name: str, color: bool) -> str:
    if not color:
        return text
    return f"{STYLES[name]}{text}{RESET}"


def value_style(key: str, value: object) -> str | None:
    if key == "status":
        try:
            status = int(value)
        except (TypeError, ValueError):
            return None
        if 200 <= status < 300:
            return "status_ok"
        if 300 <= status < 400:
            return "status_redirect"
        if 400 <= status < 500:
            return "status_warn"
        if status >= 500:
            return "status_error"
    if key == "duration_ms":
        try:
            duration = float(value)
        except (TypeError, ValueError):
            return None
        if duration >= 1000:
            return "duration_critical"
        if duration >= 500:
            return "duration_slow"
    return None


def pretty_value(key: str, value: object) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if key == "duration_ms":
        duration = float(value)
        if duration < 1000:
            return f"{duration:g}ms"
        return f"{duration / 1000:.2f}s"
    text = str(value)
    if any(char.isspace() for char in text) or '"' in text:
        escaped = text.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
        return f'"{escaped}"'
    return text


def format_context(items: Iterable[tuple[str, object]], color: bool) -> str:
    parts: list[str] = []
    for key, value in items:
        key_text = style(f"{key}=", "key", color)
        raw_value = pretty_value(key, value)
        accent = value_style(key, value)
        value_text = style(raw_value, accent, color) if accent else raw_value
        parts.append(key_text + value_text)
    return " ".join(parts)


def format_row(row: Row, color: bool) -> list[str]:
    time_col = style(pad_display(row.time, 12), "time", color)
    level_name = row.level.lower()
    level_col = style(pad_display(row.level.upper(), 5), level_name, color)
    scope_col = style(pad_display(row.scope, 20), "scope", color)
    message_col = pad_display(row.message, 30)
    context = format_context(row.context, color)

    lines = [f"{time_col}  {level_col}  {scope_col}  {message_col}  {context}".rstrip()]
    if row.error:
        marker = style("╰─", "error_type", color)
        error_type, separator, error_message = row.error.partition(":")
        rendered_error = style(error_type, "error_type", color)
        if separator:
            rendered_error += f":{error_message}"
        lines.append(f"{' ' * 14}{marker} {rendered_error}")
        for frame in row.stack:
            lines.append(f"{' ' * 17}{style(frame, 'stack', color)}")
    return lines


def should_color(args: argparse.Namespace) -> bool:
    if args.force_color:
        return True
    if args.no_color:
        return False
    if os.environ.get("NO_COLOR") is not None:
        return False
    if os.environ.get("TERM", "").lower() == "dumb":
        return False
    if os.environ.get("FORCE_COLOR") not in {None, "", "0"}:
        return True
    return sys.stdout.isatty()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--force-color", action="store_true", help="emit ANSI even when stdout is not a TTY")
    group.add_argument("--no-color", action="store_true", help="disable ANSI while preserving column layout")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    color = should_color(args)

    if os.name == "nt" and color:
        os.system("")

    rows = (
        Row("13:42:17.410", "trace", "runtime.loop", "Tick processed", (("iteration", 128), ("duration_ms", 1.8))),
        Row("13:42:17.901", "debug", "config.loader", "Configuration loaded", (("files", 3), ("duration_ms", 12.6))),
        Row("13:42:18.604", "info", "http.access", "Request completed", (("method", "GET"), ("route", "/v1/posts/:id"), ("status", 200), ("duration_ms", 38.4), ("request_id", "req_01K3N7VZ7H"))),
        Row("13:42:19.012", "info", "api.auth", "用户登录成功", (("user_id", "user_42"), ("duration_ms", 45.8))),
        Row("13:42:20.087", "warn", "db.query", "Slow query", (("operation", "list_posts"), ("duration_ms", 842.7), ("rows", 24))),
        Row("13:42:20.718", "error", "http.access", "Request failed", (("method", "POST"), ("route", "/v1/publish"), ("status", 503), ("duration_ms", 1204.2))),
        Row("13:42:21.311", "fatal", "publisher.x.worker", "Publish worker stopped", (("account_id", "acc_7"), ("attempt", 2)), "TimeoutError: upstream timed out after 10s", ("at publisher/client.ts:184", "at worker/run.ts:72")),
    )

    for row in rows:
        for line in format_row(row, color):
            print(line)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
