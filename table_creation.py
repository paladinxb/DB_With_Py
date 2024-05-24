import psycopg2
def create_tables():
    # Подключение к базе данных
    conn = psycopg2.connect(
        dbname="your db name",
        user="your user name",
        password="your password",
        host="localhost or IP of server",
        port="5432"
    )
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Виды_туров (
        Id_вида SERIAL PRIMARY KEY,
        Вид_тура VARCHAR(255)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Страны (
        Id_страны SERIAL PRIMARY KEY,
        Страна VARCHAR(255)
    )
    ''')
    # Создание таблицы "туры"
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS туры (
        Id_тура SERIAL PRIMARY KEY,
        Цена DECIMAL(10, 2),
        Дата_отправления DATE,
        Количество_дней INTEGER,
        Количество_людей INTEGER,
        Id_страны INTEGER REFERENCES Страны(Id_страны),
        id_вида_тура INTEGER REFERENCES Виды_туров(Id_вида)
    )
    ''')


    # Создание таблицы "Клиенты"
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Клиенты (
        Id_клиента SERIAL PRIMARY KEY,
        Фамилия VARCHAR(255),
        Телефон VARCHAR(20)
    )
    ''')

    # Создание таблицы "Продажи"
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Продажи (
        Id_продажи SERIAL PRIMARY KEY,
        Дата DATE,
        Количество INTEGER,
        Id_клиента INTEGER REFERENCES Клиенты(Id_клиента),
        Id_тура INTEGER REFERENCES туры(Id_тура)
    )
    ''')

    cursor.execute('''
    CREATE VIEW tour_client_info AS
        SELECT
            туры.Id_тура,
            Клиенты.Фамилия AS Фамилия_клиента,
            туры.Цена,
            Страны.Страна
        FROM
            туры
        JOIN
            Продажи ON туры.Id_тура = Продажи.Id_тура
        JOIN
            Клиенты ON Продажи.Id_клиента = Клиенты.Id_клиента
        JOIN
            Страны ON туры.Id_страны = Страны.Id_страны;
    '''
    )
    # Сохранение изменений и закрытие соединения
    conn.commit()
    conn.close()

# Вызов функции для создания таблиц
create_tables()
