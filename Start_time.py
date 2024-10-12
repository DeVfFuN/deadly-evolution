import sqlite3 as sq
import numpy as np
from Creature import Creature as CR
from random import randint

#Определите, будут ли организмы смертными
regime = 0

param_of_env = []  #тут хранятся параметры среды

#Составим список из кортежей параметров среды
file_a = open("line_data_a.txt", "r")
lines_a = file_a.readlines()  #чтение параметров среды a
a_list = []
for param_a in lines_a:
    a_list.append(float(param_a))

#Чутка модифицируем параметры среды, создаём пирамидку
p = 0
while p < len(a_list):
    if p % 100 == 0:
        a_list = a_list[0:p] + [a_list[p]] * 100 + a_list[p:]
        p += 101
    else:
        p += 1

param_of_env = a_list
file_a.close()
# print(param_of_env)

eco_capacity = 200


# region
def over_capacity(eco_capacity, n_population):
    """Определяет коэффициент увеличения смертности при превышении лимита ёмкости среды"""
    if n_population > eco_capacity:
        coeff = (((n_population - eco_capacity) / eco_capacity) + 1)
        return coeff
    else:
        return 1


def reproduction(creature, population):
    """Выдаёт потомка"""
    parent_num_1 = creature.meosis()
    if parent_num_1[0] == "1":
        parent_num_2 = CR.mutation(partner_choice(population).chromosoma_2)
    else:
        parent_num_2 = CR.mutation(partner_choice(population).chromosoma_1)
    return CR(parent_num_1, parent_num_2)


def partner_choice(population: list):
    """случайным образом выбирает партнёра для спаривания"""
    partner = population[randint(0, len(population) - 1)]
    return partner


def life_or_death(creature, param_of_envir, coeff, death_count):
    """определяет, выживет организм или нет, пополняет списки вероятности смерти и счёта"""
    pDeath = (coeff * min(abs(param_of_envir - creature.score_1),
                          abs(param_of_envir - creature.score_2))) * 0.0015 + death_count
    # print(pDeath)
    if pDeath > 1:
        return False
    elif randint(0, 10000) > pDeath * 10000:
        return True
    else:
        return False


# endregion
size_stat = []
time_stat = []


# Основной цикл программы
def main_loop(regime, attempt):
    global eco_capacity, param_of_env
    #открываем базу данных
    with sq.connect("evol_death.db") as con:
        cur = con.cursor()
        cur.execute(f"""CREATE TABLE IF NOT EXISTS creations{attempt}{regime} (
        era INTEGER,
        pop_size INTEGER,
        env DECIMAL (5, 5))""")

        era = 0
        # начальная популяция
        population = []
        with open("population_origin.txt", "r") as my_file:
            lins = my_file.readlines()
            chromosoma1 = None
            for l in lins:
                if chromosoma1 == None:
                    chromosoma1 = l.rstrip()
                else:
                    population.append(CR(chromosoma1, l.rstrip()))
                    chromosoma1 = None
        # print(population)

        while len(population) > 0 and era < len(param_of_env):  #этот цикл считает эры
            # print(era)
            n_population = len(population)
            # print(n_population)
            del_list = []  # сюда попадают индексы под удаление
            burn_list = []  # сюда попадают вновь родившиеся
            env = param_of_env[era]  #Здесь параметры среды текущей эры в виде кортежа
            # list_res_P = []  #здесь все вероятности сдохнуть

            s = 0
            if regime == 1:  #есть ген смерти
                coeff = over_capacity(eco_capacity, n_population)
                while s < len(
                        population):  # здесь проверка на соответсвие условиям и размножение, пробегает по списку организмов
                    if s > len(population) / 2:  #от перенаселения молодое поколение страдает в 2 раза сильнее
                        coeff = 25 * coeff
                    if life_or_death(population[s], env, coeff, population[s].death_count):
                        burn_list.append(reproduction(population[s], population))
                        population[s].death_count += 0.006
                    else:
                        del_list.append(s)
                        n_population -= 1
                    s += 1

            else:  #нет гена смерти
                coeff = over_capacity(eco_capacity, n_population)
                while s < len(
                        population):  # здесь проверка на соответсвие условиям и размножение, пробегает по списку организмов
                    if s > len(population) / 2:  #от перенаселения молодое поколение страдает в 2 раза сильнее
                        coeff = 25 * coeff
                    if life_or_death(population[s], env, coeff, population[s].death_count):
                        burn_list.append(reproduction(population[s], population))
                        n_population += 1
                    else:
                        del_list.append(s)
                        n_population -= 1
                    s += 1

            # непосредственно добавляем и удаляем организмы из списка популяции
            for _ in reversed(del_list):
                population.pop(_)
            for _ in burn_list:
                population.append(_)

            pop_size = len(population)
            size_stat.append(pop_size)
            # aver_P = mean(list_res_P)

            # работа с sql запись новых данных
            cur.execute(
                f"""INSERT INTO creations{attempt}{regime} (era, pop_size, env) VALUES ({era}, {pop_size}, {env})""")

            era += 1

        if len(population) == 0:
            print(f"Популяция вымерла, эра {era}")
            time_stat.append(era)
            av_size = np.mean(size_stat)
            med_size = np.median(size_stat)
            return 0, time_stat, av_size, med_size  #Выдаёт результат, время жизни, средний размер популяции и медиану размера
        else:
            print("Популяция выжила")
            time_stat.append(era)
            av_size = np.mean(size_stat)
            med_size = np.median(size_stat)
            return 1, time_stat, av_size, med_size


luck = 0
n = 1 #количество популяций
for attempt in range(n):
    luck += main_loop(regime, attempt)[0]
    print(attempt)

print(luck / n)
