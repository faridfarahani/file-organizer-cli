from __future__ import annotations

import argparse
from pathlib import Path

from .organizer import apply_plan, build_plan, undo_last_run


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Organize files into folders by file type."
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    organize = subparsers.add_parser("organize")
    organize.add_argument("folder", type=Path)
    organize.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview the move plan without changing files.",
    )

    undo = subparsers.add_parser("undo")
    undo.add_argument("folder", type=Path)

    return parser


def main() -> int:
    args = build_parser().parse_args()

    if args.command == "organize":
        operations = build_plan(args.folder)

        if not operations:
            print("No files to organize.")
            return 0

        for operation in operations:
            print(f"{operation.source} -> {operation.destination}")

        if args.dry_run:
            print(f"Dry run complete. Planned moves: {len(operations)}")
            return 0

        apply_plan(args.folder, operations)
        print(f"Organization complete. Files moved: {len(operations)}")
        return 0

    restored = undo_last_run(args.folder)
    print(f"Undo complete. Files restored: {restored}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
