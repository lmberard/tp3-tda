import sys, csv, json, time

# Verifica si el conjunto C es una solución válida al problema de Hitting Set.
# Una solución es válida si para cada subconjunto b en B, C contiene al menos un elemento de b.
def is_solution(B, C):    
    for b in B:
        if len(C.intersection(b)) == 0:
            return False 
    return True 

# Implementa el algoritmo de backtracking para encontrar una solución al problema de Hitting Set.
# A: conjunto universal de elementos
# B: colección de subconjuntos de A
# C: conjunto actual de elementos seleccionados (hitting set parcial)
# k: tamaño máximo del hitting set
# Retorna un hitting set si encuentra una solución, o un conjunto vacío en caso contrario.
def backtracking(A, B, C, k):
    if len(C) > k:
        return set()

    if is_solution(B, C):
        return C
    
    resto = A - C
    for elem in resto:
        copia = C.copy()
        copia.add(elem)
        resultado = backtracking(A, B, copia, k)
        if len(resultado) > 0:
            return resultado
    return set()

# Función principal para resolver el problema de Hitting Set.
# Intenta encontrar una solución incrementando gradualmente el tamaño de k hasta un límite.
# Retorna la solución encontrada o None si no hay solución dentro del límite de tamaño k.
def hsp(A, B, k):
    for i in range(k+1):
        r = backtracking(A, B, set(), i)
        if r:
            return r
    return None

# Carga datos desde un archivo CSV y los devuelve como una lista de filas.
def load(filename):
    with open(filename) as f:
        reader = csv.reader(f)
        rows = []
        for row in reader:
            rows.append(row)
    return rows

# Construye el conjunto universal A y la colección de subconjuntos B a partir de las filas del CSV.
def build_sets(rows):
    A = set()
    B = set()
    for row in rows:
        b = frozenset(row)
        B.add(b)
        A = A.union(b)
    return A, B

# def main():
#     filename = sys.argv[1]
#     rows = load(filename)
#     A, B = build_sets(rows)    
#     r = hsp(A, B, len(A))
#     print(f"Resultado: {r}")

# Carga un archivo JSON y devuelve su contenido.
def load_json(filename):
    with open(filename) as f:
        return json.load(f)

# Guarda los resultados de la exportación en un archivo CSV con formato específico.
def save_export(export):
    with open('./export-backtracking.csv', 'w+') as f:
        writer = csv.writer(f)
        writer.writerow(['n', 'len', 'time'])
        for row in export:
            writer.writerow(row)

# Carga los datos
# Ejecuta el algoritmo de backtracking y guarda los resultados.
# Los datos de entrada se esperan en formato JSON
# Los resultados se exportan a un archivo CSV.
def main():
    filename = sys.argv[1]
    # rows = load(filename)
    # A, B = build_sets(rows)   
    data = load_json(filename)
    export = []

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
        
    print(export)
    save_export(export)


main()