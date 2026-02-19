from math import log2, ceil, floor
from random import randint

delta = 0.2
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
    
    def __getitem__(self, idx):
        return self.table[idx % self.size]
    
    def __repr__(self):
        table_str = str({i: x for i, x in enumerate(self.table) if x is not None})
        return f"SubArray(size={self.size}, entry_count={self.entry_count}, table={table_str})"

    __str__ = __repr__

p = 2**31-1
a = randint(1, p-1)

phi = lambda i, j: int("".join("1" + b for b in bin(j)[2:]) + "0" + bin(i)[2:], 2)
hphi = lambda i, j, value: ((a*phi(i, j) + value) % p)

class OptimalHashtable:
    def __init__(self, n, delta, c=20):
        self.n = n
        self.delta = delta
        self.batch_no = 0
        self.tables = []
        for i in range(1, floor(log2(n)) + 1):
            length = int(n / (2**i))
            if i == floor(log2(n)):
                length += 1
            self.tables.append(SubArray(length))
        self.left_in_batch = self.get_batch_size(self.batch_no)
        self.f = lambda epsilon: ceil(c * min(log2(1/epsilon)**2, log2(1/delta))) + 1

        self.valid_probes = []
        for i_idx in range(len(self.tables)):
            for j_idx in range(1, n):
                cost = phi(i_idx+1, j_idx)
                self.valid_probes.append((cost, i_idx, j_idx))

        self.valid_probes.sort(key=lambda x: x[0])

    def get_batch_size(self, batch_no):
        if batch_no == 0:
            return ceil(0.75 * self.tables[0].size)
        a1 = self.tables[batch_no-1].size
        a2 = self.tables[batch_no].size
        return a1 - floor(delta * a1 / 2) - ceil(0.75 * a1) + ceil(0.75 * a2)
    
    def insert(self, value):
        table_no, slot, probes = self.insert_from_batch(self.batch_no, value)
        self.left_in_batch -= 1
        if self.left_in_batch == 0:
            self.batch_no += 1
            self.left_in_batch = self.get_batch_size(self.batch_no)
        return (table_no, slot, probes)

    def insert_from_batch(self, batch_no, value):
        table1 = self.tables[batch_no-1]
        table2 = self.tables[batch_no]
        
        e1 = table1.epsilon
        e2 = table2.epsilon

        if batch_no == 0:
            # Do table 1
            j = 1
            while True:
                if self.tables[0].probe_empty(hphi(batch_no, j, value)):
                    self.tables[0].insert(hphi(batch_no, j, value), value)
                    return (batch_no, hphi(batch_no, j, value), j)
                j += 1

        if e1 > delta / 2 and e2 > 0.25:
            # Try table 1 first up to f(e1), then try table 2
            for j in range(1, self.f(e1)):
                if table1.probe_empty(hphi(batch_no-1, j, value)):
                    table1.insert(hphi(batch_no-1, j, value), value)
                    return (batch_no-1, hphi(batch_no-1, j, value), j)
            j = 1
            print(f"failed to insert to table 1 using {f(e1)} probes")
            while True:
                if table2.probe_empty(hphi(batch_no, j, value)):
                    table2.insert(hphi(batch_no, j, value), value)
                    return (batch_no, hphi(batch_no, j, value), j+f(e1))
                j += 1
        elif e1 <= delta / 2:
            # Do table 2
            j = 1
            while True:
                if table2.probe_empty(hphi(batch_no, j, value)):
                    table2.insert(hphi(batch_no, j, value), value)
                    return (batch_no, hphi(batch_no, j, value), j)
                j += 1
        else: # e2 <= 0.25
            # Do table 1
            j = 1
            while True:
                if table1.probe_empty(hphi(batch_no-1, j, value)):
                    table1.insert(hphi(batch_no-1, j, value), value)
                    return (batch_no-1, hphi(batch_no-1, j, value), j)
                j += 1

    def search(self, value, j_depth=2):
        for i in range(ceil(log2(1/delta))):
            for j in range(1, j_depth+1):
                slot = hphi(i, j, value) % self.tables[i].size
                if self.tables[i][slot] == value:
                    return (value, i, j, slot, i*j_depth + j)

        prev_count = i*j_depth + j

        # If that fails, do exhaustive search
        for idx, (_, i, j) in enumerate(self.valid_probes):
            slot = hphi(i, j, value) % self.tables[i].size
            if self.tables[i][slot] == value:
                return (value, i, j, slot, idx+prev_count)
        return None

ht = OptimalHashtable(n, delta)

average_insertion_probes = 0

insertion_count = 0
for i in range(int(n * (1-delta))):
    insertion_count += 1
    table_no, slot, probes = ht.insert(i)
    #print(f"Inserted {i} in {probes} probes at table {table_no}, slot {slot} (batch {batch_no})")
    average_insertion_probes += probes

average_search_probes = 0

search_count = 0
for i in range(10000):
    num = randint(0, int(n * (1-delta))-1)
    val, i, j, slot, idx = ht.search(num)
    #print(f"Found {val} at table {i}, slot {slot}, in {idx+1} probes")
    average_search_probes += idx
    search_count += 1

print(f"Average insertion probes: {average_insertion_probes / insertion_count:.3f}")
print(f"Average search probes: {average_search_probes / search_count:.3f}")
