"""Точка входа: главное меню, вход и переход в меню нужной роли."""

from constants import ROLE_ADMIN, ROLE_CLIENT, ROLE_MANAGER
from database.database import database_exists
from ui.admin_menu import admin_menu
from ui.auth import login, register
from ui.client_menu import client_menu
from ui.common import run_action
from ui.manager_menu import manager_menu

ROLE_MENUS = {
    ROLE_CLIENT: client_menu,
    ROLE_MANAGER: manager_menu,
    ROLE_ADMIN: admin_menu,
}


def main():
    if not database_exists():
        print("База данных не найдена. Сначала выполните: python init_db.py")
        return

    print("Система учета туристических путевок")

    while True:
        print("\n===== Главное меню =====")
        print("1. Вход")
        print("2. Регистрация")
        print("0. Выход из программы")

        choice = input("Выберите действие: ").strip()
        if choice == "1":
            user = login()
            if user:
                ROLE_MENUS[user.user_role](user)
        elif choice == "2":
            run_action(register)
        elif choice == "0":
            print("До свидания!")
            break
        else:
            print("Нет такого пункта")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nПрограмма завершена")
