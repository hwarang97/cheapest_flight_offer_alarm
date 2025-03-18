from dotenv import load_dotenv


load_dotenv()


class FlightData:
    def __init__(self, data: list):
        self.data = data

    def find_cheapest_flight(self) -> dict:
        cheapest_flight = self.data[0]
        for flight in self.data[1:]:
            if self._find_price(flight) < self._find_price(cheapest_flight):
                cheapest_flight = flight

        summary = {
            "departement_iata": self._find_departure(cheapest_flight),
            "arrival_iata": self._find_arrival(cheapest_flight),
            "price": self._find_price(cheapest_flight),
            "out_date": self._find_out_date(cheapest_flight),
            "return_date": self._find_return_date(cheapest_flight),
        }
        return summary

    def _find_price(self, flight: dict) -> str:
        return flight.get("price").get("total")

    def _find_departure(self, flight: dict) -> str:
        return (
            flight.get("itineraries")[0]
            .get("segments")[0]
            .get("departure")
            .get("iataCode")
        )

    def _find_arrival(self, flight: dict) -> str:
        return (
            flight.get("itineraries")[0]
            .get("segments")[0]
            .get("arrival")
            .get("iataCode")
        )

    def _find_out_date(self, flight: dict) -> str:
        return (
            flight.get("itineraries")[0].get("segments")[0].get("departure").get("at")
        )

    def _find_return_date(self, flight: dict) -> str:
        return flight.get("itineraries")[0].get("segments")[0].get("arrival").get("at")
