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

## Algoritmo Greedy

Imprime por pantalla `[N, largo-set, tiempo-transcurrido]` y lo guarda un archivo `export-greddy.csv`

```bash
python greedy.py <filename>
# Ejemplo
python greedy.py data-50.json
```

## Algoritmo Backtracking

Imprime por pantalla `[N, largo-set, tiempo-transcurrido]` y loguarda un archivo `export-backtracking.csv`.

```bash
python backtracking.py <filename>
# Ejemplo
python backtracking.py data-50.json
```