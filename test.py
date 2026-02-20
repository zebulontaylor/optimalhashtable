import elastic
import naive
from random import sample, randint

def run_test(insert, search, n, delta, values, num_searches=10000):
    average_insertion_probes = 0
    insertion_count = 0

    for i in range(int(n * (1-delta))):
        insertion_count += 1
        res = insert(values[i])
        probes = res[2] if isinstance(res, tuple) else res
        #print(f"Inserted {values[i]} in {probes} probes at table {table_no}, slot {slot} (batch {ht.batch_no})")
        average_insertion_probes += probes

    average_search_probes = 0

    search_count = 0
    for i in range(num_searches):
        num = values[randint(0, len(values)-1)]
        res = search(num)
        idx = res[4] if isinstance(res, tuple) else res
        #print(f"Found {val} at table {i}, slot {slot}, in {idx+1} probes")
        average_search_probes += idx
        search_count += 1

    print(f"Average insertion probes: {average_insertion_probes / insertion_count:.3f}")
    print(f"Average search probes: {average_search_probes / search_count:.3f}")


if __name__ == "__main__":
    delta = 0.05
    n = 2**13
    values = sample(range(n * 10), int(n * (1 - delta)))
    eht = elastic.ElasticHashtable(n, delta)
    nht = naive.NaiveHashtable(n, delta)
    print(f"Using delta={delta}, n={n}")
    print("=== Elastic Hashtable ===")
    run_test(eht.insert, eht.search, n, delta, values)
    print("=== Naive Hashtable ===")
    run_test(nht.insert, nht.search, n, delta, values)
