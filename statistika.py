from Start_time import main_loop
import numpy as np

p = [0, 0]
n = 3000
res_time = []
res_size_av = []
res_size_med = []


for i in range(2):

    luck = 0
    for attempt in range(n):
        print(attempt)
        result = main_loop(i, attempt)
        luck += result[0]
        res_time.append(result[1])
        res_size_av.append(result[2])
        res_size_med.append(result[3])
    print(f"Среднее время жизни популяции режима {i} равно ", np.mean(res_time))
    print(f"Средний размер популяции режима {i} равен ", np.mean(res_size_av))
    print(f"Средний размер популяции режима {i} для медиан равен ", np.mean(res_size_med))
    res_time.clear()
    res_size_av.clear()
    res_size_med.clear()
    p[i] = luck / n

print(p)



ese = ((p[0] * (1 - p[0]) + p[1] * (1 - p[1])) / n) ** 0.5
z = (p[0] - p[1]) / ese


print(z)
print(" Да") if z < -1.95 else print("Нет")

