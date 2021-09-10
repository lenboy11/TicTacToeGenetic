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
        parent2 = random.choice(agents)
        conv = max(0,min(1,random.gauss(0.5, 0.2)))
        try:
            child1 = agentsDead.pop(0)
            child1.name = "[" + parent1.name + "," + parent2.name + "]"
            if isinstance( child1.w, list):
                for a1 in range(len(child1.w)):
                    if isinstance( child1.w[a1], list):
                        for a2 in range(len(child1.w[a1])):
                            if isinstance( child1.w[a1][a2], list):
                                for a3 in range(len(child1.w[a1][a2])):
                                    if isinstance( child1.w[a1][a2][a3], list):
                                        for a4 in range(len(child1.w[a1][a2][a3])):
                                            child1.w[a1][a2][a3][a4] = conv*parent1.w[a1][a2][a3][a4] + (1-conv)*parent2.w[a1][a2][a3][a4]
                                    else:
                                        child1.w[a1][a2][a3] = conv*parent1.w[a1][a2][a3] + (1-conv)*parent2.w[a1][a2][a3]
                            else:
                                child1.w[a1][a2] = conv*parent1.w[a1][a2] + (1-conv)*parent2.w[a1][a2]
                    else:
                        child1.w[a1] = conv*parent1.w[a1] + (1-conv)*parent2.w[a1]
            else:
                child1.w = conv*parent1.w + (1-conv)*parent2.w
            if hasattr( child1, "balance_weights" ):
                try:
                    child1.balance_weights()
                except Exception:
                    print( "balance_weights is not a function or is not working properly" )
            offspring.append(child1)
        except Exception:
            print("Exception in crossover")
        try:
            child2 = agentsDead.pop(1)
            child2.name = "[" + parent2.name + "," + parent1.name + "]"
            if isinstance( child2.w, list):
                for a1 in range(len(child2.w)):
                    if isinstance( child2.w[a1], list):
                        for a2 in range(len(child2.w[a1])):
                            if isinstance( child2.w[a1][a2], list):
                                for a3 in range(len(child2.w[a1][a2])):
                                    if isinstance( child2.w[a1][a2][a3], list):
                                        for a4 in range(len(child2.w[a1][a2][a3])):
                                            child2.w[a1][a2][a3][a4] = conv*parent2.w[a1][a2][a3][a4] + (1-conv)*parent1.w[a1][a2][a3][a4]
                                    else:
                                        child2.w[a1][a2][a3] = conv*parent2.w[a1][a2][a3] + (1-conv)*parent1.w[a1][a2][a3]
                            else:
                                child2.w[a1][a2] = conv*parent2.w[a1][a2] + (1-conv)*parent1.w[a1][a2]
                    else:
                        child2.w[a1] = conv*parent2.w[a1] + (1-conv)*parent1.w[a1]
            else:
                child2.w = conv*parent2.w + (1-conv)*parent1.w
            if hasattr( child1, "balance_weights" ):
                try:
                    child1.balance_weights()
                except Exception:
                    print( "balance_weights is not a function or is not working properly" )
            offspring.append(child2)
        except Exception:
            print("Exception in crossover")
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
        if isinstance( targetAgent.w, list):
            t1 = random.randint(0,len(targetAgent.w)-1)
            if isinstance( targetAgent.w[t1], list):
                t2 = random.randint(0,len(targetAgent.w[t1])-1)
                if isinstance( targetAgent.w[t1][t2], list):
                    t3 = random.randint(0,len(targetAgent.w[t1][t2])-1)
                    if isinstance( targetAgent.w[t1][t2][t3], list):
                        t4 = random.randint(0,len(targetAgent.w[t1][t2])-1)
                        targetAgent.w[t1][t2][t3][t4] = targetValue
                    else:
                        targetAgent.w[t1][t2][t3] = targetValue
                else:
                    targetAgent.w[t1][t2] = targetValue
            else:
                targetAgent.w[t1] = targetValue
        else:
            targetAgent.w = targetValue
    for agent in agents:
        if hasattr( agent, "balance_weights" ):
            try:
                agent.balance_weights()
            except Exception:
                print( "balance_weights is not a function or is not working properly" )
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
        weightlist[i] = agents[i].w
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
        if len(weights) > ind:
            if isinstance(agents[ind].w, list):
                for a1 in range(len(agents[ind].w)):
                    if isinstance(agents[ind].w[a1], list):
                        for a2 in range(len(agents[ind].w[a1])):
                            if isinstance(agents[ind].w[a1][a2], list):
                                for a3 in range(len(agents[ind].w[a1][a2])):
                                    if isinstance(agents[ind].w[a1][a2][a3], list):
                                        for a4 in range(len(agents[ind].w[a1][a2][a3])):
                                            try:
                                                agents[ind].w[a1][a2][a3][a4] = weights[a1][a2][a3][a4]
                                            except Exception:
                                                print("File does not fit weightlist!\n Initalizing nongiven values with random value in [-1, 1]")
                                                agents[ind].w[a1][a2][a3][a4] = random.random()*2-1
                                    else:
                                        try:
                                            agents[ind].w[a1][a2][a3] = weights[a1][a2][a3]
                                        except Exception:
                                            print("File does not fit weightlist!\n Initalizing nongiven values with random value in [-1, 1]")
                                            agents[ind].w[a1][a2][a3] = random.random()*2-1
                            else:
                                try:
                                    agents[ind].w[a1][a2] = weights[a1][a2]
                                except Exception:
                                    print("File does not fit weightlist!\n Initalizing nongiven values with random value in [-1, 1]")
                                    agents[ind].w[a1][a2] = random.random()*2-1
                    else:
                        try:
                            agents[ind].w[a1] = weights[a1]
                        except Exception:
                            print("File does not fit weightlist!\n Initalizing nongiven values with random value in [-1, 1]")
                            agents[ind].w[a1] = random.random()*2-1
            else:
                try:
                    agents[ind].w = weights
                except Exception:
                    print("File does not fit weightlist!\n Initalizing nongiven values with random value in [-1, 1]")
                    agents[ind].w = random.random()*2-1
        else:
            if isinstance(agents[ind].w, list):
                for a1 in range(len(agents[ind].w)):
                    if isinstance(agents[ind].w[a1], list):
                        for a2 in range(len(agents[ind].w[a1])):
                            if isinstance(agents[ind].w[a1][a2], list):
                                for a3 in range(len(agents[ind].w[a1][a2])):
                                    if isinstance(agents[ind].w[a1][a2][a3], list):
                                        for a4 in range(len(agents[ind].w[a1][a2][a3])):
                                            agents[ind].w[a1][a2][a3][a4] = random.random()*2-1
                                    else:
                                        agents[ind].w[a1][a2][a3] = random.random()*2-1
                            else:
                                agents[ind].w[a1][a2] = random.random()*2-1
                    else:
                        agents[ind].w[a1] = random.random()*2-1
            else:
                agents[ind].w = random.random()*2-1
        if hasattr( agents[ind], "balance_weights" ):
            try:
                agents[ind].balance_weights()
            except Exception:
                print( "balance_weights is not a function or is not working properly" )
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