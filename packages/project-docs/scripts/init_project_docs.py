#!/usr/bin/env python3
"""Initialize the project documentation baseline."""

from __future__ import annotations

import argparse
import shutil
import sys
from datetime import datetime
from pathlib import Path


PLACEHOLDERS = {
    "{{PROJECT_NAME}}": "{name}",
    "{{PROJECT_SUMMARY}}": "{summary}",
    "{{OWNER}}": "{owner}",
    "{{DATE}}": "{date}",
}

CORE_DOCUMENTS = {
    Path("00-project-brief.md"),
    Path("01-requirements.md"),
    Path("02-system-design.md"),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Copy the project-docs baseline into a target project."
    )
    parser.add_argument(
        "--target",
        type=Path,
        default=Path.cwd(),
        help="Target project root. Defaults to the current directory.",
    )
    parser.add_argument(
        "--docs-dir",
        default="docs",
        type=Path,
        help="Documentation directory inside the target root (default: docs).",
    )
    parser.add_argument("--name", default="[待确认：项目名称]", help="Project name.")
    parser.add_argument("--owner", default="[待确认]", help="Document owner.")
    parser.add_argument(
        "--summary",
        default="[待确认：用一句话说明目标用户、核心问题和交付结果]",
        help="One-sentence project summary.",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Create every optional document template instead of the core baseline.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing files. Without this flag, existing files are skipped.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show planned actions without writing files.",
    )
    return parser.parse_args()


def render(text: str, *, name: str, owner: str, summary: str, date: str) -> str:
    values = {
        "name": name,
        "owner": owner,
        "summary": summary,
        "date": date,
    }
    for placeholder, format_string in PLACEHOLDERS.items():
        text = text.replace(placeholder, format_string.format(**values))
    return text


def main() -> int:
    args = parse_args()
    package_root = Path(__file__).resolve().parents[1]
    template_root = package_root / "assets" / "docs"

    if not template_root.is_dir():
        print(f"error: template directory not found: {template_root}", file=sys.stderr)
        return 2

    target_root = args.target.expanduser().resolve()
    destination_root = (target_root / args.docs_dir).resolve()
    if destination_root != target_root and target_root not in destination_root.parents:
        print(
            f"error: docs directory must stay inside target project: {destination_root}",
            file=sys.stderr,
        )
        return 2
    date = datetime.now().astimezone().date().isoformat()

    planned: list[tuple[Path, Path, str]] = []
    for source in sorted(template_root.rglob("*")):
        if not source.is_file():
            continue
        relative = source.relative_to(template_root)
        if not args.all and relative not in CORE_DOCUMENTS:
            continue
        destination = destination_root / relative
        action = "overwrite" if destination.exists() and args.force else "create"
        if destination.exists() and not args.force:
            action = "skip"
        planned.append((source, destination, action))

    print(f"Target project: {target_root}")
    print(f"Docs directory: {destination_root}")
    for _, destination, action in planned:
        print(f"{action:9} {destination}")

    if args.dry_run:
        print("Dry run complete; no files were written.")
        return 0

    target_root.mkdir(parents=True, exist_ok=True)
    created = overwritten = skipped = 0

    for source, destination, action in planned:
        if action == "skip":
            skipped += 1
            continue

        destination.parent.mkdir(parents=True, exist_ok=True)
        if source.suffix.lower() == ".md":
            content = source.read_text(encoding="utf-8")
            content = render(
                content,
                name=args.name,
                owner=args.owner,
                summary=args.summary,
                date=date,
            )
            destination.write_text(content, encoding="utf-8", newline="\n")
        else:
            shutil.copy2(source, destination)

        if action == "overwrite":
            overwritten += 1
        else:
            created += 1

    print(
        f"Done: {created} created, {overwritten} overwritten, {skipped} skipped."
    )
    if skipped:
        print("Use --force only when replacing existing documents is intentional.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
