# Genetic Agent Functions
import random
import math
import pickle
import keyboard
from tictactoeAgents import RandomAgent, CountAgent
from tictactoe import tictactoe
# Basic Functions for Genetic Algorithm:
# 1. Fitness, 2. Selection, 3. Crossover, 4. Mutation

# AgentType:
# Agent should has two attributes, name and weights
# Name (name) is a string and will be used to determine the parents and so on
# Weights (w) is an array with a maximum of 4 dimensions and is allowed to be uneven/inconsistent/non-uniform, e.g. len(a[0]) != len(a[1])
global AgentType
# variables for global use
global agents
global agentsDead
global population
global generations
global bestAgent
AgentType = CountAgent
agents = []
agentsDead = []
population = 1
generations = 1
bestAgent = RandomAgent('Random')

# Genetic Algorithm with Agent
def geneticAlgorithm(w):
    global agents
    global generations
    createAgents(w)
    for generation in range(generations):
        print("Agents: " + str(len(agents)))
        print('Generation: ' + str(generation))
        print("Fitness", end="|")
        fitness()                   # 1. Fitness
        print("Selection", end="|")
        selection()                 # 2. Selection
        print("Crossover", end="|")
        crossover()                 # 3. Crossover
        print("Mutation", end="|")
        mutation()                  # 4. Mutation

        if keyboard.is_pressed("a"): # if you want to break out early
            text = ""
            while text != "y" and text != "n":
                text = input("\n Want to stop here? y/n \n")
            if text == "y":
                sortAgents()
                return
            else:
                print("Well, then let's keep going")
    print("Agents: " + str(len(agents)))
    sortAgents()
    return

# 1. Fitness for Agent
def fitness():
    global agents
    global bestAgent
    for agent in agents:
        agent.fitness = 0
    for agent1 in agents:
        for i in range(100):
            res1 = tictactoe(agent1, bestAgent)
            res2 = tictactoe(bestAgent, agent1)
            agent1.fitness += res1 - res2
            bestAgent.fitness -= res1 - res2
        for agent2 in agents:
            if agent1 == agent2:
                agent1.fitness -= 0.5*max( -min( 0, tictactoe(agent1,agent2) ), 0)
            else:
                res = tictactoe(agent1,agent2)
                agent1.fitness += res
                agent2.fitness += -res
    return

# 2. Selection for Agent
def selection():
    global agents
    global agentsDead
    sortAgents()
    i = 0
    while i < len(agents):
        if i**3 * random.random() > len(agents)*10:  # probability increases with bad fitness
            agentsDead.append( agents.pop(i) )
        else:
            i += 1
    return

# Crossover for Agent
def crossover():
    global agents
    global agentsDead
    global population
    offspring = []
    for i in range( math.ceil( len(agentsDead)/2 ) ):
        parent1 = random.choice(agents)
        p1Weights = parent1.get_weights()
        parent2 = random.choice(agents)
        p2Weights = parent2.get_weights()
        conv = max(0,min(1,random.gauss(0.5, 0.2)))
        try:
            child1 = agentsDead.pop(0)
        except Exception:
            break
        try:
            child1.name = "[" + parent1.name + "," + parent2.name + "]"
            weights = child1.get_weights()
            if isinstance( weights, list):
                for a1 in range(len(weights)):
                    if isinstance( weights[a1], list):
                        for a2 in range(len(weights[a1])):
                            if isinstance( weights[a1][a2], list):
                                for a3 in range(len(weights[a1][a2])):
                                    if isinstance( weights[a1][a2][a3], list):
                                        for a4 in range(len(weights[a1][a2][a3])):
                                            weights[a1][a2][a3][a4] = conv*p1Weights[a1][a2][a3][a4] + (1-conv)*p2Weights[a1][a2][a3][a4]
                                    else:
                                        weights[a1][a2][a3] = conv*p1Weights[a1][a2][a3] + (1-conv)*p2Weights[a1][a2][a3]
                            else:
                                weights[a1][a2] = conv*p1Weights[a1][a2] + (1-conv)*p2Weights[a1][a2]
                    else:
                        weights[a1] = conv*p1Weights[a1] + (1-conv)*p2Weights[a1]
            else:
                weights = conv*p1Weights + (1-conv)*p2Weights
            child1.set_weights(weights)
            offspring.append(child1)
        except Exception:
            print("Exception in crossover Child 1")
        try:
            child2 = agentsDead.pop(1)
        except Exception:
            break
        try:
            child2.name = "[" + parent2.name + "," + parent1.name + "]"
            weights = child1.get_weights()
            if isinstance( weights, list):
                for a1 in range(len(weights)):
                    if isinstance( weights[a1], list):
                        for a2 in range(len(weights[a1])):
                            if isinstance( weights[a1][a2], list):
                                for a3 in range(len(weights[a1][a2])):
                                    if isinstance( weights[a1][a2][a3], list):
                                        for a4 in range(len(weights[a1][a2][a3])):
                                            weights[a1][a2][a3][a4] = conv*p2Weights[a1][a2][a3][a4] + (1-conv)*p1Weights[a1][a2][a3][a4]
                                    else:
                                        weights[a1][a2][a3] = conv*p2Weights[a1][a2][a3] + (1-conv)*p1Weights[a1][a2][a3]
                            else:
                                weights[a1][a2] = conv*p2Weights[a1][a2] + (1-conv)*p1Weights[a1][a2]
                    else:
                        weights[a1] = conv*p2Weights[a1] + (1-conv)*p1Weights[a1]
            else:
                weights = conv*p2Weights + (1-conv)*p1Weights
            child2.set_weights(weights)
            offspring.append(child2)
        except Exception:
            print("Exception in crossover Child 2")
    while len(agents)+len(offspring) > population:
        del offspring[-1]
    agents.extend(offspring)
    return

# Mutation for Agent
def mutation():
    global agents
    for _ in range(math.ceil(len(agents)*1.5)):
        targetAgent = random.choice(agents[int(0.2 * len(agents)):])
        targetValue = random.random()*2-1
        weights = targetAgent.get_weights()
        if isinstance( weights, list):
            t1 = random.randint(0,len(weights)-1)
            if isinstance( weights[t1], list):
                t2 = random.randint(0,len(weights[t1])-1)
                if isinstance( weights[t1][t2], list):
                    t3 = random.randint(0,len(weights[t1][t2])-1)
                    if isinstance( weights[t1][t2][t3], list):
                        t4 = random.randint(0,len(weights[t1][t2])-1)
                        weights[t1][t2][t3][t4] = targetValue
                    else:
                        weights[t1][t2][t3] = targetValue
                else:
                    weights[t1][t2] = targetValue
            else:
                weights[t1] = targetValue
        else:
            weights = targetValue
        targetAgent.set_weights(weights)
    return

# Load weights from pickle-file
def loadAgentsWeights(file):
    with open(file,"rb") as f:
        weights = pickle.load(f)
    return weights

# Save weights in pickle-file
def saveAgentsWeights(file):
    weightlist = [0] * len(agents)
    for i in range(len(agents)):
        weightlist[i] = agents[i].get_weights()
    with open(file,"wb") as f:
        pickle.dump(weightlist,f)

# Start Algorithm
def startAgent(popul=80, gener=200, file="data/Weights.pickle", agentTypeGiven=CountAgent, bestAgentGiven=RandomAgent('Random')):
    global agents
    global population
    global generations
    global AgentType
    global bestAgent
    population = popul
    generations = gener
    AgentType = agentTypeGiven
    bestAgent = bestAgentGiven
    try:
        weights = loadAgentsWeights(file)
    except Exception:
        print("Could not load weights from File: " + str(file))
        weights = []
    geneticAlgorithm(weights)
    saveAgentsWeights(file)
    return agents[0]

# Helper Functions
# Sorting the agents by fitness
def sortAgents():
    global agents
    agents = sorted(agents, key = lambda agent: agent.fitness, reverse = True)
    return

# Creating agents by given weights to global variable
def createAgents(weights):
    global agents
    init()
    for ind in range(len(agents)):
        newWeights = agents[ind].get_weights()
        if len(weights) > ind:
            if isinstance(newWeights, list):
                for a1 in range(len(newWeights)):
                    if isinstance(newWeights[a1], list):
                        for a2 in range(len(newWeights[a1])):
                            if isinstance(newWeights[a1][a2], list):
                                for a3 in range(len(newWeights[a1][a2])):
                                    if isinstance(newWeights[a1][a2][a3], list):
                                        for a4 in range(len(newWeights[a1][a2][a3])):
                                            try:
                                                newWeights[a1][a2][a3][a4] = weights[a1][a2][a3][a4]
                                            except Exception:
                                                print("File does not fit weightlist!\n Initalizing nongiven values with random value in [-1, 1]")
                                                newWeights[a1][a2][a3][a4] = random.random()*2-1
                                    else:
                                        try:
                                            newWeights[a1][a2][a3] = weights[a1][a2][a3]
                                        except Exception:
                                            print("File does not fit weightlist!\n Initalizing nongiven values with random value in [-1, 1]")
                                            newWeights[a1][a2][a3] = random.random()*2-1
                            else:
                                try:
                                    newWeights[a1][a2] = weights[a1][a2]
                                except Exception:
                                    print("File does not fit weightlist!\n Initalizing nongiven values with random value in [-1, 1]")
                                    newWeights[a1][a2] = random.random()*2-1
                    else:
                        try:
                            newWeights[a1] = weights[a1]
                        except Exception:
                            print("File does not fit weightlist!\n Initalizing nongiven values with random value in [-1, 1]")
                            newWeights[a1] = random.random()*2-1
            else:
                try:
                    newWeights = weights
                except Exception:
                    print("File does not fit weightlist!\n Initalizing nongiven values with random value in [-1, 1]")
                    newWeights = random.random()*2-1
        else:
            if isinstance(newWeights, list):
                for a1 in range(len(newWeights)):
                    if isinstance(newWeights[a1], list):
                        for a2 in range(len(newWeights[a1])):
                            if isinstance(newWeights[a1][a2], list):
                                for a3 in range(len(newWeights[a1][a2])):
                                    if isinstance(newWeights[a1][a2][a3], list):
                                        for a4 in range(len(newWeights[a1][a2][a3])):
                                            newWeights[a1][a2][a3][a4] = random.random()*2-1
                                    else:
                                        newWeights[a1][a2][a3] = random.random()*2-1
                            else:
                                newWeights[a1][a2] = random.random()*2-1
                    else:
                        newWeights[a1] = random.random()*2-1
            else:
                newWeights = random.random()*2-1
        agents[ind].set_weights(newWeights)
    return

# Creating agents to global variable
def init():
    global agents
    global agentsDead
    global AgentType
    global population
    agents = [AgentType(str(i+1)) for i in range(population)]
    agentsDead = []
    return