from math import log2, ceil, floor
from random import randint

delta = 0.4
n = 2**6

tables = []

class SubArray:
    def __init__(self, size):
        self.size = size
        self.entry_count = 0
        self.table = [None] * size
    
    @property
    def epsilon(self):
        return 1 - (self.entry_count / self.size)
    
    def probe_empty(self, idx):
        return self.table[idx % self.size] is None

    def insert(self, idx, value):
        assert self.probe_empty(idx)
        self.table[idx % self.size] = value
        self.entry_count += 1
    
    def __repr__(self):
        table_str = str({i: x for i, x in enumerate(self.table) if x is not None})
        return f"SubArray(size={self.size}, entry_count={self.entry_count}, table={table_str})"

    __str__ = __repr__

for i in range(1, floor(log2(n)) + 1):
    length = int(n / (2**i))
    if i == floor(log2(n)):
        length += 1
    tables.append(SubArray(length))

print(tables)
assert sum(t.size for t in tables) == n

phi = lambda i, j: int("".join("1" + b for b in bin(j)[2:]) + "0" + bin(i)[2:], 2)

c = 100
f = lambda epsilon: ceil(c * min(log2(1/epsilon)**2, log2(1/delta)))

p = 2**31-1
a = randint(1, p-1)
b = randint(0, p-1)

hphi = lambda i, j: ((a*phi(i, j) + b) % p) % tables[i].size

def get_batch_size(batch_no):
    a1 = tables[batch_no].size
    if batch_no == 0:
        return ceil(0.75 * a1)
    a2 = tables[batch_no+1].size
    return a1 - floor(delta * a1 / 2) - ceil(0.75 * a1) + ceil(0.75 * a2)

def insert_from_batch(batch_no, value):
    table1 = tables[batch_no]
    table2 = tables[batch_no+1]
    
    e1 = table1.epsilon
    e2 = table2.epsilon

    if e1 > delta / 2 and e2 > 0.25:
        # Try table 1 first up to f(e1), then try table 2
        for j in range(f(e1)):
            if table1.probe_empty(hphi(batch_no, j)):
                table1.insert(hphi(batch_no, j), value)
                return
        j = 0
        while True:
            if table2.probe_empty(hphi(batch_no+1, j)):
                table2.insert(hphi(batch_no+1, j), value)
                return
            j += 1
    elif e1 <= delta / 2:
        # Do table 2
        j = 0
        while True:
            if table2.probe_empty(hphi(batch_no+1, j)):
                table2.insert(hphi(batch_no+1, j), value)
                return
            j += 1
    else: # e2 <= 0.25
        # Do table 1
        j = 0
        while True:
            if table1.probe_empty(hphi(batch_no, j)):
                table1.insert(hphi(batch_no, j), value)
                return
            j += 1

batch_no = 0
left_in_batch = get_batch_size(batch_no)

print(f"inserting {int(n * (1-delta))} elements")

for i in range(int(n * (1-delta))):
    print(f"Inserting {i}; batch_no={batch_no}; left_in_batch={left_in_batch}")
    insert_from_batch(batch_no, i)
    left_in_batch -= 1
    if left_in_batch == 0:
        batch_no += 1
        left_in_batch = get_batch_size(batch_no)

print(tables)
