import tkinter as tk
import data_insert
import psycopg2
import functools
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
def open_query_menu():
    pass
    # Добавить здесь код для открытия меню работы с запросами

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
