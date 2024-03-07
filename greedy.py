import sys, csv, json, time, argparse

def next_candidate(non_hit, candidates):
    """
    Entrada
    non_hit: Set de sets disponibles que no tienen elementos en el hitting-set.
    candidates: Elementos candidatos a estar en el hitting-set

    Salida: Elemento elegido que aparece la mayor cantidad de veces en non_hit
    """
    max = 0
    candidate = None
    d = {}
    for c in candidates: # O(n)
        for b in non_hit: # O(m)
            if c in b:    # O(n)
                d[c] = d.get(c, 0) + 1 # O(1)
                if d[c] > max:
                    max = d[c]
                    candidate = c
    candidates.remove(candidate) # O(n)
    return candidate # ==> O(mn²)

def hit_sets(non_hit, candidate):
    """
    Entrada
    non_hit: Set de sets disponibles que no tienen elementos en el hitting-set.
    candidato: Elemento elegido para entrar en el hitting-set

    Salida: Se actualiza non_hit quitando los sets donde aparezca el candidato
    """
    for s in non_hit.copy():  # O(m)
        if candidate in s:    # O(n) 
            non_hit.remove(s) # O(n)
    return non_hit # => O(mn²)


def is_solution(B, C):  
    """
    Indica si C es hitting-set de B
    """  
    for b in B: #O(m)
        if len(C.intersection(b)) == 0: #O(n)
            return False 
    return True  # ==> O(mn)

def hsp(A, B, k):
    C = set()
    non_hit = B.copy()
    candidates = A.copy()

    while len(C) < k and not is_solution(B, C): # O(n)
        candidate = next_candidate(non_hit, candidates) #O(mn²)
        non_hit = hit_sets(non_hit, candidate) #O(mn²)
        C.add(candidate) 
    return C #O(mn^3)

def load(filename):
    with open(filename) as f:
        reader = csv.reader(f)
        rows = []
        for row in reader:
            rows.append(row)
    return rows

def build_sets(rows):
    A = set()
    B = set()
    for row in rows:
        b = frozenset(row)
        B.add(b)
        A = A.union(b)
    return A, B

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--json', help='Archivo json exportado por generator.py')
    parser.add_argument('--txt', help='Archivos csv usados en clase')
    return parser.parse_args()

def load_json(filename):
    with open(filename) as f:
        return json.load(f)
    
def run_json(filename):
    data = load_json(filename)

    for d in data:
        try:
            B = { frozenset(b) for b in d['B'] }
            start = time.time()
            C = hsp(set(d['A']), B, len(d['A']))
            end = time.time()
            lapse = end - start
            print(f"{d['m']};{len(C)};{C};{lapse}", flush=True)
        except TypeError as e:
            raise e

def run_txt(filename):
    rows = load(filename)
    A, B = build_sets(rows) 
    start = time.time()
    C = hsp(A, B, len(A))
    end = time.time()
    lapse = end - start
    print(f"1;{len(C)};{C};{lapse}", flush=True)

def main():
    args = parse_args()
    print("n;len;C;lapse", flush=True)
    if args.json:
        run_json(args.json)
    elif args.txt:
        run_txt(args.txt)
    else:
        raise RuntimeError('No se especificó formato de archivos')

main()