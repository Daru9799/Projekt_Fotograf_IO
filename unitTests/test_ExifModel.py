from unittest.mock import patch, MagicMock
from model.ExifModel import ExifModel


#Test dla metody get_exif_data (odczytywanie danych EXIF z pliku obrazu)
def test_get_exif_data_valid():
    #Przygotowanie mockowanych danych EXIF z nazwami tagów
    exif_data = {
        "Make": 'Canon',
        "Model": 'EOS 5D Mark IV',
        "LensModel": 'Canon RF 50mm F1.2L USM',
        "Orientation": 1,
        "DateTimeOriginal": '2025:01:10 12:34:56',
        "ISOSpeedRatings": 200,
        "FocalLength": 50.0,
        "ExposureTime": (1, 200),
        "FNumber": 1.4,
    }

    #Mock do otwierania pliku
    with patch("PIL.Image.open") as mock_open:
        mock_image = MagicMock()
        mock_image._getexif.return_value = exif_data #Przypisanie danych exif
        mock_open.return_value = mock_image

        result = ExifModel.get_exif_data("fake_path")

        #Test przypisania
        assert result is not None
        assert result.get("Make") == 'Canon'
        assert result.get("Model") == 'EOS 5D Mark IV'
        assert result.get("LensModel") == 'Canon RF 50mm F1.2L USM'
        assert result.get("DateTimeOriginal") == '2025:01:10 12:34:56'
        assert result.get("ISOSpeedRatings") == 200
        assert result.get("FocalLength") == 50.0
        assert result.get("ExposureTime") == (1, 200)
        assert result.get("FNumber") == 1.4

#Sytuacja, w której obraz nie zawiera danych EXIF.
def test_get_exif_data_no_exif():
    #Mockowanie obrazu bez EXIF
    with patch("PIL.Image.open") as mock_open:
        mock_image = MagicMock()
        mock_image._getexif.return_value = None
        mock_open.return_value = mock_image

        result = ExifModel.get_exif_data("fake_path")
        #Test
        assert result is None


#Test dla metody create_exif_obj
def test_create_exif_obj_valid():
    #Mockowanie get_exif_data
    with patch.object(ExifModel, 'get_exif_data', return_value={
        'Make': 'Canon',
        'Model': 'EOS 5D Mark IV',
        'LensModel': 'Canon RF 50mm F1.2L USM',
        'Orientation': 1,
        'DateTimeOriginal': '2025:01:10 12:34:56',
        'ISOSpeedRatings': 200,
        'FocalLength': 50.0,
        'ExposureTime': (1, 200),
        'FNumber': 1.4,
    }):
        exif_obj = ExifModel.create_exif_obj("fake_path")

        #Sprawdzanie, czy obiekt ExifModel został poprawnie utworzony
        assert exif_obj.producer == 'Canon'
        assert exif_obj.model_of_camera == 'EOS 5D Mark IV'
        assert exif_obj.lens == 'Canon RF 50mm F1.2L USM'
        assert exif_obj.capture_data == '2025:01:10 12:34:56'
        assert exif_obj.iso == 200
        assert exif_obj.focal_length == 50.0
        assert exif_obj.exposure_time == (1, 200)
        assert exif_obj.aperture == 1.4

#Testowanie sytuacji w której dane EXIF nie są dostępne
def test_create_exif_obj_no_exif():
    #Mockowanie braku danych EXIF
    with patch.object(ExifModel, 'get_exif_data', return_value=None):
        exif_obj = ExifModel.create_exif_obj("fake_path")

        #Sprawdzanie, czy obiekt ExifModel został utworzony z wartościami domyślnymi
        assert exif_obj.producer == 'No data'
        assert exif_obj.model_of_camera == 'No data'
        assert exif_obj.lens == 'No data'
        assert exif_obj.capture_data == 'No data'
        assert exif_obj.iso == 'No data'
        assert exif_obj.focal_length == 'No data'
        assert exif_obj.exposure_time == 'No data'
        assert exif_obj.aperture == 'No data'