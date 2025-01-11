import unittest
from unittest.mock import MagicMock, patch
import os
import shutil
from presenter.ExportToYolo import ExportToYolo
class TestExportToYolo(unittest.TestCase):

    def setUp(self):
        # Ustawienia dla testu
        self.mock_view = MagicMock()
        self.mock_project = MagicMock()
        self.export_to_yolo = ExportToYolo(self.mock_view, self.mock_project)

    @patch("PyQt5.QtWidgets.QFileDialog.getSaveFileName")
    def test_select_save_location(self, mock_get_save_file_name):
        # Mockowanie wyniku dialogu
        mock_get_save_file_name.return_value = ("test_path/test.yaml", "")

        # Wywołanie metody
        result = self.export_to_yolo.select_save_location()

        # Sprawdzenie czy ścieżka jest prawidłowa
        self.assertEqual(result, "test_path/test.yaml")
        mock_get_save_file_name.assert_called_once()

    @patch("os.makedirs")
    @patch("os.path.dirname")
    @patch("os.path.basename")
    def test_create_folder_structure(self, mock_basename, mock_dirname, mock_makedirs):
        # Mockowanie ścieżek
        mock_dirname.return_value = "test_path"
        mock_basename.return_value = "test.yaml"

        # Wywołanie metody
        self.export_to_yolo.create_folder_structure("test_path/test.yaml")

        # Sprawdzenie, czy os.makedirs zostało wywołane odpowiednią ilość razy
        mock_makedirs.assert_any_call("test_path\\test", exist_ok=True)
        mock_makedirs.assert_any_call("test_path\\test\\train", exist_ok=True)
        mock_makedirs.assert_any_call("test_path\\test\\valid", exist_ok=True)
        mock_makedirs.assert_any_call("test_path\\test\\train\\images", exist_ok=True)
        mock_makedirs.assert_any_call("test_path\\test\\train\\labels", exist_ok=True)
        mock_makedirs.assert_any_call("test_path\\test\\valid\\images", exist_ok=True)
        mock_makedirs.assert_any_call("test_path\\test\\valid\\labels", exist_ok=True)

    @patch("builtins.open", new_callable=MagicMock)
    @patch("os.makedirs")
    @patch("os.path.exists")
    def test_create_yaml_file(self, mock_exists, mock_makedirs, mock_open):
        # Mockowanie projektów i plików
        mock_image = MagicMock()
        mock_image.filename = "image1.jpg"
        mock_image.list_of_annotations = []
        self.mock_project.list_of_images_model = [mock_image]
        self.mock_project.list_of_classes_model = [MagicMock(class_id=0, name="Class1")]
        self.mock_project.get_full_path_by_filename.return_value = "source_path/image1.jpg"

        # Mockowanie istnienia folderów
        mock_exists.return_value = True

        # Wywołanie metody
        self.export_to_yolo.create_yaml_file("test_path")

        # Sprawdzenie, czy otworzenie pliku odbyło się prawidłowo
        mock_open.assert_called_with("test_path\\data.yaml", 'w', encoding='utf-8')  # <-- \\ zamiast /

        # Sprawdzenie, czy foldery zostały utworzone
        mock_makedirs.assert_called_with("test_path\\train\\labels", exist_ok=True)  # <-- \\ zamiast /

if __name__ == "__main__":
    unittest.main()
