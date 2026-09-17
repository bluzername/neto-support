#!/usr/bin/env python3
"""Validate zakaut-rates.json, the versioned rates file fetched by the Zakaut app.

Schema:
  version    positive int
  published  YYYY-MM-DD, a real calendar date, not in the future
  tables     object; every value must itself be an object

Stdlib only. Exit code 0 on success, 1 on any violation.
"""

import datetime
import json
import re
import sys

DEFAULT_PATH = "zakaut-rates.json"
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def load_json(path):
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def check_version(data):
    version = data.get("version")
    if isinstance(version, bool) or not isinstance(version, int):
        return ["version must be an int"]
    if version < 1:
        return ["version must be >= 1, got %d" % version]
    return []


def check_published(data, today):
    published = data.get("published")
    if not isinstance(published, str) or not DATE_PATTERN.match(published):
        return ["published must be a string matching YYYY-MM-DD"]
    try:
        parsed = datetime.date.fromisoformat(published)
    except ValueError:
        return ["published is not a real calendar date: %s" % published]
    if parsed > today:
        return ["published is in the future: %s (today is %s)" % (published, today)]
    return []


def check_tables(data):
    tables = data.get("tables")
    if not isinstance(tables, dict):
        return ["tables must be an object"]
    return [
        "tables[%r] must be an object, got %s" % (name, type(value).__name__)
        for name, value in tables.items()
        if not isinstance(value, dict)
    ]


def validate(data, today):
    if not isinstance(data, dict):
        return ["top level must be a JSON object"]
    missing = [key for key in ("version", "published", "tables") if key not in data]
    if missing:
        return ["missing required key(s): %s" % ", ".join(missing)]
    return check_version(data) + check_published(data, today) + check_tables(data)


def main(argv):
    path = argv[1] if len(argv) > 1 else DEFAULT_PATH
    try:
        data = load_json(path)
    except FileNotFoundError:
        print("ERROR: %s not found" % path)
        return 1
    except json.JSONDecodeError as exc:
        print("ERROR: %s is not valid JSON: %s" % (path, exc))
        return 1

    errors = validate(data, datetime.date.today())
    for error in errors:
        print("ERROR: %s" % error)
    if errors:
        return 1
    print(
        "OK: %s version=%d published=%s tables=%d"
        % (path, data["version"], data["published"], len(data["tables"]))
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
