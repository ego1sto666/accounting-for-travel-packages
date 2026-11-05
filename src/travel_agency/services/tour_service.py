"""Бизнес-логика туров: каталог, свободные места, управление турами."""

from datetime import datetime

from constants import DATETIME_FORMAT, ROLE_ADMIN
from models.tour import Tour
from models.user import User
from repositories import booking_repository, tour_repository
from services.user_service import check_role


# Форматы, в которых можно ввести дату. Без времени считается 00:00.
INPUT_FORMATS = (DATETIME_FORMAT, "%Y-%m-%d", "%d.%m.%Y %H:%M", "%d.%m.%Y")


def _parse_datetime(text: str, field: str) -> datetime:
    for fmt in INPUT_FORMATS:
        try:
            return datetime.strptime(text.strip(), fmt)
        except ValueError:
            pass
    raise ValueError(
        f"{field}: введите дату как 2027-03-01 10:00 или 01.03.2027 10:00"
    )


def _validate(name: str, cost: float, start: str, end: str,
              seats: int) -> tuple[str, str]:
    """Проверяет данные тура и возвращает даты в едином формате."""
    if not name.strip():
        raise ValueError("Название тура не может быть пустым")
    if cost < 0:
        raise ValueError("Стоимость не может быть отрицательной")
    if seats < 0:
        raise ValueError("Количество мест не может быть отрицательным")
    start_dt = _parse_datetime(start, "Дата начала")
    end_dt = _parse_datetime(end, "Дата окончания")
    if end_dt <= start_dt:
        raise ValueError("Дата окончания должна быть позже даты начала")
    return start_dt.strftime(DATETIME_FORMAT), end_dt.strftime(DATETIME_FORMAT)


def _with_free_seats(tour: Tour) -> Tour:
    """Заполняет служебное поле free_seats: места минус активные брони."""
    taken = booking_repository.count_active_by_tour(tour.tour_id)
    tour.free_seats = max(tour.seats - taken, 0)
    return tour


def has_started(tour: Tour) -> bool:
    start = datetime.strptime(tour.datetime_start, DATETIME_FORMAT)
    return start <= datetime.now()


def get_tour(tour_id: int) -> Tour:
    tour = tour_repository.get_by_id(tour_id)
    if not tour:
        raise ValueError("Тур не найден")
    return _with_free_seats(tour)


def get_catalog() -> list[Tour]:
    """Каталог для клиента: только доступные и еще не начавшиеся туры."""
    tours = tour_repository.get_available()
    return [_with_free_seats(t) for t in tours if not has_started(t)]


def is_tour_available(tour_id: int) -> bool:
    tour = get_tour(tour_id)
    return (
        tour.is_available == 1
        and not has_started(tour)
        and tour.free_seats > 0
    )


# ---------- Функции администратора ----------

def get_all_tours(admin: User) -> list[Tour]:
    check_role(admin, ROLE_ADMIN)
    return [_with_free_seats(t) for t in tour_repository.get_all()]


def create_tour(admin: User, name: str, cost: float, start: str, end: str,
                seats: int, description: str | None) -> int:
    check_role(admin, ROLE_ADMIN)
    start, end = _validate(name, cost, start, end, seats)
    return tour_repository.create(
        name.strip(), cost, start, end,
        seats, 1, description or None,
    )


def update_tour(admin: User, tour_id: int, name: str, cost: float,
                start: str, end: str, seats: int, is_available: int,
                description: str | None):
    check_role(admin, ROLE_ADMIN)
    get_tour(tour_id)
    start, end = _validate(name, cost, start, end, seats)

    taken = booking_repository.count_active_by_tour(tour_id)
    if seats < taken:
        raise ValueError(
            f"Мест не может быть меньше уже занятых (занято: {taken})"
        )

    tour_repository.update(
        tour_id, name.strip(), cost, start, end,
        seats, 1 if is_available else 0, description or None,
    )


def delete_tour(admin: User, tour_id: int):
    check_role(admin, ROLE_ADMIN)
    get_tour(tour_id)
    if booking_repository.count_by_tour(tour_id) > 0:
        raise ValueError(
            "На тур есть брони, удалить нельзя. Сделайте его недоступным"
        )
    tour_repository.delete(tour_id)
