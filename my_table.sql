--
-- Файл сгенерирован с помощью SQLiteStudio v3.2.1 в Пт авг 27 17:47:35 2021
--
-- Использованная кодировка текста: UTF-8
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Таблица: townhall
DROP TABLE IF EXISTS townhall;
CREATE TABLE townhall (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, user_id BIGINT REFERENCES user (user_id) ON DELETE CASCADE, country_name VARCHAR (128), age VARCHAR (128) DEFAULT Каменный, money INTEGER DEFAULT (200), food INTEGER DEFAULT (500), stock INTEGER DEFAULT (300), energy INTEGER DEFAULT (0), graviton INTEGER DEFAULT (0), timer INTEGER DEFAULT (0));
INSERT INTO townhall (id, user_id, country_name, age, money, food, stock, energy, graviton, timer) VALUES (1, 615311497, 'England', 'Железный', 2701, 258, 810, 0, 0, 1629804907);
INSERT INTO townhall (id, user_id, country_name, age, money, food, stock, energy, graviton, timer) VALUES (23, 722475023, 'Pohuy', 'Железный', 233874, 491, 40650, 0, 0, 1630009135);
INSERT INTO townhall (id, user_id, country_name, age, money, food, stock, energy, graviton, timer) VALUES (24, 461238992, 'mainbatya', 'Железный', 16166, 4604, 2416, 0, 0, 1629996934);
INSERT INTO townhall (id, user_id, country_name, age, money, food, stock, energy, graviton, timer) VALUES (27, 1305271407, 'arselon', 'Железный', 69704, 18150, 14076, 0, 0, 1629996207);
INSERT INTO townhall (id, user_id, country_name, age, money, food, stock, energy, graviton, timer) VALUES (32, 1706721796, 'Dazai_country', 'Каменный', 400, 300, 0, 0, 0, 1629660371);
INSERT INTO townhall (id, user_id, country_name, age, money, food, stock, energy, graviton, timer) VALUES (34, 1432512968, 'A', 'Каменный', 986, 2260, 0, 0, 0, 1629719064);
INSERT INTO townhall (id, user_id, country_name, age, money, food, stock, energy, graviton, timer) VALUES (35, 1079648407, 'moscow_228', 'Каменный', 200, 441, 0, 0, 0, 1629668110);
INSERT INTO townhall (id, user_id, country_name, age, money, food, stock, energy, graviton, timer) VALUES (36, 1034620983, 'arselon1', 'Бронзовый', 500, 1071, 1196, 0, 0, 1629741311);
INSERT INTO townhall (id, user_id, country_name, age, money, food, stock, energy, graviton, timer) VALUES (37, 1937853094, 'v_rot_tebya_ebal', 'Каменный', 580, 503, 0, 0, 0, 1629987912);
INSERT INTO townhall (id, user_id, country_name, age, money, food, stock, energy, graviton, timer) VALUES (38, 741945359, 'mamka', 'Железный', 1751, 6773, 5134, 0, 0, 1629990448);
INSERT INTO townhall (id, user_id, country_name, age, money, food, stock, energy, graviton, timer) VALUES (39, 1286263948, 'SaFlauy', 'Каменный', 390, 300, 0, 0, 0, 1629838106);
INSERT INTO townhall (id, user_id, country_name, age, money, food, stock, energy, graviton, timer) VALUES (40, 1611219863, 'rarity', 'Каменный', 2885, 2329, 0, 0, 0, 1630010500);

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
