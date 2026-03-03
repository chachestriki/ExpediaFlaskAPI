from app.data.reviews_data import REVIEWS


class ReviewRepository:
    def get_by_hotel_id(self, hotel_id):
        return [review for review in REVIEWS if review["hotel_id"] == hotel_id]
