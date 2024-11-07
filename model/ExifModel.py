#Model danych exif
class ExifModel:
    def __init__(self, model_of_camera="No data", location="No data", orientation="No data", flash=False, capture_data=None, iso=0, focal_length="No data", exposure_time="No data", aperture="No data"):
        self.model_of_camera = model_of_camera
        self.location = location
        self.orientation = orientation
        self.flash = flash #roznie oznaczane zazwyczaj 0, 1, 9
        self.capture_data = capture_data
        self.iso = iso #czulosc matrycy na swiatlo wartości typu 100 200 800 itd.
        self.focal_length = focal_length #ogniskowa podawana w mm
        self.exposure_time = exposure_time #czas naświetlania (zazwyczaj podawany jako 1/x sekundy)
        self.aperture = aperture #przysłona wyrazana w np. f/1.5