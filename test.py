from math import log2, ceil, floor

delta = 0.2
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

batch_no = 0

phi = lambda i, j: int("".join("1" + b for b in bin(j)[2:]) + "0" + bin(i)[2:], 2)

def get_batch_size(batch_no):
    a1 = tables[batch_no].size
    a2 = tables[batch_no+1].size
    return a1 - floor(delta * a1 / 2) - ceil(0.75 * a1) + ceil(0.75 * a2)

def insert_from_batch(batch_no):
    table1 = tables[batch_no]
    table2 = tables[batch_no+1]
    
    e1 = table1.epsilon
    e2 = table2.epsilon

    if e1 > delta / 2 and e2 > 0.25:
        for i in range(10): # CHANGE TO F(epsilon) FUNCTION
            ...
    elif e1 <= delta / 2:
        while True:
            ...
    else: # e2 <= 0.25
        while True:
            ...

for i in range(int(n * (1-delta))):
    ...
