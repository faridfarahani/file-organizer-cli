from __future__ import annotations

import json
import shutil
from dataclasses import asdict, dataclass
from pathlib import Path

from .rules import category_for_extension

LOG_NAME = "organizer_log.json"


@dataclass(frozen=True)
class MoveOperation:
    source: str
    destination: str


def _safe_destination(destination: Path) -> Path:
    if not destination.exists():
        return destination

    stem = destination.stem
    suffix = destination.suffix
    counter = 1

    while True:
        candidate = destination.with_name(f"{stem}_{counter}{suffix}")
        if not candidate.exists():
            return candidate
        counter += 1


def build_plan(folder: Path) -> list[MoveOperation]:
    folder = folder.resolve()

    if not folder.exists():
        raise FileNotFoundError(f"Folder does not exist: {folder}")

    if not folder.is_dir():
        raise NotADirectoryError(f"Not a directory: {folder}")

    operations: list[MoveOperation] = []

    for item in sorted(folder.iterdir()):
        if not item.is_file():
            continue

        if item.name == LOG_NAME:
            continue

        category = category_for_extension(item.suffix)
        destination_dir = folder / category
        destination = _safe_destination(destination_dir / item.name)

        operations.append(
            MoveOperation(
                source=str(item),
                destination=str(destination),
            )
        )

    return operations


def apply_plan(folder: Path, operations: list[MoveOperation], *, dry_run: bool = False) -> None:
    folder = folder.resolve()

    if dry_run:
        return

    completed: list[MoveOperation] = []

    for operation in operations:
        source = Path(operation.source)
        destination = Path(operation.destination)

        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(source), str(destination))
        completed.append(operation)

    log_path = folder / LOG_NAME
    log_path.write_text(
        json.dumps([asdict(item) for item in completed], indent=2),
        encoding="utf-8",
    )


def undo_last_run(folder: Path) -> int:
    folder = folder.resolve()
    log_path = folder / LOG_NAME

    if not log_path.exists():
        return 0

    raw = json.loads(log_path.read_text(encoding="utf-8"))
    operations = [MoveOperation(**item) for item in raw]

    restored = 0

    for operation in reversed(operations):
        source = Path(operation.destination)
        destination = Path(operation.source)

        if not source.exists():
            continue

        destination.parent.mkdir(parents=True, exist_ok=True)

        if destination.exists():
            destination = _safe_destination(destination)

        shutil.move(str(source), str(destination))
        restored += 1

    log_path.unlink(missing_ok=True)
    return restored
