#!/usr/bin/env python3

state = [
    [206, 243, 61, 34],
    [171, 11, 93, 31],
    [16, 200, 91, 108],
    [150, 3, 194, 51],
]

round_key = [
    [173, 129, 68, 82],
    [223, 100, 38, 109],
    [32, 189, 53, 8],
    [253, 48, 187, 78],
]

def matrix2bytes(matrix):
    """ Converts a 4x4 matrix into a 16-byte array.  """
    text = b""
    for i in range(0, len(matrix)):
        text += b"".join(int.to_bytes(k) for k in (matrix[i]))
        print(text)

def add_round_key(s, k):
    enc = b""

    for x in range(0, len(s)):
        for y in range(0, len(s[x])):
            #print(s[x][y] ^ k[x][y])
            enc += int.to_bytes(s[x][y] ^ k[x][y])

    return enc


print(add_round_key(state, round_key))

