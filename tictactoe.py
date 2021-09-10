# TicTacToe
## The Game
# The Tic Tac Toe Game for two agents who solve their goal by calling the function 'guess( board )'
# board has the 9 fields, where the field contains 1 for X, 0 for None and -1 for O
def tictactoe(agent1, agent2):
    board = [0]*9
    boardinv = [0]*9
    unused = [0,1,2,3,4,5,6,7,8]
    for i in range(9):
        if (i % 2) == 0:
            x = agent1.guess(board)
            if x in unused:
                board[x] = 1
                boardinv[x] = -1
            else:
                board[unused[0]] = 1
                boardinv[unused[0]] = -1
            unused.remove(x)
        else:
            x = agent2.guess(boardinv)
            if x in unused:
                board[x] = -1
                boardinv[x] = 1
            else:
                board[unused[0]] = -1
                boardinv[unused[0]] = 1
            unused.remove(x)
        winner = won(board)
        if winner != 0:
            return winner
    return 0

# Determine if board has a winner and if so who it is        
def won(board):
    for i in [0,1,2]:
        if 0 != board[3*i] and board[3*i] == board[3*i+1] and board[3*i+1] == board[3*i+2]:
            return board[3*i]
        elif 0 != board[i] and board[i] == board[i+3] and board[i+3] == board[i+6]:
            return board[i]
    if 0 != board[4] and ((board[4] == board[0] and board[4] == board[8]) or (board[4] == board[2] and board[4] == board[6])):
        return board[4]
    return 0