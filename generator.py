import json
import pprint
import random 
import sys

def generate_simple(m):
    values = range(m)
    sets = []
    for s in range(m):
        sets.append([s])

    sample = {
        "m": m,
        "A": list(values),
        "B": sets
    }
    return sample

def generate(m):
    values = range(m)
    set_amout = random.randint(2, m)
    sets = []
    
    for s in range(set_amout):
        k = random.randint(1, m//2 + 2)
        new_set = random.sample(values, k=k)
        sets.append(sorted(new_set))

    sample = {
        "m": m,
        "A": list(values),
        "B": sets
    }

    return sample

def save(filename, data):
    with open(filename, 'w+') as f:
        f.write(json.dumps(data, indent=2))

def main():
    MAX = int(sys.argv[1])
    FILENAME = sys.argv[2]
    data = []

    for i in range(2, MAX+1):
        data.append(generate_simple(i))
    save(FILENAME, data)

main()