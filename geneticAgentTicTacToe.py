# MAIN FILE
import gc
from tictactoe import tictactoe
from geneticAgentFunctions import startAgent, loadAgentsWeights
from tictactoeAgents import *
from helperFunctions import list_to_str

# global variables
global population
global generations
global benchmarkAgent
global agentNames
global weightsCountAgent
global weightsFastAgent
global weightsNeuralAgent
# TASK: Declare your file directory here as global (weights<Agent>)

# settings
population = 300
generations = 1000
benchmarkAgent = RandomAgent('Random')
weightsCountAgent = "data/WeightsCountAgent.pickle"
weightsFastAgent = "data/WeightsFastAgent.pickle"
weightsNeuralAgent = "data/WeightsNeuralAgent.pickle"
# TASK: Write file path here (e.g. 'data/weights<Agent>')

# Task: Add your AgentName here
agentNames = ['NeuralAgent', 'FastAgent', 'CountAgent']

# MAIN
if __name__ == '__main__':
    gc.enable()
    answer = ""
    while answer != "train" and answer != "play":
        answer = input("Do you want to play or train the AI? \n")
    
    agentString = list_to_str(agentNames)
    agentType = ""
    while not (agentType in agentNames):
        agentType = input("Do you want to use " + agentString + "? \n")

    if answer == "train":
        pop = "A"
        while not(pop.isdigit()) and pop != "q":
            pop = input("How many " + agentType + "s do you want to use? (q for quick setup)\n")

        if pop != "q":
            gen = "A"
            while not(gen.isdigit()):
                gen = input("And for how many generations?\n")
            if int(pop) != 0:
                population = int(pop)
            if int(gen) != 0:
                generations = int(gen)
            bestAgent = "None"
            while (not bestAgent in agentNames) and (bestAgent != "RandomAgent") and (bestAgent != "Player"):
                bestAgent = input("Which one is the benchmark Agent? ( RandomAgent, Player, " + agentString + ") \n")
            bestAgentType = eval(bestAgent)
            if bestAgentType == RandomAgent or bestAgentType == Player:
                benchmarkAgent = bestAgentType('Bench Mark')
            else:
                try:
                    weights = loadAgentsWeights(eval("weights" + bestAgent))
                    benchmarkAgent = bestAgentType('Bench Mark')
                    benchmarkAgent.set_weights(weights[0])
                except Exception:
                    benchmarkAgent == RandomAgent('Bench Mark')
                    pass
        agent = startAgent(popul=population, gener=generations, file=eval("weights" + agentType), agentTypeGiven=eval(agentType), bestAgentGiven=benchmarkAgent)
    else:
        agent = startAgent(popul=1, gener=0, file=eval("weights" + agentType), agentTypeGiven=eval(agentType))

    player = Player(input("What is your name?\n"))
    print("So "+ player.name + ", ")
    againBoolean = True
    while(againBoolean):
        start = input("do you want to start? y/n\n")
        if start == "y":
            x = tictactoe(player,agent)
        else:
            x = -tictactoe(agent,player)

        if x == 1:
            print("You won!")
        elif x == -1:
            print("Well, looks like the evolution went right past you.")
        else:
            print("Oh man, there is no winner in this game ... lucky for you, there is also no looser")

        again = input("Wanna play again? y/n\n")
        if again == "n":
            againBoolean = False