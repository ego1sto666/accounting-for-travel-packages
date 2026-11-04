-- Схема базы данных системы учета туристических путевок (SQLite)

-- Включаем проверку внешних ключей (в SQLite по умолчанию выключена)
PRAGMA foreign_keys = ON;

-- Удаляем таблицы, если они существовали (в обратном порядке зависимостей)
DROP TABLE IF EXISTS Booking;
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Tour;
DROP TABLE IF EXISTS BookingStatus;
DROP TABLE IF EXISTS UserRole;

-- 1. Справочник ролей пользователей
CREATE TABLE UserRole (
    userRoleID INTEGER PRIMARY KEY AUTOINCREMENT,
    name       TEXT    NOT NULL UNIQUE
);

-- 2. Справочник статусов бронирования
CREATE TABLE BookingStatus (
    statusID INTEGER PRIMARY KEY AUTOINCREMENT,
    name     TEXT    NOT NULL UNIQUE
);

-- 3. Каталог туров
CREATE TABLE Tour (
    tourID        INTEGER PRIMARY KEY AUTOINCREMENT,
    name          TEXT    NOT NULL,
    cost          REAL    NOT NULL CHECK (cost >= 0),
    datetimeStart TEXT    NOT NULL,
    datetimeEnd   TEXT    NOT NULL,
    seats         INTEGER NOT NULL DEFAULT 0 CHECK (seats >= 0),
    isAvailable   INTEGER NOT NULL DEFAULT 1 CHECK (isAvailable IN (0, 1)),
    description   TEXT
);

-- 4. Пользователи (клиенты, менеджеры, администраторы)
CREATE TABLE User (
    userID        INTEGER PRIMARY KEY AUTOINCREMENT,
    login         TEXT    NOT NULL UNIQUE,
    password_hash TEXT    NOT NULL,
    name          TEXT    NOT NULL,
    surname       TEXT    NOT NULL,
    patronymic    TEXT,
    phone         TEXT,
    userRole      INTEGER NOT NULL,
    balance       REAL    NOT NULL DEFAULT 0.0 CHECK (balance >= 0),
    FOREIGN KEY (userRole) REFERENCES UserRole (userRoleID)
);

-- 5. Бронирования (связь пользователей и туров: многие-ко-многим)
CREATE TABLE Booking (
    bookingID       INTEGER PRIMARY KEY AUTOINCREMENT,
    tourID          INTEGER NOT NULL,
    userID          INTEGER NOT NULL,
    statusID        INTEGER NOT NULL DEFAULT 1,
    datetimeBooking TEXT    NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (tourID)   REFERENCES Tour (tourID),
    FOREIGN KEY (userID)   REFERENCES User (userID),
    FOREIGN KEY (statusID) REFERENCES BookingStatus (statusID)
);

-- Тестовые данные

INSERT INTO UserRole (name)
VALUES ('Клиент'),
       ('Менеджер'),
       ('Администратор');

INSERT INTO BookingStatus (name)
VALUES ('Создана'),
       ('Оплачена'),
       ('Подтверждена'),
       ('Отменена');

INSERT INTO Tour (name, cost, datetimeStart, datetimeEnd, seats, isAvailable, description)
VALUES ('Тур по Золотому кольцу', 45000.0, '2026-12-01 09:00', '2026-12-07 20:00', 20, 1,
        'Увлекательное путешествие по древним городам.'),
       ('Отдых в Сочи', 62000.0, '2027-01-10 12:00', '2027-01-20 12:00', 15, 1,
        'Горнолыжный курорт Красная Поляна и море.'),
       ('Байкал зимой', 89000.0, '2027-02-15 08:00', '2027-02-22 18:00', 10, 1,
        'Прогулки по льду Байкала и остров Ольхон.'),
       ('Карелия: озера и водопады', 38000.0, '2026-11-20 07:00', '2026-11-24 22:00', 0, 0,
        'Тур временно недоступен: все места проданы.');

-- Тестовые пароли: client123, client456, manager123, admin123 (хранится SHA-256)
INSERT INTO User (login, password_hash, name, surname, patronymic, phone, userRole, balance)
VALUES ('ivanov', '186474c1f2c2f735a54c2cf82ee8e87f2a5cd30940e280029363fecedfc5328c',
        'Иван', 'Иванов', 'Иванович', '+79001112233', 1, 100000.0),
       ('petrova', 'e56b37a242a602bed629c6087c648f8ac1f1772dc3d51b90bc23fc71aea72f34',
        'Анна', 'Петрова', NULL, '+79004445566', 1, 20000.0),
       ('manager', '866485796cfa8d7c0cf7111640205b83076433547577511d81f8030ae99ecea5',
        'Олег', 'Смирнов', 'Петрович', '+79007778899', 2, 0.0),
       ('admin', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9',
        'Мария', 'Кузнецова', 'Андреевна', '+79000000000', 3, 0.0);

INSERT INTO Booking (tourID, userID, statusID, datetimeBooking)
VALUES (1, 1, 3, '2026-10-20 14:30'),
       (2, 1, 2, '2026-10-25 10:15'),
       (3, 2, 1, '2026-11-01 18:45'),
       (1, 2, 4, '2026-10-18 09:00');
