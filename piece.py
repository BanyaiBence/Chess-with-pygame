from constants import *
from position import Pos


def can_step(board, pos):
    return True if pos.valid and not board[pos].piece else False


def can_en_passant(board, pos):
    if pos.valid and board[pos].marked_for_en_passant:
        return True
    return False


class Piece:
    def __init__(self, role, color, pos):
        self.role = role
        self.color = color
        self.pos = pos

    def seek_step(self, board, pos):
        if can_step(board, pos):
            board.valid_moves[self.pos].append(pos)
            return True
        return False

    def can_attack(self, board, pos):
        if pos.valid:
            piece = board[pos].piece
            if piece and piece.color != self.color:
                return True
        return False

    def seek_attack(self, board, pos):
        if self.can_attack(board, pos):
            board.valid_moves[self.pos].append(pos)
            return True
        return False

    def check(self, board):
        if self.color is W:
            board.color_in_check = B
        else:
            board.color_in_check = W
        board.checks.append(self.pos)

    def can_check(self, board, pos):
        if pos.valid:
            piece = board[pos].piece
            return piece and piece.color != self.color and piece.role is KING
        return False

    def seek_check(self, board, pos):
        if self.can_check(board, pos):
            self.check(board)
            return True
        return False

    def can_move(self, board, pos):
        return can_step(board, pos) or self.can_attack(board, pos)

    def seek_move(self, board, pos):
        if self.can_move(board, pos):
            board.valid_moves[self.pos].append(pos)
            return True
        return False

    def hold(self, board, pos):
        if pos.valid:
            tile = board[pos]
            if self.color is W:
                tile.held_by_white = True
            elif self.color is B:
                tile.held_by_black = True

    def hold_tiles(self, board, list_of_pos):
        for pos in list_of_pos:
            self.hold(board, pos)

    def __repr__(self):
        return f"{COLOR_TO_STRING[self.color]} {PIECE_TO_STRING[self.role]} at {self.pos.to_notation()}"


class SlidingPiece(Piece):
    def __init__(self, color, role, pos, offsets):
        self.offsets = offsets
        super().__init__(role, color, pos)

    def pin(self, board, pos):
        if pos.valid:
            tile = board[pos]
            if self.color is W:
                tile.pinned_by_white = True
            elif self.color is B:
                tile.pinned_by_black = True

    def holds(self, board):
        # Iterating through offsets
        for offset in self.offsets:
            pos = self.pos + offset
            # If the tile is valid and empty, hold it
            while can_step(board, pos):
                self.hold(board, pos)
                pos += offset
            # If the tile is valid and occupied by an enemy piece, hold it
            if self.can_attack(board, pos):
                self.hold(board, pos)

            # If the tile is valid and occupied by the enemy king, give check
            if self.can_check(board, pos):
                self.check(board)
                # Mark tiles in the path of the king as in check path
                cast_pos = self.pos + offset
                board[pos].in_check_path = True
                while can_step(board, cast_pos):
                    board[cast_pos].in_check_path = True
                    cast_pos += offset

            # Pinning an enemy piece if their king is behind them
            pin_pos = pos + offset
            while can_step(board, pos):
                pos += offset
            if self.can_check(board, pos):
                self.pin(board, pin_pos)

    def moves(self, board):
        for offset in self.offsets:
            pos = self.pos + offset
            while self.seek_step(board, pos):
                pos += offset
            self.seek_attack(board, pos)


class Rook(SlidingPiece):
    def __init__(self, color, pos):
        offsets = [Pos(1, 0), Pos(-1, 0), Pos(0, 1), Pos(0, -1)]
        super().__init__(color, ROOK, pos, offsets)


class Bishop(SlidingPiece):
    def __init__(self, color, pos):
        offsets = [Pos(1, 1), Pos(1, -1), Pos(-1, 1), Pos(-1, -1)]
        super().__init__(color, BISHOP, pos, offsets)


class Queen(SlidingPiece):
    def __init__(self, color, pos):
        offsets = [Pos(1, 0), Pos(-1, 0), Pos(0, 1), Pos(0, -1), Pos(1, 1), Pos(1, -1), Pos(-1, 1), Pos(-1, -1)]
        super().__init__(color, QUEEN, pos, offsets)


class Knight(Piece):
    def __init__(self, color, pos):
        self.offsets = [Pos(1, 2), Pos(2, 1), Pos(-1, 2), Pos(-2, 1), Pos(1, -2), Pos(2, -1), Pos(-1, -2), Pos(-2, -1)]
        super().__init__(KNIGHT, color, pos)

    def moves(self, board):
        for offset in self.offsets:
            self.seek_move(board, self.pos + offset)
            self.seek_check(board, self.pos + offset)

    def holds(self, board):
        held_tiles = []
        for offset in self.offsets:
            held_tiles.append(self.pos + offset)
        self.hold_tiles(board, held_tiles)


class King(Piece):
    def __init__(self, color, pos):
        self.offsets = [Pos(1, 0), Pos(-1, 0), Pos(0, 1), Pos(0, -1), Pos(1, 1), Pos(1, -1), Pos(-1, 1), Pos(-1, -1)]
        super().__init__(KING, color, pos)

    def can_move(self, board, pos):
        if pos.valid:
            tile = board[pos]
            not_attacked = not tile.held_by_white if self.color is B else not tile.held_by_black
            can_move = super().can_move(board, pos)
            return can_move and not_attacked
        return False

    def seek_move(self, board, pos):
        if self.can_move(board, pos):
            board.valid_moves[self.pos].append(pos)

    def moves(self, board):
        for offset in self.offsets:
            self.seek_move(board, self.pos + offset)

    def holds(self, board):
        for offset in self.offsets:
            self.hold(board, self.pos + offset)


class Pawn(Piece):
    def __init__(self, color, pos):
        super().__init__(PAWN, color, pos)

    def seek_en_passant(self, board, pos):
        if can_en_passant(board, pos):
            board.valid_moves[self.pos].append(pos)


class WhitePawn(Pawn):
    def __init__(self, position):
        super().__init__(W, position)

    def moves(self, board):
        if can_step(board, self.pos + Pos(0, -1)) and self.pos.y == 6:
            self.seek_step(board, self.pos + Pos(0, -2))

        self.seek_step(board, self.pos + Pos(0, -1))
        self.seek_attack(board, self.pos + Pos(1, -1))
        self.seek_check(board, self.pos + Pos(1, -1))
        self.seek_en_passant(board, self.pos + Pos(1, -1))
        self.seek_attack(board, self.pos + Pos(-1, -1))
        self.seek_check(board, self.pos + Pos(-1, -1))
        self.seek_en_passant(board, self.pos + Pos(-1, -1))

    def holds(self, board):
        self.hold(board, self.pos + Pos(1, -1))
        self.hold(board, self.pos + Pos(-1, -1))


class BlackPawn(Pawn):
    def __init__(self, pos):
        super().__init__(B, pos)

    def moves(self, board):
        if can_step(board, self.pos + Pos(0, 1)) and self.pos.y == 1:
            self.seek_step(board, self.pos + Pos(0, 2))

        self.seek_step(board, self.pos + Pos(0, 1))
        self.seek_attack(board, self.pos + Pos(1, 1))
        self.seek_check(board, self.pos + Pos(1, 1))
        self.seek_en_passant(board, self.pos + Pos(1, 1))
        self.seek_attack(board, self.pos + Pos(-1, 1))
        self.seek_check(board, self.pos + Pos(-1, 1))
        self.seek_en_passant(board, self.pos + Pos(-1, 1))

    def holds(self, board):
        self.hold(board, self.pos + Pos(1, 1))
        self.hold(board, self.pos + Pos(-1, 1))


class WhiteRook(Rook):
    def __init__(self, pos):
        super().__init__(W, pos)


class BlackRook(Rook):
    def __init__(self, pos):
        super().__init__(B, pos)


class WhiteKnight(Knight):
    def __init__(self, pos):
        super().__init__(W, pos)


class BlackKnight(Knight):
    def __init__(self, pos):
        super().__init__(B, pos)


class WhiteBishop(Bishop):
    def __init__(self, pos):
        super().__init__(W, pos)


class BlackBishop(Bishop):
    def __init__(self, pos):
        super().__init__(B, pos)


class WhiteQueen(Queen):
    def __init__(self, pos):
        super().__init__(W, pos)


class BlackQueen(Queen):
    def __init__(self, pos):
        super().__init__(B, pos)


class WhiteKing(King):
    def __init__(self, pos):
        super().__init__(W, pos)

    def can_move(self, board, pos):
        if pos.valid:
            tile = board[pos]
            return super().can_move(board, pos) and not tile.held_by_black
        return False


class BlackKing(King):
    def __init__(self, pos):
        super().__init__(B, pos)

    def can_move(self, board, pos):
        if pos.valid:
            tile = board[pos]
            return super().can_move(board, pos) and not tile.held_by_white
        return False
