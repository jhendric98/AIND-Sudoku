import sys
import logging
logging.basicConfig(filename='solution.log', level=logging.DEBUG)

assignments = []

rows = 'ABCDEFGHI'
cols = '123456789'
cols_rev = cols[::-1]

# Set true if diagonal game
is_diagonal = False


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    # Find all instances of naked twins
    # Get a list of boxes with same value length and length 2.
    length2boxes = [box for box in values.keys() if len(values[box]) == 2]

    # get all peers with equal value to form our twins list
    twins = [[box1, box2] for box1 in length2boxes
             for box2 in peers[box1]
             if set(values[box1]) == set(values[box2])]

    # get a distinct list of twins to remove from future peer lists
    twinlist = list()
    for box1, box2 in twins:
        twinlist.append(box1)
        twinlist.append(box2)
        twinlist = list(set(twinlist))

    # Process each twin removing peer values
    for i in range(len(twins)):
        box1 = twins[i][0]
        box2 = twins[i][1]

        # Get the intersection of peers using set objects
        peers1 = set(peers[box1])
        peers2 = set(peers[box2])
        peers_int = peers1.union(peers2)

        # remove original twins from combined set of peers
        for box in twinlist:
            peers_int.remove(box)

        # Iterate through the intersection and remove twin values from each
        for peer in peers_int:
            digits = values[box1]

            for digit in digits:

                if len(values[peer]) > 1:
                    values[peer] = values[peer].replace(digit, '')
                    assign_value(values, peer, values[peer].replace(digit, ''))
    return values


def cross(A, B):
    """ Cross product of elements in A and elements in B. """
    return [s + t for s in A for t in B]


# initial setup of environment
# all possible boxes on the board
boxes = cross(rows, cols)
# print(boxes)

# all possible rows on the board
row_units = [cross(r, cols) for r in rows]

# all possible columns on the board
column_units = [cross(rows, c) for c in cols]

# all possible boxes on the board (should be 9)
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]

# have to calculate the diagonal units for a diagonal game
units1 = [[rows[i] + cols[i] for i in range(len(rows))]]
units2 = [[rows[i] + cols_rev[i] for i in range(len(rows))]]

if is_diagonal:
    unitlist = row_units + column_units + square_units + units1 + units2
else:
    unitlist = row_units + column_units + square_units

units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], [])) - set([s])) for s in boxes)


def grid_values(grid):
    """Convert grid string into {<box>: <value>} dict with '123456789' value for empties.

    Args:
        grid: Sudoku grid in string form, 81 characters long
    Returns:
        Sudoku grid in dictionary form:
        - keys: Box labels, e.g. 'A1'
        - values: Value in corresponding box, e.g. '8', or '123456789' if it is empty.
    """
    values = []
    all_digits = '123456789'
    for c in grid:
        if c == '.':
            values.append(all_digits)
        elif c in all_digits:
            values.append(c)
    assert len(values) == 81
    return dict(zip(boxes, values))


def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    print("\n")
    return


def eliminate(values):
    """Eliminate values from peers of each box with a single value.

        Go through all the boxes, and whenever there is a box with a single value,
        eliminate this value from the set of values of all its peers.

        Args:
            values: Sudoku in dictionary form.
        Returns:
            Resulting Sudoku in dictionary form after eliminating values.
        """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit, '')
            assign_value(values, peer, values[peer].replace(digit, ''))
    return values


def only_choice(values):
    """Finalize all values that are the only choice for a unit.

        Go through all the units, and whenever there is a unit with a value
        that only fits in one box, assign the value to this box.

        Input: Sudoku in dictionary form.
        Output: Resulting Sudoku in dictionary form after filling in only choices.
        """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                assign_value(values, dplaces[0], digit)
                values[dplaces[0]] = digit
    return values


def reduce_puzzle(values):
    """
        Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
        If the sudoku is solved, return the sudoku.
        If after an iteration of both functions, the sudoku remains the same, return the sudoku.
        Input: A sudoku in dictionary form.
        Output: The resulting sudoku in dictionary form.
        """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Use the Eliminate Strategy
        values = eliminate(values)
        # Use the Only Choice Strategy
        values = only_choice(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    """Using depth-first search and propagation, try all possible values."""
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False  # Failed earlier
    if all(len(values[s]) == 1 for s in boxes):
        return values  ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n, s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    return naked_twins(reduce_puzzle(grid_values(grid)))


if __name__ == '__main__':
    # diag_sudoku_grid ='..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'
    # diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    # diagonal test
    # diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    # diag_sudoku_grid = '9.1....8.8.5.7..4.2.4....6...7......5..............83.3..6......9................'
    # this one demo's naked twins with the fail
    diag_sudoku_grid = '5.9.2..1.4...56...8..9.3..5.87..25..654....82..15684971.82.5...7..68...3.4..7.8..'

    values = grid_values(diag_sudoku_grid)
    print("\nStarting puzzle: \n")
    display(values)
    print("\nSolved puzzle: \n")
    display(solve(diag_sudoku_grid))

    # try:
    #     from visualize import visualize_assignments
    #
    #     visualize_assignments(assignments)
    #
    # except SystemExit:
    #     sys.exit()
    #
    # except:
    #     print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
