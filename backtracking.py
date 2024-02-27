import sys, csv, json, time

# Verifica si el conjunto C es una solución válida al problema de Hitting Set.
# Una solución es válida si para cada subconjunto b en B, C contiene al menos un elemento de b.
def is_solution(B, C):    
    return all(len(C.intersection(b)) > 0 for b in B)

# Implementa el algoritmo de backtracking para encontrar una solución al problema de Hitting Set.
# A: conjunto universal de elementos
# B: colección de subconjuntos de A
# C: conjunto actual de elementos seleccionados (hitting set parcial)
# k: tamaño máximo del hitting set
# Retorna un hitting set si encuentra una solución, o un conjunto vacío en caso contrario.
def backtracking(A, B, C, k):
    if len(C) > k:
        return None
    if is_solution(B, C):
        return C
    
    for elem in A - C:
        # Poda: Si agregar el elemento actual a C no contribuye a la solución, saltarlo.
        if all(elem not in b for b in B):
            continue
        resultado = backtracking(A, B, C | {elem}, k)
        if resultado:
            return resultado
    return None

# Función principal para resolver el problema de Hitting Set.
# Intenta encontrar una solución incrementando gradualmente el tamaño de k hasta un límite.
# Retorna la solución encontrada o None si no hay solución dentro del límite de tamaño k.
def hsp(A, B, k):
    for i in range(k+1):
        r = backtracking(A, B, set(), i)
        if r is not None:
            return r
    return None

# Carga un archivo JSON y devuelve su contenido.
def load_json(filename):
    with open(filename) as f:
        return json.load(f)

# Guarda los resultados de la exportación en un archivo CSV con formato específico.
def save_export(export):
    with open('export-backtracking.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['m', 'len', 'time'])
        writer.writerows(export_data)

# Carga los datos
# Ejecuta el algoritmo de backtracking y guarda los resultados.
# Los datos de entrada se esperan en formato JSON
# Los resultados se exportan a un archivo CSV.
def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py data.json")
        sys.exit(1)
    
    filename = sys.argv[1] 
    data = load_json(filename)
    export_data = []

    for d in data:
        A = set(d['A'])
        B = {frozenset(b) for b in d['B']}
        start = time.time()
        r = hsp(A, B, len(A))
        end = time.time()
        if r is not None:
            export_data.append([d['m'], len(r), end - start])
    
    save_export(export_data)
    print("Export completed successfully.")

if __name__ == "__main__":
    main()