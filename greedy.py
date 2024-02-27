import sys, csv, json, time

# busca entre los elementos candidatos (candidates) para encontrar el que aparece 
# con mayor frecuencia en los subconjuntos que aún no han sido "golpeados" (non_hit)
# El elemento seleccionado se elimina de los candidatos, ya que será agregado al conjunto golpeador.
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

# actualiza el conjunto de subconjuntos no golpeados (non_hit) eliminando aquellos que contienen al candidato seleccionado.
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

# Verifica si el conjunto actual C es un conjunto golpeador para todos los subconjuntos en B.
def is_solution(B, C):  
    """
    Indica si C es hitting-set de B
    """  
    for b in B: #O(m)
        if len(C.intersection(b)) == 0: #O(n)
            return False 
    return True  # ==> O(mn)

# Intenta construir un conjunto golpeador utilizando un enfoque greedy. 
# Selecciona el mejor candidato utilizando next_candidate, 
# actualiza los subconjuntos no golpeados con hit_sets, 
# y repite este proceso hasta encontrar una solución o hasta alcanzar el tamaño máximo k.
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

def load_json(filename):
    with open(filename) as f:
        return json.load(f)
    
def save_export(export):
    with open('./export-greedy.csv', 'w+') as f:
        writer = csv.writer(f)
        writer.writerow(['n', 'len', 'time'])
        for row in export:
            writer.writerow(row)

def main():
    filename = sys.argv[1]
    # rows = load(filename)
    # A, B = build_sets(rows)   
    data = load_json(filename)
    export = []

    for d in data:
        start = time.time()
        r = hsp(d['A'], d['B'], len(d['A']))
        end = time.time()
        lap = end - start
        export.append([d['m'], len(r), lap])
        
    print(export)
    save_export(export)
main()