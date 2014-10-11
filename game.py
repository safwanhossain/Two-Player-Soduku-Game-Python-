import math

def play():

    ''' (None) -> None

    Co-ordinates input from user to run the game'''

    grid_size = int(float(input('Please enter grid size')))

    # check for valid grid size
    while (grid_size != 4) and (grid_size != 9) and (grid_size != 16):
        print('You have entered an invalid grid size!')
        grid_size = int(input('Please enter grid size'))

    # make a empty matrix for the game 
    global game_matrix
    game_matrix = []

    for i in range(grid_size):
        game_matrix.append([])
        for k in range(grid_size):
            game_matrix[i].append(0)

    global length
    global root_length
    length = len(game_matrix)   # length of the matrix
    root_length = int(math.sqrt(length))    # sqrt of the length

    show()    # print the grid

    game = True    
    
    # runs the game until someone wins
    while game:

        # Gather and check input from Player A
        move = True

        while move:
            inputA = input('Player A, Please Enter Your Move: ')

            if inputA == 'q':
                return    # quit the game
            if inputA == 's':
                save()    # save the game to a file
                return    # quit the game

            # process user input
            inputA = inputA.split(',')
            row, column, number = int(inputA[0]), int(inputA[1]),\
                                int(inputA[2])

            # check for valid moves and winner
            if check_move(row, column, number):
                move = False
                game_matrix[row][column] = number
                show()

                if check_win() == 1:
                    print('Congratulation Player A! You won')
                    game = False

                elif check_win() == 2:
                    print('The game is a tie')
                    game = False
            else:
                print('Invalid Move; Please Enter Again')
                move = True

        # Gather and check input from Player B    
        move = True

        while move:
            inputB = input('Player B, Please Enter Your Move: ')

            if inputB == 'q':
                return
            if inputB == 's':
                save()
                return

            inputB = inputB.split(',')
            row, column, number = int(inputB[0]), int(inputB[1]),\
                                int(inputB[2])

            if check_move(row, column, number):
                move = False
                game_matrix[row][column] = number
                show()

                if check_win() == 1:
                    print('Congratulations Player B! You won')
                    game = False

                elif check_win() == 2:
                    print('The game is a tie')
                    game = False
            else:
                print('Invalid Move; Please Enter Again')
                move = True
        
            
def show():

    ''' (None) -> None

    Prints the current grid'''

    count = 0    # keeps count of the rows 

    for i in range(root_length):    # iterates over clusters

        for j in range(root_length):    # iterates over rows
            output_str = ''

            for k in range(root_length):    # iterates over columns

                #converts to str, strips brackets and commas and adds |
                output = game_matrix[j + count]\
                         [k*root_length:(k+1)*root_length]
                output_clean = str(output).strip(']').\
                               strip('[').replace(',','')
                output_str = output_str + output_clean + '|'

            print(output_str.rstrip('|'))

        if i != root_length - 1:
            print('-' * length * 2)  # adds line after each cluster

        count = count + (j + 1)     # updates row number 


def check_move(row, column, number):

    ''' (int,int,int) -> bool

    Return True if the move is legal; else, return False'''

    # check if position is lready full
    if game_matrix[row][column] != 0:
        return False

    # check if number is in range
    if number not in range(1,len(game_matrix)+1):
        return False

    # checks if number already in row
    if number in game_matrix[row]:
        return False

    
    # checks if number already in column
    for i in range(len(game_matrix)):
        if number == game_matrix[i][column]:
            return False

    cluster = []

    # identify the cluster 
    cluster_row = (row//root_length) * (root_length)
    cluster_column = (column//root_length) * (root_length)

    #iterate over the cluster, checking if number is already present
    for i in range(root_length):
        cluster = cluster + game_matrix[cluster_row + i]\
                  [cluster_column:cluster_column + root_length] 

    if number in cluster:
        return False

    return True


def check_win():

    ''' (None) -> (int)

    Return 0 if game still has legal moves, 1 if player wins,
    and 2 if grid is full and the game is a tie'''

    # find unfilled values in grid and check for valid moves
    count = 0    # counts number of filled values in grid

    # iterates over all elements in the grid
    for i in range(length):
        for j in range(length):
            if game_matrix[i][j] == 0:
                for number in range(1, length + 1):
                    if check_move(i, j, number):
                        return 0    # Valid move
            else:
                count += 1
                
    if count == (length ** 2):
        return 2    # grid is full

    return 1    # grid is empty but no valid moves left


def save():

    ''' (None) -> None

    Save the current grid (same format as on display) into a file.'''

    file_name = input('Please Enter file name for saving')
    file = open(file_name, 'w')

    # same code structure as show()
    count = 0

    for i in range(root_length):

        for j in range(root_length):
            output_str = ''

            for k in range(root_length):
                output = game_matrix[j + count]\
                         [k*root_length:(k+1)*root_length]
                output_clean = str(output).strip(']')\
                               .strip('[').replace(',','')
                output_str = output_str + output_clean + '|'

            file.write(output_str.rstrip('|') + '\n')

        if i != (root_length - 1):
            file.write(('-' * length * 2)+ '\n')

        count = count + (j + 1)

play()
