class HotelSearchService:
    def __init__(self, hotel_repository, review_repository):
        self.hotel_repository = hotel_repository
        self.review_repository = review_repository

    def search_hotels(self, location=None, checkin_date=None, checkout_date=None, price_range=None):
        hotels = self.hotel_repository.search(location=location, price_range=price_range)
        nights = self._calculate_nights(checkin_date, checkout_date)
        hotel_results = []

        for hotel in hotels:
            reviews = self.review_repository.get_by_hotel_id(hotel["id"])
            average = self._calculate_average(reviews)

            hotel_results.append(
                {
                    "id": hotel["id"],
                    "name": hotel["name"],
                    "description": hotel["description"],
                    "location": hotel["location"],
                    "total_price": hotel["nightly_price"] * nights,
                    "image": hotel["image"],
                    "reviews": [
                        {
                            "id": review["id"],
                            "rating": review["rating"],
                            "comment": review["comment"],
                        }
                        for review in reviews
                    ],
                    "review_average": average,
                }
            )

        hotel_results.sort(key=lambda item: item["review_average"], reverse=True)
        return hotel_results

    @staticmethod
    def _calculate_average(reviews):
        if not reviews:
            return 0.0
        return round(sum(review["rating"] for review in reviews) / len(reviews), 2)

    @staticmethod
    def _calculate_nights(checkin_date, checkout_date):
        if not checkin_date or not checkout_date:
            return 1
        return (checkout_date - checkin_date).days
