S = AlphabeticString()
E =TranspositionCryptoSystem(S, 5)
K = PermutationGroupElement('(2, 3, 4, 5, 1)')
L = E.inverse_key(K)
M = S('CODINGANDCRYPTO')
e = E(K)
C = E(L)
e(M)

# INCODDCGANTORYP