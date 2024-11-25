import copy
import time
import heapq

# Tablero inicial del Sudoku
sudoku_original = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

def imprimir_tablero(tablero):
    #Imprime el tablero del Sudoku.
    for fila in tablero:
        print(" ".join(str(num) if num != 0 else "." for num in fila))
    print()

def es_valido(tablero, fila, col, num):
    #Verifica si un número puede colocarse en una celda.
    for i in range(9):
        if tablero[fila][i] == num or tablero[i][col] == num:
            return False
    bloque_fila, bloque_col = (fila // 3) * 3, (col // 3) * 3
    for i in range(bloque_fila, bloque_fila + 3):
        for j in range(bloque_col, bloque_col + 3):
            if tablero[i][j] == num:
                return False
    return True

# Divide y Vencerás con Merge Sort
#El algoritmo de Merge sort Funciona bien para listas grandes porque tiene una complejidad de tiempo segura y tambien decidi usarla ya que
#como parte de la técnica de Divide y Venceras divide los problemas en subproblemas para que sea más fácil de resolver.
def merge_sort(tablero):
    """Ejemplo de Divide y Vencerás usando Merge Sort para resolver el Sudoku."""
    def resolver_sudoku(tablero):
        for fila in range(9):
            for col in range(9):
                if tablero[fila][col] == 0:
                    opciones = [num for num in range(1, 10) if es_valido(tablero, fila, col, num)]
                    for opcion in merge_sort_list(opciones):
                        tablero[fila][col] = opcion
                        imprimir_tablero(tablero)  # Mostrar el paso
                        time.sleep(0.2)  
                        if resolver_sudoku(tablero):
                            return True
                        tablero[fila][col] = 0
                    return False
        return True

    def merge_sort_list(lista):
        if len(lista) <= 1:
            return lista
        mitad = len(lista) // 2
        izquierda = merge_sort_list(lista[:mitad])
        derecha = merge_sort_list(lista[mitad:])
        return merge(izquierda, derecha)

    def merge(izquierda, derecha):
        resultado = []
        i = j = 0
        while i < len(izquierda) and j < len(derecha):
            if izquierda[i] < derecha[j]:
                resultado.append(izquierda[i])
                i += 1
            else:
                resultado.append(derecha[j])
                j += 1
        resultado.extend(izquierda[i:])
        resultado.extend(derecha[j:])
        return resultado

    return resolver_sudoku(tablero)

# Programación Dinámica
# En la técnica Dinamica use el algoritmo de BackTraking que com su nombre lo dice trocede, intenta con cada uno de los numeros y si se -
# equivoca retocede hasta encontrar el numero o la respuesta correcta así intentando con cada numero hasta que se resuelva.
def sudoku_dinamico(tablero):
    #Resuelve el Sudoku usando Programación Dinámica implemenando el BackTraking.
    def generar_posibilidades():
        return [[[num for num in range(1, 10) if es_valido(tablero, fila, col, num)]
                 if tablero[fila][col] == 0 else [] for col in range(9)] for fila in range(9)]

    posibilidades = generar_posibilidades()

    def resolver():
        min_fila, min_col, min_posibilidades = -1, -1, 10
        for fila in range(9):
            for col in range(9):
                if tablero[fila][col] == 0 and len(posibilidades[fila][col]) < min_posibilidades:
                    min_fila, min_col, min_posibilidades = fila, col, len(posibilidades[fila][col])
        if min_posibilidades == 10:
            return True
        fila, col = min_fila, min_col
        for num in posibilidades[fila][col]:
            if es_valido(tablero, fila, col, num):
                tablero[fila][col] = num
                imprimir_tablero(tablero)  # Mostrar el paso
                time.sleep(0.6)
                posibilidades[fila][col] = []
                if resolver():
                    return True
                tablero[fila][col] = 0
        return False

    return resolver()

# Voraz con el algoritmo de Dijkstra.
#En el la tecnica Voraz Elegí el algoritmo de Dijkstra por que inicia con la primer busqueda hacia camino mas corto o en este caso hacia el numero mas corto-
# lo que deberia de facilitar la busqueda del numero para resolvel el sudoku de manera mas sencilla y más eficas.

def dijkstra(tablero):
    
    heap = []
    for fila in range(9):
        for col in range(9):
            if tablero[fila][col] == 0:
                posibles = [num for num in range(1, 10) if es_valido(tablero, fila, col, num)]
                heapq.heappush(heap, (len(posibles), fila, col, posibles))
    
    while heap:
        _, fila, col, posibles = heapq.heappop(heap)
        if tablero[fila][col] == 0:
            for num in posibles:
                tablero[fila][col] = num
                imprimir_tablero(tablero)  # Mostrar el paso
                time.sleep(0.3) 
                if dijkstra(tablero):
                    return True
                tablero[fila][col] = 0
            return False
    return all(all(tablero[fila][col] != 0 for col in range(9)) for fila in range(9))

# Aquí emepzamos a comparar los tiempos de ejecución.
tiempos = {}

# Divide y Vencerás con el algoritmo de Merge Sort.
sudoku_copia = copy.deepcopy(sudoku_original)
inicio = time.time()
merge_sort(sudoku_copia)
fin = time.time()
print("Resultado Final con Merge Sort (Divide y Vencerás):")
imprimir_tablero(sudoku_copia)
tiempos["Dibide y Venceras"] = fin - inicio

# Programación Dinámica con el metodo de BackTraking.
sudoku_copia = copy.deepcopy(sudoku_original)
inicio = time.time()
sudoku_dinamico(sudoku_copia)
fin = time.time()
print("Resultado Final con Programación Dinámica:")
imprimir_tablero(sudoku_copia)
tiempos["Dinámica"] = fin - inicio

# Algoritmo Voraz con el metodo de Dijkstra.
sudoku_copia = copy.deepcopy(sudoku_original)
inicio = time.time()
dijkstra(sudoku_copia)
fin = time.time()
print("Resultado Final con Dijkstra (Voraz):")
imprimir_tablero(sudoku_copia)
tiempos["Voraz"] = fin - inicio

# Y Aquí imprimimos la comparacion de los tiempos entre las 3 ténicas y los 3 algoritmos.
print("\nComparación de Tiempos:")
for metodo, tiempo in tiempos.items():
    print(f"{metodo}: {tiempo:.4f} segundos")
