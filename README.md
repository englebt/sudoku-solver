# Sudoku Solver

This is a Sudoku solver patterned from [Peter Norvig's solver](http://norvig.com/sudopy.html), along with an interface implemented with Tkinter, following examples found at [newcoder.io](http://newcoder.io/gui/). Changes include converting the main UI to use the grid component and including a Solve button. The solve method converts the existing grid object into a string passed to the solver, which returns a solved string. The UI's solve method then converts the solved string back into a working grid object and populates the grid.
