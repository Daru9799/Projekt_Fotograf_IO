from PyQt5.QtWidgets import (QDialog, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QScrollArea)
from PyQt5.QtGui import QIcon

class ExifWindow(QDialog):
    def __init__(self, exif_model, img_name):
        super().__init__()
        self.exif_model = exif_model
        self.img_name = img_name
        self.setWindowTitle(f"Dane EXIF - {self.img_name}")
        self.setGeometry(200, 200, 600, 400)
        self.setWindowIcon(QIcon("img/exifIcon.png"))

        container = QWidget()
        main_layout = QVBoxLayout()

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout()

        self.fields = {}
        for key, value in vars(exif_model).items():
            field_layout = QHBoxLayout()

            #Tłumaczenie kluczy
            label = QLabel(f"{self.translate_field(key)}:")
            label.setFixedWidth(150)

            #Tłumaczenie wartości
            display_value = self.translate_value(key, value)

            field = QLineEdit(display_value)
            field.setReadOnly(True)
            field.setStyleSheet("color: white")

            field_layout.addWidget(label)
            field_layout.addWidget(field)

            self.fields[key] = field
            scroll_layout.addLayout(field_layout)

        scroll_content.setLayout(scroll_layout)
        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)
        container.setLayout(main_layout)
        self.setLayout(main_layout)

    def translate_field(self, key):
        field_names = {
            "producer": "Producent",
            "model_of_camera": "Model aparatu",
            "lens": "Obiektyw",
            "orientation": "Orientacja",
            "flash": "Lampa błyskowa",
            "capture_data": "Data i godzina",
            "iso": "ISO",
            "focal_length": "Ogniskowa",
            "exposure_time": "Czas naświetlania",
            "aperture": "Przysłona",
            "saturation": "Nasycenie",
            "contrast": "Kontrast",
            "sharpness": "Ostrość",
            "digital_zoom_ratio": "Współczynnik zoomu",
            "brightness_value": "Wartość jasności",
            "exposure_bias": "Bias ekspozycji"
        }
        return field_names.get(key, key.capitalize().replace('_', ' '))

    def translate_value(self, key, value):
        # Translate based on EXIF key and value
        if value == "No data":
            return "Brak danych"
        if key == "flash":
            return self.translate_flash(value)
        if key in ["saturation", "contrast", "sharpness"]:
            return self.translate_common_levels(value)
        if key == "orientation":
            return self.translate_orientation(value)
        if key == "focal_length":
            return str(value) + "mm"
        if key == "aperture":
            return "f/" + str(value)
        if key == "digital_zoom_ratio":
            return str(value) + "x"
        if key == "brightness_value" or key == "exposure_bias":
            return str(value) + " EV"
        if key == "exposure_time":
            return str(value) + "s"
        return str(value)

    def translate_flash(self, value):
        flash_modes = {
            0: "Lampa błyskowa wyłączona",
            1: "Lampa błyskowa włączona",
            2: "Wykryto światło powrotne z lampy błyskowej",
            4: "Nie wykryto światła powrotnego z lampy błyskowej",
            8: "Tryb wymuszonej lampy błyskowej",
            16: "Tryb automatyczny",
            32: "Brak funkcji lampy błyskowej",
            64: "Tryb redukcji efektu czerwonych oczu"
        }
        return flash_modes.get(value, "Brak danych")

    def translate_common_levels(self, value):
        levels = {
            0: "Normalny",
            1: "Niski",
            2: "Wysoki"
        }
        return levels.get(value, "Brak danych")

    def translate_orientation(self, value):
        orientation_modes = {
            1: "Normalna",
            2: "Odbicie lustrzane w poziomie",
            3: "Obrót o 180°",
            4: "Odbicie lustrzane w pionie",
            5: "Obrót o 90° w prawo + odbicie w pionie",
            6: "Obrót o 90° w prawo",
            7: "Obrót o 90° w lewo + odbicie w pionie",
            8: "Obrót o 90° w lewo"
        }
        return orientation_modes.get(value, "Brak danych")