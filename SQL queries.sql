SELECT * FROM туры;

SELECT * FROM туры
JOIN Страны ON туры.Id_страны = Страны.Id_страны
WHERE Страны.Страна = 'Париж';

SELECT * FROM туры
JOIN Виды_туров ON туры.id_вида_тура = Виды_туров.Id_вида
WHERE Виды_туров.Вид_тура = 'люкс';

SELECT * FROM туры
WHERE Цена BETWEEN :min_price AND :max_price; 

SELECT * FROM туры
WHERE Дата_отправления = '2024-03-17';

SELECT * FROM Продажи
WHERE Дата BETWEEN :start_date AND :end_date; 

SELECT * FROM туры
WHERE Цена >= :min_price AND Цена <= :max_price; 

SELECT * FROM туры
JOIN Страны ON туры.Id_страны = Страны.Id_страны
WHERE Страны.Страна = :desired_country; 

SELECT * FROM Продажи
JOIN Клиенты ON Продажи.Id_клиента = Клиенты.Id_клиента
WHERE Клиенты.Фамилия = :desired_lastname; 

SELECT * FROM туры
WHERE Количество_дней > :desired_duration; 

SELECT DISTINCT Клиенты.* FROM Клиенты
JOIN Продажи ON Клиенты.Id_клиента = Продажи.Id_клиента
JOIN туры ON Продажи.Id_тура = туры.Id_тура
JOIN Страны ON туры.Id_страны = Страны.Id_страны
WHERE Страны.Страна = :desired_country; 

SELECT * FROM туры
JOIN Продажи ON туры.Id_тура = Продажи.Id_тура
JOIN Клиенты ON Продажи.Id_клиента = Клиенты.Id_клиента
WHERE Клиенты.Фамилия = :desired_lastname; 

SELECT DISTINCT Клиенты.* FROM Клиенты
JOIN Продажи ON Клиенты.Id_клиента = Продажи.Id_клиента
JOIN туры ON Продажи.Id_тура = туры.Id_тура
WHERE EXTRACT(MONTH FROM Продажи.Дата) = :desired_month; 

SELECT * FROM туры
WHERE туры.Id_тура NOT IN (SELECT DISTINCT Id_тура FROM Продажи);

SELECT *, (Количество_людей - (SELECT COALESCE(SUM(Количество), 0) FROM Продажи WHERE Продажи.Id_тура = туры.Id_тура)) AS Свободные_места FROM туры
HAVING Свободные_места < :desired_capacity; 
