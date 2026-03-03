# Hotel Review Search API (Flask)

Simple backend API for hotel search and sorting by review average.

## Requirements

- Python 3.10+
- pip

## Setup

```bash
pip install -r requirements.txt
```

## Run

```bash
python app.py
```

Server URL:

```text
http://127.0.0.1:5000
```

API endpoint:

```text
GET /api/hotels/search
```

Query params:

- `location` (string)
- `checkin_date` (YYYY-MM-DD)
- `checkout_date` (YYYY-MM-DD)
- `price_range` (format: `min,max`, example: `50,150`)

Example:

```text
/api/hotels/search?location=Barcelona&checkin_date=2026-05-10&checkout_date=2026-05-12&price_range=50,150
```

## Request Flow

1. Client calls `GET /api/hotels/search` with query params.
2. Route in `app/api.py` receives the request.
3. `app/validators.py` validates params (dates and price range format/rules).
4. `HotelSearchService` in `app/services/hotel_search_service.py` runs business logic.
5. `HotelRepository` filters hotels from in-memory datasource (`app/data/hotels_data.py`).
6. `ReviewRepository` fetches reviews for each hotel from `app/data/reviews_data.py`.
7. Service calculates:
   - `review_average` per hotel
   - `total_price` from nightly price and number of nights
8. Hotels are sorted by `review_average` (highest first).
9. API returns JSON response.

## Response shape

Each hotel contains:

- `id`
- `name`
- `description`
- `location` (`id`, `name`)
- `total_price`
- `image`
- `reviews` (`id`, `rating`, `comment`)
- `review_average` (used for sorting)

Hotels are sorted by `review_average` descending.

## Tests

```bash
python -m pytest -q
```

Run a single file:

```bash
python -m pytest tests/test_hotel_search_api.py -q
```

## Design notes

- Data is stored in memory (`app/data/*`).
- Repositories (`app/repositories/*`) isolate data access.
- Service (`app/services/hotel_search_service.py`) handles business logic.
- Request validation is centralized in `app/validators.py`.
- The route layer (`app.py`) stays thin.
