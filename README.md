# Trabajo Práctico 3: Problemas NP-Completos
El presente trabajo busca evaluar el desarrollo y análisis de un algoritmo de Backtracking para resolver un Problema NP-Completo, así como el análisis de posibles aproximaciones. 

# Modo de uso

## Generador 
Genera un archivo JSON con estructura 

```json
[
    {
        "m": 10, // Cantidad de elementos donde M=N,
        "A": [1, 2, 3, 4], // Set A con todos los elementos
        "B": [[1, 2], [2, 3, 4]] // Set B con subsets
    },
]
``` 

Ejecucion

```bash
python generator.py <N> <output-filename>
# Ejemplo
python generator.py 50 data-50.json
```

## Algoritmos

Los siguientes algoritmos imprimen por pantalla el resultado en formato CSV separado por punto y coma 

Formato impreso
Donde
- n: tamaño del conjunto A
- len: Largo de la solución
- C: Conjunto solucion
- lapse: Tiempo transcurrido en segundos

```csv
n;len;C;lapse
5;2;{0, 1};4.0531158447265625e-05
6;2;{1, 4};3.0040740966796875e-05
```

### Algoritmo Greedy

Permite leer tanto los datos de la catedra como los generados por generator.py

Ejecucion

```bash
# Modo 
python greedy.py --txt <filename.csv>
python greedy.py --json <filename.json>

# Catedra
python greedy.py --txt data/5.txt

# JSON
python greedy.py --json data-50.json
```

### Algoritmo Backtracking

```bash
# Modo 
python backtracking-reentrega.py --txt <filename.csv>
python backtracking-reentrega.py --json <filename.json>

# Catedra
python backtracking-reentrega.py --txt data/5.txt

# JSON
python backtracking-reentrega.py --json data-50.json
```

### Ejemplo

Para guardar en un archivo, se recomienda redirigir el output

```bash
# Con tee para imprimir el texto por pantalla tambien
python backtracking-reentrega.py --json data-50.json | tee export-backtracking.csv
python greedy.py --json data-50.json | tee export-greedy.csv
```