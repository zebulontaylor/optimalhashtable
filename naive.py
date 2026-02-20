from random import randint, sample

a = randint(1, 100)
b = randint(1, 100)
p = 2**31 - 1

h = lambda value, j, n: ((a*value + b + j) % p) % n

class NaiveHashtable:
    def __init__(self, n, delta):
        self.n = n
        self.delta = delta
        self.table = [None for _ in range(n)]

    def insert(self, value):
        j = 1
        while self.table[h(value, j, self.n)] is not None:
            j += 1
        self.table[h(value, j, self.n)] = value
        return j

    def search(self, value):
        j = 1
        while self.table[h(value, j, self.n)] is not None:
            if self.table[h(value, j, self.n)] == value:
                return j
            j += 1
        return j

