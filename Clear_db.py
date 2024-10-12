import sqlite3


def drop():
    # Подключение к базе данных и удаление таблицы с данными
    conn = sqlite3.connect('evol_death.db')
    cur = conn.cursor()
    for attemt in range(0, 1):
        cur.execute(f"DROP TABLE creations{attemt}0")
        cur.execute(f"DROP TABLE creations{attemt}1")


drop()
