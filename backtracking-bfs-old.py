import sys, csv, json, time
from collections import deque 
import pprint
import argparse

A = frozenset([1, 2, 3, 4, 5, 6])
B = frozenset([
    frozenset([1, 2]),
    frozenset([2, 3, 4]),
    frozenset([3, 5]),
    frozenset([6])
])

def flat_set(S):
    r = set()
    for s in S:
        for e in s:
            r.add(e)
    return r

def descartar_ya_matcheados(B, C):
    b_matcheados = set()
    b_no_matcheados = set()
    
    for b in B:
        if len(C.intersection(b)) != 0:
            b_matcheados.add(b)
        else:
            b_no_matcheados.add(b)
    
    elementos_matcheados = flat_set(b_matcheados)
    elementos_no_matcheados = flat_set(b_no_matcheados)
    descartar = elementos_matcheados - elementos_no_matcheados  
    return descartar  

def es_solucion(B, C):    
    for b in B:
        if len(C.intersection(b)) == 0:
            return False 
    return True 

def bfs_rec(q):
    if len(q) == 0: return set()

    (A, B, C, visitados) = q.popleft()
    if C in visitados:
        return bfs_rec(q)
    visitados.add(C)

    if es_solucion(B, C):
        return C

    restos = A - C
    restos -= descartar_ya_matcheados(B, C)
    for resto in restos:
        q.append((A, B, C.union(frozenset([resto])), visitados))    

    return bfs_rec(q)

def bfs(A, B):
    q = deque()
    q.append((A, B, frozenset(), set()))
    return bfs_rec(q)

def hsp(A, B):
    q = deque()
    C = frozenset()
    q.append(C)
    visitados = set()

    while q:
        C = q.popleft()
        if C in visitados:
            continue
        visitados.add(C)

        if es_solucion(B, C):
            return C

        restos = A - C
        restos -= descartar_ya_matcheados(B, C)
        for resto in restos:
            q.append(C.union(frozenset([resto])))    
    
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
    parser.add_argument('--csv', help='Archivos csv usados en clase')
    return parser.parse_args()

def load_json(filename):
    with open(filename) as f:
        return json.load(f)
    
def run_json(data):
    for d in data:
    try:
        start = time.time()
        B = { frozenset(b) for b in d['B'] }
        r = hsp(set(d['A']), B, len(d['A']))
        end = time.time()
        lap = end - start
        export.append([d['m'], len(r), lap])
        print([d['m'], len(r), lap])
    except TypeError as e:
        print(e)
        print(d)
        raise e

def main():
    args = parse_args()
    if args.json:
        data = load_json(args.json)
        run_json(data)

    filename = sys.argv[1]
    rows = load(filename)
    A, B = build_sets(rows)    
    C = bfs_iter(A, B)
    print(f"len: {len(C)} .... solucion: {C}")

main()