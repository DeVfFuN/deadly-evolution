import numpy as np
import matplotlib.pyplot as plt
import os

def exponential_sequence(coefficient, length, start_value):
    """
    Генерирует экспоненциально возрастающую последовательность.

    :param coefficient: Коэффициент, определяющий скорость роста.
    :param length: Длина последовательности.
    :param start_value: Начальное значение последовательности.
    :return: Массив значений последовательности.
    """
    x = np.arange(length)
    y = start_value * np.exp(coefficient * x)
    return x, y

# Параметры
coefficient = 0.0023  # Задайте коэффициент роста
length = 2000  # Длина последовательности
start_value = 62  # Начальное значение последовательности


x, y = exponential_sequence(coefficient, length, start_value)


script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'line_data_p.txt')
with open(file_path, 'w') as f:
    for env in y:
        f.write(f"{env}\n")


plt.plot(x, y,color="r")
plt.title(f'Экспоненциальный рост скорости изменения среды (коэффициент = {coefficient}, начальное значение = {start_value})')
plt.xlabel('Количество итераций цикла')
plt.ylabel('Значение параметра среды')
plt.grid(True)
plt.show()
