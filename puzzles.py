from z3 import *

def buying_animals():
    '''
    Spend exactly 100 dollars and buy exactly 100 animals. 
    Dogs cost 15 dollars, cats cost 1 dollar, and mice cost 25 cents each. 
    You have to buy at least one of each. How many of each should you buy?
    '''
    dogs = Int('dogs')
    cats = Int('cats')
    mice = Int('mice')
    s = Solver()
    s.add(dogs + cats + mice == 100)
    s.add(dogs * 15 + cats * 1 + mice * 0.25 == 100)
    s.add(dogs >= 1, cats >= 1, mice >= 1)
    print(s.check())
    print(s.model())



def sudoku():
    '''
    - - - | - 9 4 | - 3 -
    - - - | 5 1 - | - - 7
    - 8 9 | - - - | - 4 -
    ----------------------
    - - - | - - - | 2 - 8
    - 6 - | 2 - 1 | - 5 -
    1 - 2 | - - - | - - -
    ---------------------
    - 7 - | - - - | 5 2 -
    9 - - | - 6 5 | - - -
    - 4 - | 9 7 - | - - -
    '''
    solver = Solver()
    board = [[Int(f'board({row},{col})') for col in range(9)] for row in range(9)]
    
    # x[i][j] >= 1, x[i][j] <= 9
    solver.add([ And(board[i][j] >= 1, board[i][j] <= 9) for i in range(9) for j in range(9) ])

    # distinct items in row
    solver.add([ Distinct(board[i]) for i in range(9) ])

    # distinct items in column
    solver.add([ Distinct([ board[r][c] for r in range(9)]) for c in range(9) ])

    # distinct items in 3*3 sub matrix
    for bucket_i in range(3):
        for bucket_j in range(3):
            start_ro = bucket_i * 3
            start_col = bucket_j * 3
            solver.add(Distinct([ board[i][j] for i in range(start_ro, start_ro + 3) for j in range(start_col, start_col + 3) ]))

    initial = (
            (0,0,0,0,9,4,0,3,0),
            (0,0,0,5,1,0,0,0,7),
            (0,8,9,0,0,0,0,4,0),
            (0,0,0,0,0,0,2,0,8),
            (0,6,0,2,0,1,0,5,0),
            (1,0,2,0,0,0,0,0,0),
            (0,7,0,0,0,0,5,2,0),
            (9,0,0,0,6,5,0,0,0),
            (0,4,0,9,7,0,0,0,0)
            )
    
    # put intial values in the board
    for i in range(9):
        for j in range(9):
            if initial[i][j] != 0:
                solver.add(board[i][j] == initial[i][j])

    solver.check()
    m = solver.model()
    solution = [ [m.evaluate(board[i][j]) for j in range(9)] for i in range(9) ]
    print_matrix(solution)
    