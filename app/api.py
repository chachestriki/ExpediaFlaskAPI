from flask import Flask, jsonify, request

from app.repositories.hotel_repository import HotelRepository
from app.repositories.review_repository import ReviewRepository
from app.services.hotel_search_service import HotelSearchService
from app.validators import ValidationError, validate_search_params


def create_app():
    flask_app = Flask(__name__)

    hotel_repository = HotelRepository()
    review_repository = ReviewRepository()
    hotel_search_service = HotelSearchService(hotel_repository, review_repository)

    @flask_app.get("/api/hotels/search")
    def search_hotels():
        try:
            params = validate_search_params(request.args)
        except ValidationError as error:
            return jsonify({"error": str(error)}), 400

        hotels = hotel_search_service.search_hotels(
            location=params["location"],
            checkin_date=params["checkin_date"],
            checkout_date=params["checkout_date"],
            price_range=params["price_range"],
        )
        return jsonify({"hotels": hotels})

    return flask_app


app = create_app()
