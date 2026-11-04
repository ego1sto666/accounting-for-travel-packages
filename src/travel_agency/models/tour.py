from dataclasses import dataclass


@dataclass
class Tour:
    tour_id: int
    name: str
    cost: float
    datetime_start: str
    datetime_end: str
    seats: int
    is_available: int
    description: str | None
    # Служебное поле: сколько мест осталось (считается в сервисе по броням)
    free_seats: int | None = None
