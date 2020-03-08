PIECES = """11111111
10000000
10110100
00010011
00101001
01000100
01010111
11111101
00000000
11010111
11110101
01011110
11001101
10101010
00011000
10101100"""

BORDER = [1, 4, 6, 11, 24, 29, 31, 34]
POSITIONS = [7, 8, 9, 10, 13, 14, 15, 16, 19, 20, 21, 22, 25, 26, 27, 28]


class Piece:
    def __init__(self, bits):
        self.id = int(bits, 2)
        self.bits = bits
        self.sides = tuple(int(bits[n:n + 2], 2) for n in range(0, 7, 2))
        self.rotates = []
        for rotate in set(((self.sides + self.sides)[n:n + 4] for n in range(4))):
            self.rotates.append(dict((n, v if n < 2 else int("{:02b}".format(v)[::-1], 2)) for n, v in enumerate(rotate)))

    def __repr__(self):
        return "{0: >3} {1:0>8}: {2}".format(self.id, bin(self.id)[2:], self.rotates)


def check(board, pos):
    for delta, p1, p2 in ((-6, 0, 2), (-1, 3, 1), (1, 1, 3), (6, 2, 0)):
        try:
            border1, border2 = board[pos][p1], board[pos + delta][p2]
            if (pos + delta in BORDER and border1 & border2) or (pos + delta not in BORDER and not border1 ^ border2 == 3):
                return False
        except KeyError:
            pass
    return True


def explore(board, pieces, positions, solution=[]):
    if not pieces:
        print(" ".join(str(p) for (p, r) in solution))
        return
    pos, positions = positions[0], positions[1:]
    for n, piece in enumerate(pieces):
        lefts = pieces[:n] + pieces[n + 1:]
        for rotate in piece.rotates:
            board[pos] = rotate
            if check(board, pos):
                explore(board, lefts, positions, solution + [(piece.id, rotate)])
            del board[pos]


solutions = explore({1: {2: 0b01}, 4: {2: 0b01},
                     6: {1: 0b10}, 24: {1: 0b10},
                     11: {3: 0b01}, 29: {3: 0b01},
                     31: {0: 0b10}, 34: {0: 0b10}},
                    [Piece(bits) for bits in PIECES.split("\n")], POSITIONS)
