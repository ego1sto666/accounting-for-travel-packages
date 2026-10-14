-- Удаляем таблицы, если они существовали (в обратном порядке зависимостей)
DROP TABLE IF EXISTS Booking;
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Tour;
DROP TABLE IF EXISTS UserRole;

-- 1. Справочная таблица ролей пользователей
CREATE TABLE UserRole (
    userRoleID INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

-- 2. Таблица туров
CREATE TABLE Tour (
    TourID INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    cost REAL NOT NULL,
    datetimeStart TEXT,
    datetimeend TEXT,
    isAvalible INTEGER,
    description TEXT
);

-- 3. Таблица пользователей
CREATE TABLE User (
    userID INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    surname TEXT NOT NULL,
    patronymic TEXT,
    password_hash TEXT NOT NULL,
    userRole INTEGER NOT NULL,
    balance REAL DEFAULT 0.0,
    FOREIGN KEY (userRole) REFERENCES UserRole(userRoleID)
);

-- 4. Таблица бронирования (связь между пользователем и туром)
CREATE TABLE Booking (
    BookingID INTEGER PRIMARY KEY AUTOINCREMENT,
    TourID INTEGER NOT NULL,
    UserID INTEGER NOT NULL,
    statusPayment INTEGER,
    datatimestart TEXT,
    FOREIGN KEY (TourID) REFERENCES Tour(TourID),
    FOREIGN KEY (UserID) REFERENCES User(userID)
);

-- Заполнение начальными данными (тестовые записи)
INSERT INTO UserRole (name) VALUES ('Клиент'), ('Менеджер'), ('Администратор');

INSERT INTO Tour (name, cost, isAvalible, description) 
VALUES ('Тур по Золотому кольцу', 45000.0, 1, 'Увлекательное путешествие по древним городам.');

INSERT INTO User (name, surname, password_hash, userRole, balance) 
VALUES ('Иван', 'Иванов', 'hash12345', 1, 10000.0);