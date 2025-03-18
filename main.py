from datetime import datetime
from datetime import timedelta
from pprint import pprint
import textwrap

from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import FlightData
from notification_manager import NotificationManager

data_manager = DataManager()

# Call data from google sheet
sheet_data = data_manager.get_sheet()

flight_search = FlightSearch()

# store iata_code to sheet
for row in sheet_data:
    if not row.get("iataCode"):
        city = row.get("city")
        iata_code = flight_search.get_iatacode(city)
        id = row.get("id")
        row.update({"iataCode": iata_code})
        data_manager.put_iatacode(object_id=id, iata_code=iata_code)

# search flight offer
notification_manager = NotificationManager()
origin = "LON"
for row in sheet_data:
    department = row.get("iataCode")
    lowest_price = row.get("lowestPrice")
    dept_date = (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d")
    return_date = (datetime.today() + timedelta(days=6 * 30)).strftime("%Y-%m-%d")
    flight_offer = flight_search.get_flight_offers(
        origin, department, dept_date, return_date, lowest_price
    )
    pprint(flight_offer)

    if flight_offer.get("meta").get("count"):
        flight_date = FlightData(flight_offer.get("data"))
        flight_schedule: dict = flight_date.find_cheapest_flight()

        if float(flight_schedule.get("price")) < lowest_price:
            content = textwrap.dedent(
                f"""
            departement_iata: {flight_schedule.get("departement_iata")}\n
            arrival_iata: {flight_schedule.get("arrival_iata")}\n
            price: {flight_schedule.get("price")}\n
            out_date: {flight_schedule.get("out_date")}\n
            return_date: {flight_schedule.get("return_date")}\n
            """
            ).strip()
            notification_manager.send_mail(content=content)
