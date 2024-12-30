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
        self.img_path = None #Ścieżka do pliku do którego będa generowane tagi
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
    async def async_get_tags(self):
        with open(self.img_path, "rb") as f:
            image_data = f.read()
            try:
                result = await self.client.analyze(image_data=image_data, visual_features=[VisualFeatures.TAGS])
            except AzureError as e:
                print(f"AzureError: {e}")
                return None
            except Exception as e:
                print(f"Error: {e}")
                return None
            finally:
                await self.client.close()
                print("Kończenie działania")
            return result

    # Na razie testowo wypisywanie tagów w konsoli dla podanej ścieżki obrazka jako argument
    def generate_tags(self, language, min_accuracy):
        if self.img_path is not None:
            min_accuracy_decimal = min_accuracy / 100.0
            self.list_of_tags = []
            print(language)
            print(min_accuracy_decimal)
            print(self.img_path)

            result = asyncio.run(self.async_get_tags())
            if result is not None:
                print("Tags:")
                if result.tags is not None:
                    for tag in result.tags.list:
                        if tag.confidence >= min_accuracy_decimal:
                            confidence_percentage = round(tag.confidence * 100)
                            tag_dict = {"name": tag.name, "certainty": confidence_percentage}
                            self.list_of_tags.append(tag_dict)
                    return self.list_of_tags
                else:
                    print("No data found.")
            else:
                print("No data found.")