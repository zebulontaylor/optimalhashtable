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
