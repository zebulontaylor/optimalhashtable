from math import log2, ceil, floor
from random import randint

delta = 0.1
n = 2**8

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

c = 10
f = lambda epsilon: ceil(c * min(log2(1/epsilon)**2, log2(1/delta))) + 1

p = 2**31-1
a = randint(1, p-1)

hphi = lambda i, j, value: ((a*phi(i, j) + value) % p) % tables[i].size

## INSERTING
def get_batch_size(batch_no):
    if batch_no == 0:
        return ceil(0.75 * tables[0].size)
    a1 = tables[batch_no-1].size
    a2 = tables[batch_no].size
    return a1 - floor(delta * a1 / 2) - ceil(0.75 * a1) + ceil(0.75 * a2)

def insert_from_batch(batch_no, value):
    table1 = tables[batch_no-1]
    table2 = tables[batch_no]
    
    e1 = table1.epsilon
    e2 = table2.epsilon

    if batch_no == 0:
        # Do table 1
        j = 0
        while True:
            if table2.probe_empty(hphi(batch_no, j, value)):
                table2.insert(hphi(batch_no, j, value), value)
                return (batch_no, hphi(batch_no, j, value), j)
            j += 1

    if e1 > delta / 2 and e2 > 0.25:
        # Try table 1 first up to f(e1), then try table 2
        for j in range(f(e1)):
            if table1.probe_empty(hphi(batch_no-1, j, value)):
                table1.insert(hphi(batch_no-1, j, value), value)
                return (batch_no-1, hphi(batch_no-1, j, value), j)
        j = 0
        print(f"failed to insert to table 1 using {f(e1)} probes")
        while True:
            if table2.probe_empty(hphi(batch_no, j, value)):
                table2.insert(hphi(batch_no, j, value), value)
                return (batch_no, hphi(batch_no, j, value), j+f(e1))
            j += 1
    elif e1 <= delta / 2:
        # Do table 2
        j = 0
        while True:
            if table2.probe_empty(hphi(batch_no, j, value)):
                table2.insert(hphi(batch_no, j, value), value)
                return (batch_no, hphi(batch_no, j, value), j)
            j += 1
    else: # e2 <= 0.25
        # Do table 1
        j = 0
        while True:
            if table1.probe_empty(hphi(batch_no-1, j, value)):
                table1.insert(hphi(batch_no-1, j, value), value)
                return (batch_no-1, hphi(batch_no-1, j, value), j)
            j += 1

## SEARCHING
valid_probes = []
for i_idx in range(len(tables)):
    for j_idx in range(1, 100):
        cost = phi(i_idx, j_idx)
        valid_probes.append((cost, i_idx, j_idx))

valid_probes.sort(key=lambda x: x[0])

def search(value):
    for idx, (_, i, j) in enumerate(valid_probes):
        slot = hphi(i, j, value)
        if tables[i].table[slot] == value:
            return (value, i, j, slot, idx)
    return None

batch_no = 0
left_in_batch = get_batch_size(batch_no)

for i in range(int(n * (1-delta))):
    table_no, slot, probes = insert_from_batch(batch_no, i)
    print(f"Inserted {i} in {probes} probes at table {table_no}, slot {slot} (batch {batch_no})")
    left_in_batch -= 1
    if left_in_batch == 0:
        if batch_no > 0:
            print(tables[batch_no-1].epsilon)
        batch_no += 1
        left_in_batch = get_batch_size(batch_no)

for i in range(5):
    num = randint(0, int(n * (1-delta))-1)
    print(num)
    val, i, j, slot, idx = search(num)
    print(f"Found {val} at table {i}, slot {slot}, in {idx+1} probes")

print(tables)
