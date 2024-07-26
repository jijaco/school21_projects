def mul(A, B):
    rows_A = len(A)
    cols_A = len(A[0])
    rows_B = len(B)
    cols_B = len(B[0])
    result = [[0 for row in range(cols_B)] for col in range(rows_A)]
    for s in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                result[s][j] += A[s][k] * B[k][j]
    return result
