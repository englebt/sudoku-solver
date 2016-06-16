# Originally published by Peter Norvig: http://norvig.com/sudopy.shtml

def cross(A, B):
  """Cross product of elements in A and B."""
  return [a+b for a in A for b in B]

# Define our variables
digits = '123456789'
rows = 'ABCDEFGHI'
cols = digits
squares = cross(rows, cols)
unitlist = ([cross(rows, c) for c in cols] +
            [cross(r, cols) for r in rows] +
            [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')])
units = dict((s, [u for u in unitlist if s in u])
             for s in squares)
peers = dict((s, set(sum(units[s],[]))-set([s]))
             for s in squares)

grid1  = '003020600900305001001806400008102900700000008006708200002609500800203009005010300'
grid2  = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'

########## Parsing the Grid ##########

def parse_grid(grid):
  """Convert grid to dict of possible values, {square: digits},
  return False if contradiction detected."""
  values = dict((s, digits) for s in squares)
  for s,d in grid_values(grid).items():
    if d in digits and not assign(values, s, d):
      return false

  return values

def grid_values(grid):
  """Convert grid into dict {square: char} with '0' or '.' for empties."""
  chars = [c for c in grid if c in digits or c in '0.']
  assert len(chars) == 81
  return dict(zip(squares, chars))

########## Propagating Constraints ##########

def assign(values, s, d):
  """Eliminate all values not d from values[s] and propagate.
  Return values, return false if contradiction."""
  other_values = values[s].replace(d, '')
  if all(eliminate(values, s, d2) for d2 in other_values):
    return values
  else:
    return False

def eliminate(values, s, d):
  """Eliminate d from values[s]; propagate when values or places <= 2.
  Return values, except return False if contradiction detected."""
  if d not in values[s]:
    return values # Already eliminated
  values[s] = values[s].replace(d,'')
  # If a square is reduced to one vlaue, eliminate value from peers.
  if len(values[s]) == 0:
    return False
  elif len(values[s]) == 1:
    d2 = values[s]
    if not all(eliminate(values, s2, d2) for s2 in peers[s]):
      return False

  for u in units[s]:
    dplaces = [s for s in u if d in values[s]]
    if len(dplaces) == 0:
      return False
    elif len(dplaces) == 1:
      if not assign(values, dplaces[0], d):
        return False

  return values

########## Displaying the Grid ##########

def display(values):
  "Display the 2D grid"
  width = 1 + max(len(values[s]) for s in squares)
  line = '+'.join(['-' * (width * 3)] * 3)
  for r in rows:
    print ''.join(values[r+c].center(width) + ('|' if c in '36' else '')
                  for c in cols)
    if r in 'CF':
      print line
  print

########## Search ##########

def solve(grid):
  search(parse_grid(grid))

def search(values):
  """Using depth-first search and propoagation, try all possible values."""
  if values is False:
    return False
  if all(len(values[s]) == 1 for s in squares):
    return values

  # Choose the unfilled square with fewest possibilities.
  n,s = min((len(values[s]), s) for s in squares if len(values[s]) > 1)
  return some(search(assign(values.copy(), s, d))
              for d in values[s])

def some(seq):
  for e in seq:
    if e:
      return e
  return False
