#!/usr/bin/env python3
"""Validate devkit backend-logging NDJSON output with the Python standard library."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Iterable, TextIO

ANSI_RE = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")
TIMESTAMP_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,9})?Z$")
EVENT_RE = re.compile(r"^[a-z][a-z0-9_]*(?:\.[a-z][a-z0-9_]*)*$")
TRACE_ID_RE = re.compile(r"^[0-9a-f]{32}$")
SPAN_ID_RE = re.compile(r"^[0-9a-f]{16}$")
LEVELS = {"trace", "debug", "info", "warn", "error", "fatal"}
REQUIRED_FIELDS = ("ts", "level", "msg")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate one-JSON-object-per-line logs produced by the backend-logging contract."
    )
    parser.add_argument(
        "path",
        nargs="?",
        default="-",
        help="NDJSON file path, or '-' to read stdin (default).",
    )
    parser.add_argument(
        "--require-event",
        action="store_true",
        help="Require every record to contain a valid stable event name.",
    )
    parser.add_argument(
        "--allow-null",
        action="store_true",
        help="Allow top-level null values. The contract normally requires omitting them.",
    )
    parser.add_argument(
        "--max-errors",
        type=int,
        default=50,
        help="Stop after this many validation errors (default: 50).",
    )
    return parser.parse_args()


def open_input(path: str) -> tuple[TextIO, bool]:
    if path == "-":
        return sys.stdin, False
    stream = Path(path).open("r", encoding="utf-8")
    return stream, True


def validate_timestamp(value: object) -> str | None:
    if not isinstance(value, str):
        return "ts must be a string"
    if TIMESTAMP_RE.fullmatch(value) is None:
        return "ts must be UTC RFC 3339 in YYYY-MM-DDTHH:MM:SS[.fraction]Z form"
    try:
        datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError:
        return "ts is not a valid RFC 3339 timestamp"
    return None


def validate_error(value: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict):
        return ["error must be an object"]
    if not isinstance(value.get("type"), str) or not value.get("type"):
        errors.append("error.type must be a non-empty string")
    if not isinstance(value.get("message"), str):
        errors.append("error.message must be a string")
    if "stack" in value and not isinstance(value["stack"], str):
        errors.append("error.stack must be a string")
    if "cause" in value and not isinstance(value["cause"], dict):
        errors.append("error.cause must be an object")
    return errors


def validate_record(record: object, *, require_event: bool, allow_null: bool) -> list[str]:
    errors: list[str] = []
    if not isinstance(record, dict):
        return ["record must be a JSON object"]

    for field in REQUIRED_FIELDS:
        if field not in record:
            errors.append(f"missing required field: {field}")

    if "ts" in record:
        timestamp_error = validate_timestamp(record["ts"])
        if timestamp_error:
            errors.append(timestamp_error)

    if "level" in record:
        level = record["level"]
        if not isinstance(level, str) or level not in LEVELS:
            errors.append(
                "level must be one of: " + ", ".join(sorted(LEVELS))
            )

    if "msg" in record:
        msg = record["msg"]
        if not isinstance(msg, str) or not msg.strip():
            errors.append("msg must be a non-empty string")

    event = record.get("event")
    if require_event and event is None:
        errors.append("missing required field: event")
    if event is not None and (
        not isinstance(event, str) or EVENT_RE.fullmatch(event) is None
    ):
        errors.append("event must be a stable lower-case dotted identifier")

    if "ctx" in record and not isinstance(record["ctx"], dict):
        errors.append("ctx must be an object")

    if "error" in record:
        errors.extend(validate_error(record["error"]))

    trace_id = record.get("trace_id")
    if trace_id is not None and (
        not isinstance(trace_id, str) or TRACE_ID_RE.fullmatch(trace_id) is None
    ):
        errors.append("trace_id must be 32 lower-case hexadecimal characters")
    elif trace_id == "0" * 32:
        errors.append("trace_id must not be all zeros")

    span_id = record.get("span_id")
    if span_id is not None and (
        not isinstance(span_id, str) or SPAN_ID_RE.fullmatch(span_id) is None
    ):
        errors.append("span_id must be 16 lower-case hexadecimal characters")
    elif span_id == "0" * 16:
        errors.append("span_id must not be all zeros")
    if span_id is not None and trace_id is None:
        errors.append("trace_id is required when span_id is present")

    if not allow_null:
        null_fields = [key for key, value in record.items() if value is None]
        if null_fields:
            errors.append(
                "top-level null fields must be omitted: " + ", ".join(sorted(null_fields))
            )

    return errors


def iter_lines(stream: TextIO) -> Iterable[tuple[int, str]]:
    for number, raw_line in enumerate(stream, start=1):
        yield number, raw_line.rstrip("\n\r")


def main() -> int:
    args = parse_args()
    if args.max_errors < 1:
        print("--max-errors must be at least 1", file=sys.stderr)
        return 2

    try:
        stream, should_close = open_input(args.path)
    except OSError as exc:
        print(f"cannot open {args.path!r}: {exc}", file=sys.stderr)
        return 2

    records = 0
    failures = 0

    try:
        for line_number, line in iter_lines(stream):
            if not line:
                failures += 1
                print(f"line {line_number}: blank lines are not valid NDJSON events", file=sys.stderr)
                if failures >= args.max_errors:
                    break
                continue

            if ANSI_RE.search(line):
                failures += 1
                print(f"line {line_number}: contains ANSI escape sequences", file=sys.stderr)
                if failures >= args.max_errors:
                    break
                continue

            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                failures += 1
                print(
                    f"line {line_number}: invalid JSON at column {exc.colno}: {exc.msg}",
                    file=sys.stderr,
                )
                if failures >= args.max_errors:
                    break
                continue

            records += 1
            errors = validate_record(
                record,
                require_event=args.require_event,
                allow_null=args.allow_null,
            )
            for error in errors:
                failures += 1
                print(f"line {line_number}: {error}", file=sys.stderr)
                if failures >= args.max_errors:
                    break
            if failures >= args.max_errors:
                break
    finally:
        if should_close:
            stream.close()

    if records == 0 and failures == 0:
        print("no log events found", file=sys.stderr)
        return 1

    if failures:
        print(
            f"FAILED: {failures} validation error(s) across {records} parsed event(s)",
            file=sys.stderr,
        )
        return 1

    print(f"OK: {records} JSON log event(s) validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
