from datetime import datetime, timedelta


def generate_date_range(check_in, check_out):

    start_date = datetime.strptime(check_in, "%Y-%m-%d")
    end_date = datetime.strptime(check_out, "%Y-%m-%d")

    dates = []

    while start_date < end_date:
        dates.append(start_date.strftime("%Y-%m-%d"))
        start_date += timedelta(days=1)

    return dates


def check_availability(hotels, check_in, check_out, max_budget):

    required_dates = generate_date_range(check_in, check_out)

    filtered_hotels = []

    for hotel in hotels:

        price = hotel.get(
            "price",
            99999
        )

        if price > max_budget:
            continue
        hotel_dates = hotel.get("available_dates", [])

        is_available = all(
            date in hotel_dates
            for date in required_dates
        )

        if is_available:
            filtered_hotels.append(hotel)

    filtered_hotels.sort(
        key=lambda hotel: hotel["rating"],
        reverse=True
    )

    return filtered_hotels