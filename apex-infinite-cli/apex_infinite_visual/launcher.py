"""Subprocess launcher for the optional visual wrapper."""

from __future__ import annotations

import os
import subprocess
import sys
from collections.abc import Iterator, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, TextIO

DEFAULT_CLEANUP_TIMEOUT = 5.0


@dataclass(frozen=True)
class ApexCliLaunchOptions:  # pylint: disable=too-many-instance-attributes
    """Validated command construction options for the wrapped CLI process."""

    project_path: str | Path
    cli_script: str | Path | None = None
    python_executable: str = sys.executable
    start_command: str | None = None
    ceo_message: str | None = None
    config_path: str | Path | None = None
    provider: str | None = None
    model: str | None = None
    max_iterations: int | None = None
    dry_run: bool = False
    process_timeout_seconds: int | None = None
    extra_env: Mapping[str, str] | None = None


class ApexCliProcess:
    """Context-managed Apex Infinite CLI subprocess with cleanup."""

    def __init__(
        self,
        options: ApexCliLaunchOptions,
        popen_factory: Callable[..., subprocess.Popen] = subprocess.Popen,
    ):
        self.options = options
        self.popen_factory = popen_factory
        self.command = build_apex_cli_command(options)
        self.process: subprocess.Popen | None = None

    @property
    def stdout(self) -> TextIO | None:
        """Return the process stdout pipe."""
        return self.process.stdout if self.process else None

    @property
    def stderr(self) -> TextIO | None:
        """Return the process stderr pipe."""
        return self.process.stderr if self.process else None

    def start(self) -> "ApexCliProcess":
        """Start the CLI process with stdout reserved for JSONL events."""
        if self.process is not None and self.process.poll() is None:
            raise RuntimeError("Apex CLI process is already running")
        cli_script = resolve_cli_script(self.options.cli_script)
        env = os.environ.copy()
        if self.options.extra_env:
            env.update(dict(self.options.extra_env))
        self.process = self.popen_factory(
            self.command,
            cwd=str(cli_script.parent),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            env=env,
        )
        return self

    def iter_stdout_lines(self) -> Iterator[str]:
        """Yield JSONL stdout lines until the process closes stdout."""
        if not self.process or not self.process.stdout:
            return
        yield from self.process.stdout

    def read_stderr(self) -> str:
        """Read separated stderr text after the process exits."""
        if not self.process or not self.process.stderr:
            return ""
        return self.process.stderr.read() or ""

    def terminate(self, cleanup_timeout: float = DEFAULT_CLEANUP_TIMEOUT) -> None:
        """Terminate the process and kill it if graceful cleanup times out."""
        if not self.process:
            return
        if self.process.poll() is None:
            self.process.terminate()
            try:
                self.process.wait(timeout=cleanup_timeout)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait()

    def __enter__(self) -> "ApexCliProcess":
        return self.start()

    def __exit__(self, _exc_type, _exc, _traceback) -> bool:
        self.terminate()
        return False


def build_apex_cli_command(options: ApexCliLaunchOptions) -> list[str]:
    """Build the guarded CLI command consumed by the visual wrapper."""
    if not options.python_executable:
        raise ValueError("python_executable is required")
    cli_script = resolve_cli_script(options.cli_script)
    project_path = str(Path(options.project_path).expanduser())
    if options.max_iterations is not None and options.max_iterations < 1:
        raise ValueError("max_iterations must be positive")
    if (
        options.process_timeout_seconds is not None
        and options.process_timeout_seconds < 1
    ):
        raise ValueError("process_timeout_seconds must be positive")

    command = [
        options.python_executable,
        str(cli_script),
        "--path",
        project_path,
        "--event-stream",
        "-",
        "--machine-output",
    ]
    _append_option(command, "--start", options.start_command)
    _append_option(command, "--ceo", options.ceo_message)
    _append_option(command, "--config", options.config_path)
    _append_option(command, "--provider", options.provider)
    _append_option(command, "--model", options.model)
    if options.max_iterations is not None:
        command.extend(["--max-iterations", str(options.max_iterations)])
    if options.dry_run:
        command.append("--dry-run")

    assert_machine_output_command(command)
    return command


def resolve_cli_script(path: str | Path | None = None) -> Path:
    """Resolve the base CLI script without importing it."""
    if path is None:
        return Path(__file__).resolve().parents[1] / "apex_infinite.py"
    return Path(path).expanduser().resolve()


def assert_machine_output_command(command: list[str]) -> None:
    """Validate stdout guardrails for wrapper command construction."""
    if "--event-stream" not in command:
        raise ValueError("wrapper command must include --event-stream")
    stream_index = command.index("--event-stream")
    if stream_index + 1 >= len(command) or command[stream_index + 1] != "-":
        raise ValueError("wrapper command must write JSONL events to stdout")
    if "--machine-output" not in command:
        raise ValueError("wrapper command must include --machine-output")


def _append_option(command: list[str], flag: str, value: str | Path | None) -> None:
    if value is not None:
        command.extend([flag, str(value)])
