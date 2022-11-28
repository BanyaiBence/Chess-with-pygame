from piece import *
from constants import *
from position import Pos

pygame.init()
"""
    GRAMMAR:
        COLOR: 
            0 - WHITE
            1 - BLACK
        PIECE:
            0 - PAWN
            1 - KNIGHT
            2 - BISHOP
            3 - KING
            4 - ROOK
            5 - QUEEN
"""


class Window:
    """This class handles the window and the display, and all interactions with the user"""

    def __init__(self):
        """Initializes the window and sets the caption"""

        self.display = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chess")
        self.font_size = FONT_SIZE
        self.font = pygame.font.SysFont('arial', self.font_size)

    def update(self, board, selected_pos):
        """Updates the display

        Args:
            board (Board): The board to display
            selected_pos (Pos): The position of the selected piece
        """

        # Fill the background        
        self.display.fill(BLACK)

        # Draw the board squares
        for row in range(ROWS):
            for col in range(row % 2, ROWS, 2):
                pygame.draw.rect(self.display, WHITE, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

        # Mark tiles in the path of current check
        for check in board.checks:
            pygame.draw.rect(self.display, RED,
                             (check[0] * SQUARE_SIZE, check[1] * SQUARE_SIZE,
                              SQUARE_SIZE, SQUARE_SIZE))
        if board.color_in_check:
            king_x, king_y = board.get_king_position(board.color_in_check)
            pygame.draw.rect(self.display, RED,
                             (king_x * SQUARE_SIZE, king_y * SQUARE_SIZE,
                              SQUARE_SIZE, SQUARE_SIZE))

        for y, row in enumerate(board.tiles):
            for x, tile in enumerate(row):
                if tile.in_check_path:
                    pygame.draw.rect(self.display, RED,
                                     (x * SQUARE_SIZE, y * SQUARE_SIZE,
                                      SQUARE_SIZE, SQUARE_SIZE))

        # Draw the pieces
        for y, row in enumerate(board.tiles):
            for x, tile in enumerate(row):
                if tile.piece:
                    image = load_as_image(tile.piece)
                    self.display.blit(image, (tile.piece.pos.x * SQUARE_SIZE, tile.piece.pos.y * SQUARE_SIZE))

        # Draw a marker over the selected piece
        if selected_pos:
            pygame.draw.circle(self.display, GREEN, ((selected_pos[0] + 1) * SQUARE_SIZE - SQUARE_SIZE // 2,
                                                     (selected_pos[1] + 1) * SQUARE_SIZE - SQUARE_SIZE // 2), RADIUS)
            # Draw a marker over the tiles that the selected piece can move to/attack
            for pos in board.valid_moves[selected_pos]:
                pygame.draw.circle(self.display, BLUE,
                                   ((pos.x + 1) * SQUARE_SIZE - SQUARE_SIZE // 2,
                                    (pos.y + 1) * SQUARE_SIZE - SQUARE_SIZE // 2),
                                   RADIUS)

        # If a selected piece is a king, draw a marker over the tiles that the king can castle to
        for x, y in board.valid_castles:
            pygame.draw.circle(self.display, YELLOW,
                               ((x + 1) * SQUARE_SIZE - SQUARE_SIZE // 2,
                                (y + 1) * SQUARE_SIZE - SQUARE_SIZE // 2),
                               RADIUS)

        # Only draw the following if debug is enabled
        if DEBUG:

            for y, row in enumerate(board.tiles):
                for x, tile in enumerate(row):

                    # Draw the coordinates of each tile (according to the board)
                    cords = self.font.render(f"({x},{y})", True, RED)
                    self.display.blit(cords, (x * SQUARE_SIZE,
                                              y * SQUARE_SIZE))

                    # Draw the coordinates of each tile (according to chess)
                    col_dict = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F", 6: "G", 7: "H"}
                    mark = self.font.render(f"{col_dict[x]}{8 - y}", True, CYAN)
                    self.display.blit(mark, (x * SQUARE_SIZE,
                                             y * SQUARE_SIZE + self.font_size))

                    # Draw on all tiles that are under attack by white or black
                    w_mark = self.font.render("W", True, YELLOW)
                    b_mark = self.font.render("B", True, BLUE)
                    if tile.held_by_white:
                        self.display.blit(w_mark, (x * SQUARE_SIZE,
                                                   y * SQUARE_SIZE + 2 * self.font_size))
                    if tile.held_by_black:
                        self.display.blit(b_mark, (x * SQUARE_SIZE,
                                                   y * SQUARE_SIZE + 3 * self.font_size))

                    # Draw on all tiles that are pinned by white or black
                    wpin_mark = self.font.render("P", True, YELLOW)
                    bpin_mark = self.font.render("P", True, BLUE)
                    if tile.pinned_by_white:
                        self.display.blit(wpin_mark,
                                          (x * SQUARE_SIZE + self.font_size,
                                           y * SQUARE_SIZE + 2 * self.font_size))
                    if tile.pinned_by_black:
                        self.display.blit(bpin_mark,
                                          (x * SQUARE_SIZE + self.font_size,
                                           y * SQUARE_SIZE + 3 * self.font_size))
                    en_passant_mark = self.font.render("EP", True, GREY)
                    if tile.marked_for_en_passant:
                        self.display.blit(en_passant_mark,
                                          (x * SQUARE_SIZE,
                                          y * SQUARE_SIZE + 3 * self.font_size))

        # Finally, update the display
        pygame.display.update()


class Game:
    """This object is responsible for handling main game events"""

    def __init__(self):
        """Initializes the game"""

        self.board = Board()
        self.window = Window()
        self.event_handler = EventHandler()
        self.valid_moves = {}
        self.valid_castles = {}

    def update(self):
        self.window.update(self.board, self.event_handler.selected)
        self.event_handler.events(self.board)


class Tile:
    def __init__(self):
        self.piece = None
        self.held_by_black = False
        self.held_by_white = False
        self.marked_for_en_passant = False
        self.pinned_by_black = False
        self.pinned_by_white = False
        self.in_check_path = False

    def reset(self, reset_en_passant=False, reset_piece=False):
        self.held_by_white = False
        self.held_by_black = False
        self.pinned_by_black = False
        self.pinned_by_white = False
        self.in_check_path = False
        if reset_en_passant:
            self.marked_for_en_passant = False
        if reset_piece:
            self.piece = False

    def reset_en_passant(self):
        self.marked_for_en_passant = False




class EventHandler:
    def __init__(self):
        self.selected = None

    def events(self, board):
        # Get all events
        for event in pygame.event.get():
            # If the event is a quit event, quit the game
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            # If the event is a mouse click
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.selected = None
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Get the selected tile
                pos = pygame.mouse.get_pos()
                x, y = pos
                x, y = x // SQUARE_SIZE, y // SQUARE_SIZE
                pos = Pos(x, y)
                # If we have a piece selected, try to move it
                if self.selected:
                    if board.valid_moves[self.selected]:
                        if pos in board.valid_moves[self.selected]:
                            board.move(self.selected, pos)
                            board.calc_moves()
                # If the selected tile is not a piece, deselect it
                self.selected = None
                # If the selected tile is a piece, select it
                if pos.valid:
                    piece = board[pos].piece
                    if piece and piece.color == board.turn:
                        self.selected = piece.pos


class Board:
    def __init__(self):
        self.turn = W
        self.valid_moves = {}
        self.color_in_check = None
        self.checks = []
        self.selected_piece = None
        self.valid_castles = []
        self.available_castles = [[True, True], [True, True]]
        self.en_passant_target = None
        self.halfmove_clock = 0
        self.fullmove_clock = 1
        self.col_to_char = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}
        self.char_to_col = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}

        self.tiles = [[Tile() for _ in range(8)] for _ in range(8)]
        self.sim_tiles = [[Tile() for _ in range(8)] for _ in range(8)]

        self[Pos(0, 0)].piece = BlackRook(Pos(0, 0))
        self[Pos(7, 0)].piece = BlackRook(Pos(7, 0))
        self[Pos(1, 0)].piece = BlackKnight(Pos(1, 0))
        self[Pos(6, 0)].piece = BlackKnight(Pos(6, 0))
        self[Pos(2, 0)].piece = BlackBishop(Pos(2, 0))
        self[Pos(5, 0)].piece = BlackBishop(Pos(5, 0))
        self[Pos(4, 0)].piece = BlackKing(Pos(4, 0))
        self[Pos(3, 0)].piece = BlackQueen(Pos(3, 0))

        for index, tile in enumerate(self.tiles[1]):
            tile.piece = BlackPawn(Pos(index, 1))

        self[Pos(0, 7)].piece = WhiteRook(Pos(0, 7))
        self[Pos(7, 7)].piece = WhiteRook(Pos(7, 7))
        self[Pos(1, 7)].piece = WhiteKnight(Pos(1, 7))
        self[Pos(6, 7)].piece = WhiteKnight(Pos(6, 7))
        self[Pos(2, 7)].piece = WhiteBishop(Pos(2, 7))
        self[Pos(5, 7)].piece = WhiteBishop(Pos(5, 7))
        self[Pos(4, 7)].piece = WhiteKing(Pos(4, 7))
        self[Pos(3, 7)].piece = WhiteQueen(Pos(3, 7))

        for index, tile in enumerate(self.tiles[6]):
            tile.piece = WhitePawn(Pos(index, 6))
        self.calc_moves()

    def __getitem__(self, pos):
        return self.tiles[pos[1]][pos[0]]

    def init_moves(self):
        for row in self.tiles:
            for tile in row:
                if tile.piece:
                    self.valid_moves[tile.piece.pos] = []

    def reset_tiles(self):
        for row in self.tiles:
            for tile in row:
                tile.reset()

    def reset_en_passants(self):
        for row in self.tiles:
            for tile in row:
                tile.reset_en_passant()

    def change_turn(self):
        if self.turn == W:
            self.turn = B
        else:
            self.turn = W

    def castle(self, pos):
        old_king_pos = self.selected_piece.pos
        old_rook_pos = pos
        king = self.selected_piece
        rook = self[old_rook_pos].piece

        if old_rook_pos == Pos(0, 7):
            self[Pos(2, 7)].piece = king
            self[Pos(3, 7)].piece = rook
        elif old_rook_pos == Pos(7, 7):
            self[Pos(6, 7)].piece = king
            self[Pos(5, 7)].piece = rook
        elif old_rook_pos == Pos(0, 0):
            self[Pos(2, 0)].piece = king
            self[Pos(3, 0)].piece = rook
        elif old_rook_pos == Pos(7, 0):
            self[Pos(6, 0)].piece = king
            self[Pos(5, 0)].piece = rook

        self[old_king_pos].piece = None
        self[old_rook_pos].piece = None
        self.turn = abs(self.turn - 1)

        self.reset_tiles()
        self.calc_holds()

    def calc_holds(self):
        for row in self.tiles:
            for tile in row:
                if tile.piece:
                    tile.piece.holds(self)

    def mark_for_en_passant(self, pos):
        self[pos].marked_for_en_passant = True

    def demark_for_en_passant(self, pos):
        self[pos].marked_for_en_passant = False

    def to_fen(self):
        fen = ""
        role_dict = {
            0: "P",
            1: "N",
            2: "B",
            3: "K",
            4: "R",
            5: "Q"
        }
        empty_count = 0
        for row in self.tiles:
            for tile in row:
                if tile.piece:
                    if empty_count > 0:
                        fen += str(empty_count)
                        empty_count = 0
                    if tile.piece.color is W:
                        fen += role_dict[tile.piece.role]
                    elif tile.piece.color is B:
                        fen += role_dict[tile.piece.role].lower()
                else:
                    empty_count += 1
            if empty_count > 0:
                fen += str(empty_count)
                empty_count = 0
            fen += "/"
        fen = fen[:-1]
        if self.turn is W:
            fen += " w"
        else:
            fen += " b"

        fen += " "
        castling = False
        if self.available_castles[0][0]:
            fen += "K"
            castling = True
        if self.available_castles[0][1]:
            fen += "Q"
            castling = True
        if self.available_castles[1][0]:
            fen += "k"
            castling = True
        if self.available_castles[1][1]:
            fen += "q"
            castling = True
        if not castling:
            fen += "-"
        fen += " "
        if self.en_passant_target:
            fen += self.en_passant_target
        else:
            fen += "-"
        fen += " " + str(self.halfmove_clock)
        fen += " " + str(self.fullmove_clock)
        return fen

    def can_castle(self, color=W, side=QUEEN_SIDE):
        rook = False
        empty = True
        king = False
        if color is W:
            if side is QUEEN_SIDE:
                tile = self.tiles[7][0]
                rook = tile.piece and tile.piece.role is ROOK and tile.piece.color is W
                for i in range(1, 4):
                    tile = self.tiles[7][i]
                    empty = empty and not tile.piece
                tile = self.tiles[7][4]
                king = tile.piece and tile.piece.role is KING and tile.piece.color is W
            elif side is KING_SIDE:
                tile = self.tiles[7][7]
                rook = tile.piece and tile.piece.role is ROOK and tile.piece.color is W
                for i in range(4, 6):
                    tile = self.tiles[7][i]
                    empty = empty and not tile.piece
                tile = self.tiles[7][4]
                king = tile.piece and tile.piece.role is KING and tile.piece.color is W
        elif color is B:
            if side is QUEEN_SIDE:
                tile = self.tiles[0][0]
                rook = tile.piece and tile.piece.role is ROOK and tile.piece.color is B
                for i in range(1, 4):
                    tile = self.tiles[0][i]
                    empty = empty and not tile.piece
                tile = self.tiles[0][4]
                king = tile.piece and tile.piece.role is KING and tile.piece.color is B
            elif side is KING_SIDE:
                tile = self.tiles[0][7]
                rook = tile.piece and tile.piece.role is ROOK and tile.piece.color is B
                for i in range(4, 6):
                    tile = self.tiles[0][i]
                    empty = empty and not tile.piece
                tile = self.tiles[0][4]
                king = tile.piece and tile.piece.role is KING and tile.piece.color is B
        return rook and empty and king

    def check_pawn_to_queen(self):
        for row in self.tiles:
            for tile in row:
                if tile.piece:
                    piece = tile.piece
                    if piece.role is PAWN:
                        if tile.piece.color is W and piece.pos.y == 0:
                            tile.piece = WhiteQueen(piece.pos)
                        elif piece.color is B and piece.pos.y == 7:
                            tile.piece = BlackQueen(piece.pos)

    def move(self, old_pos, new_pos):
        if self.en_passant_target:
            tx = self.char_to_col[self.en_passant_target[0]]
            ty = int(self.en_passant_target[1])
            self.demark_for_en_passant(Pos(tx, ty))
        self.en_passant_target = ""

        if not new_pos.valid:
            return
        s_piece = self[old_pos].piece
        if not s_piece:
            return

        s_piece.pos = new_pos

        self[new_pos].piece = s_piece
        self[old_pos].piece = None

        # If pawn moved 2 tiles, mark the tile behind it for en passant
        if s_piece.role is PAWN and abs(new_pos.y - old_pos.y) > 1:
            if s_piece.color is W:
                self.mark_for_en_passant(new_pos + Pos(0, 1))
                self.en_passant_target = self.col_to_char[new_pos.x] + str((8 - new_pos.y) - 1)
            elif s_piece.color is B:
                self.mark_for_en_passant(new_pos + Pos(0, -1))
                self.en_passant_target = self.col_to_char[new_pos.x] + str((8 - new_pos.y) + 1)

        self.change_turn()
        self.check_pawn_to_queen()

    def get_king_position(self, color):
        for row in self.tiles:
            for tile in row:
                if tile.piece and tile.piece.color is color and tile.piece.role is KING:
                    return tile.piece.pos

    def calc_moves(self):
        self.reset_tiles()
        self.valid_moves = {}
        self.init_moves()
        self.color_in_check = None
        self.checks = []
        for row in self.tiles:
            for tile in row:
                if tile.piece:
                    tile.piece.holds(self)
        for row in self.tiles:
            for tile in row:
                if tile.piece:
                    tile.piece.moves(self)
        self.reset_en_passants()

        for row in self.tiles:
            for tile in row:
                if tile.piece:
                    if tile.piece.color is W and tile.pinned_by_black:
                        self.valid_moves[tile.piece.pos] = []
                    elif tile.piece.color is B and tile.pinned_by_white:
                        self.valid_moves[tile.piece.pos] = []
        if self.color_in_check:
            if self.color_in_check is W:
                king_pos = self.get_king_position(W)
            else:
                king_pos = self.get_king_position(B)

            checker_pos = self.checks[0]
            for pos, moves in self.valid_moves.items():
                new_moves = []
                for move in moves:
                    if self[move].in_check_path:
                        new_moves.append(move)
                    elif move == checker_pos:
                        new_moves.append(move)
                    elif king_pos == pos:
                        new_moves.append(move)
                self.valid_moves[pos] = new_moves
            checkmate = True
            for pos, moves in self.valid_moves.items():
                if len(moves) > 0:
                    checkmate = False

            if checkmate:
                print("Checkmate")
                if self.color_in_check is W:
                    print("Black wins")
                else:
                    print("White wins")
                quit()

        """
        TODO:
        A deepcopy használata helyett hozzáadhatnánk a Board osztához egy sim_tiles nevű változót.
        Simulációk során a sim_tiles változóban tárolnánk a jelenlegi táblát.
        Majd adunk az osztályhoz egy sim_move metódust, ami a sim_tiles változóban lévő táblát módosítja.
        És egy sim_pseudo_valid_moves metódust, ami a sim_tiles változóban lévő táblát vizsgálja.
        Ekkor nem kell a teljes osztályt lemásolni, csak a változókat.
        2022.11.21. 02:36
        """

    def __repr__(self):
        result = ""
        for row in self.tiles:
            for tile in row:
                if tile.piece:
                    result += str(tile.piece) + " "
                else:
                    result += "  "
            result += "\n"
        return result


if __name__ == "__main__":
    run = True
    game = Game()
    while run:
        CLOCK.tick(FPS)
        game.update()
