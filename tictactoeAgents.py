# TicTacToe Agents
import random
import math

## Classes
# TicTacToe Agents need __init__ for creation and
#                             _|_|_
# the function guess( self, [ _|_|_ ]) with the game as 9x1 array
#                              | | 

## Class NeuralAgent with a neural network
# Not very useful since we use a genetic algorithm and neural networks need a lot of data
class NeuralAgent:
    def __init__(self, name):
        self.name = name
        self.no_inputs = 9
        self.no_layers = 3
        self.no_nodes = 9
        self.w = [[[(0) for _ in range(self.no_nodes)] for _ in range(self.no_nodes)] for _ in range(self.no_layers)]
        self.w.append( [[(0) for _ in range(self.no_nodes)] for _ in range(self.no_layers)] )
        self.balance_weights()
        self.fitness = 0
    def __str__(self):
        return self.name
    def guess(self, inputs):
        values = [[0] * len(self.w[1][0])] * len(self.w[1])
        for m in range(len(self.w[0][0][0])):
            sum = self.w[1][0][m]
            for n in range(self.no_inputs):
                sum += self.w[0][0][m][n] * inputs[n]
            values[0][m] = self.sigmoid(sum)
        for i in range(len(self.w[0]) - 1):
            for j in range(len(self.w[0][i + 1])):
                sum = self.w[1][i + 1][j]
                for k in range(len(self.w[0][i + 1][j])):
                    sum += self.w[0][i + 1][j][k] * values[i][j]
            values[i + 1][j] = self.sigmoid(sum)    
        indizes = [0]*9
        for i in range(len(inputs)):
            if inputs[i] == 0:
                indizes[i] = values[len(self.w[1]) - 1][i]
        i = self.maxIndex(indizes)
        return i
    def balance_weights(self):
        # weights with specific logic
        for i in range(6):
            self.w[0][0][0][i+3] = 0
        for i in [0,1,2,6,7,8]:
            self.w[0][0][1][i] = 0
        for i in range(6):
            self.w[0][0][2][i] = 0
        for i in [1,2,4,5,7,8]:
            self.w[0][0][3][i] = 0
        for i in [0,2,3,5,6,8]:
            self.w[0][0][4][i] = 0
        for i in [0,1,3,4,6,7]:
            self.w[0][0][5][i] = 0
        for i in [1,2,3,5,6,7]:
            self.w[0][0][6][i] = 0
        for i in [0,1,3,5,7,8]:
            self.w[0][0][7][i] = 0
        for i in range(9):
            self.w[0][0][8][i] = 0
        for i in [1,2,4,5,7,8]:
            self.w[0][1][0][i] = 0
        for i in [1,2,3,5,6,7,8]:
            self.w[0][1][1][i] = 0
        for i in [1,2,3,4,6,8]:
            self.w[0][1][2][i] = 0
        for i in [0,2,4,5,6,7,8]:
            self.w[0][1][3][i] = 0
        for i in [0,2,3,5,8]:
            self.w[0][1][4][i] = 0
        for i in [0,2,3,4,6,7,8]:
            self.w[0][1][5][i] = 0
        for i in [0,1,4,5,6,8]:
            self.w[0][1][6][i] = 0
        for i in [0,1,3,5,6,7,8]:
            self.w[0][1][7][i] = 0
        for i in [0,1,3,4,7,8]:
            self.w[0][1][8][i] = 0
    # Index with max value in the list
    def maxIndex(self, list):
        max = 0
        for i in range(len(list)):
            if list[i] > list[max]:
                max = i
        return max
    # Sigmoid funtion
    def sigmoid(self, x):
        try:
            return 1 / (1 + math.exp(-x))
        except:
            if x > 0:
                return 1
            else:
                return 0


## Class FastAgent with row and column weighting
class FastAgent:
    def __init__(self, name):
        self.name = name
        self.w = [[0.3, 0.2], [0.3, 0.2]]
        self.fitness = 0

    def __str__(self):
        return self.name

    def guess(self, inputs):
        c = [0]*3
        r = [0]*3
        # Compute Probability of every column and row and crossers
        for i in range(3):
            c[i] = self.w[0][0] * max(0,inputs[i*3]) + self.w[0][1] * max(0,-inputs[i*3]) + \
                   self.w[1][0] * max(0,inputs[i*3+1]) + self.w[1][1] * max(0,-inputs[i*3+1]) + \
                   self.w[0][0] * max(0,inputs[i*3+2]) + self.w[0][1] * max(0,-inputs[i*3+2])
            r[i] = self.w[0][0] * max(0,inputs[i]) + self.w[0][1] * max(0,-inputs[i]) + \
                   self.w[1][0] * max(0,inputs[i+3]) + self.w[1][1] * max(0,-inputs[i+3]) + \
                   self.w[0][0] * max(0,inputs[i+6]) + self.w[0][1] * max(0,-inputs[i+6])
        x = [ self.w[0][0] * max(0,inputs[0]) + self.w[0][1] * max(0,-inputs[0]) + \
              self.w[1][0] * max(0,inputs[4]) + self.w[1][1] * max(0,-inputs[4]) + \
              self.w[0][0] * max(0,inputs[8]) + self.w[0][1] * max(0,-inputs[8]), \
              self.w[0][0] * max(0,inputs[2]) + self.w[0][1] * max(0,-inputs[2]) + \
              self.w[1][0] * max(0,inputs[4]) + self.w[1][1] * max(0,-inputs[4]) + \
              self.w[0][0] * max(0,inputs[6]) + self.w[0][1] * max(0,-inputs[6]) ]
        # Add up probability up for every element
        res = [0]*9
        for i in range(9):
            res[i] += c[math.floor((i)/3)] + r[i % 3]
        res[0] += x[0]
        res[8] += x[0]
        res[2] += x[1]
        res[6] += x[1]
        res[4] += x[0] + x[1]
        # Return unused field with highest probability
        while(True):
            curMax = 8
            for i in range(8):
                if res[i] > res[curMax]:
                    curMax = i
            if (inputs[curMax] == 0):
                return curMax
                break
            else:
                res[curMax] = float('-inf')
        
class CountAgent:
    def __init__(self, name):
        self.name = name
        self.w = [0.1, [0.3, 0.25], -0.35]
        self.fitness = 0
        
    def __str__(self):
        return self.name

    def guess(self, inputs):
        c = [0]*3
        r = [0]*3
        d = [0]*2
        for i in range(3):
            x1 = max(0,inputs[i*3]) +  max(0,inputs[i*3 + 1]) +  max(0,inputs[i*3 + 2])
            x2 = max(0,-inputs[i*3]) +  max(0,-inputs[i*3 + 1]) +  max(0,-inputs[i*3 + 2])
            try:
                c[i] = self.w[0] + self.w[1][0]*x1 + self.w[1][1]*x2 + self.w[2]*x1*x2
            except Exception as e:
                print(type(self.w[0]))
                print(type(self.w[1][0]))
                print(type(self.w[1][1]))
                print(type(self.w[2]))
            x1 = max(0,inputs[i]) +  max(0,inputs[i + 3]) +  max(0,inputs[i + 6])
            x2 = max(0,-inputs[i]) +  max(0,-inputs[i + 3]) +  max(0,-inputs[i + 6])
            r[i] = self.w[0] + self.w[1][0]*x1 + self.w[1][1]*x2 + self.w[2]*x1*x2
            if i < 2:
                x1 = max(0,inputs[2*i]) +  max(0,inputs[4]) +  max(0,inputs[8 - 2*i])
                x2 = max(0,-inputs[2*i]) +  max(0,-inputs[4]) +  max(0,-inputs[8 - 2*i])
                d[i] = self.w[0] + self.w[1][0]*x1 + self.w[1][1]*x2 + self.w[2]*x1*x2
        # Add up probability up for every element
        res = [0]*9
        for i in range(9):
            res[i] += c[math.floor((i)/3)] + r[i % 3]
        res[0] += d[0]
        res[8] += d[0]
        res[2] += d[1]
        res[6] += d[1]
        res[4] += d[0] + d[1]
        # Return unused field with highest probability
        while(True):
            curMax = 8
            for i in range(8):
                if res[i] > res[curMax]:
                    curMax = i
            if (inputs[curMax] == 0):
                return curMax
                break
            else:
                res[curMax] = float('-inf')

# TASK: Add your own Agents here









## Other Agents for the Game
# Agent that selects a random, unused spot
class RandomAgent:
    def __init__(self, name):
        self.name = name
        self.fitness = 0
    def __str__(self):
        return self.name
    def guess(self, inputs):
        unused = []
        for i in range(len(inputs)):
            if inputs[i] == 0:
                unused.append(i)
        return random.choice(unused)

# class for a real world player to play against the agents
class Player:
    def __init__(self, name):
        self.name = name
        self.fitness = 0
    def __str__(self):
        return self.name
    def guess(self, inputs):
        print(self.input2XO(inputs[0]) + " | " + self.input2XO(inputs[1]) + " | " + self.input2XO(inputs[2]))
        print(self.input2XO(inputs[3]) + " | " + self.input2XO(inputs[4]) + " | " + self.input2XO(inputs[5]))
        print(self.input2XO(inputs[6]) + " | " + self.input2XO(inputs[7]) + " | " + self.input2XO(inputs[8]))
        unused = []
        for i in range(len(inputs)):
            if inputs[i] == 0:
                unused.append(i)
        while True:
            try:
                x = int(input("Where do you want to put your cross?")) - 1
                if x in unused:
                    return x
                else:
                    print("There is already a sign in this field!")
            except Exception:
                pass
    # Make Board more suitable for user
    def input2XO(input):
        if input == -1:
            return "O"
        elif input == 1:
            return "X"
        else:
            return " "