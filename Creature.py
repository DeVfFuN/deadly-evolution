from random import choice, randint
import random


class Creature:
    def __init__(self, chromosoma_1="1aaaaaaaaaa", chromosoma_2="1aaaaaaaaaa"):
        self.death_count = 0.0001 # если этот параметр станет равным 10, организм погибнет
        self.chromosoma_1 = chromosoma_1
        self.chromosoma_2 = chromosoma_2
        self.chromosoms = [chromosoma_1, chromosoma_2]
        self.score_1 = len(self.chromosoma_1)  #количество генов в хромосоме 1
        self.score_2 = len(self.chromosoma_2)  #количество генов в хромосоме 2


    @staticmethod
    def mutation(chromosoma):
        """Выбирает тип мутации и производит её"""
        if len(chromosoma) < 3:
            return chromosoma

        def len_of_mutation():
            a = random.randint(0, 1000)
            if a > 500:
                return 1
            elif a > 250:
                return 2
            elif a > 125:
                return 3
            elif a > 80:
                return 4
            elif a > 30:
                return 5
            else:
                return 6


        type_mut = choice(["dup", "del"])
        lenmut = len_of_mutation()
        if type_mut == "del":
            return "a" * (len(chromosoma) - lenmut) if lenmut < len(chromosoma) else "a"
        else:
            return "a" * (len_of_mutation() + len(chromosoma))

    def meosis(self):
        """Выбирает, какая именно хромосома будет у потомка"""
        choice_the_chromosom = choice((self.chromosoms))
        if randint(1, 100) < 5:
            return self.mutation(choice_the_chromosom)
        else:
            return choice_the_chromosom

# c1 = Creature()
# print(c1.meosis())
# print(c1.score_p, c1.score_t)





