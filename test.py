import elastic
import naive

from random import sample, randint
import csv
import tqdm

def run_test(insert, search, n, values, num_searches=40000):
    average_insertion_probes = 0
    insertion_count = 0

    for i in range(len(values)):
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

    #print(f"Average insertion probes: {average_insertion_probes / insertion_count:.3f}")
    #print(f"Average search probes: {average_search_probes / search_count:.3f}")
    return (average_insertion_probes / insertion_count, average_search_probes / search_count)


if __name__ == "__main__":
    n = 2**13
    rows = []
    for k in tqdm.tqdm(range(2, 23), desc="Deltas", position=0):
        averages = [0, 0, 0, 0]
        for i in tqdm.tqdm(range(5), desc="Inner Samples", position=1, leave=False):
            delta = 1.3**(-k)
            values = sample(range(n * 100), int(n * (1-delta)))
            eht = elastic.ElasticHashtable(n, delta)
            nht = naive.NaiveHashtable(n, delta)
            e_insert, e_search = run_test(eht.insert, eht.search, n, values)
            n_insert, n_search = run_test(nht.insert, nht.search, n, values)
            averages[0] += e_insert
            averages[1] += e_search
            averages[2] += n_insert
            averages[3] += n_search
        rows.append([delta, averages[0]/5, averages[1]/5, averages[2]/5, averages[3]/5])
    
    with open("results.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["delta", "elastic_insert", "elastic_search", "naive_insert", "naive_search"])
        writer.writerows(rows)
