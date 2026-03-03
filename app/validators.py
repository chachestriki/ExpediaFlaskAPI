from datetime import datetime


class ValidationError(Exception):
    pass


def validate_search_params(args):
    location = args.get("location")
    checkin_raw = args.get("checkin_date")
    checkout_raw = args.get("checkout_date")
    price_range_raw = args.get("price_range")

    checkin_date = _parse_date("checkin_date", checkin_raw) if checkin_raw else None
    checkout_date = _parse_date("checkout_date", checkout_raw) if checkout_raw else None

    if checkin_date and checkout_date and checkout_date <= checkin_date:
        raise ValidationError("checkout_date must be after checkin_date")

    price_range = _parse_price_range(price_range_raw) if price_range_raw else None

    return {
        "location": location,
        "checkin_date": checkin_date,
        "checkout_date": checkout_date,
        "price_range": price_range,
    }


def _parse_date(field_name, date_value):
    try:
        return datetime.strptime(date_value, "%Y-%m-%d").date()
    except ValueError as exc:
        raise ValidationError(f"{field_name} must use YYYY-MM-DD format") from exc


def _parse_price_range(raw_value):
    # Format is "min,max" so clients can send it as query string.
    parts = [part.strip() for part in raw_value.split(",")]
    if len(parts) != 2:
        raise ValidationError("price_range must be in format min,max")

    try:
        min_price = int(parts[0])
        max_price = int(parts[1])
    except ValueError as exc:
        raise ValidationError("price_range values must be integers") from exc

    if min_price < 0 or max_price < 0:
        raise ValidationError("price_range values must be non-negative")

    if min_price > max_price:
        raise ValidationError("price_range minimum must be less than or equal to maximum")

    return [min_price, max_price]
