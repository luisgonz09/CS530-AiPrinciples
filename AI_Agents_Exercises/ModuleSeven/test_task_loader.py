import json
import os
import tempfile
import unittest

from task_loader import load_completed_tasks


class TestLoadCompletedTasks(unittest.TestCase):
    def test_returns_only_completed_tasks(self):
        with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8") as temp_file:
            json.dump([
                {"id": 1, "title": "Done task", "completed": True},
                {"id": 2, "title": "Open task", "completed": False},
                {"id": 3, "title": "Another done task", "completed": True},
            ], temp_file)
            temp_path = temp_file.name

        try:
            result = load_completed_tasks(temp_path)
            self.assertEqual(result, [
                {"id": 1, "title": "Done task", "completed": True},
                {"id": 3, "title": "Another done task", "completed": True},
            ])
        finally:
            os.unlink(temp_path)

    def test_missing_file_returns_empty_list(self):
        missing_path = os.path.join(tempfile.gettempdir(), "definitely_missing_task_file.json")
        self.assertEqual(load_completed_tasks(missing_path), [])

    def test_invalid_json_returns_empty_list(self):
        with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8") as temp_file:
            temp_file.write("{not valid json}")
            temp_path = temp_file.name

        try:
            self.assertEqual(load_completed_tasks(temp_path), [])
        finally:
            os.unlink(temp_path)

    def test_top_level_not_a_list_returns_empty_list(self):
        with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8") as temp_file:
            json.dump({"id": 1, "title": "wrong shape", "completed": True}, temp_file)
            temp_path = temp_file.name

        try:
            self.assertEqual(load_completed_tasks(temp_path), [])
        finally:
            os.unlink(temp_path)

    def test_skips_invalid_record_missing_fields(self):
        with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8") as temp_file:
            json.dump([
                {"id": 1, "title": "Missing completed field"},
                {"id": 2, "title": "Valid task", "completed": True},
            ], temp_file)
            temp_path = temp_file.name

        try:
            self.assertEqual(load_completed_tasks(temp_path), [
                {"id": 2, "title": "Valid task", "completed": True},
            ])
        finally:
            os.unlink(temp_path)

    def test_skips_invalid_record_wrong_types(self):
        with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8") as temp_file:
            json.dump([
                {"id": "abc", "title": "Bad id", "completed": True},
                {"id": 5, "title": 123, "completed": True},
                {"id": 6, "title": "Good task", "completed": True},
                {"id": 7, "title": "Wrong bool", "completed": "yes"},
            ], temp_file)
            temp_path = temp_file.name

        try:
            self.assertEqual(load_completed_tasks(temp_path), [
                {"id": 6, "title": "Good task", "completed": True},
            ])
        finally:
            os.unlink(temp_path)

    def test_skips_non_dict_entries_in_list(self):
        with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8") as temp_file:
            json.dump([
                "not a dict",
                [1, 2, 3],
                {"id": 8, "title": "Valid", "completed": True},
            ], temp_file)
            temp_path = temp_file.name

        try:
            self.assertEqual(load_completed_tasks(temp_path), [
                {"id": 8, "title": "Valid", "completed": True},
            ])
        finally:
            os.unlink(temp_path)


if __name__ == "__main__":
    unittest.main(verbosity=2)
