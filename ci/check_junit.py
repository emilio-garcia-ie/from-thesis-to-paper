"""Fail CI when a required pytest report is skipped, xfailed or empty."""

from __future__ import annotations

import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def main(path: str) -> int:
    report = Path(path)
    root = ET.parse(report).getroot()
    suites = [root] if root.tag == "testsuite" else list(root.iter("testsuite"))
    tests = sum(int(suite.attrib.get("tests", 0)) for suite in suites)
    skipped = sum(int(suite.attrib.get("skipped", 0)) for suite in suites)
    failures = sum(int(suite.attrib.get("failures", 0)) for suite in suites)
    errors = sum(int(suite.attrib.get("errors", 0)) for suite in suites)
    if tests == 0 or skipped or failures or errors:
        print(
            f"invalid test report: tests={tests} skipped={skipped} failures={failures} errors={errors}",
            file=sys.stderr,
        )
        return 1
    print(f"test report OK: {tests} tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1]))
