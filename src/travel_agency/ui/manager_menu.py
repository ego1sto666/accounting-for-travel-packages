"""Меню менеджера."""

from models.user import User
from services import booking_service
from ui.common import print_bookings, read_int, run_action


def manager_menu(user: User):
    while True:
        print(f"\n===== Менеджер: {user.full_name} =====")
        print("1. Список всех броней")
        print("2. Подтвердить бронь (оформить продажу)")
        print("3. Отменить бронь")
        print("0. Выйти из аккаунта")

        choice = input("Выберите действие: ").strip()
        if choice == "1":
            run_action(lambda: show_all(user))
        elif choice == "2":
            run_action(lambda: confirm(user))
        elif choice == "3":
            run_action(lambda: cancel(user))
        elif choice == "0":
            break
        else:
            print("Нет такого пункта")


def show_all(user: User):
    print("\n--- Все брони ---")
    print_bookings(booking_service.get_all_bookings(user), show_client=True)


def confirm(user: User):
    show_all(user)
    booking_id = read_int("Номер оплаченной брони: ")
    booking_service.confirm_booking(user, booking_id)
    print("Бронь подтверждена, продажа оформлена.")


def cancel(user: User):
    show_all(user)
    booking_id = read_int("Номер брони для отмены: ")
    booking_service.cancel_booking(user, booking_id)
    print("Бронь отменена. Если она была оплачена, деньги вернулись клиенту.")
