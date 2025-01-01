import os
from azure.ai.vision.imageanalysis.aio import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import AzureError
from dotenv import load_dotenv
import asyncio
import requests
import uuid
import json


class ClassGeneratorPresenter:
    def __init__(self, view):
        self.view = view
        self.azure_cv_key = None
        self.azure_cv_endpoint = None
        self.azure_translate_key = None
        self.azure_translate_endpoint = None
        self.vision_client = None
        self.img_path = None #Ścieżka do pliku do którego będa generowane tagi
        self.list_of_tags = [] #zmienna przechowujaca liste obiektów tagów

    def load_key_and_endpoint(self):
        load_dotenv(dotenv_path="config.env")
        #Pobranie klucza i endpointu z pliku .env
        self.azure_cv_key = os.getenv("AZURE_CV_KEY")
        self.azure_cv_endpoint = os.getenv("AZURE_CV_ENDPOINT")
        self.azure_translate_key = os.getenv("AZURE_TRANSLATE_KEY")
        self.azure_translate_endpoint = os.getenv("AZURE_TRANSLATE_ENDPOINT")
        #Test
        print(f"Klucz ComputerVision: {self.azure_cv_key}")
        print(f"Endpoint ComputerVision: {self.azure_cv_endpoint}")
        print(f"Klucz Translate: {self.azure_translate_key}")
        print(f"Endpoint Translate: {self.azure_translate_endpoint}")

    def create_client(self):
        if self.azure_cv_key is not None and self.azure_cv_endpoint is not None:
            try:
                self.vision_client = ImageAnalysisClient(endpoint=self.azure_cv_endpoint, credential=AzureKeyCredential(self.azure_cv_key))
            except AzureError as e:
                print(f"AzureError: {e}")
            except Exception as e:
                print(f"Wystąpił problem: {e}")
        if self.azure_translate_key is not None and self.azure_translate_endpoint is not None:
            #DODAC OBSLUGE BLEDOW
            pass

    #Funkcja asynchroniczna do zwracania rezultatu z tagami (synchroniczna nie działała poprawnie)
    async def async_get_tags(self):
        with open(self.img_path, "rb") as f:
            image_data = f.read()
            try:
                result = await self.vision_client.analyze(image_data=image_data, visual_features=[VisualFeatures.TAGS])
            except AzureError as e:
                print(f"AzureError: {e}")
                return None
            except Exception as e:
                print(f"Error: {e}")
                return None
            finally:
                await self.vision_client.close()
                print("Kończenie działania")
            return result

    #Funkcja odpalana bezpośrednio z mainPresentera dostarczająca mu wygenerowane tagi
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

                    language_code = self.get_language_code(language)
                    if language_code != "en":
                        self.list_of_tags = self.translate_tags(self.list_of_tags, language_code)
                    return self.list_of_tags
                else:
                    print("No data found.")
            else:
                print("No data found.")

    #Zamian jezyka na kod (do translatora)
    def get_language_code(self, language_name):
        language_map = {
            "Hiszpański": "es",
            "Polski": "pl",
        }
        return language_map.get(language_name, "en")

    #Tłumaczenie tagów
    def translate_text(self, text, target_language):
        constructed_url = f"{self.azure_translate_endpoint}/translate?api-version=3.0&to={target_language}"
        headers = {
            'Ocp-Apim-Subscription-Key': self.azure_translate_key,
            'Content-type': 'application/json',
            'X-ClientTraceId': str(uuid.uuid4()),
            'Ocp-Apim-Subscription-Region': 'northeurope'
        }
        body = [{
            'text': text
        }]
        try:
            response = requests.post(constructed_url, headers=headers, json=body)
            response_json = response.json()
            translated_text = response_json[0]['translations'][0]['text']
            return translated_text
        except requests.exceptions.RequestException as e:
            print(f"Error during translation request: {e}")
            return None
        except KeyError as e:
            print(f"Error parsing response JSON: Missing key {e}")
            return None

    def translate_tags(self, tags, target_language):
        translated_tags = []
        for tag in tags:
            tag_name = tag['name']
            print(tag_name)
            translated_name = self.translate_text(tag_name, target_language)
            print(translated_name)
            translated_tags.append({
                'name': translated_name,
                'certainty': tag['certainty']
            })
        return translated_tags