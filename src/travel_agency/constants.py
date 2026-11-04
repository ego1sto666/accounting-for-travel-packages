"""Идентификаторы ролей и статусов из справочников UserRole и BookingStatus."""

# Роли пользователей (таблица UserRole)
ROLE_CLIENT = 1
ROLE_MANAGER = 2
ROLE_ADMIN = 3

# Статусы бронирования (таблица BookingStatus)
STATUS_CREATED = 1
STATUS_PAID = 2
STATUS_CONFIRMED = 3
STATUS_CANCELLED = 4

# Формат даты и времени, в котором даты хранятся в базе
DATETIME_FORMAT = "%Y-%m-%d %H:%M"
