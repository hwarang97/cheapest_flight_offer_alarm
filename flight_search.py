from urllib.error import HTTPError

from dotenv import load_dotenv
import requests
import os


load_dotenv()


class FlightSearch:
    def __init__(self):
        self._api = os.getenv("API_KEY")
        self._secret = os.getenv("API_SECRET")
        self._token_endpoint = os.getenv("AMADEUS_TOKEN_ENDPOINT")
        self._city_search_endpoint = os.getenv("AMADEUS_CITY_SEARCH_ENDPOINT")
        self._token = self._get_token()
        self._endpoint = os.getenv("AMADEUS_OFFERS_SEARCH_ENDPOINT")

    def _get_token(self):
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }

        body = {
            "grant_type": "client_credentials",
            "client_id": self._api,
            "client_secret": self._secret,
        }
        response = requests.post(url=self._token_endpoint, data=body, headers=headers)
        response.raise_for_status()
        return response.json().get("access_token")

    def get_iatacode(self, city: str) -> str:
        headers = {
            "accept": "application/vnd.amadeus+json",
            "Authorization": f"Bearer {self._token}",
        }

        body = {
            "keyword": city,
            "max": 1,
        }
        response = requests.get(
            url=self._city_search_endpoint, headers=headers, params=body
        )
        response.raise_for_status()
        iatacode = response.json().get("data")[0].get("iataCode", "Not Found")
        return iatacode

    def get_flight_offers(
        self, origin, department, dept_date, return_date, lowest_price: int
    ) -> dict | None:
        headers = {
            "Authorization": f"Bearer {self._token}",
            "accept": "application/vnd.amadeus+json",
        }

        params = {
            "originLocationCode": origin,
            "destinationLocationCode": department,
            "departureDate": dept_date,
            "returnDate": return_date,
            "adults": 1,
            "nonStop": "true",
            "currencyCode": "GBP",
            "maxPrice": lowest_price,
        }
        try:
            response = requests.get(url=self._endpoint, params=params, headers=headers)
            response.raise_for_status()
        except HTTPError:
            print(f"request is invalid")
            return None
        else:
            return response.json()
