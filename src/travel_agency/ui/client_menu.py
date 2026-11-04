"""Меню клиента."""

from models.user import User
from services import booking_service, tour_service, user_service
from ui.common import money, print_bookings, print_tours, read_float, read_int, run_action


def client_menu(user: User):
    while True:
        user = user_service.get_user(user.user_id)  # свежий баланс
        print(f"\n===== Клиент: {user.full_name} | баланс {money(user.balance)} =====")
        print("1. Каталог туров")
        print("2. Забронировать тур")
        print("3. Мои брони")
        print("4. Оплатить бронь")
        print("5. Отменить бронь")
        print("6. Пополнить баланс")
        print("0. Выйти из аккаунта")

        choice = input("Выберите действие: ").strip()
        if choice == "1":
            run_action(show_catalog)
        elif choice == "2":
            run_action(lambda: book_tour(user))
        elif choice == "3":
            run_action(lambda: print_bookings(booking_service.get_my_bookings(user)))
        elif choice == "4":
            run_action(lambda: pay(user))
        elif choice == "5":
            run_action(lambda: cancel(user))
        elif choice == "6":
            run_action(lambda: top_up(user))
        elif choice == "0":
            break
        else:
            print("Нет такого пункта")


def show_catalog():
    print("\n--- Каталог туров ---")
    print_tours(tour_service.get_catalog())


def book_tour(user: User):
    show_catalog()
    tour_id = read_int("Номер тура: ")
    booking_id = booking_service.create_booking(user, tour_id)
    print(f"Бронь №{booking_id} создана. Оплатите ее в пункте «Оплатить бронь».")


def pay(user: User):
    print_bookings(booking_service.get_my_bookings(user))
    booking_id = read_int("Номер брони для оплаты: ")
    new_balance = booking_service.pay_booking(user, booking_id)
    print(f"Оплата прошла. Остаток на балансе: {money(new_balance)}")


def cancel(user: User):
    print_bookings(booking_service.get_my_bookings(user))
    booking_id = read_int("Номер брони для отмены: ")
    booking_service.cancel_booking(user, booking_id)
    print("Бронь отменена. Если она была оплачена, деньги вернулись на баланс.")


def top_up(user: User):
    amount = read_float("Сумма пополнения: ")
    new_balance = user_service.top_up_balance(user, amount)
    print(f"Баланс пополнен: {money(new_balance)}")
