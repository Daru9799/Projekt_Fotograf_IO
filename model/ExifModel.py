#Model danych exif
# from statsmodels.sandbox.stats.contrast_tools import contrast_labels


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

#FLASH
# 0:  FlashDidNotFire
# 1:  FlashFired
# 2:  StrobeReturnLightDetected
# 4:  StrobeReturnLightNotDetected
# 8:  CompulsoryFlashMode
# 16: AutoMode
# 32: NoFlashFunction
# 64: RedEyeReductionMode
