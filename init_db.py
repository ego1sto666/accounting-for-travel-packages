import sqlite3
import os


DB_NAME = "database.db"
SCHEMA_FILE = "schema.sql"

def init_database():
   
    if not os.path.exists(SCHEMA_FILE):
        print(f"Ошибка: файл {SCHEMA_FILE} не найден в корне проекта!")
        return

   
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    print(f"Успешное подключение к базе данных: {DB_NAME}")

    
    with open(SCHEMA_FILE, "r", encoding="utf-8") as f:
        sql_script = f.read()

   
    cursor.executescript(sql_script)
    
   
    conn.commit()
    conn.close()
    print("База данных успешно создана и заполнена тестовыми данными из schema.sql!")

if __name__ == "__main__":
    init_database()