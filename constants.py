import pygame
import os


# Global functions

def load(name: str):
    """Loads an image from the assets folder"""
    if name.endswith(".png") or name.endswith(".jpg"):
        return pygame.transform.scale(pygame.image.load(os.path.join("assets", name)), (SQUARE_SIZE, SQUARE_SIZE))


def load_as_image(piece):
    """Returns the image for the piece

    Args:
        piece (Piece): The piece to get the image for

    Returns:
        image: The image representing the piece
    """
    switcher = {
        W: {
            PAWN: W_PAWN,
            KNIGHT: W_KNIGHT,
            BISHOP: W_BISHOP,
            KING: W_KING,
            ROOK: W_ROOK,
            QUEEN: W_QUEEN
        },
        B: {
            PAWN: B_PAWN,
            KNIGHT: B_KNIGHT,
            BISHOP: B_BISHOP,
            KING: B_KING,
            ROOK: B_ROOK,
            QUEEN: B_QUEEN
        }
    }
    return switcher[piece.color][piece.role]


# Constants

## Turn/Color
W = 0
B = 1

## Color to string
COLOR_TO_STRING = {W: "White", B: "Black"}
## Castling

KING_SIDE = 1
QUEEN_SIDE = 0

## Piece types
PAWN = 0
KNIGHT = 1
BISHOP = 2
KING = 3
ROOK = 4
QUEEN = 5
SLIDING_PIECES = [BISHOP, ROOK, QUEEN]

## Piece to string
PIECE_TO_STRING = {
    PAWN: "Pawn",
    KNIGHT: "Knight",
    BISHOP: "Bishop",
    KING: "King",
    ROOK: "Rook",
    QUEEN: "Queen"
}

## Debug
DEBUG = True

## FPS
FPS = 60
CLOCK = pygame.time.Clock()

## Window
SIZE = 8
WIDTH, HEIGHT = 800, 800
ROWS, COLS = SIZE, SIZE
SQUARE_SIZE = WIDTH // COLS
RADIUS = 10
FONT_SIZE = 20

## Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GREY = (128, 128, 128)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)

## Images
B_BISHOP = load("b_bishop.png")
B_KING = load("b_king.png")
B_KNIGHT = load("b_knight.png")
B_PAWN = load("b_pawn.png")
B_QUEEN = load("b_queen.png")
B_ROOK = load("b_rook.png")
W_BISHOP = load("w_bishop.png")
W_KING = load("w_king.png")
W_KNIGHT = load("w_knight.png")
W_PAWN = load("w_pawn.png")
W_QUEEN = load("w_queen.png")
W_ROOK = load("w_rook.png")

## Valid values for x and y
VALID_RANGE = range(0, SIZE)
