from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from file_organizer.organizer import apply_plan, build_plan, undo_last_run
from file_organizer.rules import category_for_extension


class RulesTests(unittest.TestCase):
    def test_known_extension(self) -> None:
        self.assertEqual(category_for_extension(".jpg"), "Images")

    def test_unknown_extension(self) -> None:
        self.assertEqual(category_for_extension(".xyz"), "Other")


class OrganizerTests(unittest.TestCase):
    def test_build_plan_and_apply(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            folder = Path(temp_dir)
            (folder / "photo.jpg").write_text("image")
            (folder / "notes.txt").write_text("text")

            plan = build_plan(folder)
            self.assertEqual(len(plan), 2)

            apply_plan(folder, plan)

            self.assertTrue((folder / "Images" / "photo.jpg").exists())
            self.assertTrue((folder / "Documents" / "notes.txt").exists())

    def test_undo(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            folder = Path(temp_dir)
            original = folder / "photo.jpg"
            original.write_text("image")

            plan = build_plan(folder)
            apply_plan(folder, plan)

            restored = undo_last_run(folder)

            self.assertEqual(restored, 1)
            self.assertTrue(original.exists())


if __name__ == "__main__":
    unittest.main()
