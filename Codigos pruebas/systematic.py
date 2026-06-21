import numpy as np

def gf2_row_reduce_to_systematic(G):
    """Convierte G a forma sistemática [I_k | P] y devuelve P."""
    G = G.copy() % 2
    k, n = G.shape
    pivot_cols = []
    row = 0

    for col in range(n):
        if row >= k:
            break
        pivot = None
        for r in range(row, k):
            if G[r, col] == 1:
                pivot = r
                break
        if pivot is None:
            continue
        if pivot != row:
            G[[row, pivot]] = G[[pivot, row]]
        pivot_cols.append(col)
        for r in range(k):
            if r != row and G[r, col] == 1:
                G[r] ^= G[row]
        row += 1

    if len(pivot_cols) != k:
        raise ValueError("La matriz no tiene rango completo.")

    # Reordenar columnas para que los pivotes estén al inicio
    non_pivot_cols = [j for j in range(n) if j not in pivot_cols]
    ordered_cols = pivot_cols + non_pivot_cols
    G_sys = G[:, ordered_cols]
    return G_sys, pivot_cols, ordered_cols

def compute_parity_check_matrix(G):
    """Calcula H a partir de G (binario)."""
    G_sys, pivots, order = gf2_row_reduce_to_systematic(G)
    k, n = G_sys.shape
    P = G_sys[:, k:]  # Parte derecha: k x (n - k)
    H_right = np.eye(n - k, dtype=int)  # I_{n-k}
    H_left = P.T  # P^T, tamaño (n - k) x k
    H_sys = np.hstack([H_left, H_right])  # (n - k) x n
    # Ahora deshacemos la permutación de columnas
    # 'order' indica: nueva_col[i] = vieja_col[order[i]]
    # Queremos H tal que H @ c_original^T = 0
    # Entonces: H = H_sys @ Pi, donde Pi reordena según 'order'
    inv_order = np.argsort(order)  # inversa de la permutación
    H = H_sys[:, inv_order]
    return H % 2

# ==============================
# Ejemplo: código de Hamming [7,4]
# ==============================
if __name__ == "__main__":
    G = np.array([
        [1, 1, 0, 1, 0, 0, 0],
        [0, 1, 1, 0, 1, 0, 0],
        [1, 1, 1, 0, 0, 1, 0],
        [1, 0, 1, 0, 0, 0, 1]
    ])

    print("Matriz generadora G (4x7):")
    print(G)

    H = compute_parity_check_matrix(G)
    print("\nMatriz de paridad H (3x7):")
    print(H)

    # Verificación: G @ H^T = 0
    product = (G @ H.T) % 2
    print("\nVerificación G * H^T (debe ser matriz cero 4x3):")
    print(product)
