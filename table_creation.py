import psycopg2

# Установка соединения с базой данных PostgreSQL
conn = psycopg2.connect(
    dbname="IlyaPrac",
    user="postgres",
    password="1",
    host="185.166.197.179",
    port="5432"
)
cur = conn.cursor()


cur.execute("""
CREATE TABLE IF NOT EXISTS Место_размещения (
    Номер_Места INT PRIMARY KEY,
    Тип_места VARCHAR(255)
);
""")
# Создание таблицы "Путевки"
cur.execute("""
CREATE TABLE IF NOT EXISTS Путевки (
    Номер_путевки SERIAL PRIMARY KEY,
    Фамилия_клиента VARCHAR(255),
    Дата_оформления DATE,
    Стоимость_путевки INT,
    Дата_начала DATE,
    Дата_окончания DATE,
    Тип_путевки VARCHAR(255),
    Статус_оплаты VARCHAR(255),
    Номер_места int,
    FOREIGN KEY (Номер_места) REFERENCES Место_размещения (Номер_Места)
                     
);
""")


# Создание таблицы "Дополнительные_услуги"
cur.execute("""
CREATE TABLE IF NOT EXISTS Дополнительные_услуги (
    Номер_путевки INT,
    Дополнительные_услуги TEXT,
    FOREIGN KEY (Номер_путевки) REFERENCES Путевки (Номер_путевки)
);
""")
cur.execute("""
CREATE TABLE IF NOT EXISTS Клиенты (
    Фамилия_клиента char(255),
    Номер_путевки Int,
    FOREIGN KEY (Номер_путевки) REFERENCES Путевки (Номер_путевки)
);
""")


# Применение изменений
conn.commit()

# Закрытие курсора и соединения
cur.close()
conn.close()

# Вывод сообщения об успешном создании таблиц
print("Таблицы успешно созданы.")