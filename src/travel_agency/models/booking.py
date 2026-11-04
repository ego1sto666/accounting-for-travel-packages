from dataclasses import dataclass


@dataclass
class Booking:
    booking_id: int
    tour_id: int
    user_id: int
    status_id: int
    datetime_booking: str
    # Служебные поля: берутся из связанных таблиц через JOIN
    status_name: str | None = None
    tour_name: str | None = None
    tour_cost: float | None = None
    user_login: str | None = None
