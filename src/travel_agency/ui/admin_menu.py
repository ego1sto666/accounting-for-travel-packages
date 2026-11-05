"""Меню администратора: управление турами и пользователями."""

from getpass import getpass

from models.user import User
from services import tour_service, user_service
from ui.common import (print_tours, print_users, read_float, read_int,
                       read_optional, read_text, read_with_default, run_action,
                       to_float)


def admin_menu(user: User):
    while True:
        print(f"\n===== Администратор: {user.full_name} =====")
        print("1. Управление турами")
        print("2. Управление пользователями")
        print("0. Выйти из аккаунта")

        choice = input("Выберите действие: ").strip()
        if choice == "1":
            tours_menu(user)
        elif choice == "2":
            users_menu(user)
        elif choice == "0":
            break
        else:
            print("Нет такого пункта")


# ---------- Туры ----------

def tours_menu(admin: User):
    while True:
        print("\n----- Управление турами -----")
        print("1. Список туров")
        print("2. Добавить тур")
        print("3. Изменить тур")
        print("4. Удалить тур")
        print("0. Назад")

        choice = input("Выберите действие: ").strip()
        if choice == "1":
            run_action(lambda: show_tours(admin))
        elif choice == "2":
            run_action(lambda: add_tour(admin))
        elif choice == "3":
            run_action(lambda: edit_tour(admin))
        elif choice == "4":
            run_action(lambda: delete_tour(admin))
        elif choice == "0":
            break
        else:
            print("Нет такого пункта")


def show_tours(admin: User):
    print_tours(tour_service.get_all_tours(admin), show_status=True)


def add_tour(admin: User):
    print("Дату можно ввести как 2027-03-01 10:00 или 01.03.2027 10:00 "
          "(время можно не писать)")
    name = read_text("Название: ")
    cost = read_float("Стоимость: ")
    start = read_text("Дата начала: ")
    end = read_text("Дата окончания: ")
    seats = read_int("Количество мест: ")
    description = read_optional("Описание (можно пропустить): ")

    tour_id = tour_service.create_tour(admin, name, cost, start, end,
                                       seats, description)
    print(f"Тур №{tour_id} добавлен")


def edit_tour(admin: User):
    show_tours(admin)
    tour = tour_service.get_tour(read_int("Номер тура: "))
    print("Enter — оставить текущее значение")

    name = read_with_default("Название", tour.name)
    cost = to_float(read_with_default("Стоимость", f"{tour.cost:g}"))
    start = read_with_default("Дата начала", tour.datetime_start)
    end = read_with_default("Дата окончания", tour.datetime_end)
    seats_text = read_with_default("Количество мест", tour.seats)
    if not seats_text.isdigit():
        raise ValueError("Количество мест должно быть целым числом")
    available = read_with_default("Доступен для бронирования (1 — да, 0 — нет)",
                                  tour.is_available)
    if available not in ("0", "1"):
        raise ValueError("Введите 1 или 0")
    description = read_with_default("Описание", tour.description or "")

    tour_service.update_tour(admin, tour.tour_id, name, cost, start, end,
                             int(seats_text), int(available), description)
    print("Тур изменен")


def delete_tour(admin: User):
    show_tours(admin)
    tour_id = read_int("Номер тура для удаления: ")
    tour_service.delete_tour(admin, tour_id)
    print("Тур удален")


# ---------- Пользователи ----------

def users_menu(admin: User):
    while True:
        print("\n----- Управление пользователями -----")
        print("1. Список пользователей")
        print("2. Добавить пользователя (сотрудника)")
        print("3. Изменить роль")
        print("4. Удалить пользователя")
        print("0. Назад")

        choice = input("Выберите действие: ").strip()
        if choice == "1":
            run_action(lambda: print_users(user_service.get_all_users(admin)))
        elif choice == "2":
            run_action(lambda: add_user(admin))
        elif choice == "3":
            run_action(lambda: change_role(admin))
        elif choice == "4":
            run_action(lambda: delete_user(admin))
        elif choice == "0":
            break
        else:
            print("Нет такого пункта")


def choose_role() -> int:
    for role in user_service.get_roles():
        print(f"  {role.user_role_id}. {role.name}")
    return read_int("Номер роли: ")


def add_user(admin: User):
    login_value = read_text("Логин: ")
    password_value = getpass("Пароль: ")
    name = read_text("Имя: ")
    surname = read_text("Фамилия: ")
    patronymic = read_optional("Отчество (можно пропустить): ")
    phone = read_optional("Телефон (можно пропустить): ")
    role_id = choose_role()

    user_id = user_service.add_user(admin, login_value, password_value, name,
                                    surname, patronymic, phone, role_id)
    print(f"Пользователь №{user_id} добавлен")


def change_role(admin: User):
    print_users(user_service.get_all_users(admin))
    user_id = read_int("Номер пользователя: ")
    role_id = choose_role()
    user_service.change_role(admin, user_id, role_id)
    print("Роль изменена")


def delete_user(admin: User):
    print_users(user_service.get_all_users(admin))
    user_id = read_int("Номер пользователя для удаления: ")
    user_service.delete_user(admin, user_id)
    print("Пользователь удален")
