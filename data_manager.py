from dotenv import load_dotenv
import requests
import os


load_dotenv()


class DataManager:
    def __init__(self):
        self._endpoint = os.getenv("SHEETY_ENDPOINT")
        self._token = f"Bearer {os.getenv("SHEETY_TOKEN")}"
        self._headers = {"Authorization": self._token}

    def get_sheet(self) -> list:
        response = requests.get(url=self._endpoint)
        response.raise_for_status()
        return response.json().get("prices", "Not invalid format")

    def put_iatacode(self, iata_code: str, object_id: int):
        endpoint = f"{self._endpoint}/{object_id}"
        body = {
            "price": {
                "iataCode": iata_code,
            }
        }
        response = requests.put(url=endpoint, json=body, headers=self._headers)
        response.raise_for_status()
