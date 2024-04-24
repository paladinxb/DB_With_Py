import psycopg2

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

def insert_into_table(conn, table_name):
    try:
        cur = conn.cursor()
        
        # Получаем названия столбцов в таблице
        cur.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}';")
        columns = [row[0] for row in cur.fetchall()]

        # Собираем значения для вставки
        values = []
        for column in columns:
            value = input(f"Введите значение для столбца '{column}': ")
            values.append(value)

        # Создаем строку запроса SQL для вставки данных
        sql = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(columns))});"

        # Выполняем запрос с введенными данными
        cur.execute(sql, values)
        
        # Применяем изменения
        conn.commit()
        
        print("Данные успешно добавлены в таблицу", table_name)

    except psycopg2.Error as e:
        print("Ошибка при вставке данных в таблицу:", e)

    finally:
        cur.close()

def get_table_columns(conn, table_name):
    try:
        cur = conn.cursor()

        # Получаем названия столбцов в таблице
        cur.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}';")
        columns = [row[0] for row in cur.fetchall()]

        return columns

    except psycopg2.Error as e:
        print("Ошибка при получении информации о столбцах:", e)
        return None

    finally:
        cur.close()

def add_column(conn, table_name, column_name, column_type):
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

def drop_column(conn, table_name, column_name):
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

def view_table(conn, table_name):
    try:
        cur = conn.cursor()

        # Проверяем, является ли введенное имя таблицей или представлением
        cur.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = %s)", (table_name,))
        is_table = cur.fetchone()[0]

        if is_table:
            # Если введенное имя - таблица, выполняем запрос для выборки всех данных из таблицы
            cur.execute(f"SELECT * FROM {table_name};")
        else:
            # Если введенное имя - представление, выполняем запрос для выборки всех данных из представления
            cur.execute(f"SELECT * FROM {table_name};")

        rows = cur.fetchall()

        # Выводим заголовки столбцов
        cur.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}';")
        columns = [row[0] for row in cur.fetchall()]

        # Определяем максимальную длину для каждого столбца (для названий столбцов и данных)
        max_widths = [max(len(str(row[i])) for row in rows + [columns]) for i in range(len(columns))]

        # Выводим заголовки столбцов с выравниванием
        for i, column in enumerate(columns):
            print(column.ljust(max_widths[i]), end=" | ")
        print()

        # Выводим разделительную строку
        for width in max_widths:
            print("-" * width, end=" | ")
        print()

        # Выводим данные с выравниванием
        for row in rows:
            for i in range(len(columns)):
                print(str(row[i]).ljust(max_widths[i]), end=" | ")
            print()

    except psycopg2.Error as e:
        print("Ошибка при просмотре таблицы или представления:", e)

    finally:
        cur.close()

def main():
    conn = connect_to_database()
    if conn:
        try:
            while True:
                choice = input("Введите 'table' для работы с таблицами или 'query' для работы с запросами (или 'exit' для выхода): ")
                if choice.lower() == 'exit':
                    break
                
                elif choice.lower() == 'table':
                    while True:
                        table_name = input("Введите имя таблицы, с которой хотите работать (или 'back' для возврата к выбору режима): ")
                        if table_name.lower() == 'back':
                            break
                        
                        # Получаем текущие столбцы таблицы
                        columns = get_table_columns(conn, table_name)
                        if columns:
                            print("Текущие столбцы в таблице:", columns)
                        else:
                            print("Не удалось получить информацию о столбцах.")
                            continue
                        
                        while True:
                            action = input("Выберите действие (add - добавить столбец, drop - удалить столбец, insert - вставить данные в строку, view - просмотреть данные, back - вернуться к выбору таблицы): ")
                            
                            if action.lower() == 'add':
                                column_name = input("Введите имя нового столбца: ")
                                column_type = input("Введите тип нового столбца (например, VARCHAR(255)): ")
                                add_column(conn, table_name, column_name, column_type)
                            
                            elif action.lower() == 'drop':
                                column_name = input("Введите имя столбца, который хотите удалить: ")
                                drop_column(conn, table_name, column_name)
                            
                            elif action.lower() == 'insert':
                                insert_into_table(conn, table_name)
                            
                            elif action.lower() == 'view':
                                view_table(conn, table_name)
                            
                            elif action.lower() == 'back':
                                break
                            
                            else:
                                print("Некорректное действие. Попробуйте снова.")
                
                elif choice.lower() == 'query':
                    print("В разработке.")
                    # Здесь будет логика работы с запросами
                
                else:
                    print("Некорректный выбор. Попробуйте снова.")
        
        finally:
            conn.close()
            print("Программа завершена.")

if __name__ == "__main__":
    main()
