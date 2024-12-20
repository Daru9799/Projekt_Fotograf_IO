#Model danych exif
# from statsmodels.sandbox.stats.contrast_tools import contrast_labels
from PIL.ExifTags import TAGS
from PIL import Image

class ExifModel:
    def __init__(self, producer="No data", model_of_camera="No data", lens="No data", orientation="No data", flash="No data", capture_data="No data", iso="No data", focal_length="No data", exposure_time="No data", aperture="No data", saturation="No data", contrast="No data", sharpness="No data", digital_zoom_ratio="No data", brightness_value="No data", exposure_bias="No data"):
        self.producer = producer
        self.model_of_camera = model_of_camera
        self.lens = lens #uzyty obiektyw
        self.orientation = orientation
        self.flash = flash #roznie oznaczane zazwyczaj 0, 1, 9, 16
        self.capture_data = capture_data
        self.iso = iso #czulosc matrycy na swiatlo wartości typu 100 200 800 itd.
        self.focal_length = focal_length #ogniskowa podawana w mm
        self.exposure_time = exposure_time #czas naświetlania (zazwyczaj podawany jako 1/x sekundy)
        self.aperture = aperture #przysłona wyrazana w np. f/1.5
        self.saturation = saturation
        self.contrast = contrast
        self.sharpness = sharpness
        self.digital_zoom_ratio = digital_zoom_ratio
        self.brightness_value = brightness_value
        self.exposure_bias = exposure_bias

    def get_info(self):
        print(f" Producer: {self.producer}, Camera Model: {self.model_of_camera}, Lens: {self.lens}, Orientation: {self.orientation}, Flash: {self.flash}, DateTime: {self.capture_data}, ISO: {self.iso}, Focal Length: {self.focal_length}, Exposure Time: {self.exposure_time}, Aperture: {self.aperture}, Saturation: {self.saturation}, Contrast: {self.contrast}, Sharpness: {self.sharpness}, Digital Zoom Ratio: {self.digital_zoom_ratio}, Brightness Value: {self.brightness_value}, Exposure Bias: {self.exposure_bias}")

    @staticmethod
    def create_exif_obj(file_path):
        exif_info = ExifModel.get_exif_data(file_path)
        #Jeśli nic nie znalazł to zwraca None
        if not exif_info:
            print("No EXIF data found.")
            return ExifModel(producer="No data", model_of_camera="No data", lens="No data", orientation="No data", flash="No data", capture_data="No data", iso="No data", focal_length="No data", exposure_time="No data", aperture="No data", saturation="No data", contrast="No data", sharpness="No data", digital_zoom_ratio="No data", brightness_value="No data", exposure_bias="No data")

        producer = exif_info.get("Make", "No data")
        model_of_camera = exif_info.get("Model", "No data")
        lens = exif_info.get("LensModel", "No data")
        orientation = exif_info.get("Orientation", "No data")
        flash = exif_info.get("Flash", "No data")
        capture_data = exif_info.get("DateTimeOriginal", "No data")
        iso = exif_info.get("ISOSpeedRatings", "No data")
        focal_length = exif_info.get("FocalLength", "No data")
        exposure_time = exif_info.get("ExposureTime", "No data")
        aperture = exif_info.get("FNumber", "No data")
        saturation = exif_info.get("Saturation","No data")
        contrast = exif_info.get("Contrast", "No data")
        sharpness = exif_info.get("Sharpness", "No data")
        digital_zoom_ratio = exif_info.get("DigitalZoomRatio", "No data")
        brightness_value = exif_info.get("BrightnessValue", "No data")
        exposure_bias = exif_info.get("ExposureBiasValue", "No data")

        exif_model = ExifModel(
            producer = producer,
            model_of_camera = model_of_camera,
            lens = lens,
            orientation = orientation,
            flash = flash,
            capture_data = capture_data,
            iso = iso,
            focal_length = focal_length,
            exposure_time = exposure_time,
            aperture = aperture,
            saturation = saturation,
            contrast = contrast,
            sharpness = sharpness,
            digital_zoom_ratio = digital_zoom_ratio,
            brightness_value = brightness_value,
            exposure_bias = exposure_bias
        )
        return exif_model

    @staticmethod
    def get_exif_data(file_path):
        image = Image.open(file_path)
        #Pobranie danych EXIF
        exif_data = image._getexif()
        if exif_data is None:
            return None
        #Przygotowanie danych EXIF
        exif_info = {}
        for tag, value in exif_data.items():
            tag_name = TAGS.get(tag, tag)
            exif_info[tag_name] = value
        return exif_info
