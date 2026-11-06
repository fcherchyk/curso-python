"""Runs an exercise's tests against the user's code.

The code is written as `exercise.py` in a temporary directory next to the tests, and pytest
runs in a subprocess (with the venv's own interpreter) under a timeout.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path

TIMEOUT_SECONDS = 15
MAX_MESSAGE_LINES = 40


@dataclass(frozen=True)
class TestResult:
    __test__ = False  # not a pytest test class

    name: str
    ok: bool
    message: str = ""


@dataclass
class RunResult:
    tests: list[TestResult] = field(default_factory=list)
    error: str | None = None
    output: str = ""

    @property
    def passed(self) -> bool:
        return self.error is None and bool(self.tests) and all(t.ok for t in self.tests)

    @property
    def passed_count(self) -> int:
        return sum(t.ok for t in self.tests)


def _copy(source: Path, target: Path) -> None:
    """Copies a support file or folder into the working directory."""
    if source.is_dir():
        shutil.copytree(source, target / source.name, ignore=shutil.ignore_patterns("__pycache__"))
    else:
        shutil.copy(source, target / source.name)


def _truncate(text: str, max_lines: int = MAX_MESSAGE_LINES) -> str:
    lines = text.strip().splitlines()
    if len(lines) > max_lines:
        lines = ["…", *lines[-max_lines:]]
    return "\n".join(lines)


_FRAME_HEADER = re.compile(r"^(\S.*?):(\d+|\?\?\?): in ")


def _clean_traceback(text: str, work_dir: Path) -> str:
    """Strips temp paths and pytest/importlib frames: keeps only the exercise's files."""
    for prefix in (f"/private{work_dir}/", f"{work_dir}/"):
        text = text.replace(prefix, "")
    lines: list[str] = []
    skip = False
    for line in text.splitlines():
        if line.startswith("Hint:") or line == "Traceback:":
            continue
        if _FRAME_HEADER.match(line) or line.startswith("<frozen"):
            skip = line.startswith(("/", "<"))
        if not skip or line.startswith("E "):
            lines.append(line)
    return "\n".join(lines)


def _parse_junit(path: Path) -> RunResult:
    result = RunResult()
    root = ET.parse(path).getroot()
    for case in root.iter("testcase"):
        problem = case.find("failure")
        if problem is None:
            problem = case.find("error")
        if problem is not None and problem.get("message") == "collection failure":
            text = problem.text or "Could not import your code."
            result.error = _truncate(_clean_traceback(text, path.parent))
            continue
        if case.find("skipped") is not None:
            continue
        message = ""
        if problem is not None:
            text = problem.text or problem.get("message", "")
            if "NotImplementedError: TODO" in text:
                message = "Pending: the function still raises NotImplementedError."
            else:
                message = _truncate(_clean_traceback(text, path.parent))
        result.tests.append(
            TestResult(name=case.get("name", "?"), ok=problem is None, message=message)
        )
    return result


def run_tests(
    code: str,
    files: list[Path],
    timeout: float = TIMEOUT_SECONDS,
) -> RunResult:
    """Runs pytest with `code` as `exercise.py` plus the support `files` (tests, data)."""
    with tempfile.TemporaryDirectory(prefix="course-") as tmp:
        work_dir = Path(tmp)
        (work_dir / "exercise.py").write_text(code, encoding="utf-8")
        for file in files:
            _copy(file, work_dir)
        # An empty pytest.ini pins the rootdir here and ignores the project's config.
        (work_dir / "pytest.ini").write_text("[pytest]\n", encoding="utf-8")
        junit = work_dir / ".result.xml"

        command = [
            sys.executable,
            "-m",
            "pytest",
            "-q",
            "--tb=short",
            "--no-header",
            "--color=no",
            "-p",
            "no:cacheprovider",
            f"--junitxml={junit}",
        ]
        env = {k: v for k, v in os.environ.items() if k not in {"FORCE_COLOR", "PY_COLORS"}} | {
            "PYTHONDONTWRITEBYTECODE": "1",
            "PYTHONUTF8": "1",
            "NO_COLOR": "1",
        }
        try:
            proc = subprocess.run(
                command,
                cwd=work_dir,
                capture_output=True,
                text=True,
                timeout=timeout,
                env=env,
            )
        except subprocess.TimeoutExpired:
            return RunResult(
                error=f"Execution stopped after {timeout:g} s. "
                "Is there an infinite loop or something waiting for input?"
            )

        output = _truncate(proc.stdout + proc.stderr, 80)
        if not junit.exists():
            return RunResult(error=output or "pytest produced no results.", output=output)

        result = _parse_junit(junit)
        result.output = output
        if not result.tests and result.error is None:
            result.error = "No tests were found to run."
        return result
