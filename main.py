# reimplementation from newcoder.io tutorial: http://newcoder.io/gui/

from Tkinter import *
import solver as sol

MARGIN = 20
SIDE = 50
WIDTH = HEIGHT = MARGIN * 2 + SIDE * 9

class SudokuError(Exception):
  """An application-specific error."""
  #pass

class SudokuBoard(object):
  """Sudku board representation."""
  def __init__(self, board_file):
    self.board = self.__create_board(board_file)

  def __create_board(self, board_file):
    board = []

    for line in board_file:
      line = line.strip()
      if len(line) != 9:
        raise SudokuError(
          "Each line in the puzzle must be 9 characters long."
        )
      board.append([])

      for c in line:
        if not c.isdigit():
          raise SudokuError(
            "Valid characters for the puzzle must be 0-9."
          )
        board[-1].append(int(c))

    if len(board) != 9:
      raise SudokuError(
        "Each puzzle must be 9 lines long."
      )

    return board

class SudokuGame(object):
  """A Sudoku game, in charge of storing the state of the board and
  checking whether the puzzle is completed."""
  def __init__(self, board_file):
    self.board_file = board_file
    self.start_puzzle = SudokuBoard(board_file).board

  def start(self):
    self.game_over = False
    self.puzzle = []
    for i in xrange(9):
      self.puzzle.append([])
      for j in xrange(9):
        self.puzzle[i].append(self.start_puzzle[i][j])

  def solve(self):
    grid = ""
    for i in xrange(9):
      for j in xrange(9):
        grid += str(self.puzzle[i][j])

    solved_grid = sol.solve(grid)

    for i in xrange(9):
      for j in xrange(9):
        self.puzzle[i][j] = int(solved_grid[9*i+j])
      
  def check_win(self):
    for row in xrange(9):
      if not self.__check_row(row):
        return False

    for col in xrange(9):
      if not self.__check_col(col):
        return False

    for row in xrange(3):
      for col in xrange(3):
        if not self.__check_square(row, col):
          return False

    self.game_over = True
    return True

  def __check_block(self, block):
    return set(block) == set(range(1,10))

  def __check_row(self, row):
    return self.__check_block(self.puzzle[row])

  def __check_col(self, col):
    return self.__check_block(
      [self.puzzle[row][col] for row in xrange(9)]
    )

  def __check_square(self, row, col):
    return self.__check_block(
      [
        self.puzzle[r][c]
        for r in xrange(row*3, (row+1)*3)
        for c in xrange(col*3, (col+1)*3)
      ]
    )

class SudokuUI(Frame):
  """The Tkinter UI, responsible for drawing the board and accepting input."""
  def __init__(self, parent, game):
    self.game = game
    Frame.__init__(self, parent)
    self.parent = parent

    self.row, self.col = -1, -1

    self.__initUI()

  def __initUI(self):
    self.parent.title("Sudoku Solver")
    self.pack(fill=BOTH, expand=1)

    self.canvas = Canvas(
      self,
      width=WIDTH,
      height=HEIGHT
    )
    #self.canvas.pack(fill=BOTH, side=TOP)
    self.canvas.grid(row=0)

    solve_button = Button(
      self,
      text="Solve",
      command=self.__solve
    )
    #solve_button.pack(fill=X, side=BOTTOM)
    solve_button.grid(row=1)

    clear_button = Button(
      self,
      text="Clear board",
      command=self.__clear_board
    )
    #clear_button.pack(fill=X, side=BOTTOM)
    clear_button.grid(row=2)

    self.__draw_grid()
    self.__draw_puzzle()

    self.canvas.bind("<Button-1>", self.__cell_clicked)
    self.canvas.bind("<Key>", self.__key_pressed)

  def __draw_grid(self):
    """Draws grid divided with blue line into 3x3 squares."""
    for i in xrange(10):
      color = "blue" if i % 3 == 0 else "gray"

      x0 = MARGIN + i * SIDE
      y0 = MARGIN
      x1 = MARGIN + i * SIDE
      y1 = HEIGHT - MARGIN
      self.canvas.create_line(x0, y0, x1, y1, fill=color)

      x0 = MARGIN
      y0 = MARGIN + i * SIDE
      x1 = WIDTH - MARGIN
      y1 = MARGIN + i * SIDE
      self.canvas.create_line(x0, y0, x1, y1, fill=color)

  def __draw_puzzle(self):
    self.canvas.delete("numbers")
    for i in xrange(9):
      for j in xrange(9):
        answer = self.game.puzzle[i][j]
        if answer != 0:
          x = MARGIN + j * SIDE + SIDE / 2
          y = MARGIN + i * SIDE + SIDE / 2
          original = self.game.start_puzzle[i][j]
          color = "black" if answer == original else "sea green"
          self.canvas.create_text(
            x, y, text=answer, tags="numbers", fill=color
          )

  def __draw_cursor(self):
    self.canvas.delete("cursor")
    if self.row >= 0 and self.col >= 0:
      x0 = MARGIN + self.col * SIDE + 1
      y0 = MARGIN + self.row * SIDE + 1
      x1 = MARGIN + (self.col + 1) * SIDE - 1
      y1 = MARGIN + (self.row + 1) * SIDE - 1
      self.canvas.create_rectangle(
        x0, y0, x1, y1,
        outline="red", tags="cursor"
      )

  def __draw_victory(self):
    x0 = y0 = MARGIN + SIDE * 2
    x1 = y1 = MARGIN + SIDE * 7
    self.canvas.create_oval(
      x0, y0, x1, y1,
      tags="victory", fill="dark orange", outline="orange"
    )

    # create text
    x = y = MARGIN + 4 * SIDE + SIDE / 2
    self.canvas.create_text(
      x, y,
      text="You win!", tags="victory",
      fill="white", font=("Arial", 32)
    )

  def __cell_clicked(self, event):
    if self.game.game_over:
      return

    x, y = event.x, event.y
    if (MARGIN < x < WIDTH - MARGIN and MARGIN < y < HEIGHT - MARGIN):
      self.canvas.focus_set()

      # get row and col numbers for x,y coords
      row, col = (y - MARGIN) / SIDE, (x - MARGIN) / SIDE

      # if cell was already selected, deselect it
      if (row, col) == (self.row, self.col):
        self.row, self.col = -1, -1
      elif self.game.puzzle[row][col] == 0:
        self.row, self.col = row, col
    else:
      self.row, self.col = -1, -1

    self.__draw_cursor()

  def __key_pressed(self, event):
    if self.game.game_over:
      return
    if self.row >= 0 and self.col >= 0 and event.char in "123456789":
      self.game.puzzle[self.row][self.col] = int(event.char)
      self.col, self.row = -1, -1
      self.__draw_puzzle()
      self.__draw_cursor()
      if self.game.check_win():
        self.__draw_victory()

  def __clear_board(self):
    self.game.start()
    self.canvas.delete("victory")
    self.__draw_puzzle()

  def __solve(self):
    self.game.solve()
    self.__draw_puzzle()
    self.__draw_cursor()

if __name__ == '__main__':
  with open('blank.sudoku', 'r') as boards_file:
    game = SudokuGame(boards_file)
    game.start()

    root = Tk()
    SudokuUI(root, game)
    root.geometry("%dx%d" % (WIDTH, HEIGHT + 40))
    root.mainloop()
