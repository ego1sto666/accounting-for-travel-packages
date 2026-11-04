"""Бизнес-логика бронирования: бронь, оплата, подтверждение, отмена."""

from constants import (ROLE_ADMIN, ROLE_CLIENT, ROLE_MANAGER, STATUS_CANCELLED,
                       STATUS_CONFIRMED, STATUS_CREATED, STATUS_PAID)
from models.booking import Booking
from models.user import User
from repositories import booking_repository, user_repository
from services import tour_service
from services.user_service import check_role, get_user


def _get_booking(booking_id: int) -> Booking:
    booking = booking_repository.get_by_id(booking_id)
    if not booking:
        raise ValueError("Бронь не найдена")
    return booking


def _get_own_booking(client: User, booking_id: int) -> Booking:
    booking = _get_booking(booking_id)
    if booking.user_id != client.user_id:
        # Не сообщаем, что чужая бронь существует
        raise ValueError("Бронь не найдена")
    return booking


# ---------- Клиент ----------

def create_booking(client: User, tour_id: int) -> int:
    check_role(client, ROLE_CLIENT)

    tour = tour_service.get_tour(tour_id)
    if tour.is_available != 1:
        raise ValueError("Тур недоступен для бронирования")
    if tour_service.has_started(tour):
        raise ValueError("Тур уже начался")
    if tour.free_seats <= 0:
        raise ValueError("Мест нет")

    for b in booking_repository.get_by_user(client.user_id):
        if b.tour_id == tour_id and b.status_id != STATUS_CANCELLED:
            raise ValueError("Вы уже забронировали этот тур")

    return booking_repository.create(tour_id, client.user_id)


def pay_booking(client: User, booking_id: int) -> float:
    """Оплата с баланса. Возвращает новый баланс."""
    check_role(client, ROLE_CLIENT)
    booking = _get_own_booking(client, booking_id)

    if booking.status_id != STATUS_CREATED:
        raise ValueError(f"Оплатить нельзя: бронь «{booking.status_name}»")

    fresh = get_user(client.user_id)
    if fresh.balance < booking.tour_cost:
        raise ValueError(
            f"Оплата не прошла: недостаточно средств "
            f"(нужно {booking.tour_cost:.0f}, на балансе {fresh.balance:.0f})"
        )

    new_balance = fresh.balance - booking.tour_cost
    user_repository.update_balance(client.user_id, new_balance)
    booking_repository.update_status(booking_id, STATUS_PAID)
    return new_balance


def get_my_bookings(client: User) -> list[Booking]:
    return booking_repository.get_by_user(client.user_id)


# ---------- Отмена (клиент или сотрудник) ----------

def cancel_booking(user: User, booking_id: int):
    """Отмена — логическое удаление: бронь остается в истории со статусом
    «Отменена». Если бронь была оплачена, деньги возвращаются клиенту."""
    if user.user_role == ROLE_CLIENT:
        booking = _get_own_booking(user, booking_id)
    else:
        check_role(user, ROLE_MANAGER, ROLE_ADMIN)
        booking = _get_booking(booking_id)

    if booking.status_id not in (STATUS_CREATED, STATUS_PAID):
        raise ValueError(f"Отменить нельзя: бронь «{booking.status_name}»")

    if booking.status_id == STATUS_PAID:
        owner = get_user(booking.user_id)
        user_repository.update_balance(owner.user_id,
                                       owner.balance + booking.tour_cost)

    booking_repository.update_status(booking_id, STATUS_CANCELLED)


# ---------- Менеджер ----------

def get_all_bookings(employee: User) -> list[Booking]:
    check_role(employee, ROLE_MANAGER, ROLE_ADMIN)
    return booking_repository.get_all()


def confirm_booking(manager: User, booking_id: int):
    """Подтверждение брони менеджером = оформление продажи."""
    check_role(manager, ROLE_MANAGER)
    booking = _get_booking(booking_id)
    if booking.status_id != STATUS_PAID:
        raise ValueError("Подтвердить можно только оплаченную бронь")
    booking_repository.update_status(booking_id, STATUS_CONFIRMED)
