#-----при выводе запросов, надо сделать навзания столбцев и все-----------------

import tkinter as tk
import data_insert
import psycopg2
import functools

def connect_to_database():
    try:
        # Установка соединения с базой данных PostgreSQL
        conn = psycopg2.connect(
            dbname="PyPrac",
            user="postgres",
            password="1",
            host="185.166.197.179",
            port="5432"
        )
        return conn
    except psycopg2.Error as e:
        print("Ошибка при подключении к базе данных:", e)
        return None

def open_table_menu():
    table_menu = tk.Toplevel(root)
    table_menu.title("Меню работы с таблицами")
    table_menu.geometry("400x400")

    # Создание метки с заголовком
    title_label = tk.Label(table_menu, text="Выберите таблицу:")
    title_label.pack(pady=10)

    # Создание кнопок для выбора таблицы
    # Здесь можно добавить кнопки для каждой таблицы в базе данных
    table1_button = tk.Button(table_menu, text="туры", command=lambda: open_table_actions("туры"))
    table1_button.pack(pady=5)

    table2_button = tk.Button(table_menu, text="Страны", command=lambda: open_table_actions("Страны"))
    table2_button.pack(pady=5)

    table3_button = tk.Button(table_menu, text="Клиенты", command=lambda: open_table_actions("Клиенты"))
    table3_button.pack(pady=5)

    table4_button = tk.Button(table_menu, text="Продажи", command=lambda: open_table_actions("Продажи"))
    table4_button.pack(pady=5)

    table2_button = tk.Button(table_menu, text="Виды_туров", command=lambda: open_table_actions("Виды_туров"))
    table2_button.pack(pady=5)

    # Кнопка для возврата в главное меню
    back_button = tk.Button(table_menu, text="Назад", command=table_menu.destroy)
    back_button.pack(pady=10)
def open_table_actions(table_name):
    # Создание нового окна для действий с таблицей
    actions_menu = tk.Toplevel(root)
    actions_menu.title(f"Меню действий с таблицей '{table_name}'")
    actions_menu.geometry("500x480")

    # Здесь можно добавить кнопки для различных действий с таблицей
    insert_button = tk.Button(actions_menu, text="Вставить данные", command=lambda: insert_data(table_name))
    insert_button.pack(pady=5)

    add_column_button = tk.Button(actions_menu, text="Добавить столбец", command=functools.partial(add_column, table_name))
    add_column_button.pack(pady=5)

    drop_column_button = tk.Button(actions_menu, text="Удалить столбец", command=functools.partial(drop_column, table_name))
    drop_column_button.pack(pady=5)

    view_data_button = tk.Button(actions_menu, text="Просмотр данных", command=lambda: view_data(table_name))
    view_data_button.pack(pady=5)

    # Кнопка для возврата к выбору таблицы
    back_button = tk.Button(actions_menu, text="Назад", command=actions_menu.destroy)
    back_button.pack(pady=10)

def insert_data(table_name):
    conn = data_insert.connect_to_database()
    if conn:
        try:
            data_insert.insert_into_table(conn, table_name)
        finally:
            conn.close()
def view_data(table_name):
    conn = data_insert.connect_to_database()
    if conn:
        try:
            data_insert.view_table(conn, table_name)
        finally:
            conn.close()


def add_column(table_name):
    conn = data_insert.connect_to_database()
    if conn:
        try:
            column_name = input("Введите имя нового столбца: ")
            column_type = input("Введите тип нового столбца (например, VARCHAR(255)): ")
            add_column_to_database(conn, table_name, column_name, column_type)
        finally:
            conn.close()
def add_column_to_database(conn, table_name, column_name, column_type):
    try:
        cur = conn.cursor()

        # Выполняем запрос на добавление столбца
        cur.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type};")

        # Применяем изменения
        conn.commit()

        print(f"Столбец '{column_name}' успешно добавлен в таблицу '{table_name}'.")

    except psycopg2.Error as e:
        print("Ошибка при добавлении столбца:", e)

    finally:
        cur.close()
def drop_column(table_name):
    conn = data_insert.connect_to_database()
    if conn:
        try:
            column_name = input("Введите имя столбца, который хотите удалить: ")
            drop_column_from_database(conn, table_name, column_name)
        finally:
            conn.close()
def drop_column_from_database(conn, table_name, column_name):
    try:
        cur = conn.cursor()

        # Выполняем запрос на удаление столбца
        cur.execute(f"ALTER TABLE {table_name} DROP COLUMN {column_name};")

        # Применяем изменения
        conn.commit()

        print(f"Столбец '{column_name}' успешно удален из таблицы '{table_name}'.")

    except psycopg2.Error as e:
        print("Ошибка при удалении столбца:", e)

    finally:
        cur.close()
conn = psycopg2.connect(dbname="PyPrac", user="postgres", password="1", host="185.166.197.179", port="5432")
cur = conn.cursor()
def open_query_menu():
    query_menu = tk.Toplevel(root)
    query_menu.title("Меню работы с запросами")
    query_menu.geometry("500x550")

    # Создание метки с заголовком
    title_label = tk.Label(query_menu, text="Выберите запрос:")
    title_label.pack(pady=10)
    query1_button = tk.Button(query_menu, text="1. Получить список всех доступных туров", command=query1)
    query1_button.pack(pady=5)

    query2_button = tk.Button(query_menu, text="2. Найти все туры в определенное место (например, 'Париж')", command=query2)
    query2_button.pack(pady=5)

    query3_button = tk.Button(query_menu, text="3. Отобразить туры с определенным типом размещения (например люкс, стандарт, стандарт +)", command=query3)
    query3_button.pack(pady=5)

    query4_button = tk.Button(query_menu, text="4. Получить список туров с определенным диапазоном цен", command=query4)
    query4_button.pack(pady=5)

    query5_button = tk.Button(query_menu, text="5. Отобразить туры с датой начала путешествия в определенном месяце", command=query5)
    query5_button.pack(pady=5)

    query6_button = tk.Button(query_menu, text="6. Найти продажи по фамилии клиента", command=query6)
    query6_button.pack(pady=5)

    query7_button = tk.Button(query_menu, text="7. Отобразить туры с продолжительностью больше определенного количества дней", command=query7)
    query7_button.pack(pady=5)

    query8_button = tk.Button(query_menu, text="8. Получить список всех клиентов, купивших тур в определенную страну", command=query8)
    query8_button.pack(pady=5)

    query9_button = tk.Button(query_menu, text="9. Найти все туры, которые купил определенный клиент", command=query9)
    query9_button.pack(pady=5)

    query10_button = tk.Button(query_menu, text="10. Найти все туры, которые еще не были проданы", command=query10)
    query10_button.pack(pady=5)

def print_query_result(rows):
    if not rows:
        print("Нет результатов")
        return

    # Получение максимальной длины каждого столбца
    max_widths = [max(len(str(value)) for value in row) for row in zip(*rows)]

    # Вывод данных с выравниванием
    for row in rows:
        for i, value in enumerate(row):
            print(str(value).ljust(max_widths[i]), end=" | ")
        print()

def execute_query(query, params=None):
    conn = psycopg2.connect(dbname="PyPrac", user="postgres", password="1", host="185.166.197.179", port="5432")
    cur = conn.cursor()
    if params:
        cur.execute(query, params)
    else:
        cur.execute(query)
    rows = cur.fetchall()
    conn.close()
    return rows
# Пример использования
def query1():
    query = "SELECT * FROM туры"
    rows = execute_query(query)

    print_query_result(rows)

def query2():
    query = "SELECT * FROM Страны"
    rows = execute_query(query)

    print_query_result(rows)

def query3():
    accommodation_type = input("Введите тип размещения: ")
    query = """
    SELECT * FROM туры
    JOIN Виды_туров ON туры.id_вида_тура = Виды_туров.Id_вида
    WHERE Виды_туров.Вид_тура = %s
    """
    rows = execute_query(query, (accommodation_type,))
    print_query_result(rows)
def query4():
    min_price = int(input("Введите минимальную цену: "))
    max_price = int(input("Введите максимальную цену: "))
    params = (min_price, max_price)
    query = "SELECT * FROM туры WHERE Цена BETWEEN %s AND %s"
    rows = execute_query(query, params)
    print_query_result(rows)

def query5():
    date = input("Введите дату: ")
    query = "SELECT * FROM туры WHERE Дата_отправления = %s"
    params = (date,)
    rows = execute_query(query, params)
    print_query_result(rows)

def query6():
    sec_name = input("Введите фамилию клиента: ")
    query = "SELECT * FROM Продажи JOIN Клиенты ON Продажи.Id_клиента = Клиенты.Id_клиента WHERE Клиенты.Фамилия = %s"
    params = (sec_name,)
    rows = execute_query(query, params)
    print_query_result(rows)

def query7():
    num_of_dys = input("Введите количество дней: ")
    query =  "SELECT * FROM туры WHERE Количество_дней > %s"
    rows = execute_query(query, (num_of_dys,))
    print_query_result(rows)

def query8():
    country = input("Введите количество дней: ")
    query =  "SELECT DISTINCT Клиенты.* FROM Клиенты JOIN Продажи ON Клиенты.Id_клиента = Продажи.Id_клиента JOIN туры ON Продажи.Id_тура = туры.Id_тура JOIN Страны ON туры.Id_страны = Страны.Id_страны WHERE Страны.Страна = %s "
    rows = execute_query(query, (country,))
    print_query_result(rows)

def query9():
    sec_name = input("Введите фамилию клиента: ")
    query =  "SELECT * FROM туры JOIN Продажи ON туры.Id_тура = Продажи.Id_тура JOIN Клиенты ON Продажи.Id_клиента = Клиенты.Id_клиента WHERE Клиенты.Фамилия = %s"
    rows = execute_query(query, (sec_name,))
    print_query_result(rows)

def query10():
    query = "SELECT * FROM туры WHERE туры.Id_тура NOT IN (SELECT DISTINCT Id_тура FROM Продажи);"
    rows = execute_query(query)

    print_query_result(rows)
# Создание главного окна
root = tk.Tk()
root.title("Программа работы с базой данных")
root.geometry("400x150")

# Создание метки с заголовком
title_label = tk.Label(root, text="Выберите действие:")
title_label.pack(pady=10)

# Создание кнопок для выбора действия
table_button = tk.Button(root, text="Работа с таблицами", command=open_table_menu)
table_button.pack(pady=5)

query_button = tk.Button(root, text="Работа с запросами", command=open_query_menu)
query_button.pack(pady=5)

# Запуск главного цикла обработки событий
root.mainloop()
