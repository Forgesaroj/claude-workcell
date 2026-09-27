#!/usr/bin/env python3
"""Check that a Workcell dispatch packet is complete enough to hand off.

This checks packet structure and filled-in fields. It does not enforce file
permissions, approval boundaries, or any other runtime security control.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_HEADINGS = (
    "Outcome",
    "Authority and constraints",
    "Scope fence",
    "Baseline measurement",
    "Deliverables",
    "Acceptance",
    "Stop conditions",
    "Worker handoff",
)
REQUIRED_FIELDS = (
    "Parent task",
    "Worker",
    "Created by",
    "Baseline commit",
    "Branch/worktree",
)
BASELINE_RE = re.compile(r"^(?:[0-9a-fA-F]{7,40})$")
PLACEHOLDER_RE = re.compile(r"<[^<>]+>")


def validate(text: str) -> list[str]:
    errors: list[str] = []
    lines = text.splitlines()
    headings = {line[3:].strip() for line in lines if line.startswith("## ")}
    for heading in REQUIRED_HEADINGS:
        if heading not in headings:
            errors.append(f"missing section: ## {heading}")

    title = next((line for line in lines if line.startswith("# Dispatch:")), "")
    if not title or PLACEHOLDER_RE.search(title):
        errors.append("title must include a task ID and outcome, with no placeholder")

    fields: dict[str, str] = {}
    for field in REQUIRED_FIELDS:
        match = re.search(rf"(?m)^- {re.escape(field)}:[ \t]*(.*?)[ \t]*$", text)
        value = match.group(1) if match else ""
        if not value or value.lower() in {"none", "todo", "tbd", "n/a"}:
            errors.append(f"fill in metadata field: {field}")
        else:
            fields[field] = value
    baseline = fields.get("Baseline commit", "")
    if baseline and not BASELINE_RE.fullmatch(baseline):
        errors.append("Baseline commit must be a 7–40 character hexadecimal commit SHA")

    for section, next_section in (
        ("Outcome", "Authority and constraints"),
        ("Baseline measurement", "Deliverables"),
        ("Deliverables", "Acceptance"),
        ("Stop conditions", "Worker handoff"),
    ):
        body = _section_body(lines, section, next_section)
        if not body.strip():
            errors.append(f"section must contain content: {section}")

    scope = _section_body(lines, "Scope fence", "Baseline measurement")
    for label in ("Allowed paths", "Excluded paths"):
        match = re.search(rf"(?m)^- {re.escape(label)}:[ \t]*(.*?)[ \t]*$", scope)
        if not match or not match.group(1).strip() or match.group(1).strip().lower() in {"none", "todo", "tbd"}:
            errors.append(f"fill in Scope fence field: {label}")

    acceptance = _section_body(lines, "Acceptance", "Stop conditions")
    checked_items = re.findall(r"(?m)^- \[x\] (.+?)\s*$", acceptance, flags=re.IGNORECASE)
    if not checked_items:
        errors.append("Acceptance must include at least one checked, completed acceptance item")
    if not re.search(r"(?m)^- \[ \] Exact commands and expected outcomes:[ \t]*\S", acceptance):
        errors.append("Acceptance must record exact commands and expected outcomes")

    unresolved = sorted(set(PLACEHOLDER_RE.findall(text)))
    if unresolved:
        errors.append("unresolved placeholders: " + ", ".join(unresolved))
    return errors


def _section_body(lines: list[str], heading: str, next_heading: str) -> str:
    start = next((i + 1 for i, line in enumerate(lines) if line == f"## {heading}"), None)
    if start is None:
        return ""
    end = next((i for i in range(start, len(lines)) if lines[i] == f"## {next_heading}"), len(lines))
    return "\n".join(lines[start:end])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packet", type=Path, help="Markdown dispatch packet to validate")
    args = parser.parse_args(argv)
    try:
        text = args.packet.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"error: cannot read {args.packet}: {exc}", file=sys.stderr)
        return 2
    errors = validate(text)
    if errors:
        print(f"{args.packet}: invalid dispatch packet")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"{args.packet}: dispatch packet is complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
