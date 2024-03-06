import sys, csv, json, time

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
    print(elementos_matcheados - elementos_no_matcheados)
    return elementos_matcheados - elementos_no_matcheados        
    

def filtrar_mayores(A, C):
    if len(C) == 0:
        return A
    
    r = set()
    for a in A:
        if a > max(C): 
            r.add(a)
    return r

def is_solution(B, C):    
    for b in B:
        if len(C.intersection(b)) == 0:
            return False 
    return True 

def backtracking(A, B, C, k):
    if len(C) > k:
        return set()

    if is_solution(B, C):
        return C
    
    resto = filtrar_mayores(A, C)
    resto -= descartar_ya_matcheados(B, C)
    for elem in resto:
        copia = C.copy()
        copia.add(elem)
        resultado = backtracking(A, B, copia, k)
        if len(resultado) > 0:
            return resultado
    return set()

def hsp(A, B, k):
    for i in range(k+1):
        r = backtracking(A, B, set(), i)
        if r:
            return r
    return None

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
    r = hsp(A, B, len(A))
    print(f"Resultado: {r}")
    print(f"len(): {len(r)}")

def load_json(filename):
    with open(filename) as f:
        return json.load(f)
    
def save_export(export):
    with open('./export-backtracking.csv', 'w+') as f:
        writer = csv.writer(f)
        writer.writerow(['n', 'len', 'time'])
        for row in export:
            writer.writerow(row)

# def main():
#     filename = sys.argv[1]
#     # rows = load(filename)
#     # A, B = build_sets(rows)   
#     data = load_json(filename)
#     export = []

#     for d in data:
#         try:
#             start = time.time()
#             B = { frozenset(b) for b in d['B'] }
#             r = hsp(set(d['A']), B, len(d['A']))
#             end = time.time()
#             lap = end - start
#             export.append([d['m'], len(r), lap])
#             print([d['m'], len(r), lap])
#         except TypeError as e:
#             print(e)
#             print(d)
#             raise e
        
#     print(export)
#     save_export(export)


main()