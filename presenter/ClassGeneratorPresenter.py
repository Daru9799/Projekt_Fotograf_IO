import os
from azure.ai.vision.imageanalysis.aio import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import AzureError
from dotenv import load_dotenv
import asyncio

class ClassGeneratorPresenter:
    def __init__(self, view):
        self.view = view
        self.azure_cv_key = None
        self.azure_cv_endpoint = None
        self.client = None
        self.list_of_tags = [] #zmienna przechowujaca liste obiektów tagów

    def load_key_and_endpoint(self):
        load_dotenv(dotenv_path="config.env")
        #Pobranie klucza i endpointu z pliku .env
        self.azure_cv_key = os.getenv("AZURE_CV_KEY")
        self.azure_cv_endpoint = os.getenv("AZURE_CV_ENDPOINT")
        #Test
        print(f"Klucz: {self.azure_cv_key}")
        print(f"Endpoint: {self.azure_cv_endpoint}")

    def create_client(self):
        if self.azure_cv_key is not None and self.azure_cv_endpoint is not None:
            try:
                self.client = ImageAnalysisClient(endpoint=self.azure_cv_endpoint, credential=AzureKeyCredential(self.azure_cv_key))
            except AzureError as e:
                print(f"AzureError: {e}")
            except Exception as e:
                print(f"Wystąpił problem: {e}")

    # Funkcja asynchroniczna do zwracania rezultatu z tagami (synchroniczna nie działała poprawnie)
    async def async_get_tags(self, img_path):
        with open(img_path, "rb") as f:
            image_data = f.read()
            try:
                result = await self.client.analyze(image_data=image_data, visual_features=[VisualFeatures.TAGS])
            except AzureError as e:
                print(f"AzureError: {e}")
                return None
            return result

    # Na razie testowo wypisywanie tagów w konsoli dla podanej ścieżki obrazka jako argument
    def print_tags(self, img_path):
        result = asyncio.run(self.async_get_tags(img_path))
        if result is not None:
            print("Tags:")
            if result.tags is not None:
                for tag in result.tags.list:
                    if tag.confidence:
                        print(f"'{tag.name}', Confidence {tag.confidence: .2f}")
            else:
                print("No data found.")