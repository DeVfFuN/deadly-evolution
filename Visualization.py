import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Подключение к базе данных
conn = sqlite3.connect('evol_death.db')

# Выполнение SQL-запроса и загрузка данных в DataFrame
query_size = "SELECT pop_size FROM creations00"
query_env_a = "SELECT env FROM creations00"

df_size = pd.read_sql_query(query_size, conn)  # создание датафрейма
df_env_p = pd.read_sql_query(query_env_a, conn)

conn.close()



# Первый график (размер популяции)
fig, ax1 = plt.subplots()

ax1.plot(df_size["pop_size"], color='b', label='размер популяции')
ax1.set_xlabel('циклы времени', fontsize=16)
ax1.set_ylabel('размер популяции', fontsize=16, color='b')
ax1.tick_params(axis='y', labelcolor='b')

# Вторая ось Y для второго графика
ax2 = ax1.twinx()

# График для env
ax2.plot(df_env_p["env"], color='r', label='env_a')


# Настройка второй оси Y
ax2.set_ylabel('Изменение параметров среды', fontsize=16, color='r')
ax2.tick_params(axis='y', labelcolor='r')

# Добавление легенд
fig.legend(loc="upper left", bbox_to_anchor=(0.005, 1))
# Заголовок графика
plt.title("График размера популяции и параметров среды", fontsize=25)
plt.show()

print(np.trapz(df_size["pop_size"]))




