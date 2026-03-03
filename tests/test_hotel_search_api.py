import pytest

from app import create_app


@pytest.fixture()
def client():
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()


def test_search_returns_hotels_sorted_by_review_average(client):
    response = client.get("/api/hotels/search?location=Barcelona")

    assert response.status_code == 200
    data = response.get_json()
    assert len(data["hotels"]) == 3
    assert data["hotels"][0]["id"] == "h3"
    assert data["hotels"][0]["review_average"] == 5.0
    assert data["hotels"][1]["id"] == "h1"
    assert data["hotels"][1]["review_average"] == 4.5


def test_search_filters_by_price_range(client):
    response = client.get("/api/hotels/search?location=Barcelona&price_range=90,130")

    assert response.status_code == 200
    data = response.get_json()
    assert len(data["hotels"]) == 2
    print(data)
    assert data["hotels"][0]["id"] == "h1"


def test_search_calculates_total_price_from_dates(client):
    response = client.get(
        "/api/hotels/search?location=Barcelona&checkin_date=2026-05-10&checkout_date=2026-05-13"
    )

    assert response.status_code == 200
    data = response.get_json()
    # h3 is first due to rating and has nightly price 80, for 3 nights.
    assert data["hotels"][0]["total_price"] == 240


def test_search_rejects_invalid_date_format(client):
    response = client.get("/api/hotels/search?checkin_date=10-05-2026")

    assert response.status_code == 400
    data = response.get_json()
    assert "YYYY-MM-DD" in data["error"]


def test_search_rejects_checkout_before_checkin(client):
    response = client.get(
        "/api/hotels/search?checkin_date=2026-05-10&checkout_date=2026-05-09"
    )

    assert response.status_code == 400
    data = response.get_json()
    assert "after checkin_date" in data["error"]


def test_search_rejects_invalid_price_range(client):
    response = client.get("/api/hotels/search?price_range=cheap,expensive")

    assert response.status_code == 400
    data = response.get_json()
    assert "integers" in data["error"]
