import sys, csv, json, time
from collections import deque 
import pprint
import argparse

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

def hsp(A, B, k):
    q = deque()
    C = frozenset()
    q.append(C)
    visitados = set()

    while q:
        C = q.popleft()

        if len(C) > k:
            break

        if C in visitados:
            continue
        visitados.add(C)

        if es_solucion(B, C):
            return C

        restos = A - C
        restos -= descartar_ya_matcheados(B, C)
        for resto in restos:
            q.append(C.union(frozenset([resto])))  

    return set() 
    
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
    
def run_json(filename):
    data = load_json(filename)

    for d in data:
        try:
            B = { frozenset(b) for b in d['B'] }
            start = time.time()
            C = hsp(set(d['A']), B, len(d['A']))
            end = time.time()
            lapse = end - start
            print(f"{len(d['A'])};{len(C)};{C};{lapse}", flush=True)
        except TypeError as e:
            raise e

def run_csv(filename):
    rows = load(filename)
    A, B = build_sets(rows) 
    start = time.time()
    C = hsp(A, B)
    end = time.time()
    lapse = end - start
    print(f"{len(A)};{len(C)};{C};{lapse}", flush=True)

def main():
    args = parse_args()
    print("n;len;C;lapse", flush=True)
    if args.json:
        run_json(args.json)
    elif args.csv:
        run_csv(args.csv)
    else:
        raise RuntimeError('No se especificó formato de archivos')

main()