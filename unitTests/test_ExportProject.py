import unittest
from unittest.mock import MagicMock, patch, mock_open
import os
import json
import platform
from presenter.ExportProject import ExportProject


class TestExportProject(unittest.TestCase):

    def setUp(self):
        self.mock_view = MagicMock()
        self.mock_project = MagicMock()
        self.export_project = ExportProject(self.mock_view, self.mock_project)

    @patch("presenter.ExportProject.ExportProject.select_save_location", return_value="test_path/test.pro")
    @patch("presenter.ExportProject.ExportProject.create_file")
    @patch("presenter.ExportProject.ExportProject.lock_file")
    @patch("presenter.ExportProject.ExportProject.unlock_file")
    def test_save_project(self, mock_unlock_file, mock_lock_file, mock_create_file, mock_select_save_location):
        result = self.export_project.save_project()
        self.assertTrue(result)
        mock_select_save_location.assert_called_once()
        mock_create_file.assert_called_once_with("test_path/test.pro")
        mock_lock_file.assert_called_once_with("test_path/test.pro")
        mock_unlock_file.assert_called()

    @patch("builtins.open", new_callable=mock_open)
    @patch("os.path.getsize", return_value=1024)
    def test_lock_file(self, mock_getsize, mock_open_file):
        file_path = "test_path/test.pro"

        if platform.system() == "Windows":
            with patch("msvcrt.locking") as mock_locking:
                self.export_project.lock_file(file_path)
                mock_locking.assert_called_once()
        else:
            with patch("fcntl.flock") as mock_flock:
                self.export_project.lock_file(file_path)
                mock_flock.assert_called_once()

    @patch("builtins.open", new_callable=mock_open)
    @patch("os.path.getsize", return_value=1024)
    def test_unlock_file(self, mock_getsize, mock_open_file):
        file_path = "test_path/test.pro"
        self.export_project.file_lock = mock_open_file(file_path)

        if platform.system() == "Windows":
            with patch("msvcrt.locking") as mock_locking:
                self.export_project.unlock_file()
                mock_locking.assert_called_once()
        else:
            with patch("fcntl.flock") as mock_flock:
                self.export_project.unlock_file()
                mock_flock.assert_called_once()


if __name__ == "__main__":
    unittest.main()
