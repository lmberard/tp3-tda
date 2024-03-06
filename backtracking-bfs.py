import sys, csv, json, time
from collections import deque 
import pprint


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

def bfs_iter(A, B):
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

def main():
    filename = sys.argv[1]
    rows = load(filename)
    A, B = build_sets(rows)    
    C = bfs_iter(A, B)
    print(f"len: {len(C)} .... solucion: {C}")

main()