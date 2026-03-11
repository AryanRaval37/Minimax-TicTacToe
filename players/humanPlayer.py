import pygame
import sys
import math

# ──────────────────────────────────────────────
#  Layout constants
# ──────────────────────────────────────────────
WINDOW_W   = 560
WINDOW_H   = 660
CELL       = 140          # each cell is 140×140 – perfect square
GRID_SIZE  = CELL * 3     # 420
GRID_OFF   = (WINDOW_W - GRID_SIZE) // 2   # 70 – horizontal centre
GRID_TOP   = 130
LINE_W     = 4
SYMBOL_PAD = 22

# ──────────────────────────────────────────────
#  Palette
# ──────────────────────────────────────────────
BG_TOP         = (15,  17,  35)
BG_BOT         = (28,  30,  55)
GRID_COLOR     = (60,  65, 110)
X_COLOR        = (94, 196, 255)
O_COLOR        = (255, 107, 156)
X_GLOW         = (30,  80, 160)
O_GLOW         = (140,  30,  80)
RESULT_BG      = (10,  12,  28)
TEXT_COLOR     = (220, 225, 255)
SUBTITLE_COLOR = (130, 135, 180)
ACCENT         = (94, 196, 255)


# ──────────────────────────────────────────────
#  Drawing helpers
# ──────────────────────────────────────────────
def _lerp(a, b, t):
    return a + (b - a) * t


def _gradient_bg(surf):
    for y in range(WINDOW_H):
        t = y / WINDOW_H
        r = int(_lerp(BG_TOP[0], BG_BOT[0], t))
        g = int(_lerp(BG_TOP[1], BG_BOT[1], t))
        b = int(_lerp(BG_TOP[2], BG_BOT[2], t))
        pygame.draw.line(surf, (r, g, b), (0, y), (WINDOW_W, y))


def _draw_x(surf, cx, cy, size, color, glow_color):
    thickness = max(7, size // 9)
    p1 = (cx - size // 2 + SYMBOL_PAD, cy - size // 2 + SYMBOL_PAD)
    p2 = (cx + size // 2 - SYMBOL_PAD, cy + size // 2 - SYMBOL_PAD)
    p3 = (cx + size // 2 - SYMBOL_PAD, cy - size // 2 + SYMBOL_PAD)
    p4 = (cx - size // 2 + SYMBOL_PAD, cy + size // 2 - SYMBOL_PAD)
    pygame.draw.line(surf, glow_color, p1, p2, thickness + 6)
    pygame.draw.line(surf, glow_color, p3, p4, thickness + 6)
    pygame.draw.line(surf, color, p1, p2, thickness)
    pygame.draw.line(surf, color, p3, p4, thickness)


def _draw_o(surf, cx, cy, size, color, glow_color):
    radius    = size // 2 - SYMBOL_PAD
    thickness = max(7, size // 9)
    pygame.draw.circle(surf, glow_color, (cx, cy), radius, thickness + 6)
    pygame.draw.circle(surf, color,      (cx, cy), radius, thickness)


def _pos_from_mouse(mx, my):
    """Return board position 1-9 from mouse, or None if outside grid."""
    if mx < GRID_OFF or mx >= GRID_OFF + GRID_SIZE:
        return None
    if my < GRID_TOP or my >= GRID_TOP + GRID_SIZE:
        return None
    col = (mx - GRID_OFF) // CELL
    row = (my - GRID_TOP) // CELL
    return int(row) * 3 + int(col) + 1


# ──────────────────────────────────────────────
#  HumanPlayer
# ──────────────────────────────────────────────
class HumanPlayer:
    """
    Human player with a Pygame UI window.
    player = 'X' or 'O'.
    """

    def __init__(self, player: str = "X"):
        player = player.upper()
        if player not in ("X", "O"):
            raise ValueError("player must be 'X' or 'O'")
        self._symbol = player
        self.player  = player
        self.mark    = 1 if player == "X" else -1
        self._title  = "Tic Tac Toe"

        pygame.init()
        self._screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
        pygame.display.set_caption(self._title)

        self._font_title   = pygame.font.SysFont("Arial", 36, bold=True)
        self._font_status  = pygame.font.SysFont("Arial", 22, bold=True)
        self._font_result  = pygame.font.SysFont("Arial", 48, bold=True)
        self._font_hint    = pygame.font.SysFont("Arial", 20)

        self._clock       = pygame.time.Clock()
        self._board_state = [0] * 9
        self._hover_cell  = None
        self._waiting     = False
        self._result_txt  = None
        self._tick        = 0

    # ── public API ──────────────────────────────

    def play(self, board) -> int:
        """Block until the human clicks a valid cell. Returns position 1-9."""
        # Detect actual side assigned by engine (X moves first)
        num_pieces = sum(1 for x in board.arr if x != 0)
        self.mark = 1 if num_pieces % 2 == 0 else -1
        self.player = "X" if self.mark == 1 else "O"
        self._symbol = self.player

        self._board_state = list(board.arr)
        self._waiting     = True
        self._result_txt  = None

        while self._waiting:
            self._tick += 1
            self._handle_events(board)
            self._draw()
            self._clock.tick(60)

        return self._choice

    def onResult(self, result_code: int, board=None):
        """Called by the engine after the game ends."""
        if board is not None:
            self._board_state = list(board.arr)

        if result_code == 0:
            self._result_txt = "It's a Draw!"
        elif result_code == self.mark:
            self._result_txt = "You Win!"
        else:
            self._result_txt = "You Lose!"

        running = True
        while running:
            self._tick += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    running = False
            self._draw()
            self._clock.tick(60)

        pygame.quit()

    # ── internals ───────────────────────────────

    def _handle_events(self, board):
        mx, my = pygame.mouse.get_pos()
        self._hover_cell = _pos_from_mouse(mx, my)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = _pos_from_mouse(*event.pos)
                if pos is not None and board.isLegalMove(pos):
                    self._choice = pos
                    self._board_state[pos - 1] = self.mark
                    self._waiting = False

    # ── drawing ─────────────────────────────────

    def _draw(self):
        _gradient_bg(self._screen)
        self._draw_header()
        self._draw_grid()
        self._draw_symbols()
        if self._result_txt:
            self._draw_result_overlay()
        pygame.display.flip()

    def _draw_header(self):
        # Title
        ts = self._font_title.render(self._title, True, TEXT_COLOR)
        self._screen.blit(ts, (WINDOW_W // 2 - ts.get_width() // 2, 20))

        # Accent underline
        acc = pygame.Surface((200, 3))
        acc.fill(ACCENT)
        self._screen.blit(acc, (WINDOW_W // 2 - 100, 62))

        # Status
        if self._waiting:
            txt   = f"Your turn  -  You are {self._symbol}"
            color = X_COLOR if self.mark == 1 else O_COLOR
        elif self._result_txt:
            txt   = f"You are {self._symbol}"
            color = X_COLOR if self.mark == 1 else O_COLOR
        else:
            txt   = f"Move confirmed  -  You are {self._symbol}"
            color = SUBTITLE_COLOR
        ss = self._font_status.render(txt, True, color)
        self._screen.blit(ss, (WINDOW_W // 2 - ss.get_width() // 2, 78))

    def _draw_grid(self):
        for row in range(3):
            for col in range(3):
                x   = GRID_OFF + col * CELL
                y   = GRID_TOP + row * CELL
                pos = row * 3 + col + 1

                cell_s = pygame.Surface((CELL, CELL), pygame.SRCALPHA)
                cell_s.fill((255, 255, 255, 10))
                self._screen.blit(cell_s, (x, y))

                if pos == self._hover_cell and self._board_state[pos - 1] == 0:
                    hov = pygame.Surface((CELL, CELL), pygame.SRCALPHA)
                    a   = 50 + int(20 * math.sin(self._tick * 0.08))
                    c   = X_COLOR if self.mark == 1 else O_COLOR
                    hov.fill((*c, a))
                    self._screen.blit(hov, (x, y))

        for i in range(1, 3):
            pygame.draw.line(self._screen, GRID_COLOR,
                             (GRID_OFF + i * CELL, GRID_TOP),
                             (GRID_OFF + i * CELL, GRID_TOP + GRID_SIZE), LINE_W)
            pygame.draw.line(self._screen, GRID_COLOR,
                             (GRID_OFF, GRID_TOP + i * CELL),
                             (GRID_OFF + GRID_SIZE, GRID_TOP + i * CELL), LINE_W)

    def _draw_symbols(self):
        for idx, val in enumerate(self._board_state):
            if val == 0:
                continue
            col = idx % 3
            row = idx // 3
            cx  = GRID_OFF + col * CELL + CELL // 2
            cy  = GRID_TOP + row * CELL + CELL // 2
            if val == 1:
                _draw_x(self._screen, cx, cy, CELL, X_COLOR, X_GLOW)
            else:
                _draw_o(self._screen, cx, cy, CELL, O_COLOR, O_GLOW)

    def _draw_result_overlay(self):
        ov = pygame.Surface((WINDOW_W, WINDOW_H), pygame.SRCALPHA)
        ov.fill((*RESULT_BG, 210))
        self._screen.blit(ov, (0, 0))

        scale = 1.0 + 0.04 * math.sin(self._tick * 0.07)
        rs    = self._font_result.render(self._result_txt, True, TEXT_COLOR)
        rw    = int(rs.get_width()  * scale)
        rh    = int(rs.get_height() * scale)
        rs    = pygame.transform.smoothscale(rs, (rw, rh))
        self._screen.blit(rs, (WINDOW_W // 2 - rw // 2, WINDOW_H // 2 - rh // 2 - 20))

        hint = self._font_hint.render("Click anywhere to continue", True, SUBTITLE_COLOR)
        self._screen.blit(hint, (WINDOW_W // 2 - hint.get_width() // 2,
                                 WINDOW_H // 2 + rh // 2 + 16))
