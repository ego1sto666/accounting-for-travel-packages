"""Общие функции интерфейса: ввод данных и вывод таблиц."""

from models.booking import Booking
from models.tour import Tour
from models.user import User


# ---------- Ввод ----------

def read_text(prompt: str) -> str:
    return input(prompt).strip()


def read_optional(prompt: str) -> str | None:
    """Необязательное поле: пустой ввод превращается в None."""
    value = input(prompt).strip()
    return value or None


def read_int(prompt: str) -> int:
    value = input(prompt).strip()
    if not value.isdigit():
        raise ValueError("Нужно ввести целое неотрицательное число")
    return int(value)


def to_float(text: str) -> float:
    """Число из строки: допускаются пробелы (45 000) и запятая (99,5)."""
    value = text.replace(" ", "").replace(",", ".")
    try:
        return float(value)
    except ValueError:
        raise ValueError("Нужно ввести число") from None


def read_float(prompt: str) -> float:
    return to_float(input(prompt))


def read_with_default(prompt: str, current) -> str:
    """Ввод при редактировании: Enter оставляет текущее значение."""
    value = input(f"{prompt} [{current}]: ").strip()
    return value if value else str(current)


# ---------- Вывод ----------

def money(value: float) -> str:
    return f"{value:,.0f}".replace(",", " ") + " руб."


def print_tours(tours: list[Tour], show_status: bool = False):
    if not tours:
        print("Туров нет")
        return
    for t in tours:
        line = (f"[{t.tour_id}] {t.name} — {money(t.cost)}, "
                f"{t.datetime_start} – {t.datetime_end}, "
                f"свободно мест: {t.free_seats} из {t.seats}")
        if show_status:
            line += ", " + ("доступен" if t.is_available else "скрыт")
        print(line)
        if t.description:
            print(f"     {t.description}")


def print_bookings(bookings: list[Booking], show_client: bool = False):
    if not bookings:
        print("Броней нет")
        return
    for b in bookings:
        line = (f"[{b.booking_id}] {b.tour_name} — {money(b.tour_cost)}, "
                f"от {b.datetime_booking}, статус: {b.status_name}")
        if show_client:
            line += f", клиент: {b.user_login}"
        print(line)


def print_users(users: list[User]):
    for u in users:
        phone = u.phone or "—"
        print(f"[{u.user_id}] {u.login} — {u.full_name}, {u.role_name}, "
              f"тел. {phone}, баланс {money(u.balance)}")


def run_action(action):
    """Выполняет действие и показывает ошибку сервиса, если она возникла."""
    try:
        action()
    except ValueError as error:
        print(f"Ошибка: {error}")
