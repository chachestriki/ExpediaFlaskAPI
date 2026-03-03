from app.data.hotels_data import HOTELS


class HotelRepository:
    def search(self, location=None, price_range=None):
        results = HOTELS

        if location:
            location_lower = location.strip().lower()
            results = [
                hotel
                for hotel in results
                if hotel["location"]["name"].lower() == location_lower
            ]

        if price_range:
            min_price, max_price = price_range
            results = [
                hotel
                for hotel in results
                if min_price <= hotel["nightly_price"] <= max_price
            ]

        return results
